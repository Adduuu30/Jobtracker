# JobTracker

A full-stack **Job Application Tracking System** built with **Python, Flask, SQLite, HTML, CSS, and Bootstrap**.

JobTracker helps users organize and manage their job applications from a single dashboard instead of maintaining everything manually in spreadsheets or notes.

## 🚀 Live Demo

**Live Application:** https://jobtracker-crz7.onrender.com

> The application is deployed on Render's free tier, so the first request may take a few seconds if the service has been inactive.

## ✨ Features

* 🔐 User registration and login
* 👤 User profile management
* 📊 Dashboard with application statistics
* ➕ Add new job applications
* 🔎 Search applications by company
* 🎯 Filter applications by status
* ↕️ Sort applications by latest or oldest
* ✏️ Manage and update job applications
* 📄 Store resume version used for each application
* 🔗 Save job posting links
* 📝 Add notes for individual applications
* 📈 Track Applied, Interview, Selected, and Rejected applications
* 👥 User-specific application data
* 🔒 Password hashing for user accounts
* 🌐 Deployed as a live web application

## 🛠️ Tech Stack

**Backend**

* Python
* Flask
* SQLite

**Frontend**

* HTML5
* CSS3
* Bootstrap
* Jinja2 Templates

**Tools & Deployment**

* Git
* GitHub
* Render

## 📂 Project Structure

```text
Jobtracker/
│
├── templates/
│   ├── add_job.html
│   ├── base.html
│   ├── index.html
│   ├── jobs.html
│   ├── login.html
│   ├── manage_jobs.html
│   ├── my_profile.html
│   └── signup.html
│
├── app.py
├── add_user_id.py
├── requirements.txt
├── .gitignore
├── README.md
└── jobtracker.db
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Adduuu30/Jobtracker.git
cd Jobtracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## 🗄️ Database

JobTracker uses **SQLite** for local data storage.

The database contains user and job application information, including:

* User accounts
* Company
* Job role
* Location
* Salary
* Application status
* Application date
* Resume version
* Job link
* Notes

## 🔐 Authentication

The application includes a basic authentication system with:

* User signup
* User login
* Session-based authentication
* Password hashing
* User-specific job application access
* Profile editing

## 📊 Dashboard

The dashboard provides an overview of the user's job search activity, including:

* Total applications
* Applied applications
* Interview applications
* Selected applications
* Rejected applications
* Recently added applications

## 🎯 Purpose

This project was built to practice and demonstrate practical **Flask web development**, including:

* Routing
* HTTP GET/POST requests
* Jinja2 templating
* Form handling
* SQLite database operations
* CRUD operations
* User authentication
* Session management
* Password hashing
* Search and filtering
* Git/GitHub workflow
* Web application deployment

## 👨‍💻 Author

**Addu**

GitHub: https://github.com/Adduuu30

---

⭐ If you find this project useful, consider giving it a star.
