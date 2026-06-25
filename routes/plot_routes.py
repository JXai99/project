from flask import Blueprint, render_template, request, flash, redirect, jsonify
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
        print("Debuggline29 MATCHI_ID", match_id_required)
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

@plotting_bp.route("/api/plot", methods=["POST","GET"])
#@login_required
def api_plot():
    if request.method == "POST":
        # 1. READ JSON FROM FRONTEND
        data = request.get_json()

        home = data.get("home_team")
        away = data.get("away_team")
            # 2. VALIDATE INPUT
        if not home or not away:
            return jsonify({"error": "Missing data"}), 400

        # 3. FIND MATCH ID (NEW IMPORTANT STEP)
        result = find_match_id(home, away)

        if result is None:
            return jsonify({"error": "Match not found"}), 404

        match_id, home_team, away_team = result

        # 4. GENERATE PLOT
        try:
            plot_path,home_goal, away_goal = generate_plot(match_id, home_team, away_team)

            return jsonify({
                #"plot_url": "/" + plot_path,
                "plot_url": f"data:image/png;base64,{plot_path}",  # No "/" prefix
                "home_team": home_team,
                "away_team": away_team,
                "home_goal": home_goal,
                "away_goal": away_goal
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template("shotmap.html", teams = sorted(VALID_TEAMS))