from app.models.basemodel import BaseModel
from app.extensions import db
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(155), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), unique=False, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=False, nullable=False)

    @staticmethod
    def init_relationships():
        from app.models.place import Place
        from app.models.user import User
        place = db.relationship(Place, backref="review", lazy=True)
        user = db.relationship(User, backref="review", lazy=True) 

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def to_dict(self):
        """Convert the Review instance into a dictionary."""
        from app.services import facade
        
        base_dict = super().to_dict()
        
        # Get user information
        user = facade.get_user(self.user_id)
        user_name = "Anonymous"
        if user:
            user_name = f"{user.first_name} {user.last_name}"
        
        base_dict.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "user_name": user_name
        })
        return base_dict
