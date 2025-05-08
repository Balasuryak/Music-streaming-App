from celery import shared_task
from .models import Song
import flask_excel as excel
from .mail_service import send_message
from .models import User

@shared_task(ignore_result=False)
def create_song_csv():
    song=Song.query.with_entities(Song.song_name,Song.lyrics,Song.genre).all()
    csv_output=excel.make_response_from_query_sets(song,["song_name","lyrics","genre"],"csv")
    filename="songs.csv"

    with open(filename, 'wb') as f:
        f.write(csv_output.data)

    return filename


@shared_task(ignore_result=False)
def daily_reminder(to,message):
    user=User.query.all()
    for u in user:
        send_message(u.Email,message,"hello")
    return "OK"

@shared_task(ignore_result=True)
def monthly_reminder(to,message):
    user=User.query.all()
    for u in user:
        send_message(u.Email,message,"hello")
    return "OK"
