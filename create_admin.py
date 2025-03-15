import json
import os
from werkzeug.security import generate_password_hash

# File path for storing admin credentials
DATA_FOLDER = "data"
ADMIN_FILE = os.path.join(DATA_FOLDER, "admin.json")

# Ensure data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# Default Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Function to read JSON file
def read_json(file_path, default_data=[]):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return default_data

# Function to write JSON file
def write_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Check if admin already exists
admins = read_json(ADMIN_FILE)
if any(admin["username"] == ADMIN_USERNAME for admin in admins):
    print("Admin user already exists.")
else:
    hashed_password = generate_password_hash(ADMIN_PASSWORD)
    admins.append({"username": ADMIN_USERNAME, "password": hashed_password})
    write_json(ADMIN_FILE, admins)
    print("Default admin user created successfully!")