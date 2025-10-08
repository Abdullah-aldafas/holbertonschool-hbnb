from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenity
from flask_bcrypt import Bcrypt
import uuid

def seed_data():
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Create admin user
        bcrypt = Bcrypt()
        admin_user = User(
            id=str(uuid.uuid4()),
            first_name='Admin',
            last_name='HBnB',
            email='admin@hbnb.io',
            password=bcrypt.generate_password_hash('admin1234').decode('utf-8'),
            is_admin=True
        )
        
        # Create amenities
        wifi = Amenity(id=str(uuid.uuid4()), name='WiFi')
        pool = Amenity(id=str(uuid.uuid4()), name='Swimming Pool')
        ac = Amenity(id=str(uuid.uuid4()), name='Air Conditioning')
        
        # Create places
        villa = Place(
            id=str(uuid.uuid4()),
            title='Beautiful Villa',
            description='A stunning villa with amazing views',
            price=150.00,
            latitude=25.2048,
            longitude=55.2708,
            owner_id=admin_user.id
        )
        
        apartment = Place(
            id=str(uuid.uuid4()),
            title='Cozy Apartment',
            description='A comfortable apartment in the city center',
            price=80.00,
            latitude=25.2048,
            longitude=55.2708,
            owner_id=admin_user.id
        )
        
        penthouse = Place(
            id=str(uuid.uuid4()),
            title='Luxury Penthouse',
            description='An exclusive penthouse with premium amenities',
            price=300.00,
            latitude=25.2048,
            longitude=55.2708,
            owner_id=admin_user.id
        )
        
        # Add to database
        db.session.add(admin_user)
        db.session.add(wifi)
        db.session.add(pool)
        db.session.add(ac)
        db.session.add(villa)
        db.session.add(apartment)
        db.session.add(penthouse)
        
        # Add place-amenity relationships
        db.session.add(PlaceAmenity(place_id=villa.id, amenity_id=wifi.id))
        db.session.add(PlaceAmenity(place_id=villa.id, amenity_id=pool.id))
        db.session.add(PlaceAmenity(place_id=apartment.id, amenity_id=wifi.id))
        db.session.add(PlaceAmenity(place_id=penthouse.id, amenity_id=wifi.id))
        db.session.add(PlaceAmenity(place_id=penthouse.id, amenity_id=pool.id))
        db.session.add(PlaceAmenity(place_id=penthouse.id, amenity_id=ac.id))
        
        db.session.commit()
        print('Data added successfully!')

if __name__ == '__main__':
    seed_data()
