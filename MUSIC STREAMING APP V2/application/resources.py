from flask_restful import Resource, Api,reqparse
from flask_security import auth_required, roles_required, current_user
from .models import Song, db
from werkzeug.datastructures import FileStorage

api=Api(prefix='/api')


parser = reqparse.RequestParser()
parser.add_argument('song_name', type=str,
                    help='Topic is required should be a string', required=True)
parser.add_argument('lyrics', type=str,
                    help='Description is required and should be a string', required=True)
parser.add_argument('genre', type=str,
                    help='Resource Link is required and should be a string', required=True)
parser.add_argument('album', type=str,
                    help='Resource Link is required and should be a string', required=True)
parser.add_argument('song_file')

class Song(Resource):
    def get(self):
        return {'hello': 'world'}
    
    def post(self):
        args = parser.parse_args()
        print(args)
        song_name=args['song_name']
        lyrics=args['lyrics']
        genre=args['genre']
        album=args['album']
        file=args['song_file'].name
        print(file)
        print(song_name,lyrics,genre,album)
        # print(file)
        # filename=file.name
        # pfile=args.get("song_pfile")
        # pfilename=pfile.name
        # song_data = Song(song_name=args.get("song_name"),lyrics=args.get("lyrics"),
        #                 filename=filename,pfile=pfilename,duration=args.get("duration"),genre=args.get("genre"),album=args.get("album"))
        # db.session.add(song_data)
        # db.session.commit()
        return {"message": "Study Resource Created"}
    
api.add_resource(Song, '/song_upload')

