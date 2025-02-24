from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize Database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT, 
                        password TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS staff (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT, 
                        department TEXT, 
                        subject TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        department TEXT, 
                        year TEXT, 
                        staff_name TEXT, 
                        subject TEXT,
                        rating INTEGER, 
                        feedback TEXT)''')

    conn.commit()
    conn.close()

init_db()

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

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admin WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and check_password_hash(result[0], password):
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

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    feedback_list = cursor.fetchall()
    cursor.execute("SELECT * FROM staff")
    staff_list = cursor.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", feedback_list=feedback_list, staff_list=staff_list)

# Route to Create a New Admin
@app.route("/create_admin", methods=["POST"])
def create_admin():
    if "admin" not in session:
        return redirect("/admin")

    new_username = request.form["new_username"]
    new_password = request.form["new_password"]

    hashed_password = generate_password_hash(new_password)

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (new_username, hashed_password))
        conn.commit()
        conn.close()
        return render_template("admin_dashboard.html", message="Admin created successfully!")
    except sqlite3.IntegrityError:
        return render_template("admin_dashboard.html", error="Username already exists!")

# Add Staff
@app.route("/admin/add_staff", methods=["POST"])
def add_staff():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    name = request.form["name"]
    department = request.form["department"]
    subject = request.form["subject"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO staff (name, department, subject) VALUES (?, ?, ?)", (name, department, subject))
    conn.commit()
    conn.close()
    
    return redirect(url_for("admin_dashboard"))

# Delete Feedback
@app.route("/admin/delete_feedback/<int:id>")
def delete_feedback(id):
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feedback WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for("admin_dashboard"))

# Student Feedback
@app.route("/student_feedback", methods=["GET", "POST"])
def student_feedback():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staff")
    staff_list = cursor.fetchall()
    conn.close()

    if request.method == "POST":
        department = request.form["department"]
        year = request.form["year"]
        staff_name = request.form["staff_name"]
        subject = request.form["subject"]
        rating = request.form["rating"]
        feedback = request.form["feedback"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (department, year, staff_name, subject, rating, feedback) VALUES (?, ?, ?, ?, ?, ?)", 
                       (department, year, staff_name, subject, rating, feedback))
        conn.commit()
        conn.close()
        
        return redirect(url_for("home"))

    return render_template("student_feedback.html", staff_list=staff_list)

# Admin Logout
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    app.run(debug=True)
