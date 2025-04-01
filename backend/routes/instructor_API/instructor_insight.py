from flask import request, jsonify
from flask_restful import Resource
from flask_security import auth_required, current_user, roles_required
import json
import os
from dotenv import load_dotenv

# Import the analytics and narrative generator
from data_analysis import PerformanceAnalytics
from llm_integration import NarrativeGenerator

# Load environment variables for API keys
load_dotenv()

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(current_dir, '..', '..', 'data')

analytics = PerformanceAnalytics(data_path=data_path)
narrative_generator = NarrativeGenerator()

class InstructorInsightAPI(Resource):
    @auth_required('token')
    @roles_required('instructor')
    def get(self):
        """
        Get instructor insights and personalized narrative
        Endpoint: /api/instructor/insights
        Method: GET
        """
        # Check if user is an instructor
        if not current_user.has_role('instructor'):
            return {'message': 'Access denied. Instructor role required.'}, 403
        
        # Get instructor name from the authenticated user
        # instructor_name = current_user.username
        instructor_name = "Dr. Anil Kumar"
        
        try:
            # Get comprehensive dashboard data
            dashboard_data = analytics.get_instructor_dashboard_data(instructor_name)
            
            # Generate narrative
            narrative = narrative_generator.generate_instructor_narrative(dashboard_data)
            
            # Return combined data
            return {
                'dashboard_data': dashboard_data,
                'narrative': narrative
            }, 200
            
        except Exception as e:
            return {'message': f'Error generating insights: {str(e)}'}, 500


class CourseInsightAPI(Resource):
    @auth_required('token')
    @roles_required('instructor')
    def get(self, course_id):
        """
        Get detailed insights for a specific course
        Endpoint: /api/instructor/courses/<course_id>/insights
        Method: GET
        """
        # Check if user is an instructor
        if not current_user.has_role('instructor'):
            return {'message': 'Access denied. Instructor role required.'}, 403
        
        # Get instructor name from the authenticated user
        instructor_name = current_user.name
        
        try:
            # Map course_id to course_code (in a real app, this would be from database)
            # For this prototype, we'll use a simple mapping
            course_mapping = {
                1: 'MLF301',  # Machine Learning Foundations
                2: 'MLT401',  # Machine Learning Techniques
                3: 'MLP501',  # Machine Learning Practice
                4: 'DL501',   # Deep Learning
                # Add other mappings as needed
            }
            
            course_code = course_mapping.get(course_id)
            if not course_code:
                return {'message': f'Course with ID {course_id} not found'}, 404
            
            # Get course performance data
            course_data = analytics.get_course_performance(course_code=course_code)
            
            # Return data
            return course_data, 200
            
        except Exception as e:
            return {'message': f'Error generating course insights: {str(e)}'}, 500


class AtRiskStudentsAPI(Resource):
    @auth_required('token')
    @roles_required('instructor')
    def get(self):
        """
        Get a list of at-risk students for the instructor
        Endpoint: /api/instructor/at-risk-students
        Method: GET
        """
        # Check if user is an instructor
        if not current_user.has_role('instructor'):
            return {'message': 'Access denied. Instructor role required.'}, 403
        
        # Get instructor name from the authenticated user
        instructor_name = current_user.name
        
        try:
            # Get at-risk students for this instructor
            at_risk_students = analytics.get_at_risk_students(instructor_name=instructor_name)
            
            # Return data
            return {'at_risk_students': at_risk_students}, 200
            
        except Exception as e:
            return {'message': f'Error retrieving at-risk students: {str(e)}'}, 500


class TrainRiskModelAPI(Resource):
    @auth_required('token')
    @roles_required('instructor')
    def post(self):
        """
        Train/update the risk prediction model
        Endpoint: /api/admin/train-risk-model
        Method: POST
        """
        # Check if user is an admin
        if not current_user.has_role('admin'):
            return {'message': 'Access denied. Admin role required.'}, 403
        
        try:
            # Train the risk prediction model
            model_result = analytics.train_risk_prediction_model()
            
            if model_result:
                return {'message': f'Risk prediction model trained successfully. Accuracy: {model_result["accuracy"]:.2f}'}, 200
            else:
                return {'message': 'Unable to train risk prediction model. Insufficient data.'}, 400
            
        except Exception as e:
            return {'message': f'Error training risk model: {str(e)}'}, 500