from app.models.base_model import BaseModel
from app import db
from sqlalchemy import ForeignKey
import uuid

class Review(BaseModel):

    __tablename__ = 'reviews'

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=True)
    place_id = db.Column(db.String(36), ForeignKey('places.id'), nullable=False)  # Clé étrangère vers Place
    user_id = db.Column(db.String(36), ForeignKey('users.id'), nullable=False)  # Clé étrangère vers User
    user = db.relationship("User", back_populates="reviews")
    place = db.relationship("Place", back_populates="reviews")

   
    @property
    def text(self):
        return self.comment

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError('comment must be a non-empty string')
        self.comment = value


    def validate(self):
        if self.rating is None or not isinstance(self.rating, int):
            raise TypeError('rating must be an integer')
        if self.rating < 0 or self.rating > 5:
            raise ValueError('rating must be between 0 and 5')

        if self.text == "" or not isinstance(self.text, str):
            raise TypeError('text must be a non-empty string')

        if self.user_id == "" or not isinstance(self.user_id, str):
            raise TypeError('user_id must be a non-empty string')

        if self.place_id == "" or not isinstance(self.place_id, str):

            raise TypeError('place_id must be a non-empty string')
