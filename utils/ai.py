from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from database.connection import SessionLocal
from models.ai import AIORM

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


def llm_select(items, user_input, context="", user_id=None):
    user_history = get_user_history(user_id) if user_id else []
    history_text = ""
    if user_history:
        history_text = "Preferências anteriores do usuário:\n" + summarize_history(user_history)

    menu_text = "\n".join([f"{item.name}: {item.description}" for item in items])

    prompt_text = f"""
    Você é uma IA que recomenda pratos.

    {history_text}

    Escolha os 4 melhores pratos do menu para o pedido do usuário.

    Menu:
    {menu_text}

    Pedido do usuário:
    {user_input}

    Retorne apenas os nomes separados por vírgula.
    """

    try:
        response = chain.invoke({
            "context": context,
            "question": prompt_text
        })
    except Exception as e:
        print(f"Erro na LLM: {e}")
        return items[:4]

    names = [n.strip() for n in response.split(",")][:4]
    recommended = [item for item in items if item.name in names]

    for item in items:
        if item not in recommended:
            recommended.append(item)
        if len(recommended) == 4:
            break

    return recommended

def get_user_history(user_id, limit=5):
    session = SessionLocal()
    try:
        interactions = (
            session.query(AIORM)
            .filter(AIORM.id_user == user_id)
            .order_by(AIORM.created_at.desc())
            .limit(limit)
            .all()
        )
        history = [ia.parsed_intent for ia in interactions]
        return history
    finally:
        session.close()

def summarize_history(history):
    summary = []
    for h in history:
        if isinstance(h, dict):
            summary.append(", ".join(f"{k}: {v}" for k, v in h.items()))
        else:
            summary.append(str(h))
    return "\n".join(summary)