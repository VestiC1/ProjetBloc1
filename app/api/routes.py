from models.crudpostgres import db_connect, db_close
from sqlalchemy import text
from fastapi import APIRouter, HTTPException, Query, Depends
from schemas.games import GameShort, GameWithGenres, GameDetail
from typing import List
from auth.dependencies import require_user_or_admin
from models.user import User
from elasticsearch import Elasticsearch
from config import elasticsearch_config

es = Elasticsearch(
    [elasticsearch_config["url"]],
    basic_auth=(elasticsearch_config["username"], elasticsearch_config["password"]),
    verify_certs=elasticsearch_config["verify_certs"],
    ssl_show_warn=False # Désactive les avertissements SSL
)

router = APIRouter(tags=["Games"])

# ENDPOINTS PROTÉGÉS (authentification requise)

@router.get("/games", response_model=List[GameShort], summary="Récupérer une liste paginée des jeux vidéo")
def get_games(
    page: int = Query(1, description="Numéro de la page", ge=1),
    per_page: int = Query(10, description="Nombre d'éléments par page", le=100),
    current_user: User = Depends(require_user_or_admin)  # Authentification requise
):
    """
    Récupère une liste paginée des jeux vidéo disponibles.

    - **page**: Le numéro de la page à récupérer.
    - **per_page**: Le nombre d'éléments à retourner par page.

    Retourne une liste de jeux vidéo avec leurs noms et identifiants.
    """
    offset = (page - 1) * per_page
    conn = db_connect()
    try:
        result = conn.execute(text(f'SELECT id,name FROM "Game" LIMIT :limit OFFSET :offset;'), {
            "limit": per_page,
            "offset": offset
        })
        games = [dict(row._mapping) for row in result]
        return games
    finally:
        db_close(conn)

@router.get("/games/{game_id}/name-storyline", summary="Récupérer le nom et le scénario d'un jeu spécifique")
def get_combined_game_details(
    game_id: int,
    current_user: User = Depends(require_user_or_admin)
):
    """
    Récupère les détails combinés d'un jeu spécifique en utilisant PostgreSQL et Elasticsearch.

    - **game_id**: L'identifiant du jeu dont on veut récupérer les détails.

    Retourne le nom du jeu ainsi que le scénario associé.
    """
    conn = db_connect()
    try:
        # Récupérer les détails du jeu depuis PostgreSQL
        pg_result = conn.execute(text('SELECT id, name FROM "Game" WHERE id = :game_id;'), {"game_id": game_id})
        game = pg_result.fetchone()

        if not game:
            raise HTTPException(status_code=404, detail="Jeu non trouvé dans PostgreSQL")

        game_details = dict(game._mapping)

        # Récupérer la storyline depuis Elasticsearch
        try:
            es_response = es.get(index="games", id=game_id)
            game_details['storyline'] = es_response['_source'].get('storyline', 'No storyline available')
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des détails du jeu depuis Elasticsearch: {str(e)}")

        return game_details

    finally:
        db_close(conn)

@router.get("/games/{game_id}/full-info", response_model=GameDetail, summary="Récupérer toutes les informations d'un jeu spécifique")
def get_game(
    game_id: int,
    current_user: User = Depends(require_user_or_admin)  # Authentification requise
):
    """
    Récupère les détails d'un jeu spécifique depuis PostgreSQL.

    - **game_id**: L'identifiant du jeu dont on veut récupérer les détails.

    Retourne le nom, le lien vers la pochette, la note IGDB, le nombre de vote, la note OpenCritic, le ou les genres, la ou les plateformes et les entreprises (éditeurs et/ou développeurs).
    """
    conn = db_connect()
    try:
        result = conn.execute(text('''
            SELECT g.id, g.name, g.cover, g.rating, g.rating_count, g.rating_opencritic,
                   array_agg(DISTINCT ge.name) as genres,
                   array_agg(DISTINCT p.name) as platforms,
                   array_agg(DISTINCT c.name) as companies
            FROM "Game" g
            LEFT JOIN "Game_Genre" gg ON g.id = gg.id_game
            LEFT JOIN "Genre" ge ON gg.id_genre = ge.id
            LEFT JOIN "Game_Plateform" gp ON g.id = gp.id_game
            LEFT JOIN "Plateform" p ON gp.id_plateform = p.id
            LEFT JOIN "Game_Company" gc ON g.id = gc.id_game
            LEFT JOIN "Company" c ON gc.id_company = c.id
            WHERE g.id = :game_id
            GROUP BY g.id;
        '''), {"game_id": game_id})

        game = result.fetchone()
        if not game:
            raise HTTPException(status_code=404, detail="Jeu non trouvé")
        return dict(game._mapping)
    finally:
        db_close(conn)

@router.get("/games/{game_id}/narrative-info", summary="Récupérer le résumé, le scénario et les mots-clés associés d'un jeu spécifique")
def get_game_details(
    game_id: int,
    current_user: User = Depends(require_user_or_admin)
):
    """
    Récupère les détails textuels d'un jeu spécifique depuis Elasticsearch.

    - **game_id**: L'identifiant du jeu dont on veut récupérer les détails.

    Retourne les détails textuels du jeu : le résumé, le scénario et les mots-clés.
    """
    try:
        # Récupérer le document correspondant au game_id
        response = es.get(index="games", id=game_id)
        game_details = response['_source']

        # Retourner les détails du jeu
        return {
            "title": game_details.get('title'),
            "summary": game_details.get('summary'),
            "storyline": game_details.get('storyline'),
            "keywords": game_details.get('keywords')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des détails du jeu: {str(e)}")

@router.get("/genres", response_model=List[str], summary="Récupérer la liste des genres de jeux vidéo")
def get_genres(
    current_user: User = Depends(require_user_or_admin)  # Authentification requise
):
    """
    Récupère la liste des genres de jeux vidéo disponibles.

    Retourne une liste de tous les genres disponibles pour les jeux vidéo présent dans la base de données.
    """
    conn = db_connect()
    try:
        result = conn.execute(text('SELECT name FROM "Genre";'))
        genres = [row[0] for row in result]
        return genres
    finally:
        db_close(conn)

@router.get("/games/{genre}", response_model=List[GameWithGenres], summary="Récupérer les jeux par genre avec pagination")
def get_games_by_genre(
    genre: str,
    page: int = Query(1, description="Numéro de la page", ge=1),
    per_page: int = Query(10, description="Nombre d'éléments par page", le=100),
    current_user: User = Depends(require_user_or_admin)  # Authentification requise
):
    """
    Récupère une liste paginée des jeux vidéo d'un genre spécifique.

    - **genre**: Le genre des jeux à récupérer.
    - **page**: Le numéro de la page à récupérer.
    - **per_page**: Le nombre d'éléments à retourner par page.

    Retourne une liste de jeux vidéo du genre spécifié.
    """
    offset = (page - 1) * per_page
    conn = db_connect()
    try:
        result = conn.execute(text("""
            SELECT g.name, array_agg(DISTINCT ge.name) as genres
            FROM "Game" g
            JOIN "Game_Genre" gg ON g.id = gg.id_game
            JOIN "Genre" ge ON gg.id_genre = ge.id
            GROUP BY g.id, g.name
            HAVING :genre = ANY(array_agg(ge.name))
            LIMIT :limit OFFSET :offset;
        """), {"genre": genre, "limit": per_page, "offset": offset})

        games = [dict(row._mapping) for row in result]
        if not games:
            raise HTTPException(status_code=404, detail="Aucun jeu trouvé pour ce genre")
        return games
    finally:
        db_close(conn)
