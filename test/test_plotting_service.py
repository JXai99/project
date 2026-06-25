from services.plotting_service import format_name
from services.plotting_service import load_shots, create_pitch, plot_shot, generate_plot

def test_format_name():
    assert format_name("Lionel Andres Messi") == "Lionel Andres"

def test_load_shots():
    df = load_shots(3857286)

    assert not df.empty
    assert "x" in df.columns
    assert "y" in df.columns

def test_plot_shot():
    shot = {
        "x": 100,
        "y": 40,
        "team_name": "Ecuador",
        "shot_outcome_name": "Goal",
        "minute": 15,
        "player_name": "Enner Valencia"
    }

    fig, ax = create_pitch()

    team = plot_shot(
        shot,
        120,
        80,
        "Ecuador",
        ax
    )

    assert team == "Ecuador"

# This test assumes that the generate_plot function not returns fig, None, df
def test_generate_plot_returns_filename():
    filename = generate_plot(
        3857286,
        "Ecuador",
        "Qatar"
    )
    #verify that the function returns a filename string that ends with .png
    assert isinstance(filename, str)
    assert filename.endswith(".png")