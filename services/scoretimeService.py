from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
import openmeteo_requests
import requests_cache
from retry_requests import retry
import os
from typing import List, Dict

from utils.find_user import find_user
from utils.items import fetch_all_menu_items, fetch_all_menu_items_name
import requests

model = ChatOpenRouter(
    model="meta-llama/llama-3.1-8b-instruct",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

prompt = ChatPromptTemplate.from_template("""
    Você é um sistema de recomendação de restaurante baseado no clima.
    
    Temperatura atual: {temperature}°C
    
    Menu:
    {menu}
    
    Escolha **exatamente 4 pratos** do menu, considerando o clima.
    
    Regras:
    - Dias quentes (>25°C): escolha **apenas** pratos leves, frios ou refrescantes. Não inclua pratos quentes ou pesados.
    - Dias amenos (15–25°C): escolha pratos equilibrados (nem muito leves, nem muito pesados).
    - Dias frios (<15°C): escolha **apenas** pratos quentes e mais pesados. Não inclua pratos frios.
    - NÃO invente pratos.
    - Use APENAS nomes do menu.
    - NÃO explique nada.
    - Responda **somente com os nomes dos 4 pratos**, separados por vírgula, sem ponto final.
    
    Resposta:
    Somente os 4 nomes separados por vírgula.
    """)

chain = prompt | model

menu_items = fetch_all_menu_items()
menu_category = fetch_all_menu_items_name()

def parse_llm_response(response) -> List[str]:
    if isinstance(response, list):
        text = getattr(response[0], "content", str(response[0]))
    else:
        text = getattr(response, "content", str(response))
    return [n.strip() for n in text.split(",") if n.strip()]

def llm_select_by_weather(temperature: float) -> List:
    response = chain.invoke({"menu": menu_category, "temperature": temperature})
    names = parse_llm_response(response)
    recommended = []
    for name in names:
        name_clean = name.strip().rstrip(".").lower()
        for item in menu_items:
            if item.name.lower() == name_clean:
                recommended.append(item)
    if len(recommended) < 4:
        recommended += [item for item in menu_items if item not in recommended][:4-len(recommended)]
    return recommended

cache_session: requests_cache.CachedSession = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
session: requests.Session = retry_session
openmeteo_client = openmeteo_requests.Client(session=session)

def get_temperature_by_coords(lat: float, lon: float, ) -> float:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "hourly": "temperature_2m"}
    responses = openmeteo_client.weather_api(url, params=params)
    response = responses[0]
    hourly_temperature_2m = response.Hourly().Variables(0).ValuesAsNumpy()
    return float(hourly_temperature_2m[0])

def recommend_menu_by_location(lat: float, lon: float, user_email) -> Dict:
    find_user(user_email)
    current_temp = get_temperature_by_coords(lat, lon)
    recommended_dishes = llm_select_by_weather(current_temp)
    return {
        "temperature": current_temp,
        "dishes": recommended_dishes
    }