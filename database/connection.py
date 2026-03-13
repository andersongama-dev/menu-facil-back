import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "menufacil.db")

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_interactions (
            id_interaction INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            input_text TEXT,
            parsed_intent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_user) REFERENCES users(id_user)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id_preference INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            preference_type TEXT,
            preference_value TEXT,
            confidence_score REAL,
            FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id_category INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            cost REAL,
            profit_margin REAL,
            id_category INTEGER,
            is_available INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_category) REFERENCES categories(id_category)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id_ingredient INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_item_ingredients (
            id_item INTEGER,
            id_ingredient INTEGER,
            PRIMARY KEY (id_item, id_ingredient),
            FOREIGN KEY (id_item) REFERENCES menu_items(id_item) ON DELETE CASCADE,
            FOREIGN KEY (id_ingredient) REFERENCES ingredients(id_ingredient) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dietary_restrictions (
            id_restriction INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_item_restrictions (
            id_item INTEGER,
            id_restriction INTEGER,
            PRIMARY KEY (id_item, id_restriction),
            FOREIGN KEY (id_item) REFERENCES menu_items(id_item) ON DELETE CASCADE,
            FOREIGN KEY (id_restriction) REFERENCES dietary_restrictions(id_restriction) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id_order INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            total_price REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_user) REFERENCES users(id_user)
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_menu_category ON menu_items(id_category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(id_user)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_menu_ingredients ON menu_item_ingredients(id_ingredient)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_interactions_user ON ai_interactions(id_user)")

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabelas criadas com sucesso!")

def populate_rich_test_data():
    conn = get_connection()
    cursor = conn.cursor()

    categories = [
        ("Massas", "Pratos à base de macarrão e massas italianas"),
        ("Hambúrgueres", "Hambúrgueres artesanais"),
        ("Bebidas", "Bebidas não alcoólicas"),
        ("Sobremesas", "Doces e sobremesas da casa"),
        ("Saladas", "Saladas frescas e saudáveis"),
        ("Sopas", "Sopas quentes e nutritivas")
    ]
    for name, desc in categories:
        cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", (name, desc))

    ingredients = [
        'Tomate','Alho','Azeite','Queijo','Leite','Cogumelo','Carne bovina','Frango','Pão',
        'Alface','Batata','Chocolate','Morango','Manjericão','Massa','Espinafre','Ervilha',
        'Cenoura','Milho','Molho pesto','Molho de tomate','Ovo','Mel','Feijão','Grão-de-bico'
    ]
    for ing in ingredients:
        cursor.execute("INSERT INTO ingredients (name) VALUES (?)", (ing,))

    restrictions = [
        ('Vegetariano', 'Não contém carne'),
        ('Sem lactose', 'Não contém leite ou derivados'),
        ('Sem glúten', 'Não contém trigo ou derivados'),
        ('Vegano', 'Não contém ingredientes de origem animal')
    ]
    for name, desc in restrictions:
        cursor.execute("INSERT INTO dietary_restrictions (name, description) VALUES (?, ?)", (name, desc))

    menu_items = [
        ("Macarrão Alho e Óleo","Massa italiana com alho dourado e azeite de oliva",28.00,10.00,18.00,1),
        ("Macarrão ao Pesto","Macarrão com molho pesto fresco de manjericão e azeite",32.00,12.00,20.00,1),
        ("Macarrão com Cogumelos","Massa com cogumelos salteados e temperos finos",34.00,13.00,21.00,1),
        ("Espaguete à Bolonhesa","Espaguete com molho de carne bovina e tomate",35.00,14.00,21.00,1),
        ("Lasanha Vegetariana","Lasanha de massa com legumes, molho de tomate e queijo",36.00,15.00,21.00,1),
        ("Fettuccine Alfredo","Fettuccine com molho cremoso de queijo e alho",33.00,12.00,21.00,1),

        ("Hambúrguer Clássico","Hambúrguer artesanal com carne bovina, queijo, alface e tomate",30.00,14.00,16.00,2),
        ("Hambúrguer de Frango","Hambúrguer com filé de frango grelhado e molho especial",29.00,13.00,16.00,2),
        ("Hambúrguer Vegano","Hambúrguer à base de grão-de-bico, sem queijo e sem carne",32.00,12.00,20.00,2),
        ("Cheeseburger","Hambúrguer de carne bovina com queijo, cebola e molho barbecue",31.00,14.00,17.00,2),

        ("Salada Caprese","Tomate, queijo mussarela, manjericão e azeite",20.00,8.00,12.00,5),
        ("Salada Verde","Alface, espinafre, rúcula e cenoura ralada",18.00,7.00,11.00,5),
        ("Salada de Grãos","Ervilha, milho, cenoura e molho leve",22.00,9.00,13.00,5),
        ("Salada Mediterrânea","Tomate, azeitonas, pepino, grão-de-bico e azeite",24.00,10.00,14.00,5),

        ("Refrigerante","Lata de refrigerante 350ml",8.00,3.00,5.00,3),
        ("Suco Natural","Suco natural de frutas variadas",10.00,4.00,6.00,3),
        ("Chá Gelado","Chá gelado de ervas com limão",9.00,3.50,5.50,3),
        ("Café Expresso","Café expresso fresco, puro ou com leite",7.00,2.50,4.50,3),

        ("Brownie de Chocolate","Brownie artesanal com chocolate belga",16.00,6.00,10.00,4),
        ("Morango com Chocolate","Morango fresco coberto com chocolate derretido",18.00,7.00,11.00,4),
        ("Pudim de Leite","Pudim cremoso de leite com calda caramelizada",15.00,5.00,10.00,4),
        ("Sorvete Vegano de Chocolate","Sorvete de chocolate sem leite, 100% vegano",20.00,8.00,12.00,4),
        ("Torta de Maçã","Torta assada com recheio de maçã e canela",19.00,8.00,11.00,4),

        ("Sopa de Legumes","Sopa nutritiva com cenoura, batata e ervilha",14.00,6.00,8.00,6),
        ("Sopa de Abóbora","Sopa cremosa de abóbora e especiarias",16.00,7.00,9.00,6)
    ]

    for name, desc, price, cost, profit, cat_id in menu_items:
        cursor.execute("""
            INSERT INTO menu_items (name, description, price, cost, profit_margin, id_category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, desc, price, cost, profit, cat_id))

    conn.commit()
    cursor.close()
    conn.close()
    print("Banco populado com pratos variados e descrições enriquecidas!")


if __name__ == "__main__":
    create_tables()
    populate_rich_test_data()

