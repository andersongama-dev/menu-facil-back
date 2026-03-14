from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
    Responda a questão abaixo.

    Histórico da conversa:
    {context}

    Pergunta:
    {question}

    Resposta:
    """

model = OllamaLLM(
    model="llama3:latest",
    base_url="http://localhost:11434"
)

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

def llm_select(items, user_input, context=""):

    menu_text = "\n".join(
        [f"{item.name}: {item.description}" for item in items]
    )

    prompt_text = f"""
    Você é uma IA que recomenda pratos.

    Escolha os 4 melhores pratos do menu para o pedido do usuário.

    Menu:
    {menu_text}

    Pedido do usuário:
    {user_input}

    Retorne apenas os nomes separados por vírgula.
    """

    response = chain.invoke({
        "context": context,
        "question": prompt_text
    })

    names = [n.strip() for n in response.split(",")][:4]

    return [item for item in items if item.name in names]