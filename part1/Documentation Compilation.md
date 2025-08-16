HBnB Evolution – Part 1: Technical Documentation
1. Introduction
This document presents the comprehensive technical documentation for HBnB Evolution, a simplified version of an AirBnB-like application. The purpose of this document is to serve as a blueprint for the system’s architecture, business logic, and interaction flows, ensuring a clear reference for the upcoming implementation phases.

Scope of the Project:
The HBnB Evolution application allows users to:
- Register and manage user profiles.
- Create and manage places.
- Submit and view reviews for places.
- Manage a list of amenities associated with places.

The document consolidates:
- High-Level Package Diagram.
- Detailed Class Diagram for the Business Logic Layer.
- Sequence Diagrams for key API calls.
2. High-Level Architecture
2.1 Diagram
![High Level Package Diagram](High-Level%20Package%20Diagram.jpg)

2.2 Description
The HBnB application follows a three-layered architecture:
1. Presentation Layer: Handles all user interactions via services and API endpoints.
2. Business Logic Layer: Contains the core models (User, Place, Review, Amenity) and implements application logic.
3. Persistence Layer: Responsible for storing and retrieving data from the database.

Facade Pattern Implementation:
The Facade Pattern is applied between the Presentation Layer and Business Logic Layer to simplify communication, provide a unified interface, and hide the complexity of internal operations.
3. Business Logic Layer


3.1 Diagram
![Class Diagram](Class%20Diagram.jpg)

3.2 Description
The Business Logic Layer consists of the following core entities:

User:
- Attributes: id, first_name, last_name, email, password, is_admin, created_at, updated_at
- Methods: register(), update_profile(), delete_account()

Place:
- Attributes: id, title, description, price, latitude, longitude, owner_id, created_at, updated_at
- Methods: create(), update(), delete(), list_places()

Review:
- Attributes: id, place_id, user_id, rating, comment, created_at, updated_at
- Methods: submit_review(), update_review(), delete_review()

Amenity:
- Attributes: id, name, description, created_at, updated_at
- Methods: create(), update(), delete()

Relationships:
- A User can own multiple Places.
- A Place can have multiple Reviews.
- A Place can have multiple Amenities (Many-to-Many relationship).
4. API Interaction Flow
4.1 User Registration
![User Registration](https://i.postimg.cc/L8QkfMCX/User-Registration.png)
User sends registration request via API. API delegates request to the Business Logic Layer for validation and processing. Data is persisted in the database, and a success response is returned.
4.2 Place Creation
![Place Creation](https://i.postimg.cc/mZ3Qj9XK/Place-Creation.png)
User submits place details via API. Business Logic validates ownership and input data. Place is saved in the database and confirmation is sent to the client.
4.3 Review Submission
![Review Submission](https://i.postimg.cc/wMkLBKR9/Review-Submission.png)
User submits review for a place via API. Business Logic checks if the user visited the place. Review is stored in the database, and acknowledgment is sent.
4.4 Fetching a List of Places
![Fetching a List of Places](https://i.postimg.cc/XJSCcNwV/Fetching-a-List-of-Places.png)
User requests a list of available places. Business Logic fetches filtered data from the database. API returns the list in the requested format.
5. Conclusion
This technical documentation provides a clear, structured, and detailed representation of HBnB Evolution’s design. By following this blueprint, the development process will be streamlined, ensuring that the system meets its intended functionality, maintains scalability, and adheres to best practices in software architecture.
