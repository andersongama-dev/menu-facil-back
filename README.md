# MenuFacil API v1.5.0

[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

## Descrição

**MenuFacil** é uma API construída com **FastAPI** para gerenciamento de cardápio, pedidos de usuários e recomendações inteligentes com IA.  

Principais funcionalidades:  
- Gerenciamento de usuários, itens de menu, categorias, ingredientes e restrições dietéticas.  
- Registro de pedidos de usuários.  
- Armazenamento de preferências detectadas do usuário (`user_preferences`).  
- Registro de interações da IA (`ai_interactions`) para aprimorar recomendações futuras.  
- Recomendações personalizadas usando o modelo **LLaMA3** via **Ollama**.

A documentação interativa está disponível em [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs).

---

## Tecnologias

- Python 3.10+  
- FastAPI  
- Banco de dados na nuvem (PostgreSQL ou similar)  
- Uvicorn  
- Ollama + LLaMA3 (recomendações de IA)

---

## Clonando o Repositório

```bash
git clone https://github.com/andersongama-dev/menu-facil-back.git
cd menu-facil-back

```

## Configurando o Ambiente

Crie e ative um ambiente virtual:

```bash
python -m venv venv

Linux / Mac:

source venv/bin/activate

Windows:

venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt

```

Observação: Para usar as recomendações de IA, instale Ollama seguindo esta documentação
 e certifique-se de ter o modelo LLaMA3 disponível localmente.

### Configuração do Banco de Dados

O banco de dados está hospedado na nuvem. Configure as credenciais via variáveis de ambiente:

```bash
Linux / Mac:

export DB_URL="postgresql://usuario:senha@host:porta/banco"
```
```bash
Windows (PowerShell):

setx DB_URL "postgresql://usuario:senha@host:porta/banco"
```

## Rodando a API
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

A API estará disponível em http://localhost:8080

A documentação interativa pode ser acessada em http://127.0.0.1:8080/docs

## Endpoints Principais
Usuários

- POST /user/register – Criar usuário

- GET /user/login/{user_email} – Buscar usuário e autenticar

Menu

- GET /menu/ – Listar itens do cardápio

- GET /menu/{menu_id} – Consultar item específico

Pedidos

- POST /order/ – Criar pedido

- GET /order/{user_id} – Listar todos os pedidos de um usuário

IA e Recomendações

- GET /ai/suggest – Buscar sugestão da IA baseada em preferências do usuário

## Banco de Dados

Principais tabelas:

- users

- ai_interactions – registra interações do usuário com a IA

- user_preferences – salva preferências detectadas do usuário

- categories

- menu_items

- ingredients

- menu_item_ingredients

- dietary_restrictions

- menu_item_restrictions

- orders

Relações:

- ai_interactions.id_user → users.id_user

- user_preferences.id_user → users.id_user (cascade delete)

- menu_items.id_category → categories.id_category

- menu_item_ingredients.id_item → menu_items.id_item (cascade delete)

- menu_item_ingredients.id_ingredient → ingredients.id_ingredient (cascade delete)

- menu_item_restrictions.id_item → menu_items.id_item (cascade delete)

- menu_item_restrictions.id_restriction → dietary_restrictions.id_restriction (cascade delete)

- orders.id_user → users.id_user

## Observações

- Preparada para deploy em servidores que suportem FastAPI/uvicorn.

- Salva interações de IA e preferências do usuário para melhorar recomendações futuras.

- Documentação interativa disponível via Swagger UI: http://127.0.0.1:8080/docs

## MIT License
