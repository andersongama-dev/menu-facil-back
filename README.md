MenuFacil API v1.0
Descrição

MenuFacil é uma API construída com FastAPI para gerenciamento de cardápio, pedidos de usuários e recomendações de IA. Permite gerenciar usuários, itens de menu, categorias, ingredientes, restrições dietéticas e registrar pedidos.

Esta versão inclui dados de teste, estrutura completa do banco SQLite e endpoints básicos para consumo da API.

Tecnologias

Python 3.10+

FastAPI

SQLite

Uvicorn

Clone o repositório:

git clone https://github.com/andersongama-dev/menu-facil-back.git
cd menu-facil-back

Crie e ative um ambiente virtual:

python -m venv venv
# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt

Verifique o banco SQLite (database/menufacil.db) e configure a variável de ambiente opcional DB_FILE caso queira customizar o caminho.

Rodando a API
uvicorn main:app --host 0.0.0.0 --port 8080

A API estará disponível em http://localhost:8080.

Endpoints Principais
Usuários

POST /user/register – Criar usuário

GET /user/login – Buscar um usuário

Menu

GET /menu – Listar itens de menu

GET /menu/{id_item} – Consultar item específico

IA e Recomendações

POST /ai/suggest – Buscar sugestão

Pedidos

POST /order – Criar pedido

Banco de Dados

Banco: SQLite (database/menufacil.db)

Tabelas principais:

users

ai_interactions

user_preferences

categories

menu_items

ingredients

menu_item_ingredients

dietary_restrictions

menu_item_restrictions

orders

Relações

ai_interactions.id_user → users.id_user

user_preferences.id_user → users.id_user (cascade delete)

menu_items.id_category → categories.id_category

menu_item_ingredients.id_item → menu_items.id_item (cascade delete)

menu_item_ingredients.id_ingredient → ingredients.id_ingredient (cascade delete)

menu_item_restrictions.id_item → menu_items.id_item (cascade delete)

menu_item_restrictions.id_restriction → dietary_restrictions.id_restriction (cascade delete)

orders.id_user → users.id_user

Dados de Teste

Categorias: Massas, Hambúrgueres, Bebidas, Sobremesas, Saladas, Sopas

Ingredientes variados e restrições dietéticas incluídas

Itens de menu com descrições, preço, custo e margem de lucro

Observações

Caminho do banco configurável via variável DB_FILE.

Preparado para deploy em servidores que suportem FastAPI/uvicorn.

Banco incluído para facilitar testes e deploy inicial.
