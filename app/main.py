from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .routers import user,post,auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield

    engine.dispose()
    
app = FastAPI(lifespan=lifespan)

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):

    try:
        database_name = db.execute(text("SELECT current_database();")).scalar()
        return {"connected": True, "database": database_name}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        )
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)