import os
from flask import render_template
from dotenv import load_dotenv
from services.cache_service import save_scores, get_cached_scores, unified_format_render
from services.futbol_api import lookup


load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable is not set")  

def get_scores(matchday):


    # 1. VERIFICO SI ESTA EN DB, DEBO UNIFICAR FORMATO Y RENDER
    cached_matches = get_cached_scores(matchday)
    #print("DebuggLINE7scores_service: ", cached_matches)
    format_matches = unified_format_render(cached_matches)
    #print("DebuggLINE194:", format_matches)
    #extracted = format_matches.get("homeTeam",{}).get("id")
    if format_matches:
        
        print("existe objeto format matches")
        return format_matches
    
    
    # 2. IF NO CACHE → CALL API
    headers = {"X-Auth-Token": API_KEY}
    try:
        api_data = lookup(matchday, headers)
        if api_data is None:
            return apology("No data found for the specified matchday", 404)
    except Exception as e:
        print ("API Error:", e)
        return apology("Error fetching data from API", 500)
    #SEASON IS DEFAULT WHEN QUERY DB WILL GENERATE SEASON, WHEN SAVING NEED TO EXTRACT SEASON FROM API, ALL INFO FROM API
    season_extracted = api_data.get("filters",{}).get("season")

    #EXTRAE MATCHES FROM API_DATA
    matches = api_data.get("matches", [])
    '''
        #manipulating result after post event to get specific match details for testing
        matchid=540417
        for match in matches:
            if match["id"] == matchid:
                print(match["homeTeam"]["name"], "vs", match["awayTeam"]["shortName"])
    '''
    all_finished = all(match["status"] == "FINISHED" for match in matches)
    if all_finished:
        save_scores(matchday,matches,season_extracted)
    return matches