import pandas as pd
#import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import sys

def generate_plot(match_id_required,home_team_required,away_team_required):
    # Generate a plot for the given match ID, home team, and away team
    # This is a placeholder function. You can replace it with your actual plotting logic.
    pitchLengthX=120
    pitchWidthY=80
    home_count = 0
    away_count = 0
    try:
        match_shots_df = load_shots(match_id_required)

    except FileNotFoundError as e:
        raise ValueError(f"Data file missing: {e}") from e
    except ValueError as e:
        raise ValueError(f"CSV parsing error: {e}") from e
        '''
            except RuntimeError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
        #print(match_df.columns)
    '''
    fig,ax=create_pitch()

    for i, shot in match_shots_df.iterrows():
        team = plot_shot(shot, pitchLengthX, pitchWidthY, home_team_required, ax)
        if team == home_team_required:
            home_count += 1
        else:
            away_count += 1
    label_teams(away_team_required,home_team_required,away_count,home_count)

    fig.set_size_inches(13.3,8)
    #fig.savefig("Output/pitch.pdf",dpi=100)
    


    # Save the plot to a file
    plot_filename = f"static/plots/match_{home_team_required}{away_team_required}.png"
    fig.savefig(plot_filename)
    plt.close(fig)
    print("Debbugline48plotting_service:✅Metricas generadas correctamente ✅. Revisar static/plots folder.")

    return plot_filename

def load_shots(match_id: int)-> pd.DataFrame:
    """
    Load and normalize shots event data for a given match_id
    Returns:
        pd.DataFrame:Normalize events DataFrame

    """
    file_name: str="data/events/world_cup_2022_events1.csv"

    try:
        df=pd.read_csv(file_name)
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {file_name}")

    except ValueError as e:
        raise RuntimeError(f"Invalid CSV format: {e}")
    #types
    df["match_id"] = df["match_id"].astype(int)
    #clean
    df = df.dropna(subset=["x", "y"])
    df["player_name"] = df["player_name"].fillna("Unknown")

    # normalize
    df["team_name"] = df["team_name"].str.strip()
    df["player_name"] = df["player_name"].str.strip()
    df["shot_outcome_name"] = df["shot_outcome_name"].str.strip()

    #match_df= df[df["match_id"]==match_id]

    # -------------------------
    # STEP: CLEAN TIME DOMAIN (IMPORTANT FIX)
    # -------------------------
    match_df = df[(df["match_id"] == match_id) & (df["period"] <= 4)]  # ✅ One filter
    #print("CSV generado correctamente ✅")
    return match_df

def create_pitch():
    pitch=Pitch(
        pitch_color="grass",
        line_color="white"
    )
    fig,ax= pitch.draw()
    fig.set_facecolor('#1f1f1f')
    ax.set_facecolor('#1f1f1f')
    return fig,ax

def plot_shot(shot, pitchx, pitchy, home_team, ax):
    x,y=shot["x"], shot["y"]
    team_name=shot["team_name"]
    is_goal=shot["shot_outcome_name"]=="Goal"
    if team_name==home_team:
        plot_x,plot_y=x, pitchy - y
        color="red"
    else:
        plot_x,plot_y=pitchx - x, y
        color="blue"

    alpha=1.0 if is_goal else 0.2

    circle= plt.Circle((plot_x,plot_y),2,color=color, alpha=alpha)
    ax.add_patch(circle)

    if is_goal:
        offset_x = 10 if plot_x < pitchx / 2 else -10
        offset_y = 10 if plot_y < pitchy / 2 else -10

        ax.annotate(
            f"{shot['minute']}' {format_name(shot['player_name'])}",
            xy=(plot_x, plot_y),
            xytext=(offset_x, offset_y),
            textcoords="offset points",
            fontsize=8,
            ha="center",
            va="center",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7),
            arrowprops=dict(arrowstyle="-", color=color, alpha=0.5),
        )
    return team_name

def format_name(name)-> str:

    """
    Format player names to "First Last" or "First Middle Last" → "First Last".
    Args:
        name (str): Original player name
    Returns:
        str: Formatted player name
    """

    parts = name.split()
    if len(parts) <= 1:
        return name
    if len(parts) == 2:
        return f"{parts[0]} {parts[1]}"
    return f"{parts[0]} {parts[-2]}"  # First + Last for 3+ part names

def label_teams(away_team_required,home_team_required,away_count,home_count):
    plt.text(
    5, 75,
    f"{away_team_required}\nShots: {away_count}",
    fontsize=12,
    fontweight="bold",
    color="black",
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="none")
    )
    #plt.text(5,75,away_team_required + ' shots')
    #plt.text(80,75,home_team_required + ' shots')
    plt.text(
    80, 75,
    f"{home_team_required}\nShots: {home_count}",
    fontsize=12,
    fontweight="bold",
    color="black",
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="none")
    )
