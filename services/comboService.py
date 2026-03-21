from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
import os
from typing import List, Dict
from utils.items import fetch_all_menu_items
import unicodedata

model = ChatOpenRouter(
    model="meta-llama/llama-3.1-8b-instruct",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

prompt_combo = ChatPromptTemplate.from_template("""
    Você é um sistema de recomendação de combos de restaurante.
    
    Prato principal: {item_name}
    
    Menu:
    {menu}
    
    Escolha exatamente 2 ou 3 itens do menu que combinem com o prato principal:
    
    - 1 bebida
    - 1 acompanhamento
    - 1 sobremesa (opcional)
    
    Regras:
    - Não repetir o prato principal
    - Não inventar itens
    - Usar exatamente os nomes do menu
    - Não explique nada
    
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

    menu_text = "\n".join([
        f"{item.name} ({item.category.name if item.category else ''}): {item.description}"
        for item in menu_items
    ])

    response = chain_combo.invoke({
        "item_name": item_name,
        "menu": menu_text
    })

    names = parse_llm_response(response)
    item_name_norm = normalize(item_name)

    print(names)

    beverage = None
    acomp = None
    sobremesa = None

    for name in names:
        name_norm = normalize(name)
        for item in menu_items:
            item_norm = normalize(item.name)
            cat_norm = normalize(item.category.name if item.category else "")

            if item_norm == item_name_norm:
                continue

            if name_norm in item_norm or item_norm in name_norm:
                if "bebida" in cat_norm and not beverage:
                    beverage = item
                elif "acompanhamento" in cat_norm and not acomp:
                    acomp = item
                elif "sobremesa" in cat_norm and not sobremesa:
                    sobremesa = item

        if beverage and (acomp or sobremesa):
            break

    for item in menu_items:
        cat_norm = normalize(item.category.name if item.category else "")
        item_norm = normalize(item.name)

        if item_norm == item_name_norm:
            continue

        if not beverage and "bebida" in cat_norm:
            beverage = item
        elif not acomp and "acompanhamento" in cat_norm:
            acomp = item
        elif not sobremesa and "sobremesa" in cat_norm:
            sobremesa = item

        if beverage and (acomp or sobremesa):
            break

    suggestions = [x for x in [beverage, acomp, sobremesa] if x]

    return {
        "items": suggestions,
        "message": f"Combo sugerido para {item_name}:"
    }