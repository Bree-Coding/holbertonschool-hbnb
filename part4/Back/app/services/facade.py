from werkzeug.security import generate_password_hash, check_password_hash
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from app import bcrypt, db

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        """Create a new user with hashed password"""
        # Hash the password before saving
        user = User(**user_data)
        
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_user_by_id(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Retrieve all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's details"""
        user = self.user_repo.get(user_id)
        if user:
            user_data['password'] = bcrypt.generate_password_hash(user_data['password'])
            self.user_repo.update(user_id, user_data)
            return user
        return None

    # Place-related methods
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if place:
            for key, value in place_data.items():
                if hasattr(place, key):
                    setattr(place, key, value)
            self.place_repo.update(place_id, vars(place))
        return place

    # Amenity-related methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            for key, value in amenity_data.items():
                if hasattr(amenity, key):
                    setattr(amenity, key, value)
            self.amenity_repo.update(amenity_id, vars(amenity))
        return amenity

    # Review-related methods
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [
            review for review in self.review_repo.get_all()
            if review.place_id == place_id
        ]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        for key, value in review_data.items():
            if hasattr(review, key):
                setattr(review, key, value)

        self.review_repo.update(review_id, vars(review))
        return review
    
    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
        return {'message': 'Review deleted successfully'}, 200
