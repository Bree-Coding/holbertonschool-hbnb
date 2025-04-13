# 📘 HBNB Projet Part 2 - Documentation

## 📚 Introduction

This document provides an overview of the **database schema** for the HBnB project, highlighting the key entities, their attributes, and the relationships between them. The schema is designed to support the core functionalities of the platform, including user management, place listings, reviews, and amenities.

---

## 📊 Entity-Relationship Diagram (ERD)

The following diagram illustrates the structure of the database schema, including the entities and their relationships:

mermaid

Copy

erDiagram
    USERS {
        string id
        string first_name
        string last_name
        string email
        string password
        bool is_admin
    }

    PLACES {
        string id
        string title
        text description
        decimal price
        float latitude
        float longitude
        string user_id
    }

    REVIEWS {
        string id
        text text
        int rating
        string user_id
        string place_id
    }

    AMENITIES {
        string id
        string name
    }

    PLACES_AMENITIES {
        string place_id
        string amenity_id
    }

    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
    PLACES }o--o{ AMENITIES : "has"
    PLACES_AMENITIES }o--|| PLACES : "references"
    PLACES_AMENITIES }o--|| AMENITIES : "references"

---

## 🧩 Entities

### 👤 **USERS**

**Role**: Represents a user of the platform.  
**Key Attributes**:

- **id** : Unique identifier for the user.
    
- **first_name** : First name of the user.
    
- **last_name** : Last name of the user.
    
- **email** : Email address of the user.
    
- **password** : Hashed password for authentication.
    
- **is_admin** : Indicates whether the user has admin privileges.
    

**Relationships**:

- A user can **own multiple places** (One-to-Many).
    
- A user can **write multiple reviews** (One-to-Many).
    

---

### 🏠 **PLACES**

**Role**: Represents a lodging or property listed on the platform.  
**Key Attributes**:

- **id** : Unique identifier for the place.
    
- **title** : Title of the place.
    
- **description** : Detailed description of the place.
    
- **price** : Price per night for the place.
    
- **latitude** : Geographic latitude of the place.
    
- **longitude** : Geographic longitude of the place.
    
- **user_id** : Foreign key referencing the user who owns the place.
    

**Relationships**:

- A place **belongs to one user** (Many-to-One).
    
- A place can **have multiple reviews** (One-to-Many).
    
- A place can **have multiple amenities** (Many-to-Many via `PLACES_AMENITIES`).
    

---

### ⭐ **REVIEWS**

**Role**: Represents a review written by a user for a place.  
**Key Attributes**:

- **id** : Unique identifier for the review.
    
- **text** : Text content of the review.
    
- **rating** : Rating given by the user (e.g., 1 to 5).
    
- **user_id** : Foreign key referencing the user who wrote the review.
    
- **place_id** : Foreign key referencing the place being reviewed.
    

**Relationships**:

- A review is **written by one user** (Many-to-One).
    
- A review is **associated with one place** (Many-to-One).
    

---

### 🛠️ **AMENITIES**

**Role**: Represents an amenity available in a place.  
**Key Attributes**:

- **id** : Unique identifier for the amenity.
    
- **name** : Name of the amenity (e.g., "Wi-Fi", "Pool").
    

**Relationships**:

- An amenity can be **associated with multiple places** (Many-to-Many via `PLACES_AMENITIES`).
    

---

### 🔗 **PLACES_AMENITIES**

**Role**: Represents the many-to-many relationship between places and amenities.  
**Key Attributes**:

- **place_id** : Foreign key referencing a place.
    
- **amenity_id** : Foreign key referencing an amenity.
    

**Relationships**:

- A row in this table **links one place to one amenity**.
    

---

## 🔑 Key Relationships

1. **USERS ||--o{ PLACES** : A user can own multiple places.
    
2. **USERS ||--o{ REVIEWS** : A user can write multiple reviews.
    
3. **PLACES ||--o{ REVIEWS** : A place can have multiple reviews.
    
4. **PLACES }o--o{ AMENITIES** : A place can have multiple amenities, and an amenity can be associated with multiple places.
    
5. **PLACES_AMENITIES }o--|| PLACES** : The `PLACES_AMENITIES` table references a place.
    
6. **PLACES_AMENITIES }o--|| AMENITIES** : The `PLACES_AMENITIES` table references an amenity.
    

---

## 📝 Design Decisions

### **Structure**

- Each entity is designed with a **unique identifier** (`id`) to ensure data integrity.
    
- **Foreign keys** are used to establish relationships between entities (e.g., `user_id` in `PLACES`).
    

### **Relationships**

- **One-to-Many** relationships (e.g., User → Places) are implemented using foreign keys.
    
- **Many-to-Many** relationships (e.g., Places ↔ Amenities) are implemented using a **join table** (`PLACES_AMENITIES`).
    

### **Extensibility**

- The schema is designed to be **scalable**. New entities or relationships can be added without disrupting existing functionality.
    
- **CRUD operations** (Create, Read, Update, Delete) are supported for all entities.
    

---

## 📜 Conclusion

This document provides a detailed overview of the **database schema** for the HBnB project. The schema is designed to support the core functionalities of the platform, including user management, place listings, reviews, and amenities. By adhering to these design principles, the HBnB project aims to deliver a **robust and scalable platform** for managing users, places, reviews, and amenities.