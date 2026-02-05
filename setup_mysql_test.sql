-- Create test database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create test user if it doesn't exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'
IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on hbnb_test_db only
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema only
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Apply privilege changes
FLUSH PRIVILEGES;
