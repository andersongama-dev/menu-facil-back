import os
import json
import ast
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate

template = """
    Você é um sistema que extrai intenção alimentar do usuário.
    
    Analise o texto e identifique:
    
    1. ingredientes que o usuário quer incluir
    2. ingredientes que o usuário quer excluir
    3. restrições alimentares
    
    Texto do usuário:
    {text}
    
    Retorne SOMENTE JSON no formato:
    
    {{
     "include": [],
     "exclude": [],
     "restrictions": []
    }}
    """

model = ChatOpenRouter(
    model="meta-llama/llama-3.1-8b-instruct",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def parse_user_intent_llm(text: str):
    try:
        response = chain.invoke({"text": text})

        if isinstance(response, list):
            response_text = getattr(response[0], "content", str(response[0])).strip()
        else:
            response_text = getattr(response, "content", str(response)).strip()

    except (RuntimeError, ValueError, TypeError, OSError) as e:
        print(f"Erro na chamada da LLM: {e}")
        return {"include": [], "exclude": [], "restrictions": []}

    try:
        data = json.loads(response_text)
    except (json.JSONDecodeError, ValueError):
        try:
            data = ast.literal_eval(response_text)
        except (SyntaxError, ValueError):
            print("Erro ao interpretar resposta da LLM")
            data = {}

    def ensure_list(value):
        return value if isinstance(value, list) else []

    return {
        "include": ensure_list(data.get("include", [])),
        "exclude": ensure_list(data.get("exclude", [])),
        "restrictions": ensure_list(data.get("restrictions", []))
    }