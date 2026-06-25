from datetime import date
from services.db_service import query_db, write_db

def get_current_season():
    today = date.today()

    return today.year if today.month >= 7 and today.day >= 24 else today.year - 1

def get_cached_scores(matchday):
    
    comando_query = """
    SELECT *
    FROM scores
    WHERE matchday = :matchday
    AND season = :season

    """
    season = get_current_season()
    return query_db(comando_query,{
        "matchday":matchday,
        "season":season
    })

def unified_format_render(cached_matches):
    formatted_matches=[]
    for match in cached_matches:
        formatted_matches.append({
            "homeTeam":{
                "name":match["home_team"],
                "id":match["home_team_id"]
            },
            "awayTeam":{
                "name":match["away_team"],
                "id":match["away_team_id"]
            },
            "score":{
                "fullTime":{
                    "home":match["home_score"],
                    "away":match["away_score"]
                }
            }

        })
    return formatted_matches

def save_scores(matchday, matches, season):
    for match in matches:
        query = """
        INSERT INTO scores (
            api_match_id,
            season,
            matchday,
            utc_date,
            home_team,
            home_short_name,
            home_team_id,
            away_team,
            away_short_name,
            away_team_id,
            home_score,
            away_score,
            winner,
            status
        )
                VALUES (
            :api_match_id,
            :season,
            :matchday,
            :utc_date,
            :home_team,
            :home_short_name,
            :home_team_id,
            :away_team,
            :away_short_name,
            :away_team_id,
            :home_score,
            :away_score,
            :winner,
            :status
        )
        ON CONFLICT (api_match_id) DO NOTHING;
        """
        write_db(query, {
            "api_match_id":match["id"],
            "season":season,
            "matchday":matchday,
            "utc_date":match["utcDate"],
            "home_team": match["homeTeam"]["name"],
            "home_short_name": match["homeTeam"]["shortName"],
            "home_team_id":match["homeTeam"]["id"],
            "away_team": match["awayTeam"]["name"],
            "away_short_name": match["awayTeam"]["shortName"],
            "away_team_id":match["awayTeam"]["id"],
            "home_score": match["score"]["fullTime"]["home"],
            "away_score": match["score"]["fullTime"]["away"],
            "winner": match["score"]["winner"],
            "status": match["status"]
        })
        print("Salvado Exitosamente")