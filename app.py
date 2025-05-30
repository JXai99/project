import os
import requests
#from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd, query_db, engine, write_db
from dotenv import load_dotenv

load_dotenv()


# Configure application
app = Flask(__name__)


# replace with your Football-Data.org key
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable is not set")  
BASE_URL = "https://api.football-data.org/v4/competitions/BL1/matches"

# Ensure templates are auto-reloaded
#app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config["SECRET_KEY"] = "your_secret_key"
#app.secret_key = "your_super_secret_key"

# Configure CS50 Library to use SQLite database
#db = SQL(DATABASE_URL)
#db = SQL("sqlite:///scores.db")
# Try to get DATABASE_URL from environment, fallback to local SQLite
#DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///scores.db")
#if not DATABASE_URL:
#    raise RuntimeError("DATABASE_URL not set"
#engine = create_engine(DATABASE_URL)
#engine = create_engine(os.environ["DATABASE_URL"])


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
#@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        name = request.form.get("username")
        if not name:
            return apology("must provide username", 400)
        pw1 = request.form.get("password")
        pw2 = request.form.get("confirmation")
        if not pw1 or not pw2:
            return apology("must provide password", 400)
        if pw1 != pw2:
            flash("Passwords do not match!", "danger")
            return apology("must provide password correctly", 400)
        #rows = db.execute("SELECT username FROM users")  OLD STYLE CS50 TO NEW
        rows = query_db("SELECT username FROM users")
        for row in rows:

            if (row["username"]) == name:
                flash("Username already exist!", "warning")
                return apology("Username already exist", 400)
        #print("username ok")
        hash = generate_password_hash(pw1)

        #update=db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", name, hash)
        update = write_db("INSERT INTO users (username, hash) VALUES (:username, :hash)", {"username": name, "hash": hash})

        if update == 0:
            flash("Username Not Registered", "success")
            return apology("Username Not Registered", 400)
        #rowsid = db.execute("SELECT id FROM users")
        #session["user_id"] = rowsid[0]["id"]
        flash("Registered successfully!", "success")
        return redirect("/login")

    else:
        return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):

            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        #rows = db.execute(
        #    "SELECT * FROM users WHERE username = ?", request.form.get("username")
        #)
        username = request.form.get("username")

        rows = query_db(
            "SELECT * FROM users WHERE username = :username",
            {"username": username}
        )
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/indexin")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/indexin", methods=["GET"])
@login_required
def indexin():
    if request.method == "GET":
        print("indexin HOMEPAGE")
        return render_template("indexin.html")
    
@app.route("/about", methods=["GET"])
@login_required
def about():
    if request.method == "GET":
        return render_template("aboutme.html")
    
@app.route("/contact", methods=["GET"])
@login_required
def contact():
    if request.method == "GET":
        return render_template("contactme.html")
    
@app.route("/scores", methods=["GET", "POST"])
@login_required
def scores():
    if request.method == "POST":
        matchday = int(request.form.get("matchday"))
    else:
        matchday = request.args.get("matchday", default=1, type=int)

    headers = {"X-Auth-Token": API_KEY}
    result = lookup(matchday, headers)

    matches = []
    if result:
        matches = result.get("matches", [])

    return render_template("scores.html", matches=matches, current_matchday=matchday)





@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


#if __name__ == "__main__":
#    app.run(debug=True)