from app.database import Base, engine
from sqlalchemy_utils import database_exists, create_database
from app import models

print("Creating database tables...")
# Create database if it doesn't exist
if not database_exists(engine.url):
    create_database(engine.url)


Base.metadata.create_all(bind=engine)
print("Done.")
