from flask import current_app as app,jsonify,send_file
from flask import Flask,render_template,request,flash,url_for,redirect
import os
from werkzeug.security import check_password_hash
from flask_security import auth_required,roles_required
from application.sec import datastore
from flask_restful import marshal, fields,reqparse
from flask_sqlalchemy import SQLAlchemy 
import flask_excel as excel
from .instances import cache
from flask_login import login_user,LoginManager,logout_user,LoginManager,current_user,UserMixin,login_required
import datetime
from celery.result import AsyncResult
from .tasks import create_song_csv
from werkzeug.security import generate_password_hash
import matplotlib
matplotlib.use('Agg') #https://stackoverflow.com/a/29172195
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from application.models import *
from config import DevelopmentConfig


@app.get('/')
def home():
    return render_template("index.html")

@app.get('/admin')
@auth_required('token')
def admin():
    return "Hello from admin"

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form.get('setuser')
        password=request.form.get('setpass')
        cpassword=request.form.get('confirmpassword')
        name=request.form.get('name')
        ph=request.form.get('ph')
        email=request.form.get('mail')
        if password==cpassword:
            data=User(username=username,password=generate_password_hash(password),Name=name,phone=ph,Email=email)
            db.session.add(data)
            db.session.commit()
        else:
            return 'error'
        return redirect('/')    

    return render_template('signup.html')

@app.post('/user-login')
def user_login():
    data = request.get_json()
    print(data)
    username = data['username']
    print(username)
    if not username:
        return jsonify({"message": "email not provided"}), 400

    user = User.query.filter_by(username=username).first()
    print(user)

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    if check_password_hash(user.password, data.get("password")):
        return jsonify({"token": user.get_auth_token(),"role": user.roles ,"userid": user.id})
    else:
        return jsonify({"message": "Wrong Password"}), 400
    
@app.get('/user-details/<int:id>')
def user_details(id):
    user= User.query.filter_by(id=id).first()
    return marshal(user,user_fields)


@app.get('/home')
@auth_required('token')
def Home():
    return render_template("index.html")


user_fields={
    "id":fields.Integer,
    "Name":fields.String,
    "username":fields.String,
    "Email":fields.String,
    "phone":fields.String
}

song_fields = {
    "id": fields.Integer,
    "pfile": fields.String,
    "song_name": fields.String,
    "lyrics":fields.String,
    "duration":fields.String,
    "genre":fields.String,
    "filename":fields.String,
    "flaged":fields.String
}

album_fields = {
    "id": fields.Integer,
    "pfile": fields.String,
    "album_name": fields.String,
    "artist":fields.String
}

Playlist_fields={
    "id":fields.Integer,
    "name":fields.String,
    "user_id":fields.Integer
}

def get_rating(id):
    rating=Rating.query.filter_by(song_id=id).all()
    length=len(rating)
    total=0
    for i in rating:
        total=total+i.rating
    if length!=0:
        avg=total/length
        return avg
    return total


@app.get('/songs')
@cache.cached(timeout=50)
def all_songs():
    songs = Song.query.all()
    print(songs)
    return marshal(songs, song_fields)

@app.get('/albums')
@cache.cached(timeout=50)
def all_Albums():
    Albums = Album.query.all()
    print(Albums)
    return marshal(Albums, album_fields)

@app.get('/album/<int:id>')
def Album_page(id):
    songs = Song.query.filter_by(album=id).all()
    if len(songs) == 0:
        return jsonify({"message": "No User Found"}), 404
    print(songs)
    return marshal(songs, song_fields)

@app.get('/playlists/<int:id>')
def all_Playlist(id):
    playlist= Playlist.query.filter_by(user_id=id).all()
    if len(playlist) == 0:
        return jsonify({"message": "No User Found"}), 404
    print(playlist)
    return marshal(playlist,Playlist_fields)

@app.post('/playlist')
def playlist():
    data = request.get_json()
    print(data)
    name=data['Playlist_name']
    id=data['id']
    playlist=Playlist(name=name,user_id=id)
    db.session.add(playlist)
    db.session.commit()    
    return jsonify({"message": "Playlist Created"})

@app.post('/add_playlist_song')
def add_playlist_song():
    data = request.get_json()
    name=data['Playlist_name']
    id=data['id']
    song=data['song_name']
    p_id=Playlist.query.filter_by(name=name).first().id
    s_id=Song.query.filter_by(song_name=song).first().id
    play_track=Playlist_tracks(song_id=s_id,playlist_id=p_id,user_id=id)
    db.session.add(play_track)
    db.session.commit()    
    return jsonify({"message": "Song added"})

@app.route('/playlist/<int:id>')
def myplaylist(id):
    songs_in_playlist = db.session.query(Song).join(Playlist_tracks, (Song.id == Playlist_tracks.song_id)).filter(Playlist_tracks.Playlist_id == id).all()
    print(songs_in_playlist)
    return marshal(songs_in_playlist, song_fields)

@app.get('/delete_playlist/<int:id>')
def delete_playlist(id):
    data= Playlist_tracks.query.filter_by(Playlist_id=id).all()
    for i in data:
        db.session.delete(i)
        db.session.commit()
    data= Playlist.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    if not data:
        return jsonify({"message": "Resource Not found"}), 404
    return jsonify({"message": "Playlist deleted successfully"})

@app.post('/edit_song')
def edit_song():
    data = request.get_json()
    name=data['name']
    id=data['id']
    lyrics=data['lyrics']
    genre=data['genre']
    songs=Song.query.filter_by(id=id).first()
    songs.name=name
    songs.lyrics=lyrics
    songs.genre=genre
    db.session.commit()    
    return jsonify({"message": "Song edited successfully"})

@app.post('/edit_album')
def edit_album():
    data = request.get_json()
    name=data['name']
    id=data['id']
    artist=data['artist']
    albums=Album.query.filter_by(id=id).first()
    albums.name=name
    albums.artist=artist
    db.session.commit()    
    return jsonify({"message": "Album edited successfully"})

@app.get('/switch-creator/<int:id>')
def switch_creator(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "Resource Not found"}), 404
    user.roles = "creator" 
    db.session.commit()
    cret=Creator(id=id)
    db.session.add(cret)
    db.session.commit()
    return jsonify({"message": "CREATOR APPROVED"})

@app.get('/albums/<int:id>')
def get_created_albums(id):
    albums = Album.query.filter_by(creator=id).all()
    if not albums:
        return jsonify({"message": "Resource Not found"}), 404
    return marshal(albums, album_fields)

@app.get('/songs/<int:id>')
def get_created_songs(id):
    songs = Song.query.filter_by(creator=id).all()
    print(songs)
    if not songs:
        return jsonify({"message": "Resource Not found"}), 404
    return marshal(songs, song_fields)


@app.route('/upload/<int:id>', methods=['GET', 'POST'])
def upload(id):
  if request.method == 'POST':
    file = request.files['file']
    pfile=request.files['pfile']
    songname=request.form.get('Songname')
    duration=request.form.get('duration')
    lyrics=request.form.get('lyrics')
    genre=request.form.get('genre')
    album=request.form.get('album')
    album_id=Album.query.filter_by(album_name=album).first().id
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pfilename = pfile.filename
        pfile.save(os.path.join(app.config['UPLOAD_FOLDER'], pfilename))

        song=Song(song_name=songname,lyrics=lyrics,pfile=pfilename, duration=duration,genre=genre,filename=filename,album=album_id,creator=id,flaged=False)
        db.session.add(song)
        db.session.commit()
        return redirect('/#/uploadsong')
  return render_template('upload.html', songs=Song.query.all(),Album=Album.query.all(),id=id)

@app.get('/delete_song/<int:id>')
def delete_song(id):
    data = Song.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    print(data)
    if not data:
        return jsonify({"message": "Resource Not found"}), 404
    return jsonify({"message": "song deleted successfully"})



@app.route('/album/edit/<int:id>', methods=['GET', 'POST'])
def album_edit(id):
    if request.method=='POST':
        file = request.files['file']
        Aname=request.form.get('albumname')
        artist=request.form.get('artist')
        if file:
            pfilename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pfilename))
            data=Album(Aname=Aname,artist=artist,pfile=pfilename,creator=id)
            db.session.add(data)
            db.session.commit()
            return redirect('/#/uploadsong')
        return render_template('album_edit.html',album=Album.query.all(),id=id)
    return render_template('album_edit.html',album=Album.query.all(),id=id)

@app.get('/delete_album/<int:id>')
def delete_album(id):
    data= Album.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    if not data:
        return jsonify({"message": "Resource Not found"}), 404
    return jsonify({"message": "Album deleted successfully"})

@app.post('/search/song')
@cache.cached(timeout=50)
def song_search():
    data=request.get_json()
    searchkey  = data['search']
    songs = Song.query.filter(
            Song.song_name.ilike('%'+searchkey+'%') |
            Song.genre.ilike('%' + searchkey+'%')
            ).all()
    return marshal(songs, song_fields)

@app.post('/search/album')
@cache.cached(timeout=50)
def album_search():
    data=request.get_json()
    searchkey  = data['search']
    albums = Album.query.filter(
            Album.album_name.ilike('%'+searchkey+'%') |
            Album.artist.ilike('%' + searchkey+'%')
            ).all()
    return marshal(albums, album_fields)

@app.post('/song/rate/<int:id>/<int:uid>')
def rate(id,uid):
    data=request.get_json()
    rate=data['rating']
    song=Rating.query.filter_by(song_id=id).all()
    for s in song:
        if (s.user_id==uid) :
            return jsonify({"message": "Already rated" })
    data=Rating(rate=rate,song_id=id,user_id=uid)
    db.session.add(data)
    db.session.commit()
    total=get_rating(id)
    return jsonify({"message": total })

@app.post('/song/t-rate/<int:id>')
def total_rate(id):
    rating=Rating.query.filter_by(song_id=id).all()
    length=len(rating)
    if length==0:
        return jsonify({"message": 0 })
    total=0
    for i in rating:
        total=total+i.rating
    if length!=0:
        avg=total/length
        return jsonify({"message": avg })
    return jsonify({"message": total })

@app.get('/creator/<int:id>')
def creator_details(id):
    s=len(Song.query.filter_by(creator=id).all())
    a=len(Album.query.filter_by(creator=id).all())
    return jsonify({"s": s,"a": a })


@app.get('/download-csv')
def download_csv():
    res=create_song_csv.delay()
    return jsonify({'task-id':res.id})

@app.get('/get-csv/<task_id>')
def get_csv(task_id):
    res=AsyncResult(task_id)
    if res.ready():
        filename=res.result
        return send_file(filename,as_attachment=True)
    else:
        return jsonify({"message":"Task pending"}),404
    
@app.get('/song_chart')
def song_chart():
    
    num_songs = len(Song.query.all())
    x=[]
    y=[]
    for s in Song.query.all():
        x.append(s.song_name)
        y.append(get_rating(s.id))

    
    tc=len(Creator.query.all())
    tu=len(User.query.all())
    ta=len(Album.query.all())
    creators=Creator.query.all()
    songs=Song.query.all()

    plt.bar(x, y)
    plt.ylabel('Rating')
    plt.xlabel('Song Name')
    plt.title('Average rating')

    plt.yticks(range(1,7))
    plt.xticks(rotation =300)

    # Save the chart as an image file in the charts folder
    chart_filename = 'chart.png'
    chart_path = os.path.join(app.config['UPLOAD_FOLDER_CHARTS'], chart_filename)
    plt.savefig(chart_path)
    plt.close()

    chart_src = url_for('static', filename=f'charts/{chart_filename}')

    return jsonify({"chart_src":chart_src,"numsong":num_songs,"tc":tc,"tu":tu,"ta":ta})


@app.get('/song/flag/<int:id>')
def flag_song(id):
    s=Song.query.get(id)
    if s.flaged==True:
        s.flaged=False
    else:
        s.flaged=True
    db.session.commit()
    return jsonify({"message":"Song Flaged Sucessfully"})
