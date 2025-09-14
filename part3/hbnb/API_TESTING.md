## HBnB API Testing Guide & Report

This document provides both the instructions for testing the HBnB API endpoints (Tasks 4–6) and the report of expected vs. actual results.

Prerequisites

Make sure the Flask application is running:

cd part2/hbnb
python run.py


The server should start on http://localhost:5000

Install required testing dependencies:

pip install requests

## Testing Methods
1. Automated API Testing Script

Run the comprehensive API test script:

cd part2
python test_api.py


This script tests:

All User endpoints (POST, GET, PUT)

All Amenity endpoints (POST, GET, PUT)

All Place endpoints (POST, GET, PUT)

All Review endpoints (POST, GET, PUT, DELETE)

Validation and error handling

Relationship integrity

 ## Unit Tests

Run the model unit tests:

cd part2
python test_models.py


This tests:

Model validation

Attribute constraints

Relationship handling

Repository integration

3. Manual Testing with cURL
## User Endpoints

Create User

curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}'


Get All Users

curl http://localhost:5000/api/v1/users/


Get User by ID

curl http://localhost:5000/api/v1/users/{user_id}


Update User

curl -X PUT http://localhost:5000/api/v1/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"}'

## Amenity Endpoints

Create Amenity

curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}'


Get All Amenities

curl http://localhost:5000/api/v1/amenities/


Get Amenity by ID

curl http://localhost:5000/api/v1/amenities/{amenity_id}


Update Amenity

curl -X PUT http://localhost:5000/api/v1/amenities/{amenity_id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Free WiFi"}'

## Place Endpoints

Create Place

curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 25.0,
    "longitude": 45.0,
    "owner_id": "{user_id}",
    "amenity_ids": ["{amenity_id}"]
  }'


Get All Places

curl http://localhost:5000/api/v1/places/


Get Place by ID

curl http://localhost:5000/api/v1/places/{place_id}


Update Place

curl -X PUT http://localhost:5000/api/v1/places/{place_id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Cozy Apartment",
    "description": "Even nicer",
    "price": 120.0,
    "latitude": 25.0,
    "longitude": 45.0
  }'

## Review Endpoints

Create Review

curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "{user_id}",
    "place_id": "{place_id}"
  }'


Get All Reviews

curl http://localhost:5000/api/v1/reviews/


Get Review by ID

curl http://localhost:5000/api/v1/reviews/{review_id}


Get Reviews for a Place

curl http://localhost:5000/api/v1/places/{place_id}/reviews


Update Review

curl -X PUT http://localhost:5000/api/v1/reviews/{review_id} \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Excellent place to stay!",
    "rating": 4
  }'


Delete Review

curl -X DELETE http://localhost:5000/api/v1/reviews/{review_id}

## Swagger Documentation

Access the interactive API documentation at:

http://localhost:5000/api/v1/


Provides:

Complete API specification

Interactive testing interface

Request/response examples

Model schemas

Validation Rules
User

first_name: Required, max 50 characters

last_name: Required, max 50 characters

email: Required, valid format, unique

is_admin: Boolean, default False

Place

title: Required, max 100 characters

description: Optional

price: Positive float

latitude: -90 to 90

longitude: -180 to 180

owner_id: Must reference existing user

amenity_ids: Optional list of amenity IDs

Review

text: Required, non-empty

rating: 1–5 integer

user_id: Must reference existing user

place_id: Must reference existing place

Amenity

name: Required, non-empty, max 50 chars

Expected Response Formats

Success

200: Resource retrieved

201: Resource created

Errors

400: Invalid input

404: Not found

500: Server error

## Testing Report

| Entity     | Test Case                              | Expected | Actual | Result |
|------------|----------------------------------------|----------|--------|--------|
| Users      | Create valid user                      | 201      | ☐      | ☐ |
| Users      | Create invalid user (bad email)        | 400      | ☐      | ☐ |
| Users      | Get all / Get by id / Update           | 200/404  | ☐      | ☐ |
| Amenities  | Create valid / invalid amenity         | 201/400  | ☐      | ☐ |
| Amenities  | Get all / Get by id / Update           | 200/404  | ☐      | ☐ |
| Places     | Create valid / invalid place           | 201/400  | ☐      | ☐ |
| Places     | Get all / Get by id / Update           | 200/404  | ☐      | ☐ |
| Reviews    | Create valid / empty / bad rating      | 201/400  | ☐      | ☐ |
| Reviews    | Get all / by id / by place             | 200/404  | ☐      | ☐ |
| Reviews    | Update (text/rating) / Delete          | 200      | ☐      | ☐ |

### Notes
- Replace `{user_id}`, `{place_id}`, `{amenity_id}`, `{review_id}` with actual IDs after creating records.
- Fill in **Actual** and **Result** after running the tests (e.g., `201` / `✅`).

