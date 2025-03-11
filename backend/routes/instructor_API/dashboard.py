from flask import request, jsonify
from flask_restful import Resource, Api
from flask_security import current_user, auth_required
from datetime import datetime
from models import db, User, Role, Courses, course_enrollment, course_documents, feedback
from sqlalchemy import func
from flask import Blueprint

instructor_bp = Blueprint('instructor_api', __name__)
api = Api(instructor_bp)

class InstructorDashboardData(Resource):
    @auth_required('token')
    def get(self):
        """Get data for instructor dashboard summary"""
        if not current_user.is_authenticated:
            return {"error": "Authentication required"}, 401
        
        # Check if user has instructor role
        is_instructor = any(role.name == 'instructor' for role in current_user.roles)
        if not is_instructor:
            return {"error": "Instructor role required"}, 403
        
        instructor_id = current_user.id
        
        # Get courses taught by instructor
        courses = Courses.query.filter_by(instructor_id=instructor_id).all()
        course_ids = [course.id for course in courses]
        
        # Get total students across all courses
        total_students = course_enrollment.query.filter(
            course_enrollment.course_id.in_(course_ids)
        ).count()
        
        # Get pending tasks (unaddressed feedback)
        pending_tasks = feedback.query.filter_by(
            instructor_id=instructor_id, 
            status=False
        ).count()
        
        # Calculate average rating from feedback
        avg_rating_query = db.session.query(
            func.avg(feedback.rating)
        ).filter(
            feedback.instructor_id == instructor_id
        ).scalar()
        
        avg_rating = float(avg_rating_query) if avg_rating_query else 0
        
        return {
            "activeCourses": len(courses),
            "totalStudents": total_students,
            "pendingTasks": pending_tasks,
            "averageRating": round(avg_rating, 1),
            "instructorName": current_user.username
        }

