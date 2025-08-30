from datetime import datetime
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
        
class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
       
        if 'email' in user_data and user_data['email']:
            user_data['email'] = user_data['email'].strip().lower()
       
        if self.get_user_by_email(user_data.get('email')):
            raise ValueError("Email already registered")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_user_by_email(self, email):
        if not email:
            return None
        return self.user_repo.get_by_attribute('email', email.strip().lower())

    # NEW:
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    # NEW:
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    # NEW:
    def list_users(self):
        return self.user_repo.get_all()

    # NEW:
    def update_user(self, user_id: str, data: dict):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # first_name
        if 'first_name' in data and data['first_name'] is not None:
            fn = str(data['first_name']).strip()
            if not fn or len(fn) > 50:
                raise ValueError("first_name must be at most 50 characters")
            user.first_name = fn

        # last_name
        if 'last_name' in data and data['last_name'] is not None:
            ln = str(data['last_name']).strip()
            if not ln or len(ln) > 50:
                raise ValueError("last_name must be at most 50 characters")
            user.last_name = ln

        # email
        if 'email' in data and data['email']:
            new_email = str(data['email']).strip().lower()
            if '@' not in new_email or '.' not in new_email:
                raise ValueError("Invalid email address")
            other = self.get_user_by_email(new_email)
            if other and other.id != user.id:
                raise ValueError("Email already registered")
            user.email = new_email

        # is_admin
        if 'is_admin' in data:
            user.is_admin = bool(data['is_admin'])

        user.updated_at = datetime.utcnow()
        return user
