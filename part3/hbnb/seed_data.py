from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.place_amenity import place_amenity

def seed_data():
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Create admin user (BaseModel generates id; User hashes password)
        admin_user = User(
            first_name='Admin',
            last_name='HBnB',
            email='admin@hbnb.io',
            password='admin1234',
            is_admin=True
        )
        # Persist admin first to ensure owner_id is available
        db.session.add(admin_user)
        db.session.flush()  # assigns generated id
        
        # Create amenities
        wifi = Amenity(name='WiFi')
        pool = Amenity(name='Swimming Pool')
        ac = Amenity(name='Air Conditioning')
        
        # Create places
        villa = Place(
            title='Beautiful Villa',
            description='A stunning villa with amazing views',
            price=150.00,
            latitude=25.2048,
            longitude=55.2708,
            owner_id=admin_user.id
        )
        
        apartment = Place(
            title='Cozy Apartment',
            description='A comfortable apartment in the city center',
            price=80.00,
            latitude=25.2048,
            longitude=55.2708,
            owner_id=admin_user.id
        )
        
        penthouse = Place(
            title='Luxury Penthouse',
            description='An exclusive penthouse with premium amenities',
            price=300.00,
            latitude=25.2048,
            longitude=55.2708,
            owner_id=admin_user.id
        )
        
        # Add to database
        db.session.add(wifi)
        db.session.add(pool)
        db.session.add(ac)
        db.session.add(villa)
        db.session.add(apartment)
        db.session.add(penthouse)
        
        # Commit first to get IDs
        db.session.commit()
        
        # Add place-amenity relationships via association table
        db.session.execute(place_amenity.insert().values(place_id=villa.id, amenity_id=wifi.id))
        db.session.execute(place_amenity.insert().values(place_id=villa.id, amenity_id=pool.id))
        db.session.execute(place_amenity.insert().values(place_id=apartment.id, amenity_id=wifi.id))
        db.session.execute(place_amenity.insert().values(place_id=penthouse.id, amenity_id=wifi.id))
        db.session.execute(place_amenity.insert().values(place_id=penthouse.id, amenity_id=pool.id))
        db.session.execute(place_amenity.insert().values(place_id=penthouse.id, amenity_id=ac.id))
        
        db.session.commit()
        
        # Create sample reviews
        from app.models.review import Review
        
        review1 = Review(
            text='Great location and very clean. Will definitely come back again!',
            rating=4,
            place_id=villa.id,
            user_id=admin_user.id
        )
        
        review2 = Review(
            text='Perfect for business trips. Excellent service and amenities.',
            rating=5,
            place_id=apartment.id,
            user_id=admin_user.id
        )
        
        db.session.add(review1)
        db.session.add(review2)
        db.session.commit()
        
        print('Data added successfully!')

if __name__ == '__main__':
    seed_data()
