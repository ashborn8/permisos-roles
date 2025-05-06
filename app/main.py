from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import get_db, setup_database, SessionLocal, engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/health") #Endpoint de prueba para los cambios en el pipeline
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """Initialize database connection and create tables."""
    try:
        logger.info("Starting up application...")
        # Initialize database connection
        engine = setup_database()
        logger.info("Database connection established")
        
        # Create tables
        logger.info("Creating database tables...")
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

@app.post("/roles/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    try:
        db_role = crud.get_role_by_name(db, name=role.name)
        if db_role:
            raise HTTPException(status_code=400, detail="El rol ya existe")
        return crud.create_role(db=db, role=role)
    except Exception as e:
        logger.error(f"Error creating role: {str(e)}")
        raise

@app.post("/permissions/", response_model=schemas.Permission)
def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db)):
    try:
        db_permission = crud.get_permission_by_name(db, name=permission.name)
        if db_permission:
            raise HTTPException(status_code=400, detail="El permiso ya existe")
        return crud.create_permission(db=db, permission=permission)
    except Exception as e:
        logger.error(f"Error creating permission: {str(e)}")
        raise

@app.post("/assign-permission/")
def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    try:
        return crud.assign_permission(db, role_id, permission_id)
    except Exception as e:
        logger.error(f"Error assigning permission to role: {str(e)}")
        raise

@app.get("/roles/", response_model=list[schemas.Role])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud.get_roles(db, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error reading roles: {str(e)}")
        raise

@app.get("/permissions/", response_model=list[schemas.Permission])
def read_permissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud.get_permissions(db, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error reading permissions: {str(e)}")
        raise

@app.get("/permissions/user/{user_id}")
def get_user_permissions(user_id: str, db: Session = Depends(get_db)):
    try:
        # Aquí deberías implementar la lógica para obtener los permisos del usuario
        # Por ahora, devolvemos un conjunto de permisos de ejemplo
        permissions = [
            "read:user",
            "write:user",
            "read:role"
        ]
        return {"permissions": permissions}
    except Exception as e:
        logger.error(f"Error getting user permissions: {str(e)}")
        raise

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query
        db.execute("SELECT 1")
        return {"status": "Database connection successful"}
    except Exception as e:
        logger.error(f"Database test failed: {str(e)}")
        return {"status": "Database connection failed", "error": str(e)}
