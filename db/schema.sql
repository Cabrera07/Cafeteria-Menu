###############################################################################
# Database Schema for Cafeteria Menu Management System
###############################################################################


-- === Database Creation ===
CREATE DATABASE IF NOT EXISTS cafeteria_menu;
USE cafeteria_menu;


-- === Categories Table ===
CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Insert default categories
INSERT INTO categories (name) VALUES
    ('Coffee & Espresso'),
    ('Tea & Infusions'),
    ('Cold Beverages'),
    ('Pastries & Bakery'),
    ('Signature Sandwiches'),
    ('Desserts');


-- === Menu Items Table ===
CREATE TABLE IF NOT EXISTS menu_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INT NOT NULL,
    image MEDIUMBLOB,
    image_name VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Indexes for faster lookup on name and category fields
CREATE INDEX idx_menu_items_name ON menu_items(name);
CREATE INDEX idx_menu_items_category ON menu_items(category_id);


-- Example queries to retrieve all categories and menu items
SELECT * FROM categories;
SELECT * FROM menu_items;