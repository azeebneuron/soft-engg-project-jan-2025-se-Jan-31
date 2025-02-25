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

from routes.student_API.deadline import DeadlineAPICreate, DeadlineAPIGet
api_handler.add_resource(DeadlineAPICreate, "/student/deadline")
api_handler.add_resource(DeadlineAPIGet, "/student/deadline")



if __name__ == "__main__":
    app.run(debug=True, port=3000)