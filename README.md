# JobTracker

JobTracker is a web-based job application tracking system built with Flask and SQLite.

It helps users manage, organize, and track their job applications from a single dashboard.

## Features

- Add new job applications
- Edit existing job applications
- Delete job applications
- Track application status
- Status options:
  - Applied
  - Interview
  - Selected
  - Rejected
- Search applications by company
- Filter applications by status
- Sort applications by latest or oldest
- Dashboard with application statistics
- Recent applications overview
- Manage Jobs section
- Dynamic application counts
- Responsive Bootstrap UI

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- Bootstrap
- Jinja2

## Project Structure

```text
Jobtracker/
│
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_job.html
│   ├── jobs.html
│   └── manage_jobs.html
│
├── requirements.txt
├── .gitignore
└── README.md