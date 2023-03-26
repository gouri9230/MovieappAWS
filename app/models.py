from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Index

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(25), unique = True, nullable=False)
    name = db.Column(db.String(20))
    password = db.Column(db.String(200))
    movies = db.relationship('Movie', backref = 'user') 
    ranks = db.relationship('RankMovie', backref = 'user')
    
    def __repr__(self):
        return f'<Usernme: "{self.name}">'
      
    
class Movie(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    movie_name = db.Column(db.String(15), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ranks = db.relationship('RankMovie', backref = 'movie')
    
    def __repr__(self):
        return f'<Movie: "{self.movie_name}">'
    
class RankMovie(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    rank = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))