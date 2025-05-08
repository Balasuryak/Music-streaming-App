from flask import Flask
from application.models import db,User,Role
from config import DevelopmentConfig
from flask_security import SQLAlchemyUserDatastore,Security
from application.resources import api
from application.sec import datastore
from application.worker import celery_init_app
from application.instances import cache
from flask import Flask,render_template,request,flash,url_for,redirect
from celery.schedules import crontab
from application.tasks import daily_reminder,monthly_reminder
import os
import flask_excel as excel
from flask_sqlalchemy import SQLAlchemy 
from flask_login import login_user,LoginManager,logout_user,LoginManager,current_user,UserMixin,login_required
import datetime
import matplotlib
matplotlib.use('Agg') #https://stackoverflow.com/a/29172195
from matplotlib import pyplot as plt
from io import BytesIO
import base64

def create_app():
    app=Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    excel.init_excel(app)
    app.security=Security(app,datastore)
    cache.init_app(app)
    with app.app_context():
        import application.views
    return app

app = create_app()
celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=19, minute=15),
        daily_reminder.s("Balasurya@email.com",'Visit breath it Music APP ENJOY!!!! unlimited song for Free'),
    )

# @celery_app.on_after_configure.connect
# def send_memail(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(hour=8, minute=18,day_of_month=1),
#     monthly_reminder.s("Balasurya@email.com",'Monthly Test'),
#     )

@celery_app.on_after_configure.connect
def send_memail(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=19, minute=15),
    monthly_reminder.s("Balasurya@email.com",'Visit breath it Music APP ENJOY!!!! unlimited song for Free'),
    )



if __name__ == '__main__':
    app.run(debug=True)