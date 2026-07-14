from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def create_database():
    create_database()
    conn = sqlite3.connect("jobtracker.db")

    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS jobs(
                   id INTEGER PRIMARY KEY AUTOICREMENT,
                   company TEXT NOT NULL,
                   role TEXT NOT NULL,
                   location TEXT,
                   salary TEXT,
                   status TEXT,
                   apply_data TEXT,
                   resume version TEXT,
                   job_link TEXT,
                   notes TEXT
                   )
                   """)
    conn.commit()
    conn.close()

    

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add-job")
def add_job():
    return render_template("add_job.html")


@app.route("/jobs")
def jobs():
    return render_template("jobs.html")
if __name__ == "__main__":
    app.run(debug=True)