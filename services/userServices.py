from fastapi import HTTPException
from database.connection import get_connection
from models.user import User

def add_user(name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    cursor.execute(
        "INSERT INTO users (name, email, phone) VALUES (?, ?, ?)",
        (name, email, phone)
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return user_id

def find_user(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return User(
            id_user=row["id_user"],
            name=row["name"],
            email=row["email"],
            phone=row["phone"]
        )
    else:
        raise HTTPException(status_code=404, detail="Usuário não encotrado")