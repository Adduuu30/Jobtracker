from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
# --------------------------
# Create Database
# --------------------------
def create_database():
    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            salary TEXT,
            status TEXT,
            apply_date TEXT,
            resume_version TEXT,
            job_link TEXT,
            notes TEXT
        )
    """)

    # Add user_id to old jobs table if it doesn't exist
    cursor.execute("PRAGMA table_info(jobs)")
    columns = [column[1] for column in cursor.fetchall()]

    if "user_id" not in columns:
        cursor.execute("ALTER TABLE jobs ADD COLUMN user_id INTEGER")

    conn.commit()
    conn.close()
# --------------------------
# Home Page
# --------------------------
@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    # Total Jobs
    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE user_id = ?",
        (user_id,)
    )
    total_jobs = cursor.fetchone()[0]

    # Applied Jobs
    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE user_id = ? AND status = 'Applied'",
        (user_id,)
    )
    applied_jobs = cursor.fetchone()[0]

    # Interview Jobs
    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE user_id = ? AND status = 'Interview'",
        (user_id,)
    )
    interview_jobs = cursor.fetchone()[0]

    # Selected Jobs
    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE user_id = ? AND status = 'Selected'",
        (user_id,)
    )
    selected_jobs = cursor.fetchone()[0]

    # Rejected Jobs
    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE user_id = ? AND status = 'Rejected'",
        (user_id,)
    )
    rejected_jobs = cursor.fetchone()[0]

    # Recent Applications - Current User Only
    cursor.execute("""
        SELECT * FROM jobs
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 5
    """, (user_id,))

    recent_jobs = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        total_jobs=total_jobs,
        applied_jobs=applied_jobs,
        interview_jobs=interview_jobs,
        selected_jobs=selected_jobs,
        rejected_jobs=rejected_jobs,
        recent_jobs=recent_jobs
    )
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("jobtracker.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """, (name, email, hashed_password))

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Email already registered"

        conn.close()

        return redirect("/login")

    return render_template("signup.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("jobtracker.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]

            return redirect("/jobs")

        return "Invalid email or password"

    return render_template("login.html")
@app.route("/my-account")
def my_account():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, email FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
        "my_account.html",
        user=user
    )
#--------------------------
# my profile
#--------------------------
@app.route("/my-profile", methods=["GET", "POST"])
def my_profile():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]

        cursor.execute(
            "SELECT id FROM users WHERE email=? AND id!=?",
            (email, user_id)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            flash("Email already exists.", "danger")
            return redirect("/my-profile")

        cursor.execute("""
            UPDATE users
            SET name=?, email=?
            WHERE id=?
        """, (
            name,
            email,
            user_id
        ))

        conn.commit()
        conn.close()

        flash("Profile updated successfully!", "success")
        return redirect("/my-profile")

    cursor.execute("""
        SELECT name, email
        FROM users
        WHERE id=?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return render_template(
        "my_profile.html",
        user=user
    )
#--------------------------
# Edit Profile
#--------------------------
@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]

        cursor.execute("""
            UPDATE users
            SET name = ?, email = ?
            WHERE id = ?
        """, (name, email, user_id))

        conn.commit()
        conn.close()

        return redirect("/my-profile")

    cursor.execute(
        "SELECT name, email FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template("edit_profile.html", user=user)
#--------------------------
# change password
#--------------------------
@app.route("/change-password", methods=["POST"])
def change_password():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    # Passwords do not match
    if new_password != confirm_password:
        flash("New passwords do not match.", "warning")
        return redirect("/my-profile")

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE id = ?",
        (user_id,)
    )

    stored_password = cursor.fetchone()[0]

    # Current password incorrect
    if not check_password_hash(stored_password, current_password):
        conn.close()
        flash("Current password is incorrect.", "danger")
        return redirect("/my-profile")

    # Update password
    new_hashed_password = generate_password_hash(new_password)

    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE id = ?
    """, (
        new_hashed_password,
        user_id
    ))

    conn.commit()
    conn.close()

    flash("Password changed successfully!", "success")
    return redirect("/my-profile")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
# --------------------------
# View All Jobs
# --------------------------
@app.route("/jobs")
def jobs():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    sort = request.args.get("sort", "latest")

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    # Total jobs - current user only
    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE user_id = ?",
        (user_id,)
    )
    total_jobs = cursor.fetchone()[0]

    # Applied jobs - current user only
    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE user_id = ? AND status = 'Applied'",
        (user_id,)
    )
    applied_jobs = cursor.fetchone()[0]

    # Interview jobs - current user only
    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE user_id = ? AND status = 'Interview'",
        (user_id,)
    )
    interview_jobs = cursor.fetchone()[0]

    # Selected jobs - current user only
    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE user_id = ? AND status = 'Selected'",
        (user_id,)
    )
    selected_jobs = cursor.fetchone()[0]

    # Rejected jobs - current user only
    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE user_id = ? AND status = 'Rejected'",
        (user_id,)
    )
    rejected_jobs = cursor.fetchone()[0]


    # Fetch current user's jobs
    query = "SELECT * FROM jobs WHERE user_id = ?"
    params = [user_id]


    # Search by company
    if search:
        query += " AND company LIKE ?"
        params.append("%" + search + "%")


    # Filter by status
    if status:
        query += " AND status = ?"
        params.append(status)


    # Sort
    if sort == "latest":
        query += " ORDER BY id DESC"
    else:
        query += " ORDER BY id ASC"


    cursor.execute(query, params)
    jobs = cursor.fetchall()

    conn.close()


    return render_template(
        "jobs.html",
        jobs=jobs,
        total_jobs=total_jobs,
        applied_jobs=applied_jobs,
        interview_jobs=interview_jobs,
        selected_jobs=selected_jobs,
        rejected_jobs=rejected_jobs,
        search=search,
        status=status,
        sort=sort
    )
# --------------------------
# Add Job
# --------------------------
@app.route("/add-job", methods=["GET", "POST"])
def add_job():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        location = request.form["location"]
        apply_date = request.form["apply_date"]
        status = request.form["status"]

        user_id = session["user_id"]

        conn = sqlite3.connect("jobtracker.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO jobs
            (company, role, location, status, apply_date, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company,
            role,
            location,
            status,
            apply_date,
            user_id
        ))

        conn.commit()
        conn.close()

        return redirect("/jobs")

    return render_template("add_job.html", job=None)
# --------------------------
# Edit Job
# --------------------------
@app.route("/edit-job/<int:id>", methods=["GET", "POST"])
def edit_job(id):

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    # Check that this job belongs to the logged-in user
    cursor.execute(
        "SELECT * FROM jobs WHERE id = ? AND user_id = ?",
        (id, user_id)
    )

    job = cursor.fetchone()

    if job is None:
        conn.close()
        return "Unauthorized", 403

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        location = request.form["location"]
        apply_date = request.form["apply_date"]
        status = request.form["status"]

        cursor.execute("""
            UPDATE jobs
            SET company=?,
                role=?,
                location=?,
                status=?,
                apply_date=?
            WHERE id=? AND user_id=?
        """, (
            company,
            role,
            location,
            status,
            apply_date,
            id,
            user_id
        ))

        conn.commit()
        conn.close()

        flash("Job updated successfully!", "success")

        return redirect("/jobs")

    conn.close()

    return render_template("add_job.html", job=job)
# --------------------------
# Delete Job
# --------------------------
@app.route("/delete-job/<int:id>")
def delete_job(id):

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM jobs
        WHERE id = ? AND user_id = ?
    """, (id, user_id))

    conn.commit()
    conn.close()

    flash("Job deleted successfully!", "danger")

    return redirect("/jobs")
#--------------------------
# status update
#--------------------------
@app.route("/update-status/<int:id>", methods=["POST"])
def update_status(id):

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    status = request.form["status"]

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET status = ?
        WHERE id = ? AND user_id = ?
    """, (status, id, user_id))

    conn.commit()
    conn.close()

    return redirect("/jobs")
# --------------------------
# Manage jobs
# --------------------------
@app.route("/manage-jobs")
def manage_jobs():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    jobs = cursor.fetchall()

    conn.close()

    return render_template(
        "manage_jobs.html",
        jobs=jobs
    )
create_database()

if __name__ == "__main__":
    app.run(debug=True)