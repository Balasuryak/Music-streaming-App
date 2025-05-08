from flask_sqlalchemy import SQLAlchemy
from  flask_login import UserMixin
from flask_security import UserMixin,RoleMixin
import datetime


db=SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    Name=db.Column(db.String())
    username=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    Email=db.Column(db.String())
    phone=db.Column(db.Integer())
    flaged=db.Column(db.Boolean(), default=False)
    roles=db.Column(db.String())
    playlists=db.relationship('Playlist')
    information=db.relationship('Info')
    Playlist=db.relationship('Playlist_tracks')
    rating=db.relationship('Rating') 
    
    def __init__(self,username,password,Email,phone,Name):
        self.username=username
        self.password=password
        self.Email=Email
        self.phone=phone
        self.Name=Name
        self.roles='user'
        self.flaged=False
        

class Admin(db.Model):
    Admin_id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Info(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    info_name=db.Column(db.String(),nullable=False)
    content=db.Column(db.String(),nullable=False)
    user=db.Column(db.Integer(),db.ForeignKey('user.id'))

class Album(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    pfile=db.Column(db.String(255))
    album_name=db.Column(db.String(),nullable=False)
    artist=db.Column(db.String(),nullable=False)
    language=db.Column(db.String())
    creator=db.Column(db.Integer(),db.ForeignKey('creator.id'))
    songs=db.relationship('Song')
    
    def __init__(self,Aname,artist,pfile,creator):
        self.album_name=Aname
        self.artist=artist
        self.pfile=pfile
        self.creator=creator

class Song(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    pfile=db.Column(db.String(255))
    song_name=db.Column(db.String(),nullable=False)
    lyrics=db.Column(db.String(4000),nullable=False)
    duration=db.Column(db.String(),nullable=False)
    genre=db.Column(db.Integer())
    filename = db.Column(db.String(255), nullable=False)
    flaged=db.Column(db.Boolean(), default=False)
    Date_created=datetime.datetime.now().strftime("%x")
    album=db.Column(db.Integer(),db.ForeignKey('album.id'))
    creator=db.Column(db.Integer(),db.ForeignKey('creator.id'))
    Playlist_tracks=db.relationship('Playlist_tracks')
    rating=db.relationship('Rating')
    
class Rating(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    rating=db.Column(db.Integer())
    comment=db.Column(db.String())
    song_id=db.Column(db.Integer(),db.ForeignKey('song.id'))
    user_id=db.Column(db.Integer(),db.ForeignKey('user.id'))

    def __init__(self,rate,song_id,user_id):
        self.rating=rate
        self.song_id=song_id
        self.user_id=user_id

class Creator(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    flaged=db.Column(db.Boolean(), default=False)
    information=db.relationship('Song')
    Album=db.relationship('Album')

    def __init__(self,id):
        self.id=id
        self.flaged=False

class Playlist(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(),nullable=False)
    user_id=db.Column(db.Integer(),db.ForeignKey('user.id'))
    tracks=db.relationship('Playlist_tracks')
    
    def __init__(self,name,user_id):
        self.name=name
        self.user_id=user_id
    
class Playlist_tracks(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    song_id=db.Column(db.Integer(),db.ForeignKey('song.id'))
    user_id=db.Column(db.Integer(),db.ForeignKey('user.id'))
    Playlist_id=db.Column(db.Integer(),db.ForeignKey('playlist.id'))

    def __init__(self,song_id,user_id,playlist_id):
        self.song_id=song_id
        self.user_id=user_id
        self.Playlist_id=playlist_id