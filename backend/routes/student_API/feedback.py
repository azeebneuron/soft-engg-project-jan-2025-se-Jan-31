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
