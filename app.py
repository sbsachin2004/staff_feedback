from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

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

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Admin Login
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        admins = read_json(ADMIN_FILE)
        admin = next((a for a in admins if a["username"] == username), None)
        
        if admin and check_password_hash(admin["password"], password):
            session["admin"] = username
            return redirect("/admin_dashboard")
        else:
            return render_template("admin_login.html", error="Invalid username or password!")
    
    return render_template("admin_login.html")

# Admin Dashboard
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    
    feedback_list = read_json(FEEDBACK_FILE)
    staff_list = read_json(STAFF_FILE)
    
    return render_template("admin_dashboard.html", feedback_list=feedback_list, staff_list=staff_list)

# Route to Create a New Admin
@app.route("/create_admin", methods=["POST"])
def create_admin():
    if "admin" not in session:
        return redirect("/admin")
    
    new_username = request.form["new_username"]
    new_password = request.form["new_password"]
    hashed_password = generate_password_hash(new_password)
    
    admins = read_json(ADMIN_FILE)
    if any(a["username"] == new_username for a in admins):
        return render_template("admin_dashboard.html", error="Username already exists!")
    
    admins.append({"username": new_username, "password": hashed_password})
    write_json(ADMIN_FILE, admins)
    return render_template("admin_dashboard.html", message="Admin created successfully!")

# Add Staff
@app.route("/admin/add_staff", methods=["POST"])
def add_staff():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    
    name = request.form["name"]
    department = request.form["department"]
    subject = request.form["subject"]
    
    staff_list = read_json(STAFF_FILE)
    staff_list.append({"name": name, "department": department, "subject": subject})
    write_json(STAFF_FILE, staff_list)
    
    return redirect(url_for("admin_dashboard"))

# Delete Feedback
@app.route("/admin/delete_feedback/<int:id>")
def delete_feedback(id):
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    
    feedback_list = read_json(FEEDBACK_FILE)
    feedback_list = [f for f in feedback_list if f.get("id") != id]
    write_json(FEEDBACK_FILE, feedback_list)
    
    return redirect(url_for("admin_dashboard"))

# Student Feedback
@app.route("/student_feedback", methods=["GET", "POST"])
def student_feedback():
    staff_list = read_json(STAFF_FILE)
    
    if request.method == "POST":
        department = request.form["department"]
        year = request.form["year"]
        staff_name = request.form["staff_name"]
        subject = request.form["subject"]
        rating = int(request.form["rating"])
        feedback = request.form["feedback"]
        
        feedback_list = read_json(FEEDBACK_FILE)
        new_id = (max([f["id"] for f in feedback_list], default=0) + 1)
        feedback_list.append({"id": new_id, "department": department, "year": year, "staff_name": staff_name, "subject": subject, "rating": rating, "feedback": feedback})
        write_json(FEEDBACK_FILE, feedback_list)
        
        return redirect(url_for("home"))
    
    return render_template("student_feedback.html", staff_list=staff_list)

# Admin Logout
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)