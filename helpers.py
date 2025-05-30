import os
import requests
from flask import redirect, render_template, session
from functools import wraps
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(matchday,headers):
    """Look up quote for symbol."""
    url = f"https://api.football-data.org/v4/competitions/BL1/matches?matchday={matchday}"
    print("ingreso a funcion helpers lookup")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

"""FOR DATABASE POSTGRESQL"""
# Get DATABASE_URL from environment, fallback to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///scores.db")

# Ensure SQLAlchemy-compatible format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Try to create database engine
try:
    engine = create_engine(DATABASE_URL)
except SQLAlchemyError as e:
    print("❌ Database connection failed:", e)
    raise RuntimeError("Failed to connect to the database.") from e

# Query helper
def query_db(query, params=None):
    """Execute a SQL query with optional parameters and return all results."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return result.mappings().all()
            #return result.fetchall()
    except SQLAlchemyError as e:
        print("❌ Query execution failed:", e)
        return None
    
def write_db(query, params=None):
    """Execute a write (INSERT, UPDATE, DELETE) query and return rowcount."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            conn.commit()  # Explicit commit when using raw connections
            return result.rowcount
    except SQLAlchemyError as e:
        print("❌ Write operation failed:", e)
        return 0
