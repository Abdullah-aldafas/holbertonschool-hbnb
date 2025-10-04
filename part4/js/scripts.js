// Global variables
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';
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
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (currentToken) {
        defaultOptions.headers['Authorization'] = `Bearer ${currentToken}`;
    }
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, finalOptions);
        
        if (!response.ok) {
            if (response.status === 401) {
                // Token expired or invalid
                deleteCookie('token');
                currentToken = null;
                window.location.href = 'login.html';
                return null;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
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
        showError('Login failed: ' + error.message);
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
        const placesList = document.getElementById('places-list');
        if (placesList) {
            placesList.innerHTML = '<div class="loading">Failed to load places. Please try again.</div>';
    }
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
        }
    } catch (error) {
        console.error('Failed to fetch place details:', error);
        const placeDetails = document.getElementById('place-details');
        if (placeDetails) {
            placeDetails.innerHTML = '<div class="loading">Failed to load place details.</div>';
        }
    }
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
        const reviews = await makeApiRequest(`/reviews/places/${placeId}/reviews`);
        if (reviews) {
            displayReviews(reviews);
        }
    } catch (error) {
        console.error('Failed to fetch reviews:', error);
    }
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
