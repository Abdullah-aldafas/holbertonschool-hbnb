HBnB – Part 2: Business Logic and API Endpoints

Overview
This part implements the Presentation and Business Logic layers using Flask and Flask-RESTx. It includes the in-memory persistence, a facade to orchestrate business operations, and RESTful endpoints for Users, Amenities, Places, and Reviews.

Project Structure
```
hbnb/
├── app/
│   ├── __init__.py                # Flask app factory + namespace registry
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py           # User endpoints
│   │       ├── places.py          # Place endpoints
│   │       ├── reviews.py         # Review endpoints
│   │       └── amenities.py       # Amenity endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py          # BaseModel: id, created_at, updated_at
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   ├── __init__.py            # facade singleton
│   │   └── facade.py              # HBnBFacade (business coordination)
│   └── persistence/
│       ├── __init__.py
│       └── repository.py          # InMemoryRepository
├── run.py
├── config.py
├── requirements.txt
└── README.md (this file)
```

Key Design Notes
- BaseModel centralizes id (UUID), created_at, updated_at and update logic.
- Models store relationships by IDs for consistency across layers:
  - Place.owner_id: str, Place.amenities: list[str]
  - Review.user_id: str, Review.place_id: str
- HBnBFacade validates foreign keys and orchestrates create/update flows.
- InMemoryRepository provides simple storage with a consistent interface.

Setup
1) Install dependencies
```
pip install -r requirements.txt
```

2) Run the app
```
python run.py
```

3) Swagger (Flask-RESTx UI)
Open: http://127.0.0.1:5000/api/v1/

Endpoints (v1)
- Users: /api/v1/users
  - POST /           Create user (201)
  - GET /            List users (200)
  - GET /<id>        Get user by id (404 if not found)
  - PUT /<id>        Update user (200 / 404 / 400)

- Amenities: /api/v1/amenities
  - POST /           Create amenity (201)
  - GET /            List amenities (200)
  - GET /<id>        Get amenity (404 if not found)
  - PUT /<id>        Update amenity (200 / 404 / 400)

- Places: /api/v1/places
  - POST /           Create place (payload includes owner_id, amenities: [ids]) (201)
  - GET /            List places with expanded owner and amenities (200)
  - GET /<id>        Get place with expanded owner and amenities (404 if not found)
  - PUT /<id>        Update place (200 / 404 / 400)

- Reviews: /api/v1/reviews
  - POST /           Create review (requires user_id, place_id, rating 1-5) (201)
  - GET /            List reviews (200)
  - GET /<id>        Get review (404 if not found)
  - PUT /<id>        Update review (200 / 404 / 400)
  - DELETE /<id>     Delete review (200 / 404)
  - GET /places/<place_id>/reviews   List reviews for a place (404 if place not found)

Validation Summary
- User: first_name/last_name required (≤50), valid email, unique email (facade-level).
- Place: title required (≤100), price > 0, latitude in [-90, 90], longitude in [-180, 180], owner exists, amenities IDs exist.
- Review: text required, rating 1..5, user/place exist.
- Amenity: name required (≤50).

Quick cURL Samples
Create user
```
curl -X POST http://127.0.0.1:5000/api/v1/users/ -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com"}'
```

Create place
```
curl -X POST http://127.0.0.1:5000/api/v1/places/ -H "Content-Type: application/json" \
  -d '{"title":"Villa","description":"Nice","price":120,"latitude":25,"longitude":45,"owner_id":"<USER_ID>","amenities":[]}'
```

Create review
```
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ -H "Content-Type: application/json" \
  -d '{"text":"Great","rating":5,"user_id":"<USER_ID>","place_id":"<PLACE_ID>"}'
```

Testing
- Run built-in tests
```
python -m unittest part2/hbnb/test_models.py -v
python -m unittest part2/hbnb/test_api.py -v
```
- Use Swagger UI as a reference and for manual testing at /api/v1/

Notes
- DELETE is only implemented for Reviews in Part 2.
- Authentication/authorization (JWT, RBAC) is deferred to Part 3.