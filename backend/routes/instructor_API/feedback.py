import os
from models import db, user_datastore, User, Role, Courses, course_enrollment, course_documents, deadlines, feedback as FeedbackModel
from flask_security import auth_token_required, roles_required, current_user
import datetime
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource
# from sqlalchemy.orm import joinedby

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

class InstructorFeedbackAPI(Resource):
    @auth_token_required
    @roles_required('instructor')
    def get(self):
        # Get all feedback items where the current user is the instructor
        feedback_items = (
            FeedbackModel.query
            .filter_by(instructor_id=current_user.id)
            .join(User, FeedbackModel.user_id == User.id)  # Join with User table
            .add_columns(User.id, User.email)  # Include student details
            .all()
        )
        
        student_feedback = []
        
        for feedback_item, student_id, student_email in feedback_items:
            # Calculate how long ago the feedback was submitted
            time_difference = datetime.datetime.now() - feedback_item.date
            days_ago = time_difference.days
            
            if days_ago == 0:
                time_ago = "Today"
            elif days_ago == 1:
                time_ago = "Yesterday"
            elif days_ago < 7:
                time_ago = f"{days_ago} days ago"
            elif days_ago < 30:
                weeks = days_ago // 7
                time_ago = f"{weeks} week{'s' if weeks > 1 else ''} ago"
            else:
                months = days_ago // 30
                time_ago = f"{months} month{'s' if months > 1 else ''} ago"
            
            # Get course name if available
            course_name = "N/A"
            if feedback_item.course_id:
                course = Courses.query.filter_by(id=feedback_item.course_id).first()
                if course:
                    course_name = course.name
            
            # Format the data in the structure expected by the frontend
            student_data = {
                "id": feedback_item.id,
                "roll": str(student_id).zfill(4),  # Format ID like "1001"
                "feedback": feedback_item.content,
                "email": student_email,
                "lastUpdated": time_ago,
                "course": course_name,
                "attachment": feedback_item.attachment,
                "status": feedback_item.status,
                "date": feedback_item.date.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            student_feedback.append(student_data)
        
        return make_response(jsonify(student_feedback), 200)
    # @auth_token_required
    # @roles_required('instructor')
    # def post(self):
    #     """Update the status of a feedback item"""
    #     data = request.get_json()
    #     feedback_id = data.get('id')
        
    #     if not feedback_id:
    #         return make_response(jsonify({"error": "Feedback ID is required"}), 400)
        
    #     feedback_item = FeedbackModel.query.filter_by(id=feedback_id, instructor_id=current_user.id).first()
        
    #     if not feedback_item:
    #         return make_response(jsonify({"error": "Feedback not found or you don't have permission"}), 404)
        
    #     # Update status if provided
    #     if 'status' in data:
    #         feedback_item.status = data['status']
        
    #     # Add a reply if provided
    #     if 'reply' in data:
    #         # You might want to create a new model for replies or add a reply field to your feedback model
    #         # For this example, we'll assume you'll handle the email reply through the frontend
    #         pass
        
    #     db.session.commit()
        
    #     return make_response(jsonify({"message": "Feedback updated successfully"}), 200)