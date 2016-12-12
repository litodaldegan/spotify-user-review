from sqlalchemy import Column,  Integer, String, Boolean,ForeignKey
from app import db


class User(db.Model):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	spotify_id = Column(String)
	display_name = Column(String)
	email = Column(String)
	kind = Column(String)
	country = Column(String)
	followers = Column(Integer)
	product = Column(String)

	def __iter__(self):
		yield 'spotify_id', self.spotify_id
		yield 'display_name', self.display_name
		yield 'email', self.email
		yield 'kind', self.kind
		yield 'country', self.country
		yield 'followers', self.followers
		yield 'product', self.product


class PlayList(db.Model):
	__tablename__ = 'playlist'

	id = Column(Integer, primary_key=True)
	user = Column('user_id', Integer, ForeignKey("user.id"), nullable=False)
	playlist_id = Column(String)
	owner = Column(String)
	name = Column(String)
	url = Column(String)
	image = Column(String)
	public = Column(Boolean)
