import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid_email"
        })
        self.assertEqual(response.status_code, 400)

class TestPlaceEndpoints(unittest.TestCase):
        
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
            
    def test_create_place_success(self):
        """Test creating a place with valid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Seaside villa",
            "description": "ok mek",
            "price": 50.0,
            "latitude": 80.6253,
            "longitude": -100.0070,
            "owner_id": "50f648fd-5f7b-4aa9-a09e-033b09438f4a"
            })
        self.assertEqual(response.status_code, 201)
        
    def test_create_place_invalid_desciption(self):
        """Test creating a place with valid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Seaside villa",
            "description": "",
            "price": 50,
            "latitude": 80.6253,
            "longitude": -100.0070,
            "owner_id": "50f648fd-5f7b-4aa9-a09e-033b09438f4a"
            })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_price(self):
        """Test creating a place with an invalid price (negative)"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Seaside villa",
            "description": "ok mek",
            "price": -50.0,
            "latitude": 80.6253,
            "longitude": -100.0070,
            "owner_id": "50f648fd-5f7b-4aa9-a09e-033b09438f4a"
        })
        self.assertEqual(response.status_code, 400)
        
    def test_create_place_invalid_price(self):
        """Test creating a place with an invalid price (negative)"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Seaside villa",
            "description": "ok mek",
            "price": 50,
            "latitude": 80.6253,
            "longitude": -100.0070,
            "owner_id": "50f648fd-5f7b-4aa9-a09e-033b09438f4a"
        })
        self.assertEqual(response.status_code, 400)
        

    def test_create_place_invalid_latitude(self):
        """Test creating a place with valid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Seaside villa",
            "description": "ok mek",
            "price": 50.0,
            "latitude": 180.6253,
            "longitude": -100.0070,
            "owner_id": "50f648fd-5f7b-4aa9-a09e-033b09438f4a"
            })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        """Test creating a place with valid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Seaside villa",
            "description": "ok mek",
            "price": 50.0,
            "latitude": 80.6253,
            "longitude": -1000.0070,
            "owner_id": "50f648fd-5f7b-4aa9-a09e-033b09438f4a"
            })
        self.assertEqual(response.status_code, 400)
 
        
    def test_create_place_invalid_title(self):
        """Test creating a place with valid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "ok mek",
            "price": 50.0,
            "latitude": 80.6253,
            "longitude": -100.0070,
            "owner_id": "50f648fd-5f7b-4aa9-a09e-033b09438f4a"
            })
        self.assertEqual(response.status_code, 400)
        
    def test_create_place_invalid_owner(self):
        """Test creating a place with valid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Seaside villa",
            "description": "ok mek",
            "price": 50.0,
            "latitude": 80.6253,
            "longitude": -100.0070,
            "owner_id": ""
            })
        self.assertEqual(response.status_code, 400)        

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review_success(self):
        """Test creating a review with valid data"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing place to stay!",
            "rating": 5,
            "user_id": "valid_user_id",
            "place_id": "valid_place_id"
        })
        self.assertEqual(response.status_code, 201)
        
    def test_create_review_invalid_text(self):
        """Test creating a review with valid data"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": "valid_user_id",
            "place_id": "valid_place_id"
        })
        self.assertEqual(response.status_code, 400)
        
    def test_create_review_invalid_rating_inf_0(self):
        """Test creating a review with valid data"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "text",
            "rating": -1,
            "user_id": "valid_user_id",
            "place_id": "valid_place_id"
        })
        self.assertEqual(response.status_code, 400)
        
    def test_create_review_invalid_rating_sup_5(self):
        """Test creating a review with valid data"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "text",
            "rating": 10,
            "user_id": "valid_user_id",
            "place_id": "valid_place_id"
        })
        self.assertEqual(response.status_code, 400)
        
    def test_create_review_invalid_user_id(self):
        """Test creating a review with valid data"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing place to stay!",
            "rating": 5,
            "user_id": "",
            "place_id": "valid_place_id"
        })
        self.assertEqual(response.status_code, 400)
        

    def test_create_review_invalid_place_id(self):
        """Test creating a review with non-existent user_id and place_id"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing place to stay!",
            "rating": 5,
            "user_id": "non_existent_user",
            "place_id": ""
        })
        self.assertEqual(response.status_code, 400)

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity_success(self):
        """Test creating an amenity with valid data"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Swimming Pool"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_create_amenity_empty_name(self):
        """Test creating an amenity with an empty name"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)
        
    def test_get_amenity_not_found(self):
        """Test retrieving a non-existent amenity"""
        response = self.client.get('/api/v1/amenities/12345')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json.get("error"), "Amenity not found")           

if __name__ == "__main__":
    unittest.main()