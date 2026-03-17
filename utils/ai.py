from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
import os

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
    menu_text = "\n".join([
        f"{i.name} ({i.category}): {i.description}"
        for i in items
    ])

    response = chain.invoke({
        "menu": menu_text,
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