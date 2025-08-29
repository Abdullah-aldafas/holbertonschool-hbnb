from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

owner_ref = api.model('OwnerRef', {
    'id': fields.String(required=True, description='Owner user id')
})

amenity_ref = api.model('AmenityRef', {
    'id': fields.String(required=True, description='Amenity id')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=False, description='Description'),
    'price': fields.Float(required=True, description='Price'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner user id'),
    'amenity_ids': fields.List(fields.String, required=False, description='List of amenity ids')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        data = api.payload or {}
        try:
            place = facade.create_place(data)
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': place.owner.id,
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email,
                },
                'amenities': [
                    {'id': a.id, 'name': a.name} for a in (place.amenities or [])
                ],
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat(),
            }, 201
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'price': p.price,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'owner': {
                'id': p.owner.id,
                'first_name': p.owner.first_name,
                'last_name': p.owner.last_name,
                'email': p.owner.email,
            },
            'amenities': [
                {'id': a.id, 'name': a.name} for a in (p.amenities or [])
            ],
            'created_at': p.created_at.isoformat(),
            'updated_at': p.updated_at.isoformat(),
        } for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        p = facade.get_place(place_id)
        if not p:
            return {'error': 'Place not found'}, 404
        return {
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'price': p.price,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'owner': {
                'id': p.owner.id,
                'first_name': p.owner.first_name,
                'last_name': p.owner.last_name,
                'email': p.owner.email,
            },
            'amenities': [
                {'id': a.id, 'name': a.name} for a in (p.amenities or [])
            ],
            'created_at': p.created_at.i
