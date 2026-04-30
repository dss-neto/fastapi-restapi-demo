from sqlalchemy import create_engine
from src.backend.database.models import Base

engine = create_engine("sqlite:///src/backend/database/main_database.db")
Base.metadata.create_all(bind=engine)