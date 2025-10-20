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
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(email='admin@hbnb.io').first()
        if not admin_user:
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
        
        # Create additional users for reviews
        ahmad_user = User.query.filter_by(email='ahmad@example.com').first()
        if not ahmad_user:
            ahmad_user = User(
                first_name='Ahmad',
                last_name='Ali',
                email='ahmad@example.com',
                password='password123',
                is_admin=False
            )
            db.session.add(ahmad_user)
            db.session.flush()
        
        sara_user = User.query.filter_by(email='sara@example.com').first()
        if not sara_user:
            sara_user = User(
                first_name='Sara',
                last_name='Mohammed',
                email='sara@example.com',
                password='password123',
                is_admin=False
            )
            db.session.add(sara_user)
            db.session.flush()
        
        db.session.commit()
        
        # Create amenities (check if they exist first)
        amenities_data = [
            ('WiFi', 'wifi'),
            ('Swimming Pool', 'pool'),
            ('Air Conditioning', 'ac'),
            ('Free Parking', 'parking'),
            ('Gym', 'gym'),
            ('Kitchen', 'kitchen'),
            ('TV', 'tv'),
            ('Balcony', 'balcony'),
            ('Garden', 'garden'),
            ('24/7 Security', 'security')
        ]
        
        amenities = {}
        for name, var_name in amenities_data:
            existing = Amenity.query.filter_by(name=name).first()
            if existing:
                amenities[var_name] = existing
            else:
                amenity = Amenity(name=name)
                db.session.add(amenity)
                amenities[var_name] = amenity
        
        db.session.commit()
        
        # Get amenity objects
        wifi = amenities['wifi']
        pool = amenities['pool']
        ac = amenities['ac']
        parking = amenities['parking']
        gym = amenities['gym']
        kitchen = amenities['kitchen']
        tv = amenities['tv']
        balcony = amenities['balcony']
        garden = amenities['garden']
        security = amenities['security']
        
        # Create places (check if they exist first)
        places_data = [
            ('Beautiful Villa', 'A stunning villa with amazing views', 150.00, 'villa'),
            ('Cozy Apartment', 'A comfortable apartment in the city center', 80.00, 'apartment'),
            ('Luxury Penthouse', 'An exclusive penthouse with premium amenities', 300.00, 'penthouse')
        ]
        
        places = {}
        for title, description, price, var_name in places_data:
            existing = Place.query.filter_by(title=title).first()
            if existing:
                places[var_name] = existing
            else:
                place = Place(
                    title=title,
                    description=description,
                    price=price,
                    latitude=25.2048,
                    longitude=55.2708,
                    owner_id=admin_user.id
                )
                db.session.add(place)
                places[var_name] = place
        
        db.session.commit()
        
        # Get place objects
        villa = places['villa']
        apartment = places['apartment']
        penthouse = places['penthouse']
        
        # Add place-amenity relationships via association table (check if they exist first)
        from app.models.place_amenity import place_amenity
        
        # Villa amenities
        villa_amenities = [wifi.id, pool.id, garden.id, parking.id, security.id]
        for amenity_id in villa_amenities:
            existing = db.session.execute(
                db.select(place_amenity).where(
                    place_amenity.c.place_id == villa.id,
                    place_amenity.c.amenity_id == amenity_id
                )
            ).first()
            if not existing:
                db.session.execute(place_amenity.insert().values(place_id=villa.id, amenity_id=amenity_id))
        
        # Apartment amenities
        apartment_amenities = [wifi.id, ac.id, tv.id, kitchen.id]
        for amenity_id in apartment_amenities:
            existing = db.session.execute(
                db.select(place_amenity).where(
                    place_amenity.c.place_id == apartment.id,
                    place_amenity.c.amenity_id == amenity_id
                )
            ).first()
            if not existing:
                db.session.execute(place_amenity.insert().values(place_id=apartment.id, amenity_id=amenity_id))
        
        # Penthouse amenities
        penthouse_amenities = [wifi.id, pool.id, ac.id, gym.id, balcony.id, parking.id, security.id]
        for amenity_id in penthouse_amenities:
            existing = db.session.execute(
                db.select(place_amenity).where(
                    place_amenity.c.place_id == penthouse.id,
                    place_amenity.c.amenity_id == amenity_id
                )
            ).first()
            if not existing:
                db.session.execute(place_amenity.insert().values(place_id=penthouse.id, amenity_id=amenity_id))
        
        db.session.commit()
        
        # Create sample reviews (delete old ones first, then add new ones)
        from app.models.review import Review
        
        # Delete all existing reviews first
        Review.query.delete()
        
        # Create new reviews with different users
        reviews_data = [
            ('Amazing villa with beautiful garden and pool! Perfect for family vacation.', 5, villa.id, ahmad_user.id),
            ('Great location and very clean. Will definitely come back again!', 4, villa.id, sara_user.id),
            ('Perfect for business trips. Excellent service and amenities.', 5, apartment.id, ahmad_user.id),
            ('Cozy and comfortable. Great value for money!', 4, apartment.id, sara_user.id),
            ('Luxury at its finest! The balcony view is breathtaking.', 5, penthouse.id, ahmad_user.id),
            ('Outstanding penthouse with all premium amenities. Highly recommended!', 5, penthouse.id, sara_user.id)
        ]
        
        for text, rating, place_id, user_id in reviews_data:
            review = Review(
                text=text,
                rating=rating,
                place_id=place_id,
                user_id=user_id
            )
            db.session.add(review)
        
        db.session.commit()
        
        print('Data added successfully!')

if __name__ == '__main__':
    seed_data()
