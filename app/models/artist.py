from sqlalchemy import Column,  Integer, String, Boolean,ForeignKey
from app import db

class Artist(db.Model):
	__tablename__ = 'playlist'

	id = Column(Integer, primary_key=True)
	user = Column('user_id', Integer, ForeignKey("user.id"), nullable=False)

	name = Column(String)
	spotify_id = Column(String)
	img = Column(String)
	url = Column(String)
