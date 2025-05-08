from main import app
from application.sec import datastore
from application.models import db,Admin,Role,User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name="admin", description="User is an admin")
    db.session.commit()
    data=User(Name='admin',phone=4568987916,Email='abc@gmail.com',username="admin@email.com", password=generate_password_hash("admin"))
    data.roles='admin'
    db.session.add(data)
    db.session.commit()
    data=User(Name='user1',phone=4568987916,Email='cab@gmail.com',username="user1@email.com", password=generate_password_hash("user1"))
    db.session.add(data)
    db.session.commit()




    
    # if not datastore.find_user(username="admin@email.com"):
    #     datastore.create_user(
    #         username="admin@email.com", password="admin", roles="admin")


    # admin=Admin(username='admin',password='admin')
    # db.session.add(admin)
    # try:
    #     db.session.commit()
    # except:
    #     pass