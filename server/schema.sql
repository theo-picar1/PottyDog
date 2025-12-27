DROP DATABASE PottyDOG;
CREATE DATABASE PottyDOG;
USE PottyDOG;

-- Users table. 
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),                    
    email VARCHAR(100) NOT NULL UNIQUE,     
    password VARCHAR(255), -- password hash; can be NULL for Google users
    dog_name VARCHAR(50),                    
    profile_picture VARCHAR(255),             
    google_id VARCHAR(100) UNIQUE, -- for Google OAuth login
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
)

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

-- Actual potty tracker device table. 1:1 relationship with users
CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Repesents PubNub channel
    user_id INT NULL UNIQUE,
    can_read BOOLEAN DEFAULT TRUE,
    can_write BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_devices_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
)

-- Inserting device that I have
INSERT INTO devices (can_read, can_write)
VALUES (TRUE, TRUE);

UPDATE devices
SET user_id = 13 -- My own user_id for my own device
WHERE id = 1 AND user_id IS NULL;