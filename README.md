# HBnB Evolution - Part 1: Technical Documentation

## 📖 Overview
This repository contains the technical documentation for the **HBnB Evolution** application (Part 1 of the project).  
The documentation provides a detailed blueprint of the application's architecture, business logic, and API interaction flow.

## 📝 Tasks
1. **High-Level Package Diagram** – Shows the 3-layer architecture (Presentation, Business Logic, Persistence) with Facade pattern.
2. **Detailed Class Diagram** – Models core entities: User, Place, Review, Amenity, with attributes, methods, and relationships.
3. **Sequence Diagrams** – Four diagrams showing the flow for:
   - User Registration
   - Place Creation
   - Review Submission
   - Fetching a List of Places
4. **Documentation Compilation** – Combined diagrams and explanatory notes into a cohesive document.

## 📂 Diagrams

### 1. High-Level Package Diagram
![High-Level Package Diagram](diagrams/package_diagram.png)
*Shows the layered architecture and how components interact via the Facade pattern.*

### 2. Detailed Class Diagram
![Detailed Class Diagram](diagrams/class_diagram.png)
*Represents the core business logic entities, their attributes, and relationships.*

### 3. Sequence Diagrams
#### a) User Registration
![User Registration](diagrams/sequence_user_registration.png)
#### b) Place Creation
![Place Creation](diagrams/sequence_place_creation.png)
#### c) Review Submission
![Review Submission](diagrams/sequence_review_submission.png)
#### d) Fetching a List of Places
![Fetching Places](diagrams/sequence_fetch_places.png)

## 🛠 Tools Used
- **draw.io** – For creating UML diagrams.
- **Mermaid.js** – For code-based diagram generation.
- **GitHub** – For version control and documentation hosting.

## 📌 Notes
- All diagrams follow UML notation standards.
- The design is based on the given business rules and requirements.
- This documentation will guide the implementation in later parts of the project.
