import mysql.connector
from werkzeug.security import generate_password_hash

# Database Configuration (Update with your MySQL details)
DB_HOST = "mysql://root:zCepfysNNWiXYLbSVTLHuwqKHzSDayAN@trolley.proxy.rlwy.net:24149/railway"
DB_USER = "root"  # Change if needed
DB_PASSWORD = "root"  # Update with your MySQL password
DB_NAME = "student_feedback_db"  # Update to match your database

# Default Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Hash the admin password
hashed_password = generate_password_hash(ADMIN_PASSWORD)

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()

    # Check if the default admin exists
    cursor.execute("SELECT * FROM admin WHERE username = %s", (ADMIN_USERNAME,))
    existing_admin = cursor.fetchone()

    if existing_admin:
        print("Admin user already exists.")
    else:
        # Insert the default admin credentials
        cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", 
                       (ADMIN_USERNAME, hashed_password))
        conn.commit()
        print("Default admin user created successfully!")

except mysql.connector.Error as e:
    print("Error:", e)

finally:
    cursor.close()
    conn.close()
