from models import db, user_datastore, User, Role, Courses, course_enrollment, course_documents, deadlines
from flask_security import auth_token_required, roles_required, current_user
import datetime
from flask import request, jsonify, make_response
from flask_restful import Resource

class DeadlineAPICreate(Resource):
    @auth_token_required
    @roles_required('student')
    def post(self):
        print('Current user:', current_user)
        data = request.get_json()
        course = data.get('course')
        title = data.get('title')
        deadline_str = data.get('deadline')

        try:
            # Convert deadline from 'dd-mm-yyyy' format to datetime object
            deadline = datetime.datetime.strptime(deadline_str, '%d-%m-%Y')
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date format. Use dd-mm-yyyy'}), 400)

        # Get user_id from current authenticated user
        user_id = current_user.id

        new_deadline = deadlines(user_id=user_id, course=course, deadline=deadline, title=title)
        db.session.add(new_deadline)
        db.session.commit()

        return make_response(jsonify({'message': 'Deadline added successfully'}), 200)


class DeadlineAPIGet(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        user_id = current_user.id
        user_deadlines = deadlines.query.filter_by(user_id=user_id).all()

        # Format deadlines for JSON response
        deadlines_list = [
            {
                'course': deadline.course,
                'title': deadline.title,
                'deadline': deadline.deadline.strftime('%d-%m-%Y')
            }
            for deadline in user_deadlines
        ]

        return make_response(jsonify({'deadlines': deadlines_list}), 200)
    
class DeadlineAPIDelete(Resource):
    @auth_token_required
    @roles_required('student')
    def delete(self):
        data = request.get_json()
        if not data or 'id' not in data:
            return make_response(jsonify({'error': 'ID is required'}), 400)

        id = data.get('id')
        deadline = deadlines.query.filter_by(id=id).first()

        if not deadline:
            return make_response(jsonify({'error': 'Deadline with the given ID does not exist'}), 404)

        db.session.delete(deadline)
        db.session.commit()
        return make_response(jsonify({'message': 'Deadline deleted successfully'}), 200)

class DeadlineAPIUpdate(Resource):
    @auth_token_required
    @roles_required('student')
    def put(self):
        data = request.get_json()
        if not data or 'id' not in data:
            return make_response(jsonify({'error': 'ID is required'}), 400)

        id = data.get('id')
        course = data.get('course')
        title = data.get('title')
        deadline_str = data.get('deadline')

        deadline = deadlines.query.filter_by(id=id).first()

        if not deadline:
            return make_response(jsonify({'error': 'Deadline with the given ID does not exist'}), 404)

        try:
            if deadline_str:
                deadline.deadline = datetime.datetime.strptime(deadline_str, '%d-%m-%Y')
            if course:
                deadline.course = course
            if title:
                deadline.title = title
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date format. Use dd-mm-yyyy'}), 400)

        db.session.commit()

        return make_response(jsonify({'message': 'Deadline updated successfully'}), 200)

class CourseAPIGet(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        user_id = current_user.id
        
        # Get all course enrollments for the current user
        enrollments = course_enrollment.query.filter_by(user_id=user_id).all()
        
        # Extract the course IDs from enrollments
        course_ids = [enrollment.course_id for enrollment in enrollments]
        
        # Query for all courses that the user is enrolled in
        user_courses = Courses.query.filter(Courses.id.in_(course_ids)).all()
        
        # Format courses for JSON response
        courses_list = [
            {
                'id': course.id, 
                'name': course.name,
                'description': course.description,
                'instructor_id': course.instructor_id
            }
            for course in user_courses
        ]
        
        return make_response(jsonify({'courses': courses_list}), 200)