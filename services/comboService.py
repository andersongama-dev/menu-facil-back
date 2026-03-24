from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
import os
from typing import List, Dict
from utils.items import fetch_all_menu_items, fetch_menu_item_by_name, fetch_all_menu_items_name
import unicodedata

model = ChatOpenRouter(
    model="meta-llama/llama-3.1-8b-instruct",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

prompt_combo = ChatPromptTemplate.from_template("""
    Você é um sistema de recomendação de combos de restaurante.
    
    Item de referência: {item_name}
    
    Menu completo:
    {item_name_category}
    
    Escolha exatamente 2 ou 3 itens do menu que combinem com o item de referência.
    Use apenas os nomes exatos do menu, separados por vírgula.
    Não explique nada, não adicione caracteres extras, não use aspas, não coloque quebras de linha.
    
    Resposta:
    nome1, nome2, nome3
    """)

chain_combo = prompt_combo | model

def normalize(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')

def parse_llm_response(response) -> List[str]:
    if isinstance(response, list):
        text = getattr(response[0], "content", str(response[0]))
    else:
        text = getattr(response, "content", str(response))
    return [n.strip() for n in text.split(",") if n.strip()]

def llm_combo_suggest(item_name: str) -> Dict:
    menu_items = fetch_all_menu_items()
    item_name_category = fetch_all_menu_items_name()
    item_name_fetch = fetch_menu_item_by_name(item_name)

    response = chain_combo.invoke({
        "item_name": item_name_fetch,
        "item_name_category": item_name_category
    })

    names = parse_llm_response(response)

    name_to_item = {item.name: item for item in menu_items}

    suggestions = []
    for name in names:
        if name in name_to_item and name != item_name:
            suggestions.append(name_to_item[name])

    return {
        "items": suggestions,
        "message": f"Combo sugerido para {item_name}:"
    }