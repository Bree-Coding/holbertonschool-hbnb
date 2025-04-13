# Part 3: Enhanced Backend with Authentication and Database Integration 🚀

Welcome to Part 3 of the HBnB Project. In this part, you will extend the backend by introducing user authentication, authorization, and database integration using SQLAlchemy and SQLite for development, and MySQL for production.

## Objectives 🎯

- **🔐 Authentication and Authorization**: Implement JWT-based user authentication and role-based access control.
- **🗄️ Database Integration**: Replace in-memory storage with SQLite for development and prepare for MySQL in production.
- **🛠️ CRUD Operations**: Refactor CRUD operations to interact with a persistent database.
- **📊 Database Design**: Design the database schema using mermaid.js.
- **✅ Data Validation**: Ensure data validation and constraints in the models.

## Learning Objectives 📚

By the end of this part, you will:

- 🔑 Implement JWT authentication and manage user sessions.
- 🛡️ Enforce role-based access control.
- 🗃️ Replace in-memory repositories with SQLite using SQLAlchemy and configure MySQL for production.
- 🖼️ Design and visualize a relational database schema using mermaid.js.
- 🔒 Ensure the backend is secure, scalable, and reliable.

## Project Context 🏗️

In previous parts, you worked with in-memory storage. In Part 3, you’ll transition to SQLite for development and prepare for MySQL in production. You’ll also introduce JWT-based authentication and role-based access control.

## Resources 📖

- [🔐 JWT Authentication: Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/en/stable/)
- [🗄️ SQLAlchemy ORM: SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/14/)
- [🗃️ SQLite: SQLite Documentation](https://www.sqlite.org/docs.html)
- [🌐 Flask Documentation: Flask Official Documentation](https://flask.palletsprojects.com/en/2.0.x/)
- [📊 Mermaid.js: Mermaid.js Documentation](https://mermaid-js.github.io/mermaid/#/)

## Structure 🗂️

1. **🔒 Modify User Model**: Store passwords securely using bcrypt2.
2. **🔑 Implement JWT Authentication**: Secure the API using JWT tokens.
3. **🛡️ Implement Authorization**: Restrict actions based on user roles.
4. **🗃️ SQLite Integration**: Transition to SQLite for development.
5. **🗄️ Map Entities**: Use SQLAlchemy to map entities and define relationships.
6. **🗄️ Prepare for MySQL**: Configure MySQL for production.
7. **📊 Database Design**: Create ER diagrams using mermaid.js.

By the end of Part 3, you will have a secure, scalable backend with persistent data storage and role-based access control.
