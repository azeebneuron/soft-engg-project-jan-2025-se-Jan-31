from app import create_app
from models import db, user_datastore

app, _ = create_app()

#this file is for delete the database and create the new one with the default admin and user


def create_empty_tables():
    db.drop_all()
    db.create_all()

with app.app_context():
    create_empty_tables()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='student', description='student')
    user_datastore.find_or_create_role(name='instructor', description='instructor')
    user_datastore.find_or_create_role(name='ta', description='Teaching assistant')
    db.session.commit()

    if not user_datastore.find_user(email="admin@a.com"):
        admin_user=user_datastore.create_user(email="admin@a.com", password="admin", username="admin")
        user_datastore.add_role_to_user(admin_user, "admin")

    if not user_datastore.find_user(email="user@a.com"):
        admin_user=user_datastore.create_user(email="user@a.com", password="user", username="user")
        user_datastore.add_role_to_user(admin_user, "student")

    if not user_datastore.find_user(email="instructor@a.com"):
        instructor = user_datastore.create_user(email="instructor@a.com", password="instructor", username="instructor")
        user_datastore.add_role_to_user(instructor, "instructor")

    if not user_datastore.find_user(email="ta@a.com"):
        ta = user_datastore.create_user(email="ta@a.com", password="userta", username="ta")
        user_datastore.add_role_to_user(ta, "ta")

    db.session.commit()
        