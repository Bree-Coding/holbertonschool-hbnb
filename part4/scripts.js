/** =============================
 * 1. Login, Authentication & Cookies
 * ============================= **/

// Setup the login form to send credentials and store token
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                document.cookie = `token=${data.access_token}; path=/;`;
                window.location.href = 'index.html';
            } else {
                const errorData = await response.json();
                const errorMessage = document.getElementById('error-message');
                if (errorMessage) {
                    errorMessage.textContent = errorData.error || 'Login failed';
                }
            }
        } catch (error) {
            console.error('Error logging in:', error.message);
        }
    });
}

// Check if user is authenticated based on cookie token
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (logoutButton) logoutButton.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'block';
    }
    return token;
}

// Get a cookie value by its name
function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
}

/** =============================
 * 2. Places (List, Filter, View)
 * ============================= **/

// Fetch all places from the API
async function fetchPlaces() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places');
        if (!response.ok) throw new Error(`Failed to fetch places: ${response.statusText}`);
        
        const placesResponse = await response.json();
        console.log('Places fetched:', placesResponse);

        // Extract places array from the response object
        return Array.isArray(placesResponse.places) ? placesResponse.places : [];
    } catch (error) {
        console.error('Error fetching places:', error);
        return [];
    }
}

// Display all places inside the DOM
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        
        // Add place image
        const imgElement = document.createElement('img');
        imgElement.src = `places_images/${imageMapping[place.id] || 'default.jpg'}`;
        imgElement.alt = `Image of ${place.title}`;
        imgElement.className = 'place-image';

        placeCard.innerHTML = `
            <h3>${place.title}</h3>
            <p>${place.description}</p>
            <p><strong>Price:</strong> ${place.price}€</p>
        `;

        placeCard.prepend(imgElement);

        placeCard.addEventListener('click', () => {
            window.location.href = `place.html?id=${place.id}`;
          });
           
        
        placesList.appendChild(placeCard);
    });
}

const imageMapping = {
    "b002f7e3-8dbd-4422-a677-4810b1fff34a": "Pastel House front.jpg",
    "45897b67-da31-4cde-a6ca-ee3403b39166": "Minimal House front.jpg",
    "a84515d4-8169-479a-b150-99e5a3bdca24": "Green House front.jpg",
    "9d8e44a7-a85d-45b8-b4fe-54e8781dbace": "Pink House front.jpg"
};

// Filter displayed places based on price
function filterPlacesByPrice(maxPrice) {
    const allPlaces = document.querySelectorAll('.place-card');
    allPlaces.forEach(place => {
        const priceElement = place.querySelector('p strong');
        const priceTextNode = priceElement?.nextSibling?.textContent;
        const price = parseFloat(priceTextNode?.replace('€', '')) || 0;

        place.style.display = (maxPrice === 'all' || price <= parseFloat(maxPrice)) ? 'block' : 'none';
    });
}

// Setup the price filter dropdown
function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    priceFilter.addEventListener('change', (event) => {
        const maxPrice = event.target.value;
        filterPlacesByPrice(maxPrice);
    });
}

// Handle search form
function setupSearchForm() {
    const searchForm = document.getElementById('search-form');
    if (!searchForm) return;

    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const query = document.getElementById('search-input').value.toLowerCase();
        const places = document.querySelectorAll('.place-card');

        places.forEach(place => {
            const title = place.querySelector('h3')?.textContent.toLowerCase() || '';
            const description = place.querySelector('p')?.textContent.toLowerCase() || '';
            place.style.display = (title.includes(query) || description.includes(query)) ? 'block' : 'none';
        });
    });
}


// Fetch place detail info by ID
async function fetchPlaceDetails(placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`);
        if (!response.ok) throw new Error('Failed to fetch places details');

        const placesDetails = await response.json();
        console.log('Places ID fetched:', placesDetails);
        return placesDetails

    } catch (error) {
    }
}

function getPlaceIdByUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id') || null; // Évite une valeur undefined
    console.log('Place ID récupéré :', placeId);
    return placeId;
}


// Display place details
function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');
    if (!section) return;

    const placeImages = placeImageMapping[place.id] || ['default.jpg'];

    // 1. Vider la section
    section.innerHTML = '';

    // 2. Création du conteneur global
    const container = document.createElement('div');

    // 3. Création du carrousel
    const carouselWrapper = document.createElement('div');
    carouselWrapper.className = 'carousel-wrapper';

    const carouselContainer = document.createElement('div');
    carouselContainer.className = 'place-images-carousel';

    placeImages.forEach((image, index) => {
        const imgElement = document.createElement('img');
        imgElement.src = `places_images/${image}`;
        imgElement.alt = `Image of ${place.title}`;
        imgElement.className = 'place-image-detail';
        imgElement.style.display = index === 0 ? 'block' : 'none';
        carouselContainer.appendChild(imgElement);
    });

    const prevButton = document.createElement('button');
    prevButton.textContent = '←';
    prevButton.className = 'carousel-button prev';

    const nextButton = document.createElement('button');
    nextButton.textContent = '→';
    nextButton.className = 'carousel-button next';

    carouselContainer.appendChild(prevButton);
    carouselContainer.appendChild(nextButton);
    carouselWrapper.appendChild(carouselContainer);

    // 4. Création du bloc de détails
    const detailsDiv = document.createElement('div');
    detailsDiv.className = 'place-info';

    const title = document.createElement('h1');
    title.textContent = place.title;

    const description = document.createElement('p');
    description.textContent = place.description;

    const price = document.createElement('p');
    price.innerHTML = `<strong>Price:</strong> ${place.price}€`;

    detailsDiv.appendChild(title);
    detailsDiv.appendChild(description);
    detailsDiv.appendChild(price);

    // 5. Ajout des éléments dans la section
    container.appendChild(carouselWrapper);
    container.appendChild(detailsDiv);
    section.appendChild(container);

    // 6. Carrousel - logique des boutons
    let currentImageIndex = 0;

    prevButton.addEventListener('click', () => {
        currentImageIndex = (currentImageIndex === 0) ? placeImages.length - 1 : currentImageIndex - 1;
        updateCarousel();
    });

    nextButton.addEventListener('click', () => {
        currentImageIndex = (currentImageIndex === placeImages.length - 1) ? 0 : currentImageIndex + 1;
        updateCarousel();
    });

    function updateCarousel() {
        const images = carouselContainer.getElementsByTagName('img');
        Array.from(images).forEach((img, index) => {
            img.style.display = (index === currentImageIndex) ? 'block' : 'none';
        });
    }
}


const placeImageMapping = {
    "b002f7e3-8dbd-4422-a677-4810b1fff34a": ["Pastel House front.jpg", "Pastel House living room.png", "Pastel House bedroom.png",
    "Pastel House kitchen.png", "Pastel House dining corner.png", "Pastel_House_bathroom.png", "Pastel House balcony.png"],
    "45897b67-da31-4cde-a6ca-ee3403b39166": ["Minimal House front.jpg", "Minimalist House living room.png", "Minimal House bedroom.jpg", "Minimal House kitchen.jpg", "Minimal House bathroom.jpg"],
    "a84515d4-8169-479a-b150-99e5a3bdca24": ["Green House front.jpg", "Green House living room.jpg", "Green House bedroom.jpg", "Green House kitchen.jpg", "Green House bathroom.jpg"],
    "9d8e44a7-a85d-45b8-b4fe-54e8781dbace": ["Pink House front.jpg", "Pink House living room.jpg", "Pink House bedroom.jpg", "Pink House kitchen.png", "Pink House dining corner.png", "Pink House bathroom.jpg"]
};


// Display icons (bed, bath, wifi) if available
function displayIcons(place) {
    const iconsContainer = document.getElementById('place-icons');
    if (!iconsContainer) return;

    iconsContainer.innerHTML = '';

    if (place.has_bed) iconsContainer.appendChild(createIcon('images/icon_bed.png', 'Bed Icon'));
    if (place.has_bath) iconsContainer.appendChild(createIcon('images/icon_bath.png', 'Bath Icon'));
    if (place.has_wifi) iconsContainer.appendChild(createIcon('images/icon_wifi.png', 'WiFi Icon'));
}

function createIcon(src, alt) {
    const icon = document.createElement('img');
    icon.src = src;
    icon.alt = alt;
    icon.className = 'icon';
    return icon;
}

/** =============================
 * 3. Reviews (View & Add)
 * ============================= **/

// Fetch all reviews for a place
async function fetchReviews(placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`);
        console.log('URL utilisée pour fetch:', url);
        if (!response.ok) throw new Error('Failed to fetch reviews');
        const reviews = await response.json();
        console.log('Reviews fetched:', reviews);
        displayReviews(reviews.reviews);
    } catch (error) {
    }
}

// Display reviews
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    reviewsSection.innerHTML = reviews.length === 0
        ? '<p>No reviews yet.</p>'
        : reviews.map(review => `
            <div class="review-card">
                <p><strong>Rating:</strong> ${review.rating}/5</p>
                <p>${review.text}</p>
                <p><strong>By:</strong> ${review.user_id}</p>
            </div>
        `).join('');
}

// Setup review form
function setupReviewForm(placeId, token, reviewText, rating) {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewText = document.getElementById('review-text').value;
        const rating = document.getElementById('rating')?.value || 5;

        try {
            const response = await submitReview(placeId, token, reviewText, rating);
            if (response.ok) {
                alert('Review submitted successfully!');
                reviewForm.reset();
                fetchReviews(placeId);
            } else {
                const errorData = await response.json();
                alert(`Failed to submit review: ${errorData.error || response.statusText}`);
            }
        } catch (error) {
            console.error('Error submitting review:', error.message);
        }
    });
}

function setupRatingSystem() {
    const ratings = document.querySelectorAll('.rating'); // Sélectionner toutes les sections de notation

    ratings.forEach(rating => {
        const hearts = rating.querySelectorAll('.heart'); // Récupérer les cœurs dans chaque section

        hearts.forEach(heart => {
            heart.addEventListener('click', function() {
                const value = parseInt(this.getAttribute('data-value')); // Obtenir la valeur du cœur cliqué

                // Réinitialiser tous les cœurs avant de sélectionner
                hearts.forEach(h => h.classList.remove('selected'));

                // Sélectionner tous les cœurs jusqu'à celui cliqué
                for (let i = 0; i < value; i++) {
                    hearts[i].classList.add('selected');
                }

                console.log(`Rating sélectionné : ${value}/5`);
            });
        });
    });
}



// Submit a review
async function submitReview(placeId, token, reviewText) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: token ? `Bearer ${token}` : '', // Inclure le token si authentifié
            },
            body: JSON.stringify({ text: reviewText, rating: rating}), // Envoyer le texte de l'avis en JSON
        });

        if (!response.ok) {
            throw new Error(`Échec de la soumission de l'avis : ${response.statusText}`);
        }

        const responseData = await response.json();
        console.log('Avis soumis avec succès:', responseData);

        // Recharger la section des avis après la soumission
        fetchReviews(placeId);
    } catch (error) {
        console.error('Erreur lors de la soumission de l\'avis:', error);
    }
}

/** =============================
 * DOM Initialization
 * ============================= **/
document.addEventListener('DOMContentLoaded', async () => {
    const currentPage = window.location.pathname; // Identifier la page en cours

    // Index.html : Charger et afficher les lieux
    if (currentPage.includes('index.html') || currentPage.includes('(index)')) {
        const places = await fetchPlaces();
        if (places.length) displayPlaces(places);
        setupPriceFilter(places);
        setupSearchForm(places);
    }

    // Place.html :
    else if (currentPage.includes('place.html')) {
        const placeId = getPlaceIdByUrl();
        const addReviewButton = document.getElementById('add-review-button');
        if (placeId) {
            const placeData = await fetchPlaceDetails(placeId);
            if (placeData) displayPlaceDetails(placeData);
            const placeReview = await fetchReviews(placeId);
            if (placeReview) displayReviews(placeReview)
        }
        if (addReviewButton && placeId) {
            addReviewButton.addEventListener('click', () => {
                // Rediriger vers add_review.html avec l'ID de la place dans l'URL
                window.location.href = `add_review.html?id=${placeId}`;
            });
        }
    }

    // Add_review.html : Page d'ajout d'avis
    else if (currentPage.includes('add_review.html')) {
        const token = checkAuthentication(); // Vérifier l'authentification
        const submitButton = document.getElementById('submit-button');
        const placeId = getPlaceIdByUrl();
        const placeData = await fetchPlaceDetails(placeId);
        const placeReview = await fetchReviews(placeId);
        if (!token) {
            // Si l'utilisateur n'est pas authentifié, rediriger vers la page de login
            if (submitButton) {
                submitButton.addEventListener('click', (event) => {
                    event.preventDefault(); // Empêcher la soumission du formulaire
                    window.location.href = 'login.html'; // Rediriger vers la page de login
                });
            }
            else {
                if (placeId) {
                    setupReviewForm(token, placeId);
                    setupRatingSystem();
                }
            }
        }
    }


    // Login.html : Configurer le formulaire de connexion
    else if (currentPage.includes('login.html')) {
        setupLoginForm();
    }

    // Logout call if the user is connected
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
            window.location.href = 'login.html';
        });
    }
});
