import requests
from .crud import db_connect, add_company, add_genre, add_platform, add_game, add_game_platform, add_game_genre, add_game_company, db_close
from config import igdb_config
from pprint import pprint
from datetime import datetime


class EndOfPageError(Exception):
    """Erreur de in de page"""

# Configuration de l'API IGDB
IGDB_CLIENT_ID = igdb_config["client_id"]
IGDB_CLIENT_SECRET = igdb_config["client_secret"]

# URL pour obtenir le token d'accès
IGDB_AUTH_URL = "https://id.twitch.tv/oauth2/token"

def get_access_token(client_id, client_secret):
    auth_response = requests.post(IGDB_AUTH_URL, params={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    })
    auth_response.raise_for_status()
    return auth_response.json().get('access_token')

def fetch_games(access_token, year:int, limit:int=500, page:int=1 ):
    page = int(max(page, 1))
    offset=(page-1)*limit

    IGDB_API_URL = "https://api.igdb.com/v4/games"
    headers = {
        'Client-ID': IGDB_CLIENT_ID,
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'text/plain'
    }

    payload = f"""
    fields name, cover.url, rating, rating_count, involved_companies.company.name, involved_companies.publisher, involved_companies.developer, genres.name, release_dates.platform.name, release_dates.date, involved_companies.company.websites.url, involved_companies.company.country, storyline, summary, keywords.name;
    where release_dates.y = {year};
    limit {limit};
    offset {offset};
    """

    try:
        response = requests.post(IGDB_API_URL, headers=headers, data=payload)
        response.raise_for_status()
        games = response.json()
        if len(games) == 0 :  raise EndOfPageError("No more games available.")
        return games
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(f"Response content: {response.content}")
        return None

def insert_postgres(game):
    pass

def insert_mongo(game):
    pass



def map_and_insert_data(games):

    conn = db_connect()
    for game in games:
        try:
            #pprint(game)
            game_id = game.get('id')
            name = game.get('name')
            cover_url = game.get('cover', {}).get('url')
            if cover_url:
                cover_url=f"https:{cover_url}".replace("t_thumb", "t_cover_big")
            rating = game.get('rating')
            rating_count = game.get('rating_count')
            rating_opencritic = None

            add_game(conn, game_id, name, cover_url, rating, rating_count, rating_opencritic)

            involved_companies=game.get('involved_companies', [])

            for involved_company in involved_companies:
                company         = involved_company.get('company', {})
                company_id      = company.get('id')
                company_name    = company.get('name')
                company_website = company.get('websites',[{}])[0].get('url')
                country_id      = company.get('country')
                is_developer    = involved_company.get('developer', False)
                is_publisher    = involved_company.get('publisher', False)
                add_company(conn, id=company_id, name=company_name, website=company_website, id_country=country_id)
                add_game_company(conn, id_game=game_id, id_company=company_id, developer=is_developer, publisher=is_publisher)

            for genre in game.get('genres', []):
                genre_id = genre.get('id')
                genre_name = genre.get('name')
                add_genre(conn, id=genre_id, name=genre_name)
                add_game_genre(conn, id_game=game_id, id_genre=genre_id)

            releases=game.get("release_dates", [])

            for i, release in enumerate(releases):
                platform = release.get('platform', {})
                platform_id = platform.get('id')
                platform_name = platform.get('name')
                add_platform(conn, id=platform_id, name=platform_name)
                release_date = release.get('date')
                isotimestamp = datetime.fromtimestamp(int(release_date)).isoformat() if release_date else None
                add_game_platform(conn, id_game=game_id, id_platform=platform_id, release_date=isotimestamp)

        except Exception as e:
            print(f"An error occurred while processing game {game.get('name')}: {e}")
            #pprint(game)
            
            conn.rollback()

    db_close(conn)

if __name__ == "__main__":
    access_token = get_access_token(IGDB_CLIENT_ID, IGDB_CLIENT_SECRET)
    if access_token:
        done  = False
        page  = 1
        limit = 500
        year  = 2024
        while not done:
            try :
                print(f"\rPage : {page}", end="\033[0K", flush=True )
                games = fetch_games(access_token, year=year, limit=limit, page=page)

                if games is not None :
                    map_and_insert_data(games)
                    page += 1
                else :
                    done = True
            except EndOfPageError as e:
                print("\n", e)
                done = True
        print()