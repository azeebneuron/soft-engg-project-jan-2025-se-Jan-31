# Backend

## Overview
This document provides an overview of the backend services for the project.

## For running locally
- Create a virtual environment 
```bash 
python -m venv .env_name
```
- Activate the Virtual environment
```bash
source env_name/bin/activate
```
- Install all the dependency 
```bash
pip install -r req.txt
```
- Run the following command for thr databse creation
```bash
python3 init_app.py
``` 
- Finally Run the App using 
```bash
python3 app.py
```

## yml files for testing the API endpoint 
- we hae created `openapi.yml` file , it is compatible with swagger editior so you can check each api with the help of the file

## Info about file's and folder structure
**Files**

- app.py — Runs the backend server.

- model.py — Contains all database models.

- config.py — Basic configuration file.

- init_app.py — Initializes the app by creating an instance folder with dummy users and an admin for testing.

**Directories**

routes/

- admin_API/ — Contains important APIs for admin functionalities.

- student_API/ — Contains important APIs for student functionalities.

- Instructor_API/ — Contains APIs for instructor functionalities.

- auth.py — Handles sign-in and sign-up APIs.

- chatbotapi.py — Contains APIs related to the chatbot.
