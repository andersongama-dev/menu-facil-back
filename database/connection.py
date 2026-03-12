import sqlite3

DB_FILE = "menufacil.db"

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

def populate_test_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", ("Massas", "Pratos à base de macarrão e massas italianas"))
    cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", ("Hambúrgueres", "Hambúrgueres artesanais"))
    cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", ("Bebidas", "Bebidas não alcoólicas"))
    cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", ("Sobremesas", "Doces e sobremesas da casa"))

    ingredients = ['Tomate','Alho','Azeite','Queijo','Leite','Cogumelo','Carne bovina','Frango','Pão','Alface','Batata','Chocolate','Morango','Manjericão','Massa']
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
        ("Macarrão Alho e Óleo","Macarrão com alho dourado e azeite",28.00,10.00,18.00,1),
        ("Macarrão ao Pesto","Macarrão com molho pesto de manjericão",32.00,12.00,20.00,1),
        ("Macarrão com Cogumelos","Macarrão com cogumelos salteados",34.00,13.00,21.00,1),
        ("Hambúrguer Clássico","Hambúrguer com carne, queijo, alface e tomate",30.00,14.00,16.00,2),
        ("Hambúrguer de Frango","Hambúrguer com filé de frango grelhado",29.00,13.00,16.00,2),
        ("Batata Frita","Porção de batata frita crocante",15.00,6.00,9.00,2),
        ("Refrigerante","Lata de refrigerante 350ml",8.00,3.00,5.00,3),
        ("Suco Natural","Suco natural de frutas",10.00,4.00,6.00,3),
        ("Brownie de Chocolate","Brownie artesanal com chocolate",16.00,6.00,10.00,4),
        ("Morango com Chocolate","Morango fresco coberto com chocolate",18.00,7.00,11.00,4)
    ]
    for name, desc, price, cost, profit, cat_id in menu_items:
        cursor.execute("""
            INSERT INTO menu_items (name, description, price, cost, profit_margin, id_category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, desc, price, cost, profit, cat_id))

    conn.commit()
    cursor.close()
    conn.close()
    print("Dados de teste inseridos com sucesso!")

if __name__ == "__main__":
    create_tables()
    populate_test_data()

