from flask import request, jsonify
from flask_restful import Resource
from flask_security import auth_required, current_user
import json
import os
import sys
import importlib.util

class GenerateSyntheticDataAPI(Resource):
    @auth_required('token')
    def post(self):
        """
        Generate synthetic data for demo purposes
        Endpoint: /api/admin/generate-data
        Method: POST
        """
        # Check if user is an admin
        if not current_user.has_role('admin'):
            return {'message': 'Access denied. Admin role required.'}, 403
        
        try:
            # Get parameters from request
            data = request.get_json() or {}
            num_students = data.get('num_students', 150)
            
            # Import the data generation module
            spec = importlib.util.spec_from_file_location(
                "synthetic_data_generator", 
                os.path.join(os.path.dirname(__file__), '..', '..', 'synthetic_data_generator.py')
            )
            data_generator = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(data_generator)
            
            # Create data directory if it doesn't exist
            data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # Generate data
            students, enrollments, performance, interactions, feedback, courses = data_generator.save_data_to_csv()
            
            return {
                'message': 'Synthetic data generated successfully',
                'stats': {
                    'students': len(students),
                    'enrollments': len(enrollments),
                    'performance_records': len(performance),
                    'interactions': len(interactions),
                    'feedback': len(feedback),
                    'courses': len(courses)
                }
            }, 200
            
        except Exception as e:
            import traceback
            return {
                'message': f'Error generating synthetic data: {str(e)}',
                'traceback': traceback.format_exc()
            }, 500