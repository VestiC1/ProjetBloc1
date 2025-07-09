import csv
from sqlalchemy import text
from .crudpostgres import db_connect, db_close

def read_csv(file_path):
    games = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            games.append({"name": row["name"], "rating_opencritic": row["rating"]})
    return games

def update_opencritic_ratings(games_csv, min_similarity=0.7):
    conn = db_connect()
    try:
        for game in games_csv:
            name = game["name"]
            rating_opencritic = game["rating_opencritic"]

            # Utiliser pg_trgm pour trouver le jeu le plus similaire
            result = conn.execute(text("""
                SELECT id, name, similarity(name, :name) AS sim
                FROM "Game"
                WHERE name %> :name AND similarity(name, :name) >= :min_similarity
                ORDER BY sim DESC
                LIMIT 1
            """), {"name": name, "min_similarity": min_similarity}).fetchone()

            if result:
                game_id, game_name, game_sim = result
                print(f"Mise à jour de {game_name} avec la note OpenCritic {rating_opencritic} ({game_sim})")

                # Mettre à jour la note OpenCritic
                conn.execute(text("""
                    UPDATE "Game"
                    SET rating_opencritic = :rating_opencritic
                    WHERE id = :game_id
                """), {"rating_opencritic": rating_opencritic, "game_id": game_id})

        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la mise à jour des notes OpenCritic: {e}")
        conn.rollback()
    finally:
        db_close(conn)

def main():
    games_csv = read_csv('../donnees/opencritic_games.csv')
    update_opencritic_ratings(games_csv)

if __name__ == "__main__": main()
