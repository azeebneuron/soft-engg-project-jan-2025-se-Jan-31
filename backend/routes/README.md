# Backend Routes Documentation

## Overview
This document provides an overview of the backend routes available in the application. Currently, the application supports user signup and signin functionalities.

## Base URL
The base URL for accessing the backend routes is:
```
http://127.0.0.1:3000
```

## Routes

### 1. Signup
- **URL:** `/signup`
- **Method:** `POST`
- **Description:** This route is used for user registration.
- **Request Body:**
    ```json
    {
        "username": "string",
        "password": "string",
        "email": "string"
    }
    ```
- **Response:**
    - `201 Created`: User successfully registered.
    - `400 Bad Request`: Invalid input data.

### 2. Signin
- **URL:** `/signin`
- **Method:** `POST`
- **Description:** This route is used for user authentication.
- **Request Body:**
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```
- **Response:**
    - `200 OK`: User successfully authenticated.
    - `401 Unauthorized`: Invalid username or password.


### 3. Add Deadline
- **URL:** `/student/deadline`
- **Method:** `POST`
- **Description:** This route is used to add a new deadline for a student.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Request Body:**
    ```json
    {
        "course": "string",
        "title": "string",
        "deadline_str": "string in dd-mm-yyyy formate"
    }
    ```
- **Response:**
    - `201 Created`: Deadline successfully added.
    - `400 Bad Request`: Invalid input data.
    - `401 Unauthorized`: Missing or invalid authentication token.

### 4. Get Deadlines
- **URL:** `/student/deadline`
- **Method:** `GET`
- **Description:** This route is used to retrieve all deadlines for a student.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Response:**
    - `200 OK`: Successfully retrieved deadlines.
    - `401 Unauthorized`: Missing or invalid authentication token.
- **Response Body:**
    ```json
    [
        {
            "id": "string",
            "title": "string",
            "description": "string",
            "dueDate": "string"
        }
    ]
    ```

### 5. Deactivate User
- **URL:** `/admin/user/deactivate`
- **Method:** `POST`
- **Description:** This route is used to deactivate a user account.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Request Body:**
    ```json
    {
        "user_id": "string"
    }
    ```
- **Response:**
    - `200 OK`: User successfully deactivated.
    - `400 Bad Request`: Invalid input data.
    - `401 Unauthorized`: Missing or invalid authentication token.

### 6. Activate User
- **URL:** `/admin/user/activate`
- **Method:** `POST`
- **Description:** This route is used to activate a user account.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Request Body:**
    ```json
    {
        "user_id": "string"
    }
    ```
- **Response:**
    - `200 OK`: User successfully activated.
    - `400 Bad Request`: Invalid input data.
    - `401 Unauthorized`: Missing or invalid authentication token.

### 7. List Users
- **URL:** `/admin/user/list`
- **Method:** `GET`
- **Description:** This route is used to retrieve a list of all users.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Response:**
    - `200 OK`: Successfully retrieved user list.
    - `401 Unauthorized`: Missing or invalid authentication token.
- **Response Body:**
    ```json
    [
        {
            "id": "string",
             "username": "string",
            "email": "string",
            "status": "string"
        }
    ]
    ```


### For Feedback use the following command
```sh
➜  ~ curl -X POST http://127.0.0.1:3000/student/feedback \
    -H "Authorization: Token" \
    -H "Content-Type: multipart/form-data" \
    -F "content=This is my feedback" \
    -F "attachment=@/Filepath"
```


## Testing
You can test the signin route using the following URL:
```
http://127.0.0.1:3000/signin
```

## Notes
- Ensure the backend server is running before testing the routes.
- Use appropriate tools like Postman or curl to send HTTP requests to the routes.

For any issues or further assistance, please contact the development team.
