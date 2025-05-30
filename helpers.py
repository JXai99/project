import requests

from flask import redirect, render_template, session
from functools import wraps
import os
from sqlalchemy import create_engine, text


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
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///scores.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def query_db(query, params=None):
    """Execute a SQL query with optional parameters and return all results."""
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        return result.fetchall()