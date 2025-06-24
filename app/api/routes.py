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

router = APIRouter(prefix="/api/v1", tags=["games"])

# ENDPOINTS PROTÉGÉS (authentification requise)

@router.get("/games", response_model=List[GameShort])
def get_games(
    page: int = Query(1, description="Numéro de la page", ge=1),
    per_page: int = Query(10, description="Nombre d'éléments par page", le=100),
    current_user: User = Depends(require_user_or_admin)  # 🔒 Authentification requise
):
    """Récupérer les jeux avec pagination"""
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

@router.get("/games/{game_id}", response_model=GameDetail)
def get_game(
    game_id: int,
    current_user: User = Depends(require_user_or_admin)  # 🔒 Authentification requise
):
    """Récupérer les détails d'un jeu spécifique"""
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

@router.get("/games/{game_id}/details")
def get_game_details(
    game_id: int,
    current_user: User = Depends(require_user_or_admin)
):
    """Récupérer les détails d'un jeu spécifique depuis Elasticsearch"""
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

@router.get("/genres", response_model=List[str])
def get_genres(
    current_user: User = Depends(require_user_or_admin)  # 🔒 Authentification requise
):
    """Récupérer la liste des genres"""
    conn = db_connect()
    try:
        result = conn.execute(text('SELECT name FROM "Genre";'))
        genres = [row[0] for row in result]
        return genres
    finally:
        db_close(conn)

@router.get("/games/genre/{genre}", response_model=List[GameWithGenres])
def get_games_by_genre(
    genre: str,
    page: int = Query(1, description="Numéro de la page", ge=1),
    per_page: int = Query(10, description="Nombre d'éléments par page", le=100),
    current_user: User = Depends(require_user_or_admin)  # 🔒 Authentification requise
):
    """Récupérer les jeux par genre avec pagination"""
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
