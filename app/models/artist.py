from sqlalchemy import Column, Integer,ForeignKey, String
from app import db

class Artist(db.Model):
	__tablename__ = 'artist'

	id = Column(Integer, primary_key=True)
	user = Column('user_id', Integer, ForeignKey("user.id"), nullable=False)
	name = Column(String)
	spotify_id = Column(String)
	image = Column(String)
	url = Column(String)
	popularity = Column(Integer)
	genres = Column(String)

	def __repr__(self):
		return '<Name: %s>' % self.name

	def __iter__(self):
		yield 'name', self.name
		yield 'spotify_id', self.spotify_id
		yield 'image', self.image
		yield 'url', self.url
		yield 'popularity', self.popularity
		yield 'genres', self.genres
