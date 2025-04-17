from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import login_user, verify_password, current_user, hash_password
from models import db, user_datastore, User


# API for Register
class Signup(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        username = data.get("username")

        # Input validation
        if not email:
            return make_response(jsonify({"error": "Email is required"}), 400)
        if not password:
            return make_response(jsonify({"error": "Password is required"}), 400)
        if not username:
            return make_response(jsonify({"error": "Username is required"}), 400)
        if user_datastore.find_user(email=email):
            return make_response(jsonify({"error": "Email is already registered"}), 400)

    
        hashed_password = hash_password(password)

        user = user_datastore.create_user(email=email, password=hashed_password, username=username)

        user_datastore.add_role_to_user(user, "student")
        db.session.commit()

        return make_response(jsonify({"message": "User created successfully"}), 201)


# API for Login
class Signin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email:
            return make_response(jsonify({"error": "Email is required"}), 400)
        if not password:
            return make_response(jsonify({"error": "Password is required"}), 400)

        user = user_datastore.find_user(email=email)
        if not user or not verify_password(password, user.password):
            return make_response(jsonify({"error": "Invalid email or password"}), 401)

        if not user.active:
            return make_response(jsonify({"error": "Account is inactive. Please contact support."}), 403)

        token = user.get_auth_token()  # Assuming Flask-Security is set up with token auth
        login_user(user)

        # Role determination
        role = "student"
        if "admin" in [role.name for role in user.roles]:
            role = "admin"
        elif "instructor" in [role.name for role in user.roles]:
            role = "instructor"
        elif "ta" in [role.name for role in user.roles]:
            role = "ta"

        return make_response(jsonify({
            "message": f"{role.capitalize()} login successful",
            "token": token,
            "role": role
        }), 200)
