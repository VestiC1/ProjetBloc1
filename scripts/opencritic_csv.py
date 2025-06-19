from bs4 import BeautifulSoup
import csv
from requests_ratelimiter import LimiterSession

session = LimiterSession(per_second=1) # 1 requête par seconde au maximum

def scrape_opencritic_page(url):
    response = session.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    games = []
    game_elements = soup.find_all('div', class_='mobile-game-display')
    is_terminated = False

    for game_element in game_elements:
        name = game_element.find('div', class_='flex-grow-1 ml-1').text.strip()
        rating = game_element.find('div', class_='score-orb').text.strip()
        if rating == "-1":
            is_terminated = True
            break
        games.append({"name": name, "rating": rating})

    return games, is_terminated

def save_to_csv(data, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'rating'])
        writer.writeheader()
        writer.writerows(data)

def scrape_all_pages(base_url):
    all_games = []
    done = False

    page=1
    while not done:
        url = f"{base_url}?page={page}"
        print(f"Scraping page {page}...")
        games, done = scrape_opencritic_page(url)
        all_games.extend(games)
        page+=1

    return all_games

def main():
    base_url = "https://opencritic.com/browse/all/2024"

    all_games = scrape_all_pages(base_url)
    save_to_csv(all_games, 'donnees/opencritic_games.csv')

    print("Les données ont été enregistrées dans opencritic_games.csv")

if __name__ == "__main__": main()
