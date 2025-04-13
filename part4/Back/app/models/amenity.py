from app.models.base_model import BaseModel
from app import db
import uuid

# Table d'association pour la relation Many-to-Many
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    # Relation Many-to-Many avec Place
    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities', lazy=True)

    def validate(self):
        if not self.name:
            raise ValueError("Amenity name must not be empty")
        elif len(self.name) > 50:
            raise ValueError("Amenity name must be <= 50 characters")