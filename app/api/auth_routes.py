from fastapi import APIRouter, Depends, HTTPException
from schemas.auth import UserLogin, UserCreate
from schemas.response import success_response
from auth.auth_service import AuthService
from auth.dependencies import require_admin, get_current_active_user, require_user_or_admin
from exceptions.custom_exceptions import ValidationError

from models.crudpostgres import db_connect


router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

@router.post("/register")
def register(user_data: UserCreate):
    """Créer un nouveau compte utilisateur"""
    try:
        return AuthService.create_user(user_data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la création du compte")

@router.post("/login")
def login(login_data: UserLogin):
    """Se connecter et obtenir un token JWT"""
    try:
        return AuthService.login(login_data)
    except ValidationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la connexion")

@router.get("/me")
def get_me(current_user: dict = Depends(require_user_or_admin)):
    """Récupérer les informations de l'utilisateur connecté"""
    return success_response(
        data=current_user,
        message="Informations utilisateur récupérées"
    )

@router.get("/users")
def get_all_users(current_user: dict = Depends(require_admin)):
    """Récupérer tous les utilisateurs (admin seulement)"""
    try:
        return AuthService.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des utilisateurs")
