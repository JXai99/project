# sportSSoCCer Web App
#### Video Demo:  <URL HERE>
#### Description:
This is my cs50X final project, is a soccer scores web app, that provides you the scores about all the matchdays from 2024-2025 Bundesliga season.
it is a full-stack web application built with Flask for the back-end and html with bootstrap for front-end. It is designed for both local development (using SQLite) and deployment (using PostgreSQL on Render).
The app pulls real-time match data from the [Football-Data.org API](https://www.football-data.org/) and allows users to view the actual matchday, a list of the matches with the home team name and away team name, a center badge for match status and score. And team's logo for every each team, logos from the [Football-Data.org CRESTS API](https://crests.football-data.org/)

sportSSoCCer Web App allows users to register, log in, and track football match results from the German Bundesliga. 

---
## File Structure and Responsibilities

According with flask application strcuture, there is a project directory which contains 'app.py' is the main application entry point. define all the routes and functions to perform for each action. This file is the root of our Flask application. Initializes the Flask app, configures sessions, handles routing for registration, login, logout, homepage, and score viewing.
'helpers.py' Contains utility functions for database queries (`query_db`, `write_db`), as well as helper functions like `apology()` for rendering errors and `lookup()` fetching API data. Also initializes the SQLAlchemy database engine.

'static' folder contains CSS, images, or JavaScript files used to style and enhance the frontend. Inside is the 'favicon.ico' file for this app is a soccer ball emoji. 'schema.sql' where can find the database strcuture developed in PostgreSQL. 'styles.css' has all the classes with color, borders, paddings, gradients, hover events, opacity, positions, height, width and personalized backgrounds for my html pages. And 3 differents .png files inside 'images' folder. Each one of them are a personalized and mixed soccer realistic ilustration generated with sora chat gpt engine. Applying knowledge for prompts and Generative Pre-training Transformer.

'templates' folder contains all HTML templates (e.g., `login.html`, `register.html`, `index.html`, etc.) using Jinja2 templating for dynamic rendering.
'aboutme.html' contains a hero header and a description of what the app is about.A file called 'apology.html' to show error messages.'contactme.html' where is the sportSSoCCer social media contact buttons.'index.html' contains the hero page with a description of the app.'indexin.html' contains the main page once user is loggin.'layout.html' contains the app's pages html template with the bootstrap, favicon, stylesheet reference links and the title in the head part and in the  body part with nav-bar,flashed messages and main block.'login.html' and regsiter.html' have the login form and register form respectively. And 'scores.html' contains a selecr where to chooses the machday and 'view' button. In this page displays a list of the matches, teams, logos, scores and live status.
This project uses Bootstrap, a powerful, open-source frontend toolkit for developing responsive, mobile-first web applications.
In this project, Bootstrap is included via CDN in the HTML templates. It is used to:
Style forms for login and registration pages.
Display alerts for feedback messages using Bootstrap’s alert classes (alert-warning, alert-success, etc.).
Implement responsive navigation bars and layout containers.
Enhance the visual presentation of tables, buttons, and cards on various pages.

'Requirements.txt' lists all Python dependencies required to run the app (e.g., Flask, SQLAlchemy, psycopg2, requests). A text file 'README.md' with the introduction, information and usage of the project.

'Procfile' is a mechanism for declaring what commands for running a Python web application needs, in this case with Gunicorn command 'web: gunicorn app:app', a common practice for deploying Python web apps in production environments.'scores.db' is the sqlite3 database file used for locally development.

'.env' stores environment variables like `DATABASE_URL` and `API_KEY` (not committed to version control).

'.gitignore' file is a text file that tells Git which files or folders to ignore in a project, these files are for Python, Virtual environment, Secrets, VS Code:

__pycache__/
*.pyc

venv/
 
.env

.vscode/ 

.DS_Store (short for Desktop Services Store) is a hidden system file created by macOS in every folder you open in Finder

---

## Technologies Used

- **Backend**: Python (Flask), SQLAlchemy, Jinja2
- **Database**: PostgreSQL (via Render), SQLite (locally)
- **Frontend**: HTML, CSS, Bootstrap
- **API Integration**: Football-Data.org REST API
- **Auth**: Werkzeug’s `generate_password_hash` and `check_password_hash`
- **Deployment**: Render.com (for both backend and database)

---

## Design Decisions

### PostgreSQL vs SQLite
I chose PostgreSQL for production due to its scalability, robust support for concurrent users, and cloud-friendly compatibility (Render.com). For local development and testing, SQLite is used via a fallback mechanism to reduce friction.

<pre> DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///scores.db")
</pre>

This line allows seamless switching between development and production environments with no code changes.

Query Abstraction
To avoid repetitive SQL connection logic, I abstracted query execution into helper functions:
```python
def query_db(query, params=None):
    ...
def write_db(query, params=None):
    ...
```
This promotes DRY (Don’t Repeat Yourself) principles and improves maintainability.

Username Normalization
To prevent confusion from case-sensitive usernames (e.g., "John" vs "john"), I enforce all usernames to be lowercase and whitespace-trimmed during registration and login.
```python
username = request.form.get("username", "").strip().lower()
```

This project was developed as my final project for CS50, Harvard University's introduction to the intellectual enterprises of computer science and the art of programming. It demonstrates principles from web development, RESTful APIs, SQL database design, templating, and user authentication.
