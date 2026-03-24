from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
import os
from utils.items import fetch_all_menu_items_name


def parse_llm_response(response):
    if isinstance(response, list):
        text = getattr(response[0], "content", str(response[0]))
    else:
        text = getattr(response, "content", str(response))

    names = [n.strip() for n in text.split(",") if n.strip()]
    return names


model = ChatOpenRouter(
    model="meta-llama/llama-3.1-8b-instruct",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

prompt = ChatPromptTemplate.from_template("""
    Você é um sistema de recomendação de restaurante.
    
    Menu:
    {menu}
    
    Pedido do usuário:
    {user_input}
    
    Escolha exatamente 4 pratos do menu.
    
    Regras:
    - NÃO invente pratos
    - Use APENAS nomes do menu
    - NÃO explique nada
    
    Resposta:
    Somente os 4 nomes separados por vírgula.
    """)

chain = prompt | model


def llm_select(items, user_input):

    item_name_category = fetch_all_menu_items_name()

    response = chain.invoke({
        "menu": item_name_category,
        "user_input": user_input
    })

    print("Resposta bruta:", response)

    names = parse_llm_response(response)

    recommended = []
    for name in names:
        for item in items:
            if item.name.lower() == name.lower():
                recommended.append(item)

    return recommended