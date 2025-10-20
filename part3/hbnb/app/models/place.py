from app.models.basemodel import BaseModel
from app.extensions import db
from app.models.user import User
from app.models.place_amenity import place_amenity


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(55), nullable=False)
    description = db.Column(db.String(55), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=False, nullable=False)

    @staticmethod
    def init_relationships():
        from app.models.review import Review
        from app.models.user import User
        from app.models.amenity import Amenity
        owner = db.relationship(User, backref="place", lazy=True)
        review = db.relationship(Review, backref="place", lazy=True)
        amenities = db.relationship(Amenity, secondary=place_amenity, backref=db.backref('place', lazy=True), lazy=True)
    

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        
    def to_dict(self):
        from app.services import facade
        from app.models.place_amenity import place_amenity
        from app.models.amenity import Amenity
        """Convert the Place instance into a dictionary."""
        base_dict = super().to_dict()
        facade_id = self.owner_id
        owner: User = facade.get_user(facade_id)
        
        # Get amenities for this place directly from database
        amenities = []
        try:
            # Query amenities directly using the association table
            amenity_ids = db.session.execute(
                db.select(place_amenity.c.amenity_id).where(place_amenity.c.place_id == self.id)
            ).scalars().all()
            
            for amenity_id in amenity_ids:
                amenity = db.session.get(Amenity, amenity_id)
                if amenity:
                    amenities.append(amenity.name)
        except Exception as e:
            print(f"Error getting amenities: {e}")
            amenities = []
        
        base_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": owner.to_dict() if owner else self.owner_id,
            "amenities": amenities
        })
        return base_dict
