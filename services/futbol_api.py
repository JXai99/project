import requests

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