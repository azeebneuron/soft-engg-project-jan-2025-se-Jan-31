from flask import request
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_security import Security
from models import db, user_datastore

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.localDev")

    db.init_app(app)
    
    security = Security(app, user_datastore)

    CORS(app)

    api = Api(app)

    return app, api

app, api_handler = create_app()



@app.route("/hello_world")
def hello_world():
    return "Hello World!"

# Import routes

from routes.auth import Signup, Signin
api_handler.add_resource(Signup, "/signup")
api_handler.add_resource(Signin, "/signin")

from routes.student_API.deadline import DeadlineAPICreate, DeadlineAPIGet, DeadlineAPIDelete, DeadlineAPIUpdate
api_handler.add_resource(DeadlineAPICreate, "/student/deadline")
api_handler.add_resource(DeadlineAPIGet, "/student/deadline")
api_handler.add_resource(DeadlineAPIDelete, "/student/deadline")
api_handler.add_resource(DeadlineAPIUpdate, "/student/deadline")

from routes.admin_API.user_management import DeactivateUser, ActivateUser, ListUsers
api_handler.add_resource(DeactivateUser, "/admin/user/deactivate")
api_handler.add_resource(ActivateUser, "/admin/user/activate")
api_handler.add_resource(ListUsers, "/admin/user/list")


from routes.student_API.feedback import FeedbackAPI
api_handler.add_resource(FeedbackAPI, "/student/feedback")



if __name__ == "__main__":
    app.run(debug=True, port=3000)