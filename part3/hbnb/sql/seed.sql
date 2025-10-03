-- Seed admin user and initial amenities

-- Admin user (id fixed)
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
  '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
  'Admin',
  'HBnB',
  'admin@hbnb.io',
  -- bcrypt hash for 'admin1234' (example, replace if needed)
  '$2b$12$5k9r0h6kU2k1Vv3h0F2u2e2y3l3m0Nq3o5j5o0r3b9U8m6m2QO0yS',
  TRUE
)
ON CONFLICT (id) DO NOTHING;

-- Amenities (UUID4s should be generated; placeholders here)
INSERT INTO amenities (id, name) VALUES
  ('a1111111-1111-4111-8111-111111111111', 'WiFi')
ON CONFLICT (id) DO NOTHING;

INSERT INTO amenities (id, name) VALUES
  ('b2222222-2222-4222-8222-222222222222', 'Swimming Pool')
ON CONFLICT (id) DO NOTHING;

INSERT INTO amenities (id, name) VALUES
  ('c3333333-3333-4333-8333-333333333333', 'Air Conditioning')
ON CONFLICT (id) DO NOTHING;


