import os
from models import db, user_datastore, User, Role, Courses, course_enrollment, course_documents, deadlines, feedback as FeedbackModel
from flask_security import auth_token_required, roles_required, current_user
import datetime
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

class FeedbackAPI(Resource):
    @auth_token_required
    @roles_required('student')
    def post(self):
        data = request.form
        content = data.get('content')
        course_id = data.get('course_id')
        instructor_id = data.get('instructor_id')
        file = request.files.get('attachment')

        if not content:
            return make_response(jsonify({"error": "Feedback content is required"}), 400)

        # Handle file upload
        attachment = None
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        if file and allowed_file(file.filename):
            filename = f"{current_user.id}_{file.filename}"
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            attachment = file_path

        # Save feedback to database
        new_feedback = FeedbackModel(
            user_id=current_user.id,
            instructor_id=instructor_id if instructor_id else None,
            course_id=course_id if course_id else None,
            content=content,
            attachment=attachment
        )

        db.session.add(new_feedback)
        db.session.commit()

        return make_response(jsonify({"message": "Feedback submitted successfully", "attachment": attachment}), 201)

    @auth_token_required
    @roles_required('student')
    def get(self):
        """Get all feedback for the current user"""
        user_feedbacks = FeedbackModel.query.filter_by(user_id=current_user.id).all()
        
        feedback_list = []
        for feedback in user_feedbacks:
            feedback_data = {
                'id': feedback.id,
                'content': feedback.content,
                'attachment': feedback.attachment,
                'status': 'Open' if not feedback.status else 'Closed',
                'created_at': feedback.date.strftime('%Y-%m-%d'),
                'category': 'instructor' if feedback.instructor_id else 'course'
            }
            
            # Add instructor or course information
            if feedback.instructor_id:
                instructor = User.query.get(feedback.instructor_id)
                if instructor:
                    feedback_data['instructor_name'] = instructor.username
            
            if feedback.course_id:
                course = Courses.query.get(feedback.course_id)
                if course:
                    feedback_data['course_name'] = course.name
            
            feedback_list.append(feedback_data)
            
        return make_response(jsonify(feedback_list), 200)

class InstructorAPI(Resource):
    @auth_token_required
    def get(self):
        """Get all instructors for the feedback form"""
        # Find the instructor role
        instructor_role = Role.query.filter_by(name='instructor').first()
        
        if not instructor_role:
            return make_response(jsonify([]), 200)
        
        # Query users with the instructor role
        instructors = User.query.join(User.roles).filter(Role.id == instructor_role.id).all()
        
        instructor_list = []
        for instructor in instructors:
            instructor_list.append({
                'id': instructor.id,
                'name': instructor.username or instructor.email
            })
            
        return make_response(jsonify(instructor_list), 200)