from flask import request, jsonify
from flask_restful import Resource
from flask_security import auth_required, current_user
import json
import numpy as np
import os

# Import the analytics and narrative generator
from data_analysis import PerformanceAnalytics
from llm_integration import NarrativeGenerator

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(current_dir, '..', '..', 'data')

analytics = PerformanceAnalytics(data_path=data_path)
narrative_generator = NarrativeGenerator()

class StudentInsightAPI(Resource):
    @auth_required('token')
    def get(self):
        """
        Get personalized insights for the current student
        Endpoint: /api/student/insights
        Method: GET
        """
        # Check if user is a student
        if not current_user.has_role('student'):
            return {'message': 'Access denied. Student role required.'}, 403
        
        # Get student ID from the authenticated user
        #student_id = current_user.id  # This would come from your user model
        student_id = "DS006"        
        try:
            student_data = analytics.get_student_performance(student_id)
            
            # Clean NaN values
            def clean_nans(data):
                if isinstance(data, dict):
                    return {k: clean_nans(v) for k, v in data.items()}
                elif isinstance(data, list):
                    return [clean_nans(item) for item in data]
                elif isinstance(data, float) and np.isnan(data):
                    return None
                return data
            
            cleaned_data = clean_nans(student_data)
            
            narrative = narrative_generator.generate_student_narrative(cleaned_data)
            
            return {
                'student_data': cleaned_data,
                'narrative': narrative
            }, 200
            
        except Exception as e:
            return {'message': f'Error generating insights: {str(e)}'}, 500


class CourseRecommendationAPI(Resource):
    @auth_required('token')
    def get(self):
        """
        Get personalized course recommendations for the student
        Endpoint: /api/student/recommendations
        Method: GET
        """
        # Check if user is a student
        if not current_user.has_role('student'):
            return {'message': 'Access denied. Student role required.'}, 403
        
        # Get student ID from the authenticated user
        student_id = current_user.id
        
        try:
            # Get performance data for the student
            student_data = analytics.get_student_performance(student_id)
            
            # Generate course recommendations
            recommendations = narrative_generator.generate_course_recommendation(student_data)
            
            # Return data
            return {
                'recommendations': recommendations,
                'current_trimester': student_data.get('current_trimester', 1)
            }, 200
            
        except Exception as e:
            return {'message': f'Error generating recommendations: {str(e)}'}, 500


class PerformanceComparisonAPI(Resource):
    @auth_required('token')
    def get(self, course_id):
        """
        Get student performance compared to class average for a specific course
        Endpoint: /api/student/courses/<course_id>/comparison
        Method: GET
        """
        # Check if user is a student
        if not current_user.has_role('student'):
            return {'message': 'Access denied. Student role required.'}, 403
        
        # Get student ID from the authenticated user
        student_id = current_user.id
        
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
            
            # Get student performance data
            student_data = analytics.get_student_performance(student_id)
            
            # Get course performance data (class averages)
            course_data = analytics.get_course_performance(course_code=course_code)
            
            # Extract student's performance in this course
            student_course_data = None
            for course in student_data.get('ongoing_courses', []) + student_data.get('completed_courses', []):
                if course.get('course_code') == course_code:
                    student_course_data = course
                    break
            
            if not student_course_data:
                return {'message': f'Student not enrolled in course with ID {course_id}'}, 404
            
            # Prepare comparison data
            comparison = {
                'course_code': course_code,
                'course_name': course_data.get('course_name', 'Unknown Course'),
                'student_performance': {
                    'quiz1': student_course_data.get('quiz1'),
                    'quiz2': student_course_data.get('quiz2'),
                    'endterm': student_course_data.get('endterm'),
                    'attendance': student_course_data.get('attendance_percentage'),
                    'total_score': student_course_data.get('total_score'),
                    'grade': student_course_data.get('grade')
                },
                'class_average': {
                    'quiz1': course_data.get('avg_quiz1'),
                    'quiz2': course_data.get('avg_quiz2'),
                    'endterm': course_data.get('avg_endterm'),
                    'attendance': course_data.get('avg_attendance'),
                    'pass_rate': course_data.get('pass_rate')
                },
                'percentile': calculate_percentile(student_course_data, course_data)
            }
            
            return comparison, 200
            
        except Exception as e:
            return {'message': f'Error generating comparison: {str(e)}'}, 500


def calculate_percentile(student_data, course_data):
    """
    Calculate student's percentile in the course
    This is a simplified version for the prototype
    """
    # This would typically be calculated using the actual distribution of scores
    # For the prototype, we'll use a simple estimation
    
    student_total = student_data.get('total_score')
    if not student_total:
        return None
    
    # Simplistic approach assuming a normal distribution
    # In a real implementation, you would use actual student rankings
    class_avg = (
        course_data.get('avg_quiz1', 0) * 0.15 +
        course_data.get('avg_quiz2', 0) * 0.15 +
        course_data.get('avg_endterm', 0) * 0.40 +
        course_data.get('avg_assignment_score', 0) * 0.30
    )
    
    # Assume standard deviation is 10% of the mean
    std_dev = class_avg * 0.1
    
    # Calculate z-score
    if std_dev == 0:
        return 50  # Default to median if we can't calculate
    
    z_score = (student_total - class_avg) / std_dev
    
    # Convert z-score to percentile (simplified)
    import math
    import scipy.stats as stats
    
    percentile = stats.norm.cdf(z_score) * 100
    
    return round(percentile, 1)