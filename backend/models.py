from flask_security import UserMixin, RoleMixin, AsaList, SQLAlchemyUserDatastore
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'last_login_at': self.last_login_at,
            'current_login_at': self.current_login_at,
            'last_login_ip': self.last_login_ip,
            'current_login_ip': self.current_login_ip,
            'login_count': self.login_count,
            'active': self.active,
            'fs_uniquifier': self.fs_uniquifier,
            'confirmed_at': self.confirmed_at
        }
    def get_all_users():
        return User.query.all()
    
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class Courses(db.Model):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    instructor_id = Column(Integer, ForeignKey('user.id'))
    ta_id = Column(Integer, ForeignKey('user.id'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'instructor_id': self.instructor_id,
            'ta_id': self.ta_id
        }

class course_enrollment(db.Model):
    __tablename__ = 'course_enrollment'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    def serialize(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'user_id': self.user_id
        }
    
class course_documents(db.Model):
    __tablename__ = 'course_documents'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    instructor_id = Column(Integer, ForeignKey('user.id'))
    document_name = Column(String(255))
    document_url = Column(String(255))

    def serialize(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'instructor_id': self.instructor_id,
            'document_name': self.document_name,
            'document_url': self.document_url
        }


# In the deadline model i have added courese as string but we need to update it as course.id as integer 
# As of now we dont have any course table so i am doing this 
class deadlines(db.Model):
    __tablename__ = 'deadlines'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    course = Column(String(255))
    deadline = Column(DateTime())
    title = Column(String(255))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course': self.course,
            'deadline': self.deadline,
            'description': self.description
        }

class feedback(db.Model):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    instructor_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=True)
    content = Column(String(255))
    attachment = Column(String(255), nullable=True)
    status = Column(Boolean(), default=False)
    date = Column(DateTime(), default=datetime.now)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'instructor_id': self.instructor_id,
            'course_id': self.course_id,
            'content': self.content,
            'attachment': self.attachment,
            'status': self.status,
            'date': self.date
        }
        