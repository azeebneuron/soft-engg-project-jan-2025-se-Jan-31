from flask import request
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_security import Security
from pymongo import MongoClient
from models import db, user_datastore
import json
import numpy as np
import os

def numpy_json_encoder(obj):
    """
    Enhanced JSON encoder function to handle all special types:
    - NumPy types
    - Pandas types
    - NaN values
    """
    # Handle NumPy types
    if isinstance(obj, (np.int64, np.integer)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32, np.floating)):
        return float(obj) if not np.isnan(obj) else None
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    
    # Handle Pandas types
    if pd.isna(obj):
        return None
    
    # Handle other non-serializable types
    try:
        return json.JSONEncoder().default(obj)
    except TypeError:
        return str(obj)

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.localDev")
    
    # Configure JSON handling
    app.json.ensure_ascii = False
    app.json.default = numpy_json_encoder

    # Initialize MongoDB (PyMongo)
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("DB_NAME", "virtual_ta_db")
    mongo_client = MongoClient(mongo_uri)
    app.mongo = mongo_client[db_name]  # Attach MongoDB to app
    
    db.init_app(app)
    security = Security(app, user_datastore)
    CORS(app)
    api = Api(app)
    
    # Configure a custom JSON representation for Flask-RESTful
    @api.representation('application/json')
    def output_json(data, code, headers=None):
        """
        Custom JSON representation for Flask-RESTful
        Uses the numpy_json_encoder for serialization
        """
        resp = app.make_response(
            json.dumps(data, default=numpy_json_encoder) + '\n'
        )
        resp.headers.extend(headers or {})
        resp.status_code = code
        return resp
    
    return app, api

def initialize_database(app):
    """Initialize database with default roles and users if they don't exist"""
    with app.app_context():
        try:
            # Create tables if they don't exist
            print("Creating database tables if they don't exist...")
            db.create_all()
            
            # Check if roles already exist
            admin_role = user_datastore.find_role('admin')
            
            # If admin role doesn't exist, initialize all roles and users
            if not admin_role:
                print("Initializing database with default roles and users...")
                # Create roles
                user_datastore.find_or_create_role(name='admin', description='Administrator')
                user_datastore.find_or_create_role(name='student', description='student')
                user_datastore.find_or_create_role(name='instructor', description='instructor')
                user_datastore.find_or_create_role(name='ta', description='Teaching assistant')
                db.session.commit()
                
                # Create default users
                if not user_datastore.find_user(email="admin@a.com"):
                    admin_user = user_datastore.create_user(email="admin@a.com", password="admin", username="admin")
                    user_datastore.add_role_to_user(admin_user, "admin")
                
                if not user_datastore.find_user(email="user@a.com"):
                    student_user = user_datastore.create_user(email="user@a.com", password="user", username="user")
                    user_datastore.add_role_to_user(student_user, "student")
                
                if not user_datastore.find_user(email="instructor@a.com"):
                    instructor = user_datastore.create_user(email="instructor@a.com", password="instructor", username="instructor")
                    user_datastore.add_role_to_user(instructor, "instructor")
                
                if not user_datastore.find_user(email="ta@a.com"):
                    ta = user_datastore.create_user(email="ta@a.com", password="userta", username="ta")
                    user_datastore.add_role_to_user(ta, "ta")
                
                db.session.commit()
                print("Database initialization completed.")
            else:
                print("Database already contains roles. Skipping initialization.")
        except Exception as e:
            print(f"Error during database initialization: {e}")
            db.session.rollback()

app, api_handler = create_app()

# Initialize the database with default roles and users
initialize_database(app)

@app.route("/hello_world")
def hello_world():
    return "Hello World!"

# Import routes

from routes.auth import Signup, Signin
api_handler.add_resource(Signup, "/signup")
api_handler.add_resource(Signin, "/signin")

from routes.student_API.deadline import DeadlineAPICreate, DeadlineAPIGet, DeadlineAPIDelete, DeadlineAPIUpdate, CourseAPIGet
api_handler.add_resource(DeadlineAPICreate, "/student/deadline")
api_handler.add_resource(DeadlineAPIGet, "/student/deadline")
api_handler.add_resource(DeadlineAPIDelete, "/student/deadline")
api_handler.add_resource(DeadlineAPIUpdate, "/student/deadline")
api_handler.add_resource(CourseAPIGet, "/student/courses")

from routes.admin_API.user_management import DeactivateUser, ActivateUser, ListUsers, AssignCourseToInstructor, ListCourses
api_handler.add_resource(ListUsers, '/api/users')
api_handler.add_resource(ListCourses, '/api/courses')
api_handler.add_resource(AssignCourseToInstructor, '/api/courses/assign')
api_handler.add_resource(DeactivateUser, '/api/user/deactivate')
api_handler.add_resource(ActivateUser, '/api/user/activate')


from routes.student_API.feedback import FeedbackAPI, InstructorAPI
api_handler.add_resource(FeedbackAPI, "/student/feedback")
api_handler.add_resource(InstructorAPI, "/student/instructors")

# Instructor dashboard routes
from routes.instructor_API.course import InstructorCoursesAPI, CourseResourceAPI, ResourceAPI, CourseStudentsAPI
api_handler.add_resource(InstructorCoursesAPI, '/api/instructor/courses')
api_handler.add_resource(CourseResourceAPI, '/api/instructor/courses/<int:course_id>/resources')
api_handler.add_resource(ResourceAPI, '/api/instructor/resources/<int:resource_id>')
api_handler.add_resource(CourseStudentsAPI, '/api/instructor/courses/<int:course_id>/students')

from routes.instructor_API.dashboard import InstructorDashboardData 
api_handler.add_resource(InstructorDashboardData, '/api/instructor/dashboard')

from routes.instructor_API.feedback import InstructorFeedbackAPI
api_handler.add_resource(InstructorFeedbackAPI, '/api/instructor/feedback')

# Instructor Insight APIs
from routes.instructor_API.instructor_insight import InstructorInsightAPI, CourseInsightAPI, AtRiskStudentsAPI, TrainRiskModelAPI
api_handler.add_resource(InstructorInsightAPI, '/api/instructor/insights')
api_handler.add_resource(CourseInsightAPI, '/api/instructor/courses/<int:course_id>/insights')
api_handler.add_resource(AtRiskStudentsAPI, '/api/instructor/at-risk-students')
api_handler.add_resource(TrainRiskModelAPI, '/api/admin/train-risk-model')

# Student Insight APIs
from routes.student_API.student_insight import StudentInsightAPI, CourseRecommendationAPI, PerformanceComparisonAPI
api_handler.add_resource(StudentInsightAPI, '/api/student/insights')
api_handler.add_resource(CourseRecommendationAPI, '/api/student/recommendations')
api_handler.add_resource(PerformanceComparisonAPI, '/api/student/courses/<int:course_id>/comparison')

# Data Generation API (for demo purposes)
from routes.admin_API.data_generation import GenerateSyntheticDataAPI
api_handler.add_resource(GenerateSyntheticDataAPI, '/api/admin/generate-data')

# RAG chatbot 
from chatbot.chatbotapi import ChatResource, ConversationsResource, ConversationResource
api_handler.add_resource(ChatResource, '/api/chat')
api_handler.add_resource(ConversationsResource, '/api/conversations')
api_handler.add_resource(ConversationResource, '/api/conversation/<string:conversation_id>', '/api/conversation')

# VideoBot API Routes
from videoBot import ProcessLecture, VideoChatbot, ProcessPlaylist, GetPlaylistDetails, GetAllPlaylists
api_handler.add_resource(ProcessLecture, '/api/lecture')
api_handler.add_resource(VideoChatbot, '/api/video/chat')
api_handler.add_resource(ProcessPlaylist, '/api/playlist')
api_handler.add_resource(GetPlaylistDetails, '/api/playlist/<string:playlist_id>')
api_handler.add_resource(GetAllPlaylists, '/api/playlists')


if __name__ == "__main__":
    app.run(debug=True, port=3000)