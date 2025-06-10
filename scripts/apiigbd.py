# Étape 1 : Obtenir un token OAuth2

import requests

CLIENT_ID = "l6a809yuybzbx6gvngkxh0gel31hky"
CLIENT_SECRET = "1e2lscpc7gh3agb1jux9bl9hrzp3it"

def get_access_token(client_id, client_secret):
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]

# Étape 2 : Interroger l’API IGDB

def query_igdb_games(access_token, client_id):
    url = "https://api.igdb.com/v4/games"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    body = """
    fields name, genres.name, platforms.name, release_dates.y, rating;
    sort rating desc;
    limit 10;
    """
    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()
    return response.json()

# Étape 3 : Lancer la récupération et afficher les données

if __name__ == "__main__":
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    games = query_igdb_games(access_token, CLIENT_ID)
    
    for game in games:
        print(f"Nom : {game.get('name')}")
        print(f"Note : {game.get('rating')}")
        print(f"Année de sortie : {game.get('release_dates')}")
        print(f"Genres : {game.get('genres')}")
        print(f"Plateformes : {game.get('platforms')}")
        print("-" * 40)