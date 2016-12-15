from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app import db


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

	def __iter__(self):
		yield 'playlist_id', self.playlist_id
		yield 'owner', self.owner
		yield 'name', self.name
		yield 'url', self.url
		yield 'image', self.image
		yield 'public', self.public
