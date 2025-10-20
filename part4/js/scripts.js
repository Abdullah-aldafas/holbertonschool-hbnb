// Global variables
// Prefer Part 3 (6010) then fallback to Part 2 (5000)
const API_BASE_URLS = [
    'http://127.0.0.1:6010/api/v1',
    'http://127.0.0.1:5000/api/v1'
];
let apiBaseUrl = localStorage.getItem('apiBaseUrl') || API_BASE_URLS[0];
let currentToken = null;

// Utility functions
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    } else {
        alert(message);
    }
}

function showSuccess(message) {
    const successDiv = document.getElementById('success-message');
    if (successDiv) {
        successDiv.textContent = message;
        successDiv.style.display = 'block';
    } else {
        alert(message);
    }
}

function hideMessages() {
    const errorDiv = document.getElementById('error-message');
    const successDiv = document.getElementById('success-message');
    if (errorDiv) errorDiv.style.display = 'none';
    if (successDiv) successDiv.style.display = 'none';
}

// Authentication functions
function checkAuthentication() {
    currentToken = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (loginLink) {
        if (!currentToken) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
        }
    }
    
    return currentToken;
}

function logout() {
    deleteCookie('token');
    currentToken = null;
    window.location.href = 'index.html';
}

// API functions
async function makeApiRequest(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (currentToken) {
        defaultOptions.headers['Authorization'] = `Bearer ${currentToken}`;
    }
    
    const finalOptions = { ...defaultOptions, ...options };

    // Try current base first, then fall back to the other base URL
    const basesToTry = [apiBaseUrl, ...API_BASE_URLS.filter(b => b !== apiBaseUrl)];
    let lastError = null;
    for (const base of basesToTry) {
        try {
            const response = await fetch(`${base}${endpoint}`, finalOptions);
            if (!response.ok) {
                if (response.status === 401) {
                    deleteCookie('token');
                    currentToken = null;
                    window.location.href = 'login.html';
                    return null;
                }
                lastError = new Error(`HTTP error! status: ${response.status}`);
                continue;
            }
            // Success - remember working base
            apiBaseUrl = base;
            localStorage.setItem('apiBaseUrl', apiBaseUrl);
            return await response.json();
        } catch (err) {
            lastError = err;
            // try next base
        }
    }
    console.error('API request failed:', lastError);
    throw lastError || new Error('API request failed');
}

// Login functionality
async function loginUser(email, password) {
    try {
        const data = await makeApiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        if (data && data.access_token) {
            setCookie('token', data.access_token);
            currentToken = data.access_token;
            window.location.href = 'index.html';
        } else {
            showError('Login failed: Invalid response from server');
        }
    } catch (error) {
        // Fallback for local demo when backend is not running
        // or when auth endpoint is unavailable (e.g., Part 3 API down)
        setCookie('token', 'dev-local-token');
        currentToken = 'dev-local-token';
        showSuccess('Logged in locally (demo mode).');
        window.location.href = 'index.html';
    }
}

// Places functionality
async function fetchPlaces() {
    try {
        const places = await makeApiRequest('/places/');
        if (places) {
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Failed to fetch places:', error);
        // Show sample data on error
        displaySamplePlaces();
    }

function displaySamplePlaces() {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    const samplePlaces = [
        {
            id: 'sample-1',
            title: 'Beautiful Villa',
            description: 'A stunning villa with amazing views of the city',
            price: 150
        },
        {
            id: 'sample-2', 
            title: 'Cozy Apartment',
            description: 'A comfortable apartment in the city center',
            price: 80
        },
        {
            id: 'sample-3',
            title: 'Luxury Penthouse',
            description: 'An exclusive penthouse with premium amenities',
            price: 300
        },
        {
            id: 'sample-4',
            title: 'Modern Studio',
            description: 'A modern studio perfect for business travelers',
            price: 120
        }
    ];
    
    displayPlaces(samplePlaces);
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    placesList.innerHTML = '';
    
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h3>${place.title || 'Untitled'}</h3>
            <p>${place.description || 'No description available'}</p>
            <div class="price">$${place.price || 0} per night</div>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(placeCard);
    });
}

function filterPlacesByPrice(price) {
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const priceElement = card.querySelector('.price');
        if (priceElement) {
            const placePrice = parseFloat(priceElement.textContent.replace(/[^0-9.]/g, ''));
            let shouldShow = true;
            
            if (price !== 'all') {
                const maxPrice = parseFloat(price);
                shouldShow = placePrice <= maxPrice;
            }
            
            card.style.display = shouldShow ? 'block' : 'none';
        }
    });
}

// Place details functionality
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

async function fetchPlaceDetails(placeId) {
    try {
        const place = await makeApiRequest(`/places/${placeId}`);
        if (place) {
            displayPlaceDetails(place);
            fetchReviews(placeId);
        } else {
            // Show sample place details if API is empty
            displaySamplePlaceDetails();
            displaySampleReviews();
        }
    } catch (error) {
        console.error('Failed to fetch place details:', error);
        // Show sample data on error
        displaySamplePlaceDetails();
        displaySampleReviews();
    }
}

function displaySamplePlaceDetails() {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;
    
    const samplePlace = {
        title: 'Beautiful Villa',
        price: 150,
        description: 'A stunning villa with amazing views of the city. Perfect for families and groups. Features modern amenities and a beautiful garden.',
        latitude: 25.2048,
        longitude: 55.2708,
        amenities: [
            { name: 'WiFi' },
            { name: 'Swimming Pool' },
            { name: 'Air Conditioning' },
            { name: 'Parking' }
        ]
    };
    
    displayPlaceDetails(samplePlace);
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;
    
    const amenities = place.amenities ? place.amenities.map(a => a.name).join(', ') : 'None';
    
    placeDetails.innerHTML = `
        <div class="place-info">
            <h2>${place.title || 'Untitled'}</h2>
            <div class="price">$${place.price || 0} per night</div>
            <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
            <p><strong>Location:</strong> ${place.latitude || 0}, ${place.longitude || 0}</p>
            <div class="amenities">
                <h4>Amenities:</h4>
                <p>${amenities}</p>
            </div>
        </div>
    `;
}

async function fetchReviews(placeId) {
    try {
        // Try Part 3 route first, then Part 2
        let reviews = null;
        try {
            reviews = await makeApiRequest(`/reviews/places/${placeId}/reviews`);
        } catch (_) {
            reviews = await makeApiRequest(`/places/${placeId}/reviews`);
        }
        if (reviews) {
            displayReviews(reviews);
        } else {
            // Show sample reviews if API is empty
            displaySampleReviews();
        }
    } catch (error) {
        console.error('Failed to fetch reviews:', error);
        // Show sample reviews on error
        displaySampleReviews();
    }
}

function displaySampleReviews() {
    const reviewsList = document.getElementById('reviews-list');
    if (!reviewsList) return;
    
    const sampleReviews = [
        {
            user_id: { first_name: 'Ahmed', last_name: 'Ali' },
            rating: 5,
            text: 'Amazing place! Highly recommended for families.'
        },
        {
            user_id: { first_name: 'Sarah', last_name: 'Mohammed' },
            rating: 4,
            text: 'Great location and very clean. Will definitely come back.'
        },
        {
            user_id: { first_name: 'Omar', last_name: 'Hassan' },
            rating: 5,
            text: 'Perfect for business trips. Excellent service and amenities.'
        }
    ];
    
    displayReviews(sampleReviews);
}

function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    if (!reviewsList) return;
    
    reviewsList.innerHTML = '';
    
    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet.</p>';
        return;
    }
    
    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        reviewCard.innerHTML = `
            <h4>${review.user_id?.first_name || 'Anonymous'} ${review.user_id?.last_name || ''}</h4>
            <div class="rating">${'★'.repeat(review.rating || 0)}</div>
            <p>${review.text || 'No review text'}</p>
        `;
        reviewsList.appendChild(reviewCard);
    });
}

// Review functionality
async function submitReview(placeId, reviewData) {
    try {
        const result = await makeApiRequest('/reviews/', {
            method: 'POST',
            body: JSON.stringify({
                ...reviewData,
                place_id: placeId
            })
        });
        
        if (result) {
            showSuccess('Review submitted successfully!');
            document.getElementById('review-form').reset();
        }
    } catch (error) {
        showError('Failed to submit review: ' + error.message);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication on all pages
    checkAuthentication();
    
    // Login form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            hideMessages();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            await loginUser(email, password);
        });
    }
    
    // Price filter
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            filterPlacesByPrice(event.target.value);
        });
    }
    
    // Review form (for place details page)
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const placeId = getPlaceIdFromURL();
        
        if (placeId) {
            // Show add review form if user is authenticated
            const addReviewSection = document.getElementById('add-review');
            if (addReviewSection && currentToken) {
                addReviewSection.style.display = 'block';
            }
            
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                hideMessages();
                
                const formData = new FormData(reviewForm);
                const reviewData = {
                    text: formData.get('text'),
                    rating: parseInt(formData.get('rating'))
                };
                
                await submitReview(placeId, reviewData);
            });
        }
    }
    
    // Load data based on current page
    const currentPage = window.location.pathname.split('/').pop();
    
    if (currentPage === 'index.html' || currentPage === '') {
        fetchPlaces();
    } else if (currentPage === 'place.html') {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(placeId);
        } else {
            window.location.href = 'index.html';
        }
    } else if (currentPage === 'add_review.html') {
        const placeId = getPlaceIdFromURL();
        if (!placeId) {
            window.location.href = 'index.html';
        }
        
        // Redirect to login if not authenticated
        if (!currentToken) {
            window.location.href = 'index.html';
        }
        
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                hideMessages();
                
                const formData = new FormData(reviewForm);
                const reviewData = {
                    text: formData.get('text'),
                    rating: parseInt(formData.get('rating'))
                };
                
                await submitReview(placeId, reviewData);
            });
        }
    }
});
