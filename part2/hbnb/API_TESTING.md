
HBnB API – Testing Report
This report documents manual tests (cURL + Swagger UI) for Users, Places, Amenities, Reviews.
 Both successful and failing cases were executed to verify validation rules and status codes.
Environment
Base URL: http://localhost:5000
Swagger UI: http://localhost:5000/api/v1/

1) Users
 Create user (success)

curl -X POST "http://localhost:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{"first_name":"John","last_name":"Doe","email":"john@example.com"}'
Expected: 201 Created
 Actual: ☐ Fill after run
 Notes: —
 Create user (invalid email / empty names)

curl -X POST "http://localhost:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{"first_name":"","last_name":"","email":"invalid"}'
Expected: 400 Bad Request
 Actual: ☐
 Notes: —
 Get all users

curl "http://localhost:5000/api/v1/users/"
Expected: 200 OK + list
 Actual: ☐
 Get user by id

curl "http://localhost:5000/api/v1/users/<user_id>"
Expected: 200 OK (or 404 Not Found if missing)
 Actual: ☐
 Update user

curl -X PUT "http://localhost:5000/api/v1/users/<user_id>" \
-H "Content-Type: application/json" \
-d '{"first_name":"Jane","last_name":"Doe","email":"jane@example.com"}'
Expected: 200 OK
 Actual: ☐
2) Amenities
 Create amenity (success)

curl -X POST "http://localhost:5000/api/v1/amenities/" \
-H "Content-Type: application/json" \
-d '{"name":"WiFi"}'
Expected: 201 Created
 Actual: ☐
 Create amenity (empty name)

curl -X POST "http://localhost:5000/api/v1/amenities/" \
-H "Content-Type: application/json" \
-d '{"name":""}'
Expected: 400 Bad Request
 Actual: ☐
 Get all amenities

curl "http://localhost:5000/api/v1/amenities/"
Expected: 200 OK
 Actual: ☐
 Get amenity by id

curl "http://localhost:5000/api/v1/amenities/<amenity_id>"
Expected: 200 OK (or 404)
 Actual: ☐
 Update amenity

curl -X PUT "http://localhost:5000/api/v1/amenities/<amenity_id>" \
-H "Content-Type: application/json" \
-d '{"name":"Free WiFi"}'
Expected: 200 OK
 Actual: ☐
3) Places
Create a valid user first and keep its id as <owner_id>.
 (Optionally) create an amenity and use its id in amenity_ids.
 Create place (success)

curl -X POST "http://localhost:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 100.0,
  "latitude": 25.0,
  "longitude": 45.0,
  "owner_id": "<owner_id>",
  "amenity_ids": ["<amenity_id>"]
}'
Expected: 201 Created
 Actual: ☐
 Create place (negative price)

curl -X POST "http://localhost:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
  "title": "Bad Place",
  "description": "Wrong price",
  "price": -10,
  "latitude": 25.0,
  "longitude": 45.0,
  "owner_id": "<owner_id>",
  "amenity_ids": []
}'
Expected: 400 Bad Request
 Actual: ☐
 Get all places

curl "http://localhost:5000/api/v1/places/"
Expected: 200 OK
 Actual: ☐
 Get place by id

curl "http://localhost:5000/api/v1/places/<place_id>"
Expected: 200 OK (or 404)
 Actual: ☐
 Update place

curl -X PUT "http://localhost:5000/api/v1/places/<place_id>" \
-H "Content-Type: application/json" \
-d '{
  "title": "Updated Cozy Apartment",
  "description": "Even nicer",
  "price": 120.0,
  "latitude": 25.0,
  "longitude": 45.0
}'
Expected: 200 OK
 Actual: ☐
4) Reviews
Create valid <user_id> and <place_id> first.
 Create review (success)

curl -X POST "http://localhost:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "text": "Great place to stay!",
  "rating": 5,
  "user_id": "<user_id>",
  "place_id": "<place_id>"
}'
Expected: 201 Created
 Actual: ☐
 Create review (empty text)

curl -X POST "http://localhost:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "text": "",
  "rating": 5,
  "user_id": "<user_id>",
  "place_id": "<place_id>"
}'
Expected: 400 Bad Request
 Actual: ☐
 Create review (invalid rating)

curl -X POST "http://localhost:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "text": "Bad rating",
  "rating": 10,
  "user_id": "<user_id>",
  "place_id": "<place_id>"
}'
Expected: 400 Bad Request
 Actual: ☐
 Get all reviews

curl "http://localhost:5000/api/v1/reviews/"
Expected: 200 OK
 Actual: ☐
 Get review by id

curl "http://localhost:5000/api/v1/reviews/<review_id>"
Expected: 200 OK (or 404)
 Actual: ☐
 Get reviews for a place

curl "http://localhost:5000/api/v1/places/<place_id>/reviews"
Expected: 200 OK (or 404 if place missing)
 Actual: ☐
 Update review (text & rating only)

curl -X PUT "http://localhost:5000/api/v1/reviews/<review_id>" \
-H "Content-Type: application/json" \
-d '{
  "text": "Excellent stay!",
  "rating": 4
}'
Expected: 200 OK
 Actual: ☐
 Delete review

curl -X DELETE "http://localhost:5000/api/v1/reviews/<review_id>"
Expected: 200 OK
 Actual: ☐
5) Summary Table
EntityTest caseExpectedActualResultUsersCreate valid user201☐☐UsersCreate invalid user (bad email/empty)400☐☐UsersGet all / Get by id / Update200/404☐☐AmenitiesCreate valid / invalid (empty name)201/400☐☐AmenitiesGet all / Get by id / Update200/404☐☐PlacesCreate valid / invalid (neg. price)201/400☐☐PlacesGet all / Get by id / Update200/404☐☐ReviewsCreate valid / empty text / bad rating201/400☐☐ReviewsGet all / by id / by place200/404☐☐ReviewsUpdate (text/rating) / Delete200☐☐
6) Notes & Issues
Write any discrepancies or bugs found during testing here.
Mention payloads that caused unexpected behavior.
7) Swagger Verification
Verified models and routes appear correctly under:
/api/v1/users, /api/v1/places, /api/v1/amenities, /api/v1/reviews
Example requests and schemas match implementation.
8) How to Run Automated Tests (reference)

# API tests
python tests/test_api.py

# Model/Facade tests
python tests/test_models.py
