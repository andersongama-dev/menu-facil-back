import re
import numpy as np
from difflib import get_close_matches
from typing import List, Tuple, Optional

from sentence_transformers import SentenceTransformer
from database.connection import get_connection
from models.menu import Menu

INGREDIENTS = {
    "macarrão": ["massa", "espaguete", "fettuccine", "lasanha"],
    "cogumelos": ["champignon", "portobello"],
    "queijo": ["queijo", "muçarela", "parmesão"],
    "alho": ["alho", "dentes de alho"],
    "pesto": ["pesto", "molho pesto"],
    "tomate": ["tomate", "tomatinhos"],
    "alface": ["alface", "rúcula", "espinafre"],
    "carne": ["carne", "frango", "porco", "hambúrguer"],
    "azeite": ["azeite", "azeite de oliva"],
    "batata": ["batata", "batatas", "batata frita"]
}
RESTRICTIONS = {
    "vegetariano": ["carne", "frango", "bovina", "porco"],
    "vegano": ["carne", "frango", "bovina", "porco", "queijo", "leite", "ovo", "mel"],
    "sem lactose": ["leite", "queijo", "iogurte"],
    "sem glúten": ["trigo", "massa", "pão"]
}
EXCLUDE_WORDS = {
    "prato", "que", "de", "e", "com", "o", "a", "um",
    "uma", "quero", "gostaria", "por", "favor"
}
model = SentenceTransformer("all-MiniLM-L6-v2")
ITEMS_CACHE: List[Menu] = []
ITEM_EMBEDDINGS: Optional[np.ndarray] = None


def normalize_text(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text.lower())


def match_partial(word: str, token: str) -> bool:
    return word in token or token in word

def fuzzy_match(word: str, token_list: List[str], cutoff: float = 0.6) -> bool:
    return bool(get_close_matches(word, token_list, n=1, cutoff=cutoff))

def preload_menu_embeddings() -> None:
    global ITEMS_CACHE, ITEM_EMBEDDINGS
    ITEMS_CACHE = fetch_menu_items()
    if not ITEMS_CACHE:
        ITEM_EMBEDDINGS = None
        return
    item_texts = [
        normalize_text(item.name + " " + item.description)
        for item in ITEMS_CACHE
    ]
    ITEM_EMBEDDINGS = model.encode(item_texts)
    print(f"[INFO] Pré-carregados {len(ITEMS_CACHE)} itens com embeddings.")


def extract_keywords(user_text: str) -> Tuple[List[str], List[str], List[str]]:
    text = normalize_text(user_text)
    tokens = [w for w in text.split() if w not in EXCLUDE_WORDS]
    keywords: List[str] = []
    excludes: List[str] = []
    restrictions: List[str] = []
    for ing, syns in INGREDIENTS.items():
        for token in tokens:
            if (
                match_partial(ing, token)
                or any(match_partial(s, token) for s in syns)
                or fuzzy_match(token, [ing] + syns)
            ):
                keywords.append(ing)
    keywords = list(set(keywords))
    pattern = r"(sem|não quero) (\w+)"
    matches = re.findall(pattern, text)
    for _, w in matches:
        for ing, syns in INGREDIENTS.items():
            if (
                match_partial(ing, w)
                or any(match_partial(s, w) for s in syns)
                or fuzzy_match(w, [ing] + syns)
            ):
                excludes.append(ing)
    excludes = list(set(excludes))
    for r in RESTRICTIONS.keys():
        for token in tokens:
            if match_partial(r, token) or fuzzy_match(token, [r]):
                restrictions.append(r)
    restrictions = list(set(restrictions))
    return keywords, excludes, restrictions

def fetch_menu_items() -> List[Menu]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_item, name, description, price, cost, profit_margin, id_category
        FROM menu_items
        WHERE is_available = 1
    """)
    rows = cursor.fetchall()
    items: List[Menu] = []
    for row in rows:
        items.append(
            Menu(
                id_item=row["id_item"],
                name=row["name"],
                description=row["description"],
                price=row["price"],
                cost=row["cost"],
                profit_margin=row["profit_margin"],
                id_category=row["id_category"],
            )
        )
    cursor.close()
    conn.close()
    return items

def filter_by_restrictions(items: List[Menu], restrictions: List[str]) -> List[Menu]:
    filtered: List[Menu] = []
    for item in items:
        tokens = normalize_text(item.name + " " + item.description).split()
        conflict = False
        for r in restrictions:
            forbidden = RESTRICTIONS[r]
            if any(f in tokens for f in forbidden):
                conflict = True
                break
        if not conflict:
            filtered.append(item)
    return filtered

def score_items(
    user_text: str,
    items: List[Menu],
    keywords: List[str],
    excludes: List[str],
    kw_weight: float = 1.0,
    exclude_weight: float = 1.5,
    vec_weight: float = 2.0,
) -> List[Menu]:
    global ITEM_EMBEDDINGS
    if ITEM_EMBEDDINGS is None:
        return items
    scored = []
    user_vec = model.encode(user_text)
    for idx, item in enumerate(items):
        text_tokens = set(
            normalize_text(item.name + " " + item.description).split()
        )
        keyword_score = sum(
            any(match_partial(k, t) for t in text_tokens) for k in keywords
        )
        exclude_score = sum(
            any(match_partial(e, t) for t in text_tokens) for e in excludes
        )
        item_vec = ITEM_EMBEDDINGS[idx]
        vec_score = np.dot(user_vec, item_vec) / (
            np.linalg.norm(user_vec) * np.linalg.norm(item_vec)
        )
        total_score = (
            kw_weight * keyword_score
            - exclude_weight * exclude_score
            + vec_weight * vec_score
        )
        scored.append((total_score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in scored]


def ai_suggest_menu(user_text: str, top_k: int = 4, debug: bool = False) -> List[Menu]:
    global ITEMS_CACHE, ITEM_EMBEDDINGS
    if not ITEMS_CACHE or ITEM_EMBEDDINGS is None:
        preload_menu_embeddings()
    keywords, excludes, restrictions = extract_keywords(user_text)
    if debug:
        print("=== DEBUG MENU ===")
        print("User:", user_text)
        print("Keywords:", keywords)
        print("Excludes:", excludes)
        print("Restrictions:", restrictions)
    items = filter_by_restrictions(ITEMS_CACHE, restrictions)
    if not items:
        return []
    scored_items = score_items(user_text, items, keywords, excludes)
    if debug:
        for idx, item in enumerate(scored_items[:top_k]):
            print(f"{idx+1}. {item.name} - {item.description}")
    return scored_items[:top_k]