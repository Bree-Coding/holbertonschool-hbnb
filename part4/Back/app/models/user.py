from .base_model import BaseModel
import re
from app import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=True) # TODO : default=False
    places = db.relationship('Place', back_populates='user', lazy=True)  # One-to-Many avec Place
    reviews = db.relationship('Review', back_populates='user', lazy=True)  # One-to-Many avec Review


    def hash_password(self, password):
        """Hache le mot de passe avant de le stocker."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe en clair correspond au hachage."""
        if not self.password:
            raise ValueError('Password is not set')
        if not password:
            raise ValueError('Password is empty')
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire sans inclure le mot de passe."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
        }

    def validate(self):
        if self.first_name is None or not isinstance(self.first_name, str):
            raise TypeError('first_name must be a non-empty string')
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError('first_name must be non-empty and 50 characters or less')

        if self.last_name is None or not isinstance(self.last_name, str):
            raise TypeError('last_name must be a non-empty string')
        if not self.last_name or len(self.last_name) > 50:
            raise ValueError('last_name must be non-empty and 50 characters or less')

        if self.email is None or not isinstance(self.email, str):
            raise TypeError('email must be a non-empty string')
        if not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            raise ValueError('please enter a valid email address')

        if not isinstance(self.is_admin, bool):
            raise TypeError('user must be an admin')