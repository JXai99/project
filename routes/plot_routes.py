from flask import Blueprint, render_template, request, flash, redirect
from services.plotting_service import generate_plot
from helpers import login_required, apology

#Blueprint for plotting routes
plotting_bp = Blueprint('plotting', __name__)

#Route for plot page. plotting.html wil have a form to input match_id, home_team and away_team
@plotting_bp.route('/plot', methods=['GET', 'POST'])
@login_required
def get_match_plot():
    if request.method == "GET":
    # Example usage of the plotting service
        match_id = 3857286  # Replace with actual match ID
        home_team = "Ecuador"  # Replace with actual home team name
        away_team = "Qatar"  # Replace with actual away team name

        try:
            plot_filename = generate_plot(match_id, home_team, away_team)
            return {'plot': plot_filename, 'status': 'success'}
        except ValueError as e:
            flash(str(e), "danger")
            return redirect("/indexin")   
