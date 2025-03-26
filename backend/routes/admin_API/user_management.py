from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, roles_required, current_user
from models import db, User, Role, Courses, course_enrollment

# List All Users with Roles
class ListUsers(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        # Fetch all users with their roles
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = user.serialize()
            # Add roles to user data
            user_data['roles'] = [{'id': role.id, 'name': role.name} for role in user.roles]
            
            # If user is an instructor, fetch their courses
            if any(role.name == 'instructor' for role in user.roles):
                user_courses = Courses.query.filter_by(instructor_id=user.id).all()
                user_data['courses'] = [course.serialize() for course in user_courses]
            else:
                user_data['courses'] = []
            
            user_list.append(user_data)
        
        return make_response(jsonify(user_list), 200)

# List All Courses
class ListCourses(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        courses = Courses.query.all()
        course_list = []
        for course in courses:
            course_data = course.serialize()
            # Add instructor details if exists
            if course.instructor_id:
                instructor = User.query.get(course.instructor_id)
                if instructor:
                    course_data['instructor'] = {
                        'id': instructor.id,
                        'name': instructor.username or instructor.email
                    }
            course_list.append(course_data)
        
        return make_response(jsonify(course_list), 200)

# Assign Course to Instructor
class AssignCourseToInstructor(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        instructor_id = data.get('instructor_id')
        course_id = data.get('course_id')
        
        if not instructor_id or not course_id:
            return make_response(jsonify({"error": "Instructor ID and Course ID are required"}), 400)
        
        # Verify instructor exists and has instructor role
        instructor = User.query.get(instructor_id)
        if not instructor:
            return make_response(jsonify({"error": "Instructor not found"}), 404)
        
        # Verify instructor has 'instructor' role
        if not any(role.name == 'instructor' for role in instructor.roles):
            return make_response(jsonify({"error": "User is not an instructor"}), 400)
        
        # Verify course exists
        course = Courses.query.get(course_id)
        if not course:
            return make_response(jsonify({"error": "Course not found"}), 404)
        
        # Check if course is already assigned
        if course.instructor_id:
            return make_response(jsonify({"error": "Course is already assigned to an instructor"}), 400)
        
        # Assign course to instructor
        course.instructor_id = instructor_id
        db.session.commit()
        
        return make_response(jsonify({
            "message": f"Course {course.name} assigned to {instructor.username}",
            "course": course.serialize(),
            "instructor": instructor.serialize()
        }), 200)

# Deactivate a user by setting their active status to False
class DeactivateUser(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        user_id = data.get("user_id")
        
        if not user_id:
            return make_response(jsonify({"error": "User ID is required"}), 400)
        
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
        
        user.active = False
        db.session.commit()
        
        return make_response(jsonify({
            "message": f"User {user.username} has been deactivated",
            "user": user.serialize()
        }), 200)

# Activate a user by setting their active status to True
class ActivateUser(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        user_id = data.get("user_id")
        
        if not user_id:
            return make_response(jsonify({"error": "User ID is required"}), 400)
        
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
        
        user.active = True
        db.session.commit()
        
        return make_response(jsonify({
            "message": f"User {user.username} has been activated",
            "user": user.serialize()
        }), 200)