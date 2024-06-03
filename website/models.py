# creating db models
# from sqlalchemy import Identity
from . import db
# custom class that gives user specifics about the user
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('Users', backref=db.backref('notes', lazy=True))

    def json(self):
        return {
            'id': self.id,
            'data': self.data,
            'date_created': self.date_created,
            'users_id': self.users_id
        }

    
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    username = db.Column(db.String(80))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)

    def json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'notes': [note.json() for note in self.notes]
        }
        
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tmdb_movies_id = db.Column(db.Integer, db.ForeignKey('tmdb_movies.id'))
    watched = db.Column(db.String(150))
    users = db.relationship('Users', backref=db.backref('wishlists', lazy=True))
    movie = db.relationship('tmdb_movies', backref=db.backref('wishlists', lazy=True))

    def __repr__(self):
        return f'<Wishlist {self.movie.title}>'
 
class Ratings(db.Model):
    # id_s = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tmdb_movies_id = db.Column(db.Integer, db.ForeignKey('tmdb_movies.id'))
    rating = db.Column(db.Float)
    users_rate = db.relationship('Users', backref=db.backref('ratings', lazy=True))
    movie_rate = db.relationship('tmdb_movies', backref=db.backref('ratings', lazy=True))
     # Define the relationship between Ratings and tmdb_movies
    # tmdb_movies = db.relationship('tmdb_movies', backref='ratings')
       # Define the relationship between Ratings and tmdb_movies
    # tmdb_movie = db.relationship('tmdb_movies', back_populates='ratings')

    def __repr__(self):
        return f'<Rating {self.movie_rate.title}>'

class tmdb_movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_movie = db.Column(db.Integer)
    budget = db.Column(db.Float)
    genres = db.Column(db.Text)
    homepage = db.Column(db.Text)
    keywords = db.Column(db.Text)
    original_language = db.Column(db.String(100))
    original_title = db.Column(db.String(200))
    overview = db.Column(db.Text)
    popularity = db.Column(db.Float)
    production_companies = db.Column(db.Text)
    production_countries = db.Column(db.Text)
    release_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    revenue = db.Column(db.Float)
    runtime = db.Column(db.Integer)
    spoken_languages = db.Column(db.Text)
    status = db.Column(db.String(10))
    tagline = db.Column(db.Text)
    title = db.Column(db.String(100))
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Float)
    tittle = db.Column(db.String(250))
    cast_movie = db.Column(db.Text)
    crew = db.Column(db.Text)
    director = db.Column(db.String(50))
    soup = db.Column(db.Text)
    
      # Define the relationship between tmdb_movies and Ratings
    # ratings = db.relationship('Ratings', back_populates='tmdb_movie')
