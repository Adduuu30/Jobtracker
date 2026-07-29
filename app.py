from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --------------------------
# Create Database
# --------------------------
def create_database():
    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    """, )

    conn.commit()
    conn.close()



create_database()

# --------------------------
# Home Page
# --------------------------
@app.route("/")
def home():

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    # Total Jobs
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]

    # Applied Jobs
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Applied'")
    applied_jobs = cursor.fetchone()[0]

    # Interview Jobs
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Interview'")
    interview_jobs = cursor.fetchone()[0]

    # Selected Jobs
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Selected'")
    selected_jobs = cursor.fetchone()[0]

    # Rejected Jobs
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Rejected'")
    rejected_jobs = cursor.fetchone()[0]

    # Recent Applications
    cursor.execute("""
    SELECT * FROM jobs
    ORDER BY id DESC
    LIMIT 5
    """)
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

# --------------------------
# View All Jobs
# --------------------------
@app.route("/jobs")
def jobs():

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    sort = request.args.get("sort", "latest")

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    # Total jobs
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]

    # Applied jobs
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Applied'")
    applied_jobs = cursor.fetchone()[0]

    # Interview jobs
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Interview'")
    interview_jobs = cursor.fetchone()[0]

    # Selected jobs
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Selected'")
    selected_jobs = cursor.fetchone()[0]

    # Rejected jobs
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Rejected'")
    rejected_jobs = cursor.fetchone()[0]

    # Fetch jobs with search and status filter
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if search:
        query += " AND company LIKE ?"
        params.append("%" + search + "%")

    if status:
        query += " AND status = ?"
        params.append(status) 
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
        sort=sort,
        
    )
# --------------------------
# Add Job
# --------------------------
@app.route("/add-job", methods=["GET", "POST"])
def add_job():

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        location = request.form["location"]
        apply_date = request.form["apply_date"]
        status = request.form["status"]

        conn = sqlite3.connect("jobtracker.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO jobs
            (company, role, location, status, apply_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            company,
            role,
            location,
            status,
            apply_date
        ))

        conn.commit()
        conn.close()

        return redirect("/jobs")

    return render_template("add_job.html", job=None)
# --------------------------
# Edit Job
# --------------------------
# --------------------------
# Edit Job
# --------------------------
@app.route("/edit-job/<int:id>", methods=["GET", "POST"])
def edit_job(id):

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

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
            WHERE id=?
        """, (
            company,
            role,
            location,
            status,
            apply_date,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/jobs")

    cursor.execute("SELECT * FROM jobs WHERE id=?", (id,))
    job = cursor.fetchone()

    conn.close()

    return render_template("add_job.html", job=job)
# --------------------------
# Delete Job
# --------------------------
@app.route("/delete-job/<int:id>")
def delete_job(id):

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/jobs")
# --------------------------
# Status slider
# --------------------------

@app.route("/update-status/<int:id>", methods=["POST"])
def update_status(id):

    status = request.form["status"]

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET status=?
        WHERE id=?
    """, (status, id))

    conn.commit()
    conn.close()

    return redirect("/jobs")


# --------------------------
# Manage jobs
# --------------------------
@app.route("/manage-jobs")
def manage_jobs():

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
    jobs = cursor.fetchall()

    conn.close()
    

    return render_template("manage_jobs.html", jobs=jobs)
if __name__ == "__main__":
    app.run(debug=True)