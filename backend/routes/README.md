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

## Testing
You can test the signin route using the following URL:
```
http://127.0.0.1:3000/signin
```

## Notes
- Ensure the backend server is running before testing the routes.
- Use appropriate tools like Postman or curl to send HTTP requests to the routes.

For any issues or further assistance, please contact the development team.
