## Overview
This document provides an overview of the test function for admin_API routes available in the application. 

## How to Run
To run the admin_test.py file move it to backend folder first 
-> run init_app.py to initialize the db
-> run the backend server(app.py), once the server is active 
-> run pytest admin_test.py -s

## Coverage
The tests cover the following key scenarios:
Valid requests: Ensures the API correctly activates/deactivates users and returns the expected success messages.
Invalid input handling: Checks if the API returns appropriate errors when required data is missing or incorrect.
Authentication & Authorization: Verifies that only admins can perform restricted actions and unauthorized users are denied access.

## Conclusion
All 12 tests passed successfully, confirming that the User Management API correctly enforces authentication, authorization, and input validation.

