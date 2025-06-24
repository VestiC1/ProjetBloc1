import requests

# URL de base de votre API
BASE_URL = "http://localhost:8001"

def test_api():
    print("*** Test de l'API Jeux Vidéo ***\n")

    # Test 1: Page d'accueil
    print("1_ Test de la page d'accueil")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Réponse: {response.json()}\n")

    # Test 2: Tous les jeux avec pagination
    print("2_ Test récupération de tous les jeux avec pagination")
    params = {"page": 1, "per_page": 10}
    response = requests.get(f"{BASE_URL}/api/v1/games", params=params)
    print(f"Status: {response.status_code}")
    print(f"Nombre de jeux: {len(response.json())}\n")

    # Test 3: Jeux par genre avec pagination
    print("3_ Test récupération des jeux du genre Adventure avec pagination")
    params = {"page": 1, "per_page": 10}
    response = requests.get(f"{BASE_URL}/api/v1/games/genre/Adventure", params=params)
    print(f"Status: {response.status_code}")
    print(f"Nombre de jeux Adventure: {len(response.json())}\n")

    # Test 4: Vérification des champs retournés pour les jeux
    print("4_ Test vérification des champs retournés pour les jeux")
    response = requests.get(f"{BASE_URL}/api/v1/games", params={"page": 1, "per_page": 1})
    games = response.json()
    if games:
        game = games[0]
        print(f"Champs retournés pour un jeu: {game.keys()}\n")

    # Test 5: Vérification des champs retournés pour les jeux par genre
    print("5_ Test vérification des champs retournés pour les jeux par genre")
    response = requests.get(f"{BASE_URL}/api/v1/games/genre/Adventure", params={"page": 1, "per_page": 1})
    games = response.json()
    if games:
        game = games[0]
        print(f"Champs retournés pour un jeu par genre: {game.keys()}\n")

if __name__ == "__main__":
    test_api()
