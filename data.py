import sqlite3
from werkzeug.security import generate_password_hash

def create_admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create admin table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")
    hashed_password = generate_password_hash(password)
    
    try:
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("Admin user created successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists! Try a different one.")
    
    conn.close()

if __name__ == "__main__":
    create_admin()
