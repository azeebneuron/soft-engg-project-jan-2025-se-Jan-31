# Instructor Dashboard API Documentation

## Overview
This document provides an overview of the backend routes available for the instructor dashboard. These endpoints allow instructors to manage courses, resources, view student enrollments, and access student feedback.

## Base URL
The base URL for accessing the backend routes is:
```
http://127.0.0.1:3000
```

## Authentication
All instructor routes require authentication using a token in the Authorization header:
```
Authorization: Bearer <token>
```

## Routes

### 1. Get Instructor Courses
- **URL:** `/api/instructor/courses`
- **Method:** `GET`
- **Description:** Retrieves all courses where the current user is the instructor.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Response:**
    - `200 OK`: Successfully retrieved courses.
    - `401 Unauthorized`: Missing or invalid authentication token.
- **Response Body:**
    ```json
    [
        {
            "id": 1,
            "name": "Deep Learning",
            "enrolledStudents": 150,
            "resources": [
                {
                    "id": 1,
                    "title": "Introduction to Neural Networks",
                    "link": "https://example.com/intro-nn.pdf"
                }
            ]
        }
    ]
    ```

### 2. Create Course
- **URL:** `/api/instructor/courses`
- **Method:** `POST`
- **Description:** Creates a new course with the current user as instructor.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Request Body:**
    ```json
    {
        "name": "Software Engineering",
        "description": "Introduction to software engineering principles"
    }
    ```
- **Response:**
    - `201 Created`: Course successfully created.
    - `400 Bad Request`: Invalid input data.
    - `401 Unauthorized`: Missing or invalid authentication token.
- **Response Body:**
    ```json
    {
        "message": "Course created successfully",
        "id": 2
    }
    ```

### 3. Get Course Resources
- **URL:** `/api/instructor/courses/<course_id>/resources`
- **Method:** `GET`
- **Description:** Retrieves all resources for a specific course.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Response:**
    - `200 OK`: Successfully retrieved resources.
    - `401 Unauthorized`: Missing or invalid authentication token.
    - `404 Not Found`: Course not found or instructor doesn't have permission.
- **Response Body:**
    ```json
    {
        "course_id": 1,
        "name": "Deep Learning",
        "resources": [
            {
                "id": 1,
                "title": "Introduction to Neural Networks",
                "link": "https://example.com/intro-nn.pdf"
            }
        ]
    }
    ```

### 4. Add Course Resource
- **URL:** `/api/instructor/courses/<course_id>/resources`
- **Method:** `POST`
- **Description:** Adds a new resource to a specific course.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Request Body:**
    ```json
    {
        "title": "Advanced Neural Networks",
        "link": "https://example.com/advanced-nn.pdf"
    }
    ```
- **Response:**
    - `201 Created`: Resource successfully added.
    - `400 Bad Request`: Invalid input data.
    - `401 Unauthorized`: Missing or invalid authentication token.
    - `404 Not Found`: Course not found or instructor doesn't have permission.
- **Response Body:**
    ```json
    {
        "id": 2,
        "title": "Advanced Neural Networks",
        "link": "https://example.com/advanced-nn.pdf"
    }
    ```

### 5. Delete Resource
- **URL:** `/api/instructor/resources/<resource_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific resource.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Response:**
    - `200 OK`: Resource successfully deleted.
    - `401 Unauthorized`: Missing or invalid authentication token.
    - `403 Forbidden`: Instructor doesn't have permission to delete this resource.
    - `404 Not Found`: Resource not found.
- **Response Body:**
    ```json
    {
        "message": "Resource deleted successfully"
    }
    ```

### 6. Get Course Students
- **URL:** `/api/instructor/courses/<course_id>/students`
- **Method:** `GET`
- **Description:** Retrieves all students enrolled in a specific course.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Response:**
    - `200 OK`: Successfully retrieved students.
    - `401 Unauthorized`: Missing or invalid authentication token.
    - `404 Not Found`: Course not found or instructor doesn't have permission.
- **Response Body:**
    ```json
    [
        {
            "id": 1,
            "email": "student1@example.com",
            "username": "student1"
        }
    ]
    ```

### 7. Get Instructor Feedback
- **URL:** `/api/instructor/feedback`
- **Method:** `GET`
- **Description:** Retrieves all feedback submitted to the current instructor.
- **Headers:**
    - `Authorization: Bearer <token>`
- **Response:**
    - `200 OK`: Successfully retrieved feedback.
    - `401 Unauthorized`: Missing or invalid authentication token.
- **Response Body:**
    ```json
    [
        {
            "id": 1,
            "roll": "0001",
            "feedback": "I found the course materials very helpful",
            "email": "student1@example.com",
            "lastUpdated": "3 days ago",
            "course": "Deep Learning",
            "attachment": "feedback_file.pdf",
            "status": "unread",
            "date": "2025-03-01 14:30:22"
        }
    ]
    ```

## Testing
You can test these endpoints using tools like Postman or curl. Here's an example of how to get all instructor courses using curl:

```sh
curl -X GET http://127.0.0.1:3000/api/instructor/courses \
    -H "Authorization: Bearer YOUR_TOKEN"
```

Example of adding a course resource:

```sh
curl -X POST http://127.0.0.1:3000/api/instructor/courses/1/resources \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"title": "Course Slides", "link": "https://example.com/slides.pdf"}'
```

Example of retrieving instructor feedback:

```sh
curl -X GET http://127.0.0.1:3000/api/instructor/feedback \
    -H "Authorization: Bearer YOUR_TOKEN"
```