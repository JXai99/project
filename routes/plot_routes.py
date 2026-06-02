from flask import Blueprint, render_template, request, flash, redirect
from services.plotting_service import generate_plot, find_match_id
from helpers import login_required, apology, VALID_TEAMS

#Blueprint for plotting routes
plotting_bp = Blueprint('plotting', __name__)

#Route for plot page. plotting.html wil have a form to input match_id, home_team and away_team
@plotting_bp.route('/plot', methods=['GET', 'POST'])
@login_required
def get_match_plot():
    if request.method == "POST":
    # Example usage of the plotting service
        #match_id = 3857286  # Replace with actual match ID
        #home_team = "Ecuador"  # Replace with actual home team name
        #away_team = "Qatar"  # Replace with actual away team name
        
        team1 = request.form.get("team1")
        team2 = request.form.get("team2")
        
        if not team1 or not team2:
            return apology("Invalid team", 400)
        
        result = find_match_id(team1, team2)  # store first
        if result is None:                     # check before unpacking
            return apology("Invalid match", 400)
            #print(f"[ERROR] No match found for '{team1}' vs '{team2}'. Check team names.")
        match_id_required, home_team_required, away_team_required = result
        try:
            plot_filename = generate_plot(match_id_required, home_team_required, away_team_required)
            plot_filename = plot_filename.replace("static/", "")
            print("Debuggline20plot_routes ",plot_filename)
            return render_template("shotmap.html", plot_filename = plot_filename,team1=home_team_required, team2=away_team_required, teams = sorted(VALID_TEAMS))
            return {'plot': plot_filename, 'status': 'success'}
        except (ValueError, RuntimeError) as e:
            flash(str(e), "danger")
            return apology("Plotting Error ", 400)   
    return render_template("shotmap.html", teams = sorted(VALID_TEAMS))
