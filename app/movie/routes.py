
from . import mov
from app import db
from flask import render_template, request, redirect, url_for, flash
from ..models import Movie, RankMovie
from flask_restful import Api
import requests, json 
from flask_login import current_user, login_required

api = Api(mov)
api_key = 'e6ba148a06e13fea97aa690066688f2b'

@mov.route("/addmovie", methods=["POST","GET"])
@login_required
def addmovie():
    if request.method == "POST":
        movie = request.form.get('movie_name')
        movies = Movie.query.filter(Movie.user_id == current_user.id).all()
        found = True if any(movie == _movie.movie_name for _movie in movies) else False
        if not found: 
            new_movie = Movie(movie_name = movie, user_id = current_user.id)
            flash("Movie added to your list", category='success') 
            db.session.add(new_movie)
            db.session.commit()
        else: flash("Movie already present in your list", category='error')    
            
    return render_template("movie/addmovie.html", user = current_user)


@mov.route("/movie",methods=["POST","GET"])
@login_required
def movie():
    if request.method == "POST":
        movie = request.form.get('movie_name').lower()
        movie_details = {"puss in boots: the last wish":315162,
                          "m3gan":536554,
                          "shotgun wedding":758009,
                          "avatar the way of water":76600,
                          "troll":736526,
                          "the last of us":100088,
                          "knock at the cabin": 631842,
                          "black panther: wakanda forever": 505642,
                          "plane": 646389, 
                          "shark side of the moon":1011679,
                          "little dixie": 1058949,
                          "huesera: the bone woman": 772515,
                          "diabolik - ginko all'attacco": 823999,
                          "bandit": 842942,
                          "ant-man and the wasp: quantumania": 640146,
                          "lord of the streets": 965839,
                          "there are no saints": 267805,
                          "black adam": 436270,
                          "a man called otto": 937278,
                          "the simpsons meet the bocellis in feliz navidad": 1058732,
                          "detective knight: independence": 1035806}
        
        if movie in movie_details.keys():
            response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_details[movie]}?api_key={api_key}&language=en-US&page=1')
            response_result = response.json()
            attribute_list = ['title','original_language','release_date','overview','budget','popularity']
            movie_dict = {}
            for key in attribute_list:
                movie_dict[key] = response_result[key]
            return render_template("movie/movie.html", value = movie_dict, user = current_user)
        else:
            flash("Please enter a valid movie name from the list or check spelling/spaces/special characters!",category='error')
        
    return render_template("movie/movie.html", user = current_user)


@mov.route("/listofmovies", methods=["POST","GET"])
@login_required
def listofmovies():
    if request.method == "GET":
        movies = Movie.query.filter(Movie.user_id == current_user.id).all() 
    return render_template('movie/listofmovies.html', movies = movies, user = current_user)


@mov.route('/deletemovie/<int:id>', methods = ["GET"])
@login_required
def deletemovie(id):
    movie_id = Movie.query.get(id)
    db.session.delete(movie_id)
    db.session.commit()
    return redirect(url_for('mov.listofmovies'))


@mov.route('/deleterank/<int:id>', methods = ["GET"])
@login_required
def deleterank(id):
    rank_id = RankMovie.query.get(id)
    db.session.delete(rank_id)
    db.session.commit()
    return redirect(url_for('mov.viewrank'))


@mov.route('/rank/<int:id>', methods = ['POST', "GET"])
@login_required
def rank(id):
    if request.method == "POST":
        rank_no = request.form.get('rank')
        ranks = RankMovie.query.filter(RankMovie.userid == current_user.id).all()
        print(ranks)
        found = True if any(id == rank.movie_id for rank in ranks) else False
        if found:
            flash("Movie is already ranked!", category='error')
        else:
            if 0 < int(rank_no) <= 20:
                rank = RankMovie(rank = rank_no, movie_id = id, userid = current_user.id)
                db.session.add(rank)
                db.session.commit()
                return redirect(url_for('mov.listofmovies'))
            else:
                flash("Rank movie only between 1- 20", category='error')
                
    return render_template('movie/rank.html', user=current_user)


@mov.route('/modifyrank/<int:id>', methods = ['POST', "GET"])
@login_required
def modifyrank(id):
    if request.method == "POST":
        rank_no = request.form.get('rank')
        rank_ = RankMovie.query.get(id)
        if 0 < int(rank_no) <= 20:
            rank_.rank = rank_no
            db.session.commit()
            return redirect(url_for('mov.viewrank'))
        else:
            flash("Rank movie only between 1- 20", category='error')
    
    return render_template('movie/modifyrank.html', user=current_user)


@mov.route('/viewrank', methods = ["GET", "POST"])
@login_required
def viewrank():
    if request.method == "GET":
        ranks = RankMovie.query.filter(RankMovie.userid == current_user.id).all()
    return render_template('movie/viewrank.html', ranks = ranks, user=current_user)
      