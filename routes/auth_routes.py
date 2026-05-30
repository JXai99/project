from flask import Blueprint, render_template, request, flash, redirect, session
from services.db_service import query_db, write_db
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required 

# Blueprint = group of auth-related routes

auth_bp = Blueprint("auth", __name__)
# Route for registration page. register.html will have form to input username and password
#.route() decorator registers the function as a route handler for the specified URL and HTTP methods.

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        #name = request.form.get("username")
        name = request.form.get("username", "").strip().lower()
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
    
@auth_bp.route("/login", methods=["GET", "POST"])
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
        #username = request.form.get("username")
        username = request.form.get("username", "").strip().lower()


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
    