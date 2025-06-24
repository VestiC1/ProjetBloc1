from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from models.crudpostgres import db_connect, db_close
from .jwt_handler import JWTHandler

# Sécurité HTTP Bearer (pour récupérer le token des headers)
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dépendance pour récupérer l'utilisateur actuel"""
    token = credentials.credentials
    conn = db_connect()
    try:
        payload = JWTHandler.decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide ou expiré",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = conn.execute(
            text("SELECT id, email, role, is_active FROM \"users\" WHERE id = :user_id"),
            {"user_id": payload["user_id"]}
        ).fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )

        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }
    finally:
        db_close(conn)

def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """Dépendance pour vérifier que l'utilisateur est actif"""
    if not current_user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilisateur inactif"
        )
    return current_user

def require_admin(current_user: dict = Depends(get_current_active_user)):
    """Dépendance pour vérifier que l'utilisateur est admin"""
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Droits administrateur requis"
        )
    return current_user

def require_user_or_admin(current_user: dict = Depends(get_current_active_user)):
    """Dépendance pour vérifier que l'utilisateur est connecté (user ou admin)"""
    if current_user["role"] not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentification requise"
        )
    return current_user
