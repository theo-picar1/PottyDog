DROP DATABASE PottyDog;
CREATE DATABASE PottyDog;
USE PottyDog;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS potty_logs;
DROP TABLE IF EXISTS devices;

-- Users table. 
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),                    
    email VARCHAR(100) NOT NULL UNIQUE,     
    password VARCHAR(255), -- password hash; can be NULL for Google users
    dog_name VARCHAR(50),                    
    profile_picture VARCHAR(255),             
    google_id VARCHAR(100) UNIQUE, -- for Google OAuth login
    is_admin BOOLEAN DEFAULT FALSE,
    can_read BOOLEAN DEFAULT TRUE,
    can_write BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Settings table. 1:1 relationship with users.
CREATE TABLE settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    light_mode BOOLEAN DEFAULT TRUE,
    disabled_alerts BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id) 
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Potty logs table. M:1 relationship with users.
CREATE TABLE potty_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    logged_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    potty_type ENUM('pee', 'poop', 'both', 'other') NOT NULL,
    notes TEXT,
    CONSTRAINT fk_potty_logs_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- M:1 relationship with users table
CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    device_name VARCHAR(25) NOT NULL,
    device_location VARCHAR(30) NOT NULL,
    status VARCHAR(10) CHECK (status IN ('idle', 'active', 'offline')) NOT NULL DEFAULT 'offline',
    has_camera BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_device_user 
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
)