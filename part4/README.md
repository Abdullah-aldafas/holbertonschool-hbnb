# HBnB - Part 4: Simple Web Client

This is the frontend web client for the HBnB application, built with HTML5, CSS3, and JavaScript ES6.

## Features

- **Login System**: JWT-based authentication with token storage in cookies
- **Places Listing**: Dynamic display of places with client-side filtering
- **Place Details**: Detailed view of individual places with reviews
- **Review System**: Add reviews for places (authenticated users only)
- **Responsive Design**: Mobile-friendly interface

## Pages

1. **index.html** - Main page with places listing and filtering
2. **login.html** - User authentication page
3. **place.html** - Individual place details with reviews
4. **add_review.html** - Form to add reviews for places

## Setup Instructions

1. **Install Dependencies** (for the backend API):
   ```bash
   cd ../part3/hbnb
   pip install -r requirements.txt
   ```

2. **Start the Backend API**:
   ```bash
   cd ../part3/hbnb
   python run.py
   ```
   The API will be available at `http://127.0.0.1:5000`

3. **Open the Frontend**:
   - Use a local web server (like Live Server in VS Code)
   - Or open directly in browser (some features may not work due to CORS)
   - Recommended: Use `http://127.0.0.1:5500` or `http://localhost:5500`

## File Structure

```
part4/
├── index.html          # Main page
├── login.html          # Login page
├── place.html          # Place details page
├── add_review.html     # Add review page
├── css/
│   └── style.css       # Main stylesheet
├── js/
│   └── scripts.js      # Main JavaScript functionality
├── images/
│   ├── logo.png        # Application logo
│   └── icon.png        # Favicon
└── README.md           # This file
```

## API Integration

The frontend communicates with the backend API through:
- **Authentication**: `POST /api/v1/auth/login`
- **Places**: `GET /api/v1/places/`
- **Place Details**: `GET /api/v1/places/{id}`
- **Reviews**: `GET /api/v1/reviews/places/{id}/reviews`
- **Add Review**: `POST /api/v1/reviews/`

## Key Features

### Authentication
- JWT token storage in cookies
- Automatic token validation
- Redirect to login for unauthenticated users

### Places Listing
- Dynamic loading from API
- Client-side price filtering
- Responsive grid layout

### Place Details
- Complete place information
- Reviews display
- Add review form (authenticated users)

### Review System
- Form validation
- Rating system (1-5 stars)
- Authentication required

## Browser Compatibility

- Modern browsers supporting ES6
- Fetch API support required
- Cookie support required

## Development Notes

- All pages are W3C valid
- Responsive design for mobile devices
- Error handling for API failures
- Loading states for better UX

## Testing

1. Start the backend API
2. Open the frontend in a browser
3. Test login with valid credentials
4. Browse places and view details
5. Add reviews (requires authentication)
6. Test filtering functionality
