from flask import Blueprint, render_template, request
from helpers import login_required, apology
from services.scores_service import get_scores

# Blueprint = group of score-related routes
scores_bp = Blueprint("scores",__name__)

# Route for scores page. scores.html will have form to input matchday and display results
#.route() decorator registers the function as a route handler for the specified URL and HTTP methods. 
# In this case, it means that when a user visits "/scores" with either a GET or POST request, 
# the scores() function will be called to handle that request. 
# The @login_required decorator ensures that only authenticated users can access this route, 
# redirecting unauthenticated users to the login page.
@scores_bp.route("/scores", methods=["GET", "POST"])
@login_required
def scores():
    games=[]
    matchday = None
    MAX_MATCHDAYS = 34 
    
    if request.method == "POST":
        try:
            matchday = request.form.get("matchday", type=int)
            #matchday = int(request.form.get("matchday")) or 1
            
            #IF IS MISSING OR INVALID
            if matchday is None:
                #raise ValueError("Invalid matchday")
                return apology("Invalid matchday", 400) 
            # 2. Validate it falls within an acceptable range (e.g., 1 to 38)          
            if not (1 <= matchday <= MAX_MATCHDAYS):
                return apology("Invalid matchday", 400)
        except (ValueError, TypeError):
            return apology("Invalid matchday", 400)

        games = get_scores(matchday)

    return render_template("scores.html", matches=games, current_matchday=matchday)