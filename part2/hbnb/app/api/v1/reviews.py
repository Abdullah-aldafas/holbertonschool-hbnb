from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
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
    def post(self):
        """Register a new review"""
        data = api.payload or {}
        if not facade.get_user(data['user_id']):
            return {'error':'User not found'}, 400
        if not facade.get_place(data['place_id']):
            return {'error':'Place not found'}, 400
        if not 1 <= data['rating'] <= 5:
            return{'error': 'rating must be between 1 and 5'}, 400
        data['text'] = data['text'].strip()
        if not data['text']:
            return {'error': 'text cannot be empty'}, 400
        review = facade.create_review(data)
        return { "id": review.id,
            'text': review.text, 'rating': review.rating,'user_id':review.user_id,
            'place_id':review.place_id,"created_at": review.created_at.isoformat(),
            "updated_at": review.updated_at.isoformat()
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        result = []
        for n in reviews:
            item = {
                'id':n.id,
            'text': n.text, 'rating': n.rating,'user_id':n.user_id,
            'place_id':n.place_id,"created_at": n.created_at.isoformat(),
            "updated_at": n.updated_at.isoformat()
            }
            result.append(item)
        return result, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        rev = facade.get_review(review_id)
        if not rev:
            return {'error':'Review not found'}, 404
        return {
            'id':rev.id,
            'text': rev.text, 'rating': rev.rating,'user_id':rev.user_id,
            'place_id':rev.place_id,"created_at": rev.created_at.isoformat(),
            "updated_at": rev.updated_at.isoformat()
        }, 200

    @api.expect(review_model , validate=False)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload or {}
        try:
            u = facade.update_review(review_id, data)
            if not u:
                return {'error': 'Review not found'},404
            return {
            'id':u.id,
            'text': u.text, 'rating': u.rating,'user_id':u.user_id,
            'place_id':u.place_id,"created_at": u.created_at.isoformat(),
            "updated_at": u.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        rev = facade.get_review(review_id)
        if not rev:
            return {'error':'Review not found'},404
        facade.delete_review(review_id)
        return {
            'id':rev.id,
            'text': rev.text, 'rating': rev.rating,'user_id':rev.user_id,
            'place_id':rev.place_id,"created_at": rev.created_at.isoformat(),
            "updated_at": rev.updated_at.isoformat()
        }, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'},404
        reviews = facade.get_reviews_by_place(place_id)
        result = []
        for r in reviews:
            item =  {
                'id':r.id,
                'text': r.text, 'rating': r.rating,'user_id':r.user_id,
                'place_id':r.place_id,"created_at": r.created_at.isoformat(),
                'updated_at': r.updated_at.isoformat()
            }
            result.append(item)
        return result, 200