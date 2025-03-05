from flask import request
from flask_restful import Resource
from flask_security import auth_token_required, roles_required, current_user

class Chatbot(Resource):
    @auth_token_required
    def post(self):
        data = request.get_json()
        question = data.get("question", "")
        
        if not question:
            return {"error": "Question is required"}, 400
        
        # Simple hardcoded response
        response = f"You asked: '{question}'. Here is a simple reply!"
        return {"answer": response}
