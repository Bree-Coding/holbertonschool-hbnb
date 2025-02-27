from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        if not place_data:
            return {'message': 'Invalid input data'}, 400
        if not place_data['title']:
            return {'message': 'Title is required'}, 400
        if not place_data['price']:
            return {'message': 'Price is required'}, 400
        if not place_data['latitude']:
            return {'message': 'Latitude is required'}, 400
        if not place_data['longitude']:
            return {'message': 'Longitude is required'}, 400
        if not place_data['owner_id']:
            return {'message': 'Owner ID is required'}, 400
        if not place_data['amenities']:
            return {'message': 'Amenities are required'}, 400

        new_place = facade.create_place(place_data)
        return {
                    "id": new_place.id,
                    "title": new_place.title,
                    "description": new_place.description,
                    "price": new_place.price,
                    "latitude": new_place.latitude,
                    "longitude": new_place.longitude,
                    "owner_id": new_place.owner_id,
                    "amenities": new_place.amenities
                }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return {'places': [{'id': place.id,
                            'title': place.title,
                            'description': place.description,
                            'price': place.price,
                            'latitude': place.latitude,
                            'longitude': place.longitude,
                            'owner_id': place.owner_id,
                            'amenities': [{'id': amenity.id,
                                        'name': amenity.name
                                        } for amenity in place.amenities],
                            } for place in places]}, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Placeholder for the logic to retrieve a place by ID, including associated owner and amenities
        place_data = facade.get_place(place_id)

        if not place_data:
            return {'message': 'Place not found'}, 404
        return {
                    "id": place_data.id,
                    "title": place_data.title,
                    "description": place_data.description,
                    "price": place_data.price,
                    "latitude": place_data.latitude,
                    "longitude": place_data.longitude,
                    "owner_id": place_data.owner_id,
                    "amenities": place_data.amenities
                }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)

        if not updated_place:
            return {'message': 'Place not found'}, 404
        return {
                    "id": updated_place.id,
                    "title": updated_place.title,
                    "description": updated_place.description,
                    "price": updated_place.price,
                    "latitude": updated_place.latitude,
                    "longitude": updated_place.longitude,
                    "owner_id": updated_place.owner_id,
                    "amenities": updated_place.amenities
                }, 200