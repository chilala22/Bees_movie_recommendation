
# setting up flask application

from flask import Flask,jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# defining the db
db = SQLAlchemy()
# DB_NAME = "database.db"


#define function that creates the app
def create_app():
    #initialise app, __name__: represents name of the file that will be run
    app=Flask(__name__)
    #secret_key: encrypts/secures the session data related to website
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/movie_recommendation' #f'sqlite:///{DB_NAME}'
    # CORS(app,resources={r"/*":{"origins":"*"}})
    CORS(app) 
    if app.config['SQLALCHEMY_DATABASE_URI'] == None:
        print("Need database config") 
    db.init_app(app)
    
    
    
    from .veiws import views
    from .auth import auth
    
    
    #register routes with flask applicstion
    #url_prefix: specifies which prefix to go to
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    
    # import .models
    from .models import Users, Note,tmdb_movies
    # creates db if it doesn't exist already otherwise does not override
    with app.app_context():
        db.create_all()
   
    login_manager = LoginManager()
    # where user should be if not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # tells flask how the user is loaded though the id
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))
    
    return app

#checks if db exists if not creates it
def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')
# with app.app_context():
#     db.create_all()


# df2 = pd.read_csv('E:/DIPLOMA/Content-Based-MRS/backend/website/model/tmdb.csv')
# backend\website\model\tmdb.csv

