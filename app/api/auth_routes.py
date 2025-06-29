from fastapi import APIRouter, Depends, HTTPException
from schemas.auth import UserLogin, UserCreate
from schemas.response import success_response
from auth.auth_service import AuthService
from auth.dependencies import require_admin, require_user_or_admin
from exceptions.custom_exceptions import ValidationError


router = APIRouter(tags=["Authentication"])

@router.post("/register", summary="Créer un compte utilisateur")
def register(user_data: UserCreate):
    """
    Crée un nouveau compte utilisateur avec les informations fournies.

    - **user_data**: Les informations nécessaires pour créer un compte utilisateur, incluant le mail de l'utilisateur et le mot de passe.

    Retourne un message de succès si le compte est créé avec succès.
    """
    try:
        return AuthService.create_user(user_data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la création du compte")

@router.post("/login", summary="Se connecter et obtenir un token JWT")
def login(login_data: UserLogin):
    """
    Permet à un utilisateur de se connecter et d'obtenir un token JWT pour accéder aux points de terminaison sécurisés.

    - **login_data**: Les informations d'identification de l'utilisateur, incluant le mail de l'utilisateur et le mot de passe.

    Retourne un token JWT valide pour les requêtes authentifiées.
    """
    try:
        return AuthService.login(login_data)
    except ValidationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la connexion")

@router.get("/me", summary="Récupérer les informations de l'utilisateur connecté")
def get_me(current_user: dict = Depends(require_user_or_admin)):
    """
    Récupère les informations de l'utilisateur actuellement connecté.

    - **current_user**: L'utilisateur actuellement authentifié, récupéré via le token JWT.

    Retourne les informations de l'utilisateur connecté.
    """
    return success_response(
        data=current_user,
        message="Informations utilisateur récupérées"
    )

@router.get("/users", summary="Récupérer tous les utilisateurs (admin seulement)")
def get_all_users(current_user: dict = Depends(require_admin)):
    """
    Récupère la liste de tous les utilisateurs enregistrés. Accessible uniquement aux administrateurs.

    - **current_user**: L'utilisateur actuellement authentifié, doit être un administrateur.

    Retourne une liste de tous les utilisateurs enregistrés.
    """
    try:
        return AuthService.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des utilisateurs")

@router.delete("/delete-account", summary="Supprimer le compte de l'utilisateur connecté")
async def delete_account(current_user: dict = Depends(require_user_or_admin)):
    """
    Supprime le compte de l'utilisateur actuellement connecté.

    - **current_user**: L'utilisateur actuellement authentifié, récupéré via le token JWT.

    Retourne un message de succès si le compte est supprimé avec succès.
    """
    try:
        user_id = current_user.get("id")
        AuthService.delete_user(user_id)
        return success_response(message="Votre compte a été supprimé avec succès.")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression du compte")
