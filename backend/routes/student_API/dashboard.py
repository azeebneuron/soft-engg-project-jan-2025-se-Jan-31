from models import db, User, Role, Courses, course_enrollment, course_documents, deadlines, feedback
from flask_security import auth_token_required, roles_required, current_user
from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime, timedelta

class DashboardStatsAPI(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        user_id = current_user.id
        
        # Get student name
        student = User.query.get(user_id)
        student_name = student.username if student.username else student.email
        
        # Get upcoming deadlines
        upcoming_deadlines_data = deadlines.query.filter_by(user_id=user_id).all()
        upcoming_deadlines = []
        
        for deadline in upcoming_deadlines_data:
            days_left = (deadline.deadline - datetime.now()).days
            if days_left >= 0:  # Only include future deadlines
                upcoming_deadlines.append({
                    'id': deadline.id,
                    'title': deadline.title,
                    'course': deadline.course,
                    'daysLeft': days_left
                })
        
        # Sort by days left (closest deadlines first)
        upcoming_deadlines = sorted(upcoming_deadlines, key=lambda x: x['daysLeft'])[:4]
        
        # Get course progress
        enrollments = course_enrollment.query.filter_by(user_id=user_id).all()
        courses_data = []
        
        # Calculate total course progress (would normally be based on completed modules/assignments)
        # For demonstration, generating random progress values
        import random
        for enrollment in enrollments:
            course = Courses.query.get(enrollment.course_id)
            if course:
                courses_data.append({
                    'id': course.id,
                    'name': course.name,
                    'progress': random.randint(50, 95)  # Simulated progress
                })
        
        # Get recent activities (placeholder - would be based on actual user activity)
        # In a real app, you'd have a separate user_activity table
        recent_activities = [
            {
                'id': 1, 
                'type': 'submission', 
                'icon': '📝', 
                'title': 'Submitted Assignment 2', 
                'timestamp': (datetime.now() - timedelta(hours=2)).strftime('%d-%m-%Y %H:%M')
            },
            {
                'id': 2, 
                'type': 'quiz', 
                'icon': '✍️', 
                'title': 'Completed Quiz 3', 
                'timestamp': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y %H:%M')
            },
            {
                'id': 3, 
                'type': 'study', 
                'icon': '📚', 
                'title': 'Study Session: 2 hours', 
                'timestamp': (datetime.now() - timedelta(days=2)).strftime('%d-%m-%Y %H:%M')
            }
        ]
        
        # Get study stats (placeholder - would be based on actual tracked study time)
        study_stats = {
            'today_hours': '2h 45m',
            'weekly_goal_percentage': 75
        }
        
        # Calculate GPA (placeholder - would be based on actual grades)
        gpa_data = {
            'current': 3.85,
            'change': 0.1,
            'trend': 'positive'  # 'positive', 'negative', or 'neutral'
        }
        
        # Study streak (placeholder - would be based on actual daily logins/activity)
        streak_data = {
            'days': 5,
            'message': 'Keep it up!'
        }
        
        return make_response(jsonify({
            'studentName': student_name,
            'gpa': gpa_data,
            'upcomingDeadlines': upcoming_deadlines,
            'courses': courses_data,
            'recentActivities': recent_activities,
            'studyStats': study_stats,
            'streak': streak_data
        }), 200)

class QuickLinksAPI(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        # This would typically be fetched from a database
        # For now, returning a static list
        quick_links = [
            {'id': 1, 'icon': '📚', 'label': 'Library', 'url': '/library'},
            {'id': 2, 'icon': '📝', 'label': 'Notes', 'url': '/notes'},
            {'id': 3, 'icon': '📅', 'label': 'Calendar', 'url': '/calendar'},
            {'id': 4, 'icon': '📊', 'label': 'Grades', 'url': '/grades'},
            {'id': 5, 'icon': '💬', 'label': 'Forums', 'url': '/forums'},
            {'id': 6, 'icon': '📧', 'label': 'Messages', 'url': '/messages'}
        ]
        
        return make_response(jsonify({'quickLinks': quick_links}), 200)