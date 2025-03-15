import json
import os
from werkzeug.security import generate_password_hash

DATA_FOLDER = "data"
ADMIN_FILE = os.path.join(DATA_FOLDER, "admin.json")
STAFF_FILE = os.path.join(DATA_FOLDER, "staff.json")
FEEDBACK_FILE = os.path.join(DATA_FOLDER, "feedback.json")

# Ensure data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

def read_json(file_path, default_data=[]):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return default_data

def write_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Initialize JSON storage if empty
if not os.path.exists(ADMIN_FILE):
    write_json(ADMIN_FILE, [])
if not os.path.exists(STAFF_FILE):
    write_json(STAFF_FILE, [])
if not os.path.exists(FEEDBACK_FILE):
    write_json(FEEDBACK_FILE, [])

def init_db():
    """Initialize the JSON database files."""
    write_json(ADMIN_FILE, read_json(ADMIN_FILE, []))
    write_json(STAFF_FILE, read_json(STAFF_FILE, []))
    write_json(FEEDBACK_FILE, read_json(FEEDBACK_FILE, []))
    print("Database initialized successfully!")

def create_admin():
    """Create an admin user and store it in the JSON database."""
    admins = read_json(ADMIN_FILE)
    
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")
    hashed_password = generate_password_hash(password)
    
    if any(admin["username"] == username for admin in admins):
        print("Username already exists! Try a different one.")
        return
    
    admins.append({"username": username, "password": hashed_password})
    write_json(ADMIN_FILE, admins)
    print("Admin user created successfully!")

if __name__ == "__main__":
    init_db()  # Initialize the database files
    create_admin()  # Create an admin user
