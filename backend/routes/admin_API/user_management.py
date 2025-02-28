from models import db, user_datastore, User, Role, Courses, course_enrollment, course_documents, deadlines
from flask_security import auth_token_required, roles_required, current_user
import datetime
from flask import request, jsonify, make_response
from flask_restful import Resource


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

        return make_response(jsonify({"message": f"User {user.username} has been deactivated"}), 200)

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

        return make_response(jsonify({"message": f"User {user.username} has been activated"}), 200)


class ListUsers(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        # Fetch all users excluding those with the 'admin' role
        users = User.query.filter(~User.roles.any(name='admin')).all()
        user_list = [user.serialize() for user in users]

        return make_response(jsonify(user_list), 200)


