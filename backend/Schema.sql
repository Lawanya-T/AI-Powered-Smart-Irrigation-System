 CREATE TABLE IF NOT EXISTS farmer (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  phone VARCHAR(20) UNIQUE,
  preferred_language VARCHAR(20) DEFAULT 'en'
);
 
CREATE TABLE IF NOT EXISTS crop (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  growth_stage VARCHAR(50),
  water_requirement_mm_per_day FLOAT
);
 
CREATE TABLE IF NOT EXISTS field (
  id SERIAL PRIMARY KEY,
  farmer_id INT REFERENCES farmer(id),
  crop_id INT REFERENCES crop(id),
  location_lat FLOAT,
  location_lng FLOAT,
  size_acres FLOAT,
  sensor_id VARCHAR(50)
);
 
CREATE TABLE IF NOT EXISTS sensor_reading (
  id SERIAL PRIMARY KEY,
  sensor_id VARCHAR(50),
  field_id INT REFERENCES field(id),
  moisture_value FLOAT,
  reading_timestamp TIMESTAMP DEFAULT NOW()
);
 
CREATE TABLE IF NOT EXISTS weather_data (
  id SERIAL PRIMARY KEY,
  field_id INT REFERENCES field(id),
  temperature FLOAT,
  humidity FLOAT,
  rainfall FLOAT,
  forecast_date DATE
);
 
CREATE TABLE IF NOT EXISTS irrigation_history (
  id SERIAL PRIMARY KEY,
  field_id INT REFERENCES field(id),
  water_applied_mm FLOAT,
  irrigated_at TIMESTAMP
);
 
