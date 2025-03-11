import os
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource
from flask_security import auth_token_required, roles_required, current_user
from models import db, User, Courses, course_enrollment, course_documents
from yaml_log import log_to_yaml
from datetime import datetime

class InstructorCoursesAPI(Resource):
    @auth_token_required
    @roles_required('instructor')
    def get(self):
        # Log the GET request
        log_to_yaml('get_courses', {
            'instructor_id': current_user.id,
            'action': 'fetch_all_courses'
        })
        
        # Get all courses where the current user is the instructor
        courses_data = Courses.query.filter_by(instructor_id=current_user.id).all()
        
        result = []
        for course in courses_data:
            # Get number of enrolled students
            enrolled_count = course_enrollment.query.filter_by(course_id=course.id).count()
            
            # Get all resources for this course
            resources = course_documents.query.filter_by(course_id=course.id).all()
            resources_list = []
            
            for resource in resources:
                resources_list.append({
                    "id": resource.id,
                    "title": resource.document_name,
                    "link": resource.document_url
                })
            
            result.append({
                "id": course.id,
                "name": course.name,
                "enrolledStudents": enrolled_count,
                "resources": resources_list
            })
            
        return make_response(jsonify(result), 200)
    
    @auth_token_required
    @roles_required('instructor')
    def post(self):
        # Log the POST request
        log_to_yaml('create_course_attempt', {
            'instructor_id': current_user.id,
            'data': request.get_json()
        })
        
        # Create a new course
        data = request.get_json()
        if not data or not data.get('name'):
            return make_response(jsonify({"error": "Course name is required"}), 400)
        
        new_course = Courses(
            name=data.get('name'),
            description=data.get('description', ''),
            instructor_id=current_user.id
        )
        
        db.session.add(new_course)
        db.session.commit()

        # Log the course creation event
        log_to_yaml('course_created', {
            'course_id': new_course.id,
            'course_name': new_course.name,
            'instructor_id': current_user.id
        })
        
        return make_response(jsonify({"message": "Course created successfully", "id": new_course.id}), 201)

class CourseResourceAPI(Resource):
    @auth_token_required
    @roles_required('instructor')
    def get(self, course_id):
        # Log the GET request
        log_to_yaml('get_course_resources', {
            'instructor_id': current_user.id,
            'course_id': course_id,
            'action': 'fetch_resources'
        })
        
        # Verify course exists and belongs to instructor
        course = Courses.query.filter_by(id=course_id, instructor_id=current_user.id).first()
        if not course:
            return make_response(jsonify({"error": "Course not found or you don't have permission"}), 404)
        
        # Get resources for the course
        resources = course_documents.query.filter_by(course_id=course_id).all()
        resources_data = []
        
        for resource in resources:
            resources_data.append({
                "id": resource.id,
                "title": resource.document_name,
                "link": resource.document_url
            })
        
        return make_response(jsonify({
            "course_id": course_id,
            "name": course.name,
            "resources": resources_data
        }), 200)
    
    @auth_token_required
    @roles_required('instructor')
    def post(self, course_id):
        # Log the POST request
        log_to_yaml('add_course_resource_attempt', {
            'instructor_id': current_user.id,
            'course_id': course_id,
            'data': request.get_json()
        })
        
        # Verify course exists and belongs to instructor
        course = Courses.query.filter_by(id=course_id, instructor_id=current_user.id).first()
        if not course:
            return make_response(jsonify({"error": "Course not found or you don't have permission"}), 404)
        
        data = request.get_json()
        if not data or not data.get('title') or not data.get('link'):
            return make_response(jsonify({"error": "Resource title and link are required"}), 400)
        
        # Create new resource
        new_resource = course_documents(
            course_id=course_id,
            instructor_id=current_user.id,
            document_name=data.get('title'),
            document_url=data.get('link')
        )
        
        db.session.add(new_resource)
        db.session.commit()
        
        # Log the resource creation event
        log_to_yaml('course_resource_created', {
            'course_id': course_id,
            'resource_id': new_resource.id,
            'instructor_id': current_user.id
        })
        
        return make_response(jsonify({
            "id": new_resource.id,
            "title": new_resource.document_name,
            "link": new_resource.document_url
        }), 201)

class ResourceAPI(Resource):
    @auth_token_required
    @roles_required('instructor')
    def delete(self, resource_id):
        # Log the DELETE request
        log_to_yaml('delete_resource_attempt', {
            'instructor_id': current_user.id,
            'resource_id': resource_id
        })
        
        # Get the resource
        resource = course_documents.query.get(resource_id)
        
        if not resource:
            return make_response(jsonify({"error": "Resource not found"}), 404)
        
        # Verify course belongs to instructor
        course = Courses.query.filter_by(id=resource.course_id, instructor_id=current_user.id).first()
        if not course:
            return make_response(jsonify({"error": "You don't have permission to delete this resource"}), 403)
        
        db.session.delete(resource)
        db.session.commit()
        
        # Log the resource deletion event
        log_to_yaml('resource_deleted', {
            'resource_id': resource_id,
            'course_id': resource.course_id,
            'instructor_id': current_user.id
        })
        
        return make_response(jsonify({"message": "Resource deleted successfully"}), 200)

class CourseStudentsAPI(Resource):
    @auth_token_required
    @roles_required('instructor')
    def get(self, course_id):
        # Log the GET request
        log_to_yaml('get_course_students', {
            'instructor_id': current_user.id,
            'course_id': course_id,
            'action': 'fetch_students'
        })
        
        # Verify course exists and belongs to instructor
        course = Courses.query.filter_by(id=course_id, instructor_id=current_user.id).first()
        if not course:
            return make_response(jsonify({"error": "Course not found or you don't have permission"}), 404)
        
        # Get all enrolled students
        enrollments = course_enrollment.query.filter_by(course_id=course_id).all()
        students = []
        
        for enrollment in enrollments:
            student = User.query.get(enrollment.user_id)
            if student:
                students.append({
                    "id": student.id,
                    "email": student.email,
                    "username": student.username
                })
        
        return make_response(jsonify(students), 200)