from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from database.connection import SessionLocal
from models.ai import AIORM
from models.user_preference import UserPreferenceORM

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
    history_text = ""
    preferences_text = ""

    if user_id:
        user_history = get_user_history(user_id)
        if user_history:
            history_text = "Histórico recente do usuário:\n" + summarize_history(user_history)

        user_preferences = get_user_preferences(user_id)
        if user_preferences:
            preferences_summary = [
                f"{p['preference_type']}: {p['preference_value']} (score: {p['confidence_score']})"
                for p in user_preferences
            ]
            preferences_text = "Preferências do usuário:\n" + "\n".join(preferences_summary)

    menu_text = "\n".join([f"{item.name}: {item.description}" for item in items])

    prompt_text = f"""
    Você é uma IA especializada em recomendar pratos de restaurante. Sempre siga o pedido do usuário. 
    Use o histórico e as preferências apenas se o pedido for vago ou pouco claro.

    Menu disponível:
    {menu_text}

    {preferences_text}
    {history_text}

    Pedido do usuário:
    {user_input}

    Escolha os 4 melhores pratos para o pedido do usuário. Retorne apenas os nomes, separados por vírgula.
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

def get_user_preferences(user_id, limit=10):
    session = SessionLocal()
    try:
        preferences = (
            session.query(UserPreferenceORM)
            .filter(UserPreferenceORM.id_user == user_id)
            .order_by(UserPreferenceORM.confidence_score.desc())
            .limit(limit)
            .all()
        )
        result = [
            {
                "preference_type": pref.preference_type,
                "preference_value": pref.preference_value,
                "confidence_score": float(pref.confidence_score) if pref.confidence_score is not None else None
            }
            for pref in preferences
        ]
        return result
    finally:
        session.close()

