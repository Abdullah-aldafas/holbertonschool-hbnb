from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = api.payload or {}
        try:
            amenity = facade.create_amenity(data)
            return {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at.isoformat(),
                'updated_at': amenity.updated_at.isoformat(),
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{
            'id': a.id,
            'name': a.name,
            'created_at': a.created_at.isoformat(),
            'updated_at': a.updated_at.isoformat(),
        } for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        a = facade.get_amenity(amenity_id)
        if not a:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': a.id,
            'name': a.name,
            'created_at': a.created_at.isoformat(),
            'updated_at': a.updated_at.isoformat(),
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = request.get_json() or {}
        try:
            a = facade.update_amenity(amenity_id, data)
            if not a:
                return {'error': 'Amenity not found'}, 404
            return { 'message': 'Amenity updated successfully' }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
