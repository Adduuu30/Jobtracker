from flask import Flask, render_template, request, redirect
import sqlite3

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
    """)

    conn.commit()
    conn.close()


# --------------------------
# Home Page
# --------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------
# View All Jobs
# --------------------------
@app.route("/jobs")
def jobs():

    conn = sqlite3.connect("jobtracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    conn.close()

    return render_template("jobs.html", jobs=jobs)


# --------------------------
# Add Job
# --------------------------
@app.route("/add-job", methods=["GET", "POST"])
def add_job():

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]

        conn = sqlite3.connect("jobtracker.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO jobs (company, role, status)
        VALUES (?, ?, ?)
        """, (company, role, status))

        conn.commit()
        conn.close()

        return redirect("/jobs")

    return render_template("add_job.html", job=None)


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
        status = request.form["status"]

        cursor.execute("""
        UPDATE jobs
        SET company=?, role=?, status=?
        WHERE id=?
        """, (company, role, status, id))

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
# Run App
# --------------------------
if __name__ == "__main__":
    create_database()
    app.run(debug=True)