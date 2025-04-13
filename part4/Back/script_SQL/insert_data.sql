INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES
    ('ea152844-7d1b-4f0f-8204-d04a0907db98', Admin, HBnB, admin@hbnb.io, '$2a$12$M6b8rmKikihpo5eEkRmcROZI.MMDEFgmfyLL70ULaHDk9r7LvugjO', TRUE),

INSERT INTO amenities (id, name)
VALUES
('07c58f46-ecfc-42ae-b861-23dfc68b46db', 'Wifi')
('60e93525-9c79-4f4e-aca4-c5a1a69a9a6e', 'Swimming Pool')
('08c7ef97-19f1-47ed-8975-e87a6179f7d6', 'Air conditioning');

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES
("3b1f1ce1-9664-45ed-99bf-2db3d4fada5a", "Beautiful place", "This is a beautiful place", 46.00, 80.00, -100.00, "ea152844-7d1b-4f0f-8204-d04a0907db98"),

INSERT INTO places_amenity (place_id, amenity_id)
VALUES
();

INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES
("6a62a9ce-fe95-4fa9-b331-8c60a612b730", "This place is amazing", 5, "aa1fbac2-c982-4f33-9254-c24670c225c6", "3b1f1ce1-9664-45ed-99bf-2db3d4fada5a");
