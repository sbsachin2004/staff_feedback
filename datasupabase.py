import os
from supabase import create_client

# Supabase credentials (Replace with your actual details)
SUPABASE_URL = "https://rovmncqgvsgzapykctiv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvdm1uY3FndnNnemFweWtjdGl2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIxMTA3NDAsImV4cCI6MjA1NzY4Njc0MH0.KCLknrB0SJ6Zr9mfnNCVgZEiC0mydfW4E9IKDWY_MPI"

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Define bucket name and folder path
BUCKET_NAME = "json-files"
LOCAL_FOLDER = r"E:\student_staff_feedback\data"  # JSON files location
STORAGE_FOLDER = "uploads"  # Folder inside Supabase Storage

# Get all JSON files from the folder
json_files = [f for f in os.listdir(LOCAL_FOLDER) if f.endswith(".json")]

# Upload each JSON file
for json_file in json_files:
    local_file_path = os.path.join(LOCAL_FOLDER, json_file)
    storage_path = f"{STORAGE_FOLDER}/{json_file}"  # Path in Supabase Storage

    with open(local_file_path, "rb") as file:
        response = supabase.storage.from_(BUCKET_NAME).upload(storage_path, file)
    
    print(f"Uploaded: {json_file} ✅")

print("✅ All files uploaded successfully!")
