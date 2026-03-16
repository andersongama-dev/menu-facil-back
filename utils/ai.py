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
    base_url="https://infusorial-louisa-penetratively.ngrok-free.dev/"
)

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def extract_exclusions(user_input):
    exclusions = []
    lower_input = user_input.lower()
    if "não quero" in lower_input:
        parts = lower_input.split("não quero")[1:]  # tudo após 'não quero'
        for p in parts:
            words = p.strip().split()
            if words:
                exclusions.append(words[0])
    return exclusions

def filter_items_by_exclusion(items, exclusions):
    if not exclusions:
        return items
    filtered = []
    for item in items:
        name_desc = f"{item.name} {item.description}".lower()
        if not any(excl in name_desc for excl in exclusions):
            filtered.append(item)
    return filtered if filtered else items

def llm_select(items, user_input, context="", user_id=None):
    history_text = ""
    preferences_text = ""
    exclusions = extract_exclusions(user_input)
    items_filtered = filter_items_by_exclusion(items, exclusions)
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

    menu_text = "\n".join([f"{item.name}: {item.description}" for item in items_filtered])

    prompt_text = f"""
        Você é uma IA especializada em recomendar pratos de restaurante. Sempre siga estritamente o pedido do usuário. 
        Se o usuário disser que NÃO quer algum ingrediente ou tipo de prato, **não inclua esses itens** na recomendação.

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
        return items_filtered[:4]
    names = [n.strip() for n in response.split(",")][:4]
    recommended = [item for item in items_filtered if item.name in names]
    for item in items_filtered:
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