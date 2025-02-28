from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

facade = HBnBFacade()

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data_amenities = api.payload
        if not data_amenities:
            return {'message': 'Invalid input data'}, 400

        new_amenities = facade.create_amenity(data_amenities)
        return {'id': new_amenities.id, 'name': new_amenities.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return {'amenities': [{'id': amenity.id,
                               'name': amenity.name}]
                for amenity in amenities
                }, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenities_data = facade.get_amenity(amenity_id)
        if not amenities_data:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenities_data.id, 'name': amenities_data.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload

        if not amenity_data:
            return {'message': 'Invalid input data'}, 400

        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'message': 'Amenity not found'}, 404

        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200
