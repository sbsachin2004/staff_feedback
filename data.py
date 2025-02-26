import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

# MySQL Connection Function
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",   # Change if using a remote MySQL server
            user="root",        # Replace with your MySQL username
            password="root",  # Replace with your MySQL password
            database="student_feedback_db"   # Ensure this database exists
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Initialize Database and Tables
def init_db():
    conn = connect_db()
    if conn is None:
        return

    cursor = conn.cursor()
    
    # Create Admin Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        username VARCHAR(255) UNIQUE NOT NULL, 
                        password VARCHAR(512) NOT NULL)''')

    # Create Staff Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS staff (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        name VARCHAR(255), 
                        department VARCHAR(255), 
                        subject VARCHAR(255))''')

    # Create Feedback Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        department VARCHAR(255), 
                        year VARCHAR(50), 
                        staff_name VARCHAR(255), 
                        subject VARCHAR(255),
                        rating INT, 
                        feedback TEXT)''')

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully!")

# Create Admin User
def create_admin():
    conn = connect_db()
    if conn is None:
        return

    cursor = conn.cursor()

    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")
    hashed_password = generate_password_hash(password)

    try:
        cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        print("Admin user created successfully!")
    except mysql.connector.IntegrityError:
        print("Username already exists! Try a different one.")
    
    cursor.close()
    conn.close()

# Run the script
if __name__ == "__main__":
    init_db()  # Initialize the database tables
    create_admin()  # Create an admin user
