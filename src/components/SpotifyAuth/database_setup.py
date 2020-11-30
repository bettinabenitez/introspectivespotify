import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_STRING = os.getenv("DB_STRING")

Base = declarative_base()

# user table
class User(Base):
   __tablename__ = 'user'

   discord_id = Column(String, primary_key=True, unique=True)
   spotify_name = Column(String, unique=True)
   access_token = Column(String)
   expires_at = Column(Integer)
   refresh_token = Column(String)

   @property
   def serialize(self):
      return{
         "access_token": self.access_token,
         "token_type": "Bearer",
         "expires_in": 3600,
         "scope": "playlist-modify-public, user-modify-playback-state, user-read-currently-playing, user-read-playback-position, user-read-playback-state, user-read-private user-read-recently-played, user-top-read,",
         "expires_at": self.expires_at,
         "refresh_token": self.refresh_token
      }

engine = create_engine(DB_STRING)
# Base.metadata.create_all(engine)

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# recreate_database()
