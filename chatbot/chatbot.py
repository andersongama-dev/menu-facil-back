from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
    
    Responda a questão abaixo.
    
    Esté é um historico da nossa conversa {context}
    
    Pergunta {question}
    
    Resposta:
    """

model = OllamaLLM(model="llama3:latest", base_url="http://localhost:11434")
prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model


def manter():
    context = ""
    print("Seja bem vindo a IA do menu facil. Digite sair para encerrar o chat")

    while True:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            break
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\n AI: {result}"

if __name__ == "__main__":
    manter()