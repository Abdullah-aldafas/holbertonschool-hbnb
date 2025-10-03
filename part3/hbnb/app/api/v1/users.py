from flask_restx import fields, Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.models.user import User

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=True, description='checking is admin or not', default=False)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(400, 'Email already exists')
    @api.response(200, 'User added successfully')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        user_data = api.payload or {}
        if facade.get_user_by_email(user_data.get('email')):
            return {'error': 'Email already exists'}, 400
        new_user = facade.add_user(user_data)
        return new_user.to_dict(), 201
    
    @api.response(400, 'List is empty')
    @api.response(200, 'List retrieved successfully')
    def get(self):
        users = facade.get_all_users()
        if users:
            data = []
            for user in users:
                data.append(user.to_dict())
            return data, 200
        
        return 'List is empty', 400
        
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(400, 'Invalid input')
    @api.response(200, 'User retrieved successfully')
    def get(self, user_id):
        user: User = facade.get_user(user_id)
        if not user:
            return 'Invalid input', 400
        
        return user.to_dict(), 200  
    
    @api.expect(user_model, validate=True)
    @api.response(400, 'Invalid input')
    @api.response(200, 'User updated successfully')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        user: User = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        # Non-admin can only update self, without email/password
        if (user_id != current_user['id']) and not current_user.get('is_admin'):
            return {'error': 'Unauthorized action'}, 403
        user_data = api.payload or {}
        if not current_user.get('is_admin') and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password'}, 400
        new_user = facade.update_user(user_id, user_data) if hasattr(facade, 'update_user') else facade.update(user_id, user_data)
        return new_user.to_dict() if hasattr(new_user, 'to_dict') else user.to_dict(), 200
    
    @api.response(400, 'Invalid input')
    @api.response(200, 'Deleted successfully')
    def delete(self, user_id):
        current_user = get_jwt_identity()
        if (user_id != current_user['id']) and not current_user.get('is_admin'):
            return {'error': 'Unauthorized action'}, 403
        deleted_user: User = facade.delete_user(user_id) if hasattr(facade, 'delete_user') else facade.delete(user_id)
        if deleted_user or deleted_user is True:
            return {"message": "User successfully deleted"}, 200
        return {"error": "User not found"}, 404
