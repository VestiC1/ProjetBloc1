from sqlalchemy import URL, create_engine, text
from config import db_config


# Création URL avec la fonction SQLAlchemy
POSTGRES_URI = URL.create(
    drivername="postgresql+psycopg2",
    username=db_config["user"],
    password=db_config["password"],
    host=db_config["host"],
    port=db_config["port"],
    database=db_config["name"]
)

engine = create_engine(POSTGRES_URI)

def db_connect():
    return engine.connect()

def db_close(conn):
    conn.close()

def create_companies(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS "Company" (
            "id" INTEGER PRIMARY KEY,
            "name" VARCHAR(255) NOT NULL,
            "website" VARCHAR(255)
        );
    """))
    conn.commit()

def create_genres(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS "Genre" (
            "id" INTEGER PRIMARY KEY,
            "name" VARCHAR(255) NOT NULL
        );
    """))
    conn.commit()

def create_platforms(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS "Plateform" (
            "id" INTEGER PRIMARY KEY,
            "name" VARCHAR(255) NOT NULL
        );
    """))
    conn.commit()

def create_games(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS "Game" (
            "id" INTEGER PRIMARY KEY,
            "name" VARCHAR(255) NOT NULL,
            "cover" VARCHAR(255),
            "rating" INTEGER,
            "rating_count" INTEGER
        );
    """))
    conn.commit()

def create_game_platforms(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS "Game_Plateform" (
            "id_game" INTEGER,
            "id_plateform" INTEGER,
            "release_date" TIMESTAMP,
            PRIMARY KEY ("id_game", "id_plateform"),
            FOREIGN KEY ("id_game") REFERENCES "Game"("id"),
            FOREIGN KEY ("id_plateform") REFERENCES "Plateform"("id")
        );
    """))
    conn.commit()

def create_game_genres(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS "Game_Genre" (
            "id_game" INTEGER,
            "id_genre" INTEGER,
            PRIMARY KEY ("id_game", "id_genre"),
            FOREIGN KEY ("id_game") REFERENCES "Game"("id"),
            FOREIGN KEY ("id_genre") REFERENCES "Genre"("id")
        );
    """))
    conn.commit()

def create_game_companies(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS "Game_Company" (
            "id_game" INTEGER,
            "id_company" INTEGER,
            "developer" BOOLEAN NOT NULL,
            "publisher" BOOLEAN NOT NULL,
            PRIMARY KEY ("id_game", "id_company"),
            FOREIGN KEY ("id_game") REFERENCES "Game"("id"),
            FOREIGN KEY ("id_company") REFERENCES "Company"("id")
        );
    """))
    conn.commit()

def create_all(conn):
    create_companies(conn)
    create_genres(conn)
    create_platforms(conn)
    create_games(conn)
    create_game_platforms(conn)
    create_game_genres(conn)
    create_game_companies(conn)

def drop_all(conn):
    conn.execute(text("DROP TABLE IF EXISTS \"Game_Company\" CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS \"Game_Genre\" CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS \"Game_Plateform\" CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS \"Game\" CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS \"Company\" CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS \"Genre\" CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS \"Plateform\" CASCADE;"))
    conn.commit()

def add_company(conn, id, name, website):
    conn.execute(text("""
        INSERT INTO "Company" (id, name, website)
        VALUES (:id, :name, :website)
        ON CONFLICT (id) DO NOTHING;
    """), {"id": id, "name": name, "website": website})
    conn.commit()

def add_genre(conn, id, name):
    conn.execute(text("""
        INSERT INTO "Genre" (id, name)
        VALUES (:id, :name)
        ON CONFLICT (id) DO NOTHING;
    """), {"id": id, "name": name})
    conn.commit()

def add_platform(conn, id, name):
    conn.execute(text("""
        INSERT INTO "Plateform" (id, name)
        VALUES (:id, :name)
        ON CONFLICT (id) DO NOTHING;
    """), {"id": id, "name": name})
    conn.commit()

def add_game(conn, id, name, cover, rating, rating_count):
    conn.execute(text("""
        INSERT INTO "Game" (id, name, cover, rating, rating_count)
        VALUES (:id, :name, :cover, :rating, :rating_count)
        ON CONFLICT (id) DO NOTHING;
    """), {"id": id, "name": name, "cover": cover, "rating": rating, "rating_count": rating_count})
    conn.commit()

def add_game_platform(conn, id_game, id_platform, release_date):
    conn.execute(text("""
        INSERT INTO "Game_Plateform" (id_game, id_plateform, release_date)
        VALUES (:id_game, :id_plateform, :release_date)
        ON CONFLICT (id_game, id_plateform) DO NOTHING;
    """), {"id_game": id_game, "id_plateform": id_platform, "release_date": release_date})
    conn.commit()

def add_game_genre(conn, id_game, id_genre):
    conn.execute(text("""
        INSERT INTO "Game_Genre" (id_game, id_genre)
        VALUES (:id_game, :id_genre)
        ON CONFLICT (id_game, id_genre) DO NOTHING;
    """), {"id_game": id_game, "id_genre": id_genre})
    conn.commit()

def add_game_company(conn, id_game, id_company, developer, publisher):
    conn.execute(text("""
        INSERT INTO "Game_Company" (id_game, id_company, developer, publisher)
        VALUES (:id_game, :id_company, :developer, :publisher)
        ON CONFLICT (id_game, id_company) DO NOTHING;
    """), {"id_game": id_game, "id_company": id_company, "developer": developer, "publisher": publisher})
    conn.commit()

if __name__ == "__main__":
    conn = db_connect()
    #drop_all(conn)
    create_all(conn)
    db_close(conn)
