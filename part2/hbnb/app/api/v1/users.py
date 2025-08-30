#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'is_admin': fields.Boolean(required=False, description='Admin flag', default=False),
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        
        data = api.payload or {}
       
        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400
       
        data['email'] = data['email'].strip().lower()
        user = facade.create_user(data)
        return {
            'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name,
            'email': user.email, 'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat(), 'updated_at': user.updated_at.isoformat(),
        }, 201

    @api.response(200, 'Users retrieved')
    def get(self):
        
        users = facade.list_users()
        return [{
            'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name,
            'email': u.email, 'is_admin': u.is_admin,
            'created_at': u.created_at.isoformat(), 'updated_at': u.updated_at.isoformat(),
        } for u in users], 200


@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        
        u = facade.get_user(user_id)
        if not u:
            return {'error': 'User not found'}, 404
        return {
            'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name,
            'email': u.email, 'is_admin': u.is_admin,
            'created_at': u.created_at.isoformat(), 'updated_at': u.updated_at.isoformat(),
        }, 200

    @api.expect(user_model, validate=False)
    @api.response(200, 'User updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid data')
    def put(self, user_id):
        
        data = api.payload or {} 
        try:
            u = facade.update_user(user_id, data)
            if not u:
                return {'error': 'User not found'}, 404
            return {
                'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name,
                'email': u.email, 'is_admin': u.is_admin,
                'created_at': u.created_at.isoformat(), 'updated_at': u.updated_at.isoformat(),
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
