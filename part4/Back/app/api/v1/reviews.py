from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade


api = Namespace('reviews', description='Review operations')

facade = HBnBFacade()

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        current_user = get_jwt_identity()
        review_data['user_id'] = current_user['id']

        if (
            'user_id' not in review_data or
            'place_id' not in review_data or
            'rating' not in review_data or
            'text' not in review_data
        ):
            return {'message': 'Missing required fields'}, 400
        
        place = facade.get_place(review_data['place_id'])
        existing_review = facade.get_reviews_by_place(review_data['place_id'])

        if review_data['user_id'] != current_user['id']:
            return {'error': 'Unauthorized action : Should be an user'}, 403
        if place.owner_id == current_user['id']:
            return {'error': 'Unauthorized action: Cannot review your own place'}, 403
        if existing_review:
            return {'error': 'Unauthorized action: Cannot review the same place more than once'}, 403

        try:
            new_review = facade.create_review(review_data)
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400
        
        return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return {
            'reviews': [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id
                    } for review in reviews
                ]
            }, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            review.validate()
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

        return {'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id}, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        current_user = get_jwt_identity()

        if review.user_id != current_user['id']:
            return {'error': 'Unauthorized action: Cannot modify other user\'s review'}, 403

        try:
            review = facade.get_review(review_id)
            review.validate()
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400
        
        if not review:
            return {'error': 'Review not found'}, 404
        if (
            'user_id' not in review_data or
            'place_id' not in review_data or
            'rating' not in review_data or
            'text' not in review_data
        ):
            return {'message': 'Missing required fields'}, 400
        try:
            updated_review = facade.update_review(review_id, review_data)
            updated_review.validate()
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

        return {'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id}, 200
    
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()

        review = facade.get_review(review_id)
        review.validate()
        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user['id']:
            return {'error': 'Unauthorized action: Cannot delete other user\'s review'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place_reviews = facade.get_reviews_by_place(place_id)

        if not place_reviews:
            return {'error': 'Place not found'}, 404
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }for review in place_reviews
                ], 200
