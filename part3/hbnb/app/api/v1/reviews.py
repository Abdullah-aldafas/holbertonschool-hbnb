from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            data = api.payload or {}
            
            print(f"Received review data: {data}")
            print(f"Current user: {current_user}")
            
            # Validate required fields
            if not data.get('place_id'):
                return {'error': 'place_id is required'}, 400
            if not data.get('text') or data.get('text').strip() == '':
                return {'error': 'text is required'}, 400
            if not data.get('rating') or not isinstance(data.get('rating'), int):
                return {'error': 'rating is required and must be a number'}, 400
                
            data['user_id'] = current_user['id']
            place_id = data.get('place_id')
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Invalid place'}, 400
            if place.owner_id == current_user['id']:
                return {'error': 'You cannot review your own place.'}, 400
            existing = [r for r in facade.get_all_reviews() if r.place_id == place_id and r.user_id == current_user['id']]
            if existing:
                return {'error': 'You have already reviewed this place.'}, 400
            if data.get('rating') < 1 or data.get('rating') > 5:
                return {'error': 'Invalid rating'}, 400
            
            print(f"Creating review with data: {data}")
            new_review = facade.add_review(data)
            print(f"Review created successfully: {new_review}")
            return new_review.to_dict(), 201
        except Exception as e:
            print(f"Error in review creation: {e}")
            import traceback
            traceback.print_exc()
            return {'error': f'Failed to create review: {str(e)}'}, 400


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        reviews = facade.get_all_reviews()
        if reviews:
            data = []
            for review in reviews:
                data.append(review.to_dict())
            return data, 200
        return {'error': 'List is empty'}, 400

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if review:
            return review.to_dict()
        return {'error': 'Invalid input'}, 404

    @api.expect(review_model, validate=False)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Invalid review id'}, 400
        if (review.user_id != current_user['id']) and not current_user.get('is_admin'):
            return {'error': 'Unauthorized action'}, 403
        review_data = api.payload or {}
        new_review = facade.update_review(review_id, review_data)
        return new_review.to_dict(), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Invalid id'}, 400
        if (review.user_id != current_user['id']) and not current_user.get('is_admin'):
            return {'error': 'Unauthorized action'}, 403
        deleted_review = facade.delete_review(review_id)
        return deleted_review.to_dict(), 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        reviews = facade.get_all_reviews()
        reviews_data = [review for review in reviews if review.place_id == place_id]
        
        data = []
        for review in reviews_data:
            data.append(review.to_dict())
        return data, 200
    
@api.route('/users/<user_id>/reviews')
class UserReviewList(Resource):
    @api.response(200, 'List of reviews for the user retrieved successfully')
    @api.response(404, 'user not found')
    def get(self, user_id):
        reviews = facade.get_all_reviews()

        reviews_data = [review for review in reviews if review.user_id == user_id]
        if reviews_data:
            data = []
            for review in reviews_data:
                data.append(review.to_dict())
            return data, 200
        
        return {'error': 'user not found'}, 404
