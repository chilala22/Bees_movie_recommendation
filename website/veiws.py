#this shows that there are a bunch of files available
from flask import Blueprint, redirect,render_template,request,flash, jsonify, url_for
import flask
from flask_login import login_required,current_user
from sqlalchemy import desc
from .models import Note, Ratings, Wishlist,tmdb_movies
from . import db
import json 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from wtforms import StringField, Form
# from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy  
import random

# setting up the blueprint for the application
views=Blueprint('views',__name__)

import pickle
import requests

def fetch_poster(movie_id):
    #  api_key =6a3b4548f5c45f56fcf882e7ef655440
    #  url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

     url = "https://api.themoviedb.org/3/movie/{}?api_key=6a3b4548f5c45f56fcf882e7ef655440&language=en-US".format(movie_id)
     data=requests.get(url)
     data=data.json()
     poster_path = data['poster_path']
     release_date_path = data['release_date']
     runtime_path = data['runtime']
     full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
     return full_path,release_date_path,runtime_path
 
 
movies=pickle.load(open("./movies_list_part1.pkl", "rb"))
# similarities will be gotten from the similarity.pkl
similarity=pickle.load(open("./similarity_part1.pkl", "rb"))
# helps get the names of the movies from the id in title
movies_list = movies['title'].values
# best_rated_movies=pickle.load(open("./backend/best_rated_movies.pkl", "rb"))
best_rated_movies = pd.read_pickle("./best_rated_movies.pkl")
popular_movies = pd.read_pickle("./most_popular_movies.pkl")

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    # stores the recommendations on list so that it can be returned
    recommended_movies = []
    recommend_poster = []
    recommended_movie_ids = []
    movie_release_dates = []
    movie_runtimes = []
    # returns the top 5 recommendations for the selected movie
    for i in distance[1:11]:
        movies_id=movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # recommend_poster.append(fetch_poster(movies_id))
        recommended_movie_ids.append(movies_id)
        poster, release_date, runtime = fetch_poster(movies_id)
        recommend_poster.append(poster)
        movie_release_dates.append(release_date)
        movie_runtimes.append(runtime)
    return recommended_movies,recommend_poster,recommended_movie_ids, movie_release_dates, movie_runtimes

@views.route('/')
@login_required  #cannot get user from route if not logged in
def home():
    """
    Display the top 10 recommended movies on the home page.
    """
    top_10_best_movies = best_rated_movies.head(10)[['id', 'original_title', 'overview', 'score']]
    movie_posters = [fetch_poster(movie['id']) for movie in top_10_best_movies.to_dict('records')]
    movie_page_urls = [url_for('views.movie_page', movie_name_req=movie['original_title'], movie_id=movie['id']) for movie in top_10_best_movies.to_dict('records')]

    # Enumerate the movies list
    # enumerate_best_movies = list(enumerate(top_10_best_movies.to_dict('records')))
    # Query the Ratings table to get the rating for each movie
    best_ratings = db.session.query(Ratings).filter(
        Ratings.tmdb_movies_id.in_(top_10_best_movies['id']),
        Ratings.users_id == current_user.id  # Filter by the current user's ID
        ).all()

    # Create a dictionary to store the popular_ratings
    best_ratings_dict = {rating.tmdb_movies_id: rating.rating for rating in best_ratings}
    # Enumerate the movies list and add the rating to each movie
    enumerate_best_movies = [(i, {**movie, 'rating': best_ratings_dict.get(movie['id'])}) for i, movie in enumerate(top_10_best_movies.to_dict('records'))]
    
    top_10_popular_movies = popular_movies.head(10)[['id', 'original_title', 'overview', 'popularity']]
    movie_posters_popular = [fetch_poster(movie_pop['id']) for movie_pop in top_10_popular_movies.to_dict('records')]
    movie_page_urls_pop = [url_for('views.movie_page', movie_name_req=movie_pop['original_title'], movie_id=movie_pop['id']) for movie_pop in top_10_popular_movies.to_dict('records')]

    # Query the Ratings table to get the rating for each movie
    # popular_ratings = db.session.query(Ratings).filter(
    #     Ratings.tmdb_movies_id.in_(top_10_popular_movies['id'])).all()
    # Query the Ratings table to get the rating for each movie for the current user
    popular_ratings = db.session.query(Ratings).filter(
        Ratings.tmdb_movies_id.in_(top_10_popular_movies['id']),
        Ratings.users_id == current_user.id  # Filter by the current user's ID
    ).all()

  
    # # Create a dictionary to store the popular_ratings
    # popular_ratings_dict = {rating.tmdb_movies_id: rating.rating for rating in popular_ratings}
    # # Enumerate the movies list and add the rating to each movie
    # enumerate_popular_movies = [(i, {**movie, 'rating': popular_ratings_dict.get(movie['id'])}) for i, movie in enumerate(top_10_popular_movies.to_dict('records'))]
    # Create a dictionary to store the popular_ratings
    popular_ratings_dict = {rating.tmdb_movies_id: rating.rating for rating in popular_ratings}
    # Enumerate the movies list and add the rating to each movie
    enumerate_popular_movies = [(i, {**movie, 'rating': popular_ratings_dict.get(movie['id'])}) for i, movie in enumerate(top_10_popular_movies.to_dict('records'))]

    return render_template('home.html', 
                           users=current_user, 
                           best_movies=enumerate_best_movies, 
                           popular_movies = enumerate_popular_movies,
                           movie_posters=movie_posters, 
                           movie_posters_popular = movie_posters_popular,
                           movie_page_urls=movie_page_urls,
                           movie_page_urls_pop=movie_page_urls_pop
                           )


# define view endpoint
@views.route('/add-note',methods=['GET','POST'])
@login_required  #cannot get user from route if not logged in
def add_note():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note)<1:
            flash('Note is too short',category='error')
        else:
            new_note = Note(data=note,users_id=current_user.id)
            db.session.add(new_note) #adds new note to the db
            db.session.commit()
            flash('Note added!',category='success')
    return render_template("notes.html",users=current_user)

# another route that deletes the notes
@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.users_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!',category='success')
    else:
        flash('Error, unable to delete this note.', category='error')
    return jsonify({})

@views.route('/movie-search-image', methods=['GET', 'POST'])
def movie_search_image():
    name = ''
    movie_name_req = []
    recommendations_poster = []
    recommended_movie_ids = []
    movie_release_dates = []
    movie_runtimes = []
    error_message = ''
    rating_value = []
   
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:  # Check if the text box is blank
            error_message = 'Please enter a movie title.'
            flash('Please enter a movie title.', category='error')
        else:
            try:
                movie_name_req, recommendations_poster, recommended_movie_ids, movie_release_dates, movie_runtimes = recommend(name)

                if not movie_name_req:  # Check if the movie is not found in the database
                    error_message = 'Movie not found in our database.'
                    flash('Movie not found in our database.', category='error')
                else:
                    # Calculate average ratings for recommended movies
                    for rec_id in recommended_movie_ids:
                        rec_id = int(rec_id)
                        ratings = db.session.query(Ratings.rating).filter(
                            Ratings.tmdb_movies_id == rec_id,
                            Ratings.users_id == current_user.id # Filter by the current user's ID
                            ).all()
                        avg_rating = sum([rating[0] for rating in ratings]) / len(ratings) if ratings else None
                        rating_value.append(avg_rating)
                        
            except Exception as e:  # Catch any exceptions raised by the recommend function
                error_message = 'An error occurred. Please try again.'
                flash('An error occurred. Please try again.', category='error')

    return flask.render_template('search_movie.html',
                                 name=name,
                                 users=current_user,
                                 movies=movies_list,
                                 movie_name_req=movie_name_req,
                                 recommendations_poster=recommendations_poster,
                                 recommended_movie_ids=recommended_movie_ids,
                                 movie_page_urls=[f'/movie-page/{movie_name_req[i]}/{movie_id}' for i, movie_id in enumerate(recommended_movie_ids)] if movie_name_req else [],
                                 movie_release_dates=movie_release_dates,
                                 movie_runtimes=movie_runtimes,
                                 error_message=error_message,
                                 rating_value = rating_value
                                 )

@views.route('/movie-page/<string:movie_name_req>/<int:movie_id>')
def movie_page(movie_name_req,movie_id):
    rating_value = ''
    movie_details = tmdb_movies.query.get(movie_id)
    movie_poster, release_date, runtime = fetch_poster(movie_id)
    rating = Ratings.query.filter_by(tmdb_movies_id=movie_id, users_id=current_user.id).first()
    rating_value = rating.rating if rating else None

    # Retrieve additional details from the database
    # render the movie page template with the movie name
    return render_template('movie_page.html',
                           users=current_user,
                           movie_name_req=movie_name_req, 
                           movie_id=movie_id,
                           movie_details=movie_details,
                           movie_poster=movie_poster,
                           rating_value = rating_value
                        #    cast_movie=cast_movie,
                        #    director=director
                           )

@views.route('/movie-wishlist/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def movie_wishlist(movie_id: int):
    if request.method == 'POST':
        if Wishlist.query.filter_by(users_id=current_user.id, tmdb_movies_id=movie_id).first():
            flash('Movie already exists in your wishlist!', category='info')
        else:
            wishlist = Wishlist(users_id=current_user.id, tmdb_movies_id=movie_id)
            db.session.add(wishlist)
            db.session.commit()
            flash('Movie added to wishlist!', category='success')
        return redirect(url_for('views.movies_wishlist'))
    return redirect(url_for('views.movies_wishlist'))


@views.route('/delete-movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    movie = tmdb_movies.query.get(movie_id)
    wishlist = Wishlist.query.filter_by(tmdb_movies_id=movie_id, users_id=current_user.id).first()
    if wishlist:
        db.session.delete(wishlist)
        db.session.commit()
    return redirect(url_for('views.movies_wishlist'))

@views.route('/wishlist')
@login_required
def movies_wishlist():
    wishlist_movies = Wishlist.query.filter_by(users_id=current_user.id).all()
    movies = []
    movie_poster_wish = []
    release_date =[]
    runtime = []
    for wishlist in wishlist_movies:
        movie = tmdb_movies.query.get(wishlist.tmdb_movies_id)
        if movie:
            movie_poster_wish, release_date, runtime = fetch_poster(movie.id)
            # Query the Ratings table to get the rating for this movie
            rating = Ratings.query.filter_by(tmdb_movies_id=movie.id, users_id=current_user.id).first()
            rating_value = rating.rating if rating else None
            movies.append({
                'movie': movie,
                'movie_poster_wish': movie_poster_wish,
                'release_date': release_date,
                'runtime': runtime,
                'rating': rating_value
            })
    
    return render_template('movies_wishlist.html', users=current_user, movies=movies)



@views.route('/rate-movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def rate_movie(movie_id):
    if request.method == 'POST':
        rating_count = request.form["ratings"]
        # Check if the user has already rated this movie
        existing_rating = Ratings.query.filter_by(users_id=current_user.id, tmdb_movies_id=movie_id).first()
        if existing_rating:
            # Update the existing rating
            existing_rating.rating = rating_count
        else:
            # Create a new rating
            movie_rating = Ratings(users_id=current_user.id, tmdb_movies_id=movie_id, rating=rating_count)
            db.session.add(movie_rating)
        db.session.commit()
        flash('Rating submitted successfully!', category='success')
        
        # Get the movie name from the database
        movie_details = tmdb_movies.query.get(movie_id)
        movie_name_req = movie_details.title
        
        # Redirect back to the movie page
        return redirect(url_for('views.movie_page', movie_name_req=movie_name_req, movie_id=movie_id))
    return render_template('movie_page.html', users=current_user)

@views.route('/rated-movie-recommendations', methods=['GET'])
@login_required
def rated_movie_recommendations():
    # Get the number of movies the current user has rated
    user_ratings_count = db.session.query(Ratings).filter(Ratings.users_id == current_user.id).count()

    # Get movies rated by the current user with a rating of 3 or higher
    rated_movies = db.session.query(
        tmdb_movies.id, tmdb_movies.title, tmdb_movies.genres, tmdb_movies.budget, tmdb_movies.homepage
    ).join(Ratings, tmdb_movies.id == Ratings.tmdb_movies_id).filter(Ratings.rating >= 1, Ratings.users_id == current_user.id).order_by(desc(Ratings.rating)).all()

    # Check if the user has rated at least 4 movies with a rating of 3 or higher
    if len(rated_movies) < 4:
        flash('You need to rate at least 4 movies with a rating of 3 or higher to get recommendations.', 'warning')
        return render_template('movie_rating_page.html', user_ratings_count=user_ratings_count, movies=[], recommended_movies=[], users=current_user)

    # Randomly select 4 movies from the list
    random_movies = random.sample(rated_movies, 4)

    # Get the recommended movies for each of the random movies
    recommended_movies = []
    for movie in random_movies:
        title = movie[1]  # Get the title of the movie
        _id = movie[0]  # Get the id of the movie
        rec_movies, rec_posters, rec_ids, rec_release_dates, rec_runtimes = recommend(title)

        rec_movies_with_ratings = []
        for i, rec_id in enumerate(rec_ids):
            rec_id = int(rec_id)  # Convert numpy.int64 to Python int
            ratings = db.session.query(Ratings.rating).filter(Ratings.tmdb_movies_id == rec_id).all()
            avg_rating = sum([rating[0] for rating in ratings]) / len(ratings) if ratings else None
            rec_movies_with_ratings.append({
                'title': rec_movies[i],
                'poster': rec_posters[i],
                'id': rec_id,
                'release_date': rec_release_dates[i],
                'runtime': rec_runtimes[i],
                'avg_rating': avg_rating
            })

        recommended_movies.append({
            'id': _id, 
            'title': title, 
            'recommended_movies': rec_movies_with_ratings
        })

    return render_template('movie_rating_page.html', user_ratings_count=user_ratings_count, movies=random_movies, recommended_movies=recommended_movies, users=current_user)
