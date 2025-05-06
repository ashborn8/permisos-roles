from sqlalchemy.orm import Session
import models
import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Role).offset(skip).limit(limit).all()

def get_permission_by_name(db: Session, name: str):
    return db.query(models.Permission).filter(models.Permission.name == name).first()

def create_permission(db: Session, permission: schemas.PermissionCreate):
    db_permission = models.Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def get_permissions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Permission).offset(skip).limit(limit).all()

def assign_permission(db: Session, role_id: int, permission_id: int):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    
    if role and permission:
        role.permissions.append(permission)
        db.commit()
        return True
    return False
