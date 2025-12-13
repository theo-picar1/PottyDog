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