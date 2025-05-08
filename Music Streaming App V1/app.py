from flask import Flask,render_template,request,flash,url_for,redirect
import os
from flask_sqlalchemy import SQLAlchemy 
from flask_login import login_user,LoginManager,logout_user,LoginManager,current_user,UserMixin,login_required
import datetime
import matplotlib
matplotlib.use('Agg') #https://stackoverflow.com/a/29172195
from matplotlib import pyplot as plt
from io import BytesIO
import base64


app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/audios'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///breath_it.sqlite3'
app.config['UPLOAD_FOLDER_CHARTS'] = 'static/charts'
app.config['SECRET_KEY']="myrandomsecretkey"


db=SQLAlchemy(app)
login_manager=LoginManager(app) 

app.app_context().push()

class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    Name=db.Column(db.String())
    username=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    Email=db.Column(db.String())
    phone=db.Column(db.Integer())
    flaged=db.Column(db.String() )
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
        self.flaged=False
        

class Admin(db.Model):
    Admin_id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    

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
    language=db.column(db.String())
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
    flaged=db.Column(db.String())
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

    def __init__(self,rate,comment,song_id,user_id):
        self.rating=rate
        self.comment=comment
        self.song_id=song_id
        self.user_id=user_id

class Creator(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    flaged=db.Column(db.String())
    information=db.relationship('Song')
    Album=db.relationship('Album')

    def __init__(self,id,username,password,flag):
        self.id=id
        self.username=username
        self.password=password
        self.flaged=flag

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




    





#------------------------------------------------------------All Logins--------------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/login', methods=['GET','POST'])
def log_user_in():
    if request.method=='POST':
        username=request.form.get('user')
        password=request.form.get('pass')
        this_user=User.query.filter_by(username=username).first()
        song=Song.query.all()
        
        all=Song.query.all()
        if this_user:
            if this_user.password == password:
                login_user(this_user,remember=True)
                flash('logged in succesfully', category='success')
                creator=Creator.query.filter_by(id=current_user.id).first()
                if creator is not None:
                    c=creator.flaged
                else:
                    c=False
                fav=[]
                for song in Song.query.all():
                    if get_rating(song.id)>=4:
                        fav.append(song)
                return render_template('Home.html',all=all,User=this_user,Song=Song.query.order_by(Song.id.desc()).all(),Album=Album.query.all(),flash="logged in succesfully",creator_exist=creator_exist(current_user.id),c=c,fav=fav)
            else:
                return 'Invalid password'
        else:
            return 'User does not exit'
    return render_template('login_form.html')


@app.route('/sign_up',methods=['GET','POST'])
def user_sign_up():
    if request.method=='POST':
        
        username=request.form.get('setuser')
        password=request.form.get('setpass')
        cpassword=request.form.get('confirmpassword')
        name=request.form.get('name')
        ph=request.form.get('ph')
        email=request.form.get('mail')
        if password==cpassword:
            data=User(username=username,password=password,Name=name,phone=ph,Email=email)
            db.session.add(data)
            db.session.commit()
        else:
            return 'error'
        return redirect('/login')    

    return render_template('Sign_up_form.html')


#---------------------------------------------------------Admin functionalities-----------------------------------------------------------------

@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        username=request.form.get('user')
        password=request.form.get('pass')
        this_user=Admin.query.filter_by(username=username).first()
        if this_user:
            if this_user.password == password:
                return redirect('/song_chart')
            else:
                return 'Invalid password'
        else:
            return 'Admin does not exit'
    return render_template('admin_login_form.html')

@app.route('/song_chart')
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

    return render_template('Admin_dashboard.html', chart_src=chart_src,numsong=num_songs,tc=tc,tu=tu,ta=ta,creators=creators,songs=songs)


@app.route('/song/admin/delete/<int:id>',methods=['GET','POST'])
def admin_delete_song(id):
    if request.method=='POST':
        data=Song.query.filter_by(id=id).first()
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('song_chart'))
    
@app.route('/song/flag/<int:id>',methods=['GET','POST'])
def flag_song(id):
    if request.method=='POST':
        s=Song.query.get(id)
        if s.flaged==True:
            s.flaged=False
        else:
            s.flaged=True
        db.session.commit()
        return redirect(url_for('song_chart'))

@app.route('/creator/flag/<int:id>',methods=['GET','POST'])
def flag_creator(id):
    if request.method=='POST':
        c=Creator.query.get(id)
        c.flaged=True
        db.session.commit()
        return redirect(url_for('song_chart'))

@app.route('/creator/flagremove/<int:id>',methods=['GET','POST'])
def flagremove_creator(id):
    if request.method=='POST':
        c=Creator.query.get(id)
        c.flaged=False
        db.session.commit()
        return redirect(url_for('song_chart'))

#--------------------------------------------simple functions-----------------------------------------------------------------------------------
def creator_exist(id):
    creator_exist=Creator.query.filter_by(id=id).first()
    if creator_exist is not None:
        return True
    return False

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

#-------------------------------------------search_function---------------------------------------------------------------------------

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        searchkey = request.form['searchitem']
        result = []
        # search for matching venues
        songs = Song.query.filter(
            Song.song_name.ilike('%'+searchkey+'%') |
            Song.genre.ilike('%' + searchkey+'%')
            ).all()
        Albums = Album.query.filter(
            Album.album_name.ilike('%'+searchkey+'%') |
            Album.artist.ilike('%' + searchkey+'%')
            ).all()
        # print(songs)
        return render_template('search.html',songs=songs,albums=Albums)

        
    return render_template('search.html')

#---------------------------------------------------PROFILE---------------------------------------------------------------------------------------

@app.route('/user.details')
@login_required
def details():
    this_user=User.query.get(current_user.id)
    return render_template('info.html',User=this_user,creator_exist=creator_exist(current_user.id))


#----------------------------------------------------------Song_CRUD---------------------------------------------------------------------------


@app.route('/song/<int:id>',methods=['GET','POST'])
def song_page(id):
    song=Song.query.filter_by(id=id).first()
    flag=song.flaged
    if request.method=='POST':
        rated=request.form.get('rate')
        
        db.session.commit()
    comments=Rating.query.filter_by(song_id=id).all()
    return render_template('song_page.html',Song=Song.query.filter_by(id=id).first(),avg_rating=get_rating(id),comments=comments,flag=flag)

@app.route('/song/edit',methods=['GET','POST'])
def edit_song():
    return render_template('edit_song.html',songs=Song.query.filter_by(creator=current_user.id))

@app.route('/song/edit/<int:id>',methods=['GET','POST'])
def song_edit_page(id):
    if request.method=='POST':
        songname=request.form.get('Songname')
        duration=request.form.get('duration')
        lyrics=request.form.get('lyrics')
        genre=request.form.get('genre')
        album=request.form.get('album')
        song = Song.query.get(id)
        if songname:
            song.song_name = songname
        if duration:
            song.duration=duration
        if lyrics:
            song.lyrics=lyrics
        if genre:
            song.genre=genre
        if album:
            song.album=album
        db.session.commit()
        return redirect(url_for('edit_song'))
    return render_template('song_edit_page.html',song=Song.query.filter_by(id=id).first(),Album=Album.query.all())

@app.route('/song/delete/<int:id>',methods=['GET','POST'])
def delete_song(id):
    if request.method=='POST':
        data=Song.query.filter_by(id=id).first()
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('edit_song'))
    


@app.route('/song/rate/<int:id>',methods=['GET','POST'])
def rate(id):
    if request.method=="POST":
        rate=request.form.get('rate')
        comment=request.form.get('comment')
        song=Rating.query.filter_by(song_id=id).all()
        for s in song:
            if s.user_id==current_user.id:
                return redirect(url_for('play'))
        data=Rating(rate=rate,comment=comment,song_id=id,user_id=current_user.id,)
        db.session.add(data)
        db.session.commit()

        return redirect(url_for('play'))

#------------------------------------------------------CREATOR_FUNCTIONALITIES---------------------------------------------------------------

@app.route('/creator',methods=['GET','POST'])
def creator_page():
    if request.method=='POST':
        existing_user=Creator.query.filter_by(username=current_user.username).first()
            # if current_user.username not in Creator.query(Creator.username):
        if existing_user is None:
            data=Creator(id=current_user.id,username=current_user.username,password=current_user.password,flag=False)
            db.session.add(data)
            db.session.commit()
            return redirect('/upload')
        else:
            return redirect('/upload')
        #return redirect('/upload')
    return render_template('creator_registration.html')

@app.route('/creator_profile',methods=['GET','POST'])
def creator_profile():
    creator=Creator.query.filter_by(id=current_user.id).first()
    return render_template('creator_profile.html',ts=len(Song.query.filter_by(creator=current_user.id).all()),creator=creator)




@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
  if request.method == 'POST':
    file = request.files['file']
    pfile=request.files['pfile']
    songname=request.form.get('Songname')
    duration=request.form.get('duration')
    lyrics=request.form.get('lyrics')
    genre=request.form.get('genre')
    album=request.form.get('album')
    
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pfilename = pfile.filename
        pfile.save(os.path.join(app.config['UPLOAD_FOLDER'], pfilename))

        song=Song(song_name=songname,lyrics=lyrics,pfile=pfilename, duration=duration,genre=genre,filename=filename,album=album,creator=current_user.id,flaged=False)
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('upload'))
  return render_template('upload.html', songs=Song.query.all(),Album=Album.query.all())

@app.route('/play')
@login_required
def play():
    fav=[]
    for song in Song.query.all():
        if get_rating(song.id)>=4:
            fav.append(song)

    creator=Creator.query.filter_by(id=current_user.id).first()
    if creator is not None:
        c=creator.flaged
    else:
        c=False

    print(c)
    all=Song.query.all()
    return render_template('Home.html', all=Song.query.all(),User=current_user,Song=Song.query.order_by(Song.id.desc()).all(),Album=Album.query.all(),flash="logged in succesfully",creator_exist=creator_exist(current_user.id),c=c,fav=fav)

    

#-------------------------------------------------------PLAYLIST_FUNCTIONALITIES--------------------------------------------------------------


@app.route('/playlist/create',methods=['GET', 'POST'])
def Newplaylist():
    if request.method=='POST':
        playlistname=request.form.get('playlistname')
        data=Playlist(name=playlistname,user_id=current_user.id)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('playlist'))
    return render_template('Createplaylist.html')

@app.route('/playlist/delete/<int:id>',methods=['GET', 'POST'])
def deleteplaylist(id):
    if request.method=='POST':
        data=Playlist.query.filter_by(id=id).first()
        pt=Playlist_tracks.query.filter_by(song_id=id).first()
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('playlist'))

@app.route('/playlist_tracks/add/<int:playlistid>',methods=['GET', 'POST'])
def addplaylist(playlistid):
    if request.method=='POST':
        songname=request.form.get('songname')
        s=Song.query.filter_by(song_name=songname).first()
        songid=s.id
        data=Playlist_tracks(song_id=songid,user_id=current_user.id,playlist_id=playlistid)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('playlist')) 
        

@app.route('/playlist')
def playlist():
    result = db.session.query(Playlist,Playlist_tracks,Song).join(Playlist_tracks,Playlist.id == Playlist_tracks.Playlist_id).join(Song,Playlist_tracks.song_id == Song.id).all()
    print(result)
    for playlist,pt,song in result:
        print(f'playlist:{playlist.name},track:{pt.id},song:{song.song_name}')
    return render_template('allplaylist.html',songs=Song.query.all(),playlist=Playlist.query.filter_by(user_id=current_user.id),playlist_tracks=Playlist_tracks.query.all(),user=User.query.filter_by(id=current_user.id).first())


@app.route('/playlist/<int:id>')
def myplaylist(id):
    songs_in_playlist = db.session.query(Song).join(Playlist_tracks, (Song.id == Playlist_tracks.song_id)).filter(Playlist_tracks.Playlist_id == id).all()
    print(songs_in_playlist)
    return render_template('Myplaylist.html',song=songs_in_playlist)


#----------------------------------------------ALBUMS_CRUD------------------------------------------------------------------------------------


@app.route('/album')
def album():
    return render_template('album.html',album=Album.query.all(),creator_exist=creator_exist(current_user.id))

@app.route('/album/edit', methods=['GET', 'POST'])
def album_edit():
    if request.method=='POST':
        file = request.files['file']
        Aname=request.form.get('albumname')
        artist=request.form.get('artist')
        if file:
            pfilename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pfilename))
            data=Album(Aname=Aname,artist=artist,pfile=pfilename,creator=current_user.id)
            db.session.add(data)
            db.session.commit()
            return redirect('/album')
        return render_template('album_edit.html',album=Album.query.all())
    return render_template('album_edit.html',album=Album.query.all())

@app.route('/album/edit/<int:id>', methods=['GET', 'POST'])
def edit_album(id):
    if request.method=='POST':
        album=Album.query.filter_by(id=id).first()
        file = request.files['file']
        Aname=request.form.get('albumname')
        artist=request.form.get('artist')
        if file:
            pfilename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pfilename))
            album.pfile=pfilename
        if Aname:
            album.album_name=Aname
        if artist:
            album.artist=artist
        db.session.commit()
        return redirect(url_for('delete_album')) 
    return render_template('edit_album.html',album=Album.query.filter_by(id=id).first())



@app.route('/album/delete',methods=['GET','POST'])
def delete_album():
    return render_template('delete_album.html',album=Album.query.filter_by(creator=current_user.id).all())

@app.route('/album/delete/<int:id>',methods=['GET','POST'])
def album_delete(id):
    if request.method=='POST':
        album=Album.query.filter_by(id=id).first()
        db.session.delete(album)
        db.session.commit()
        return redirect(url_for('delete_album'))

@app.route('/album/<int:albumid>')
def album_page(albumid):
    album_name=Album.query.filter_by(id=albumid).first()
    song=Song.query.filter_by(album=album_name.album_name).all()
    return render_template('album_page.html',album=Album.query.filter_by(id=albumid).first(),song=song)



#----------------------------------------------------LOGOUTS-----------------------------------------------------------------------------

@app.route('/Logout')
@login_required
def log_user_out():
    logout_user()
    return redirect('/login')

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)





#---------------------------------------------------------------MAD_1_PROJECT-------------------------------------------------------------------

