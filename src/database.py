###############################################################################
# Database Management for Menu Items
# Handles CRUD operations, data retrieval, and search functionality for 
# menu items in a MySQL database.
###############################################################################

# === Imports ===
# Standard library imports
import os
import json
import base64
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass

# Third-party imports
import mysql.connector
from mysql.connector import Error


###############################################################################
# MenuItem Data Class - Represents a Menu Item
###############################################################################

@dataclass
class MenuItem:
    id: Optional[int]
    name: str
    description: str
    price: float
    category_id: int
    image: Optional[bytes] = None
    image_name: Optional[str] = None
    category_name: Optional[str] = None


    def equals(self, other: 'MenuItem') -> bool:
        """Compare two menu items for equality, including image comparison"""

        if not isinstance(other, MenuItem):
            return False
        
        # Basic attribute comparison
        basic_equality = (
            self.name == other.name and
            self.description == other.description and
            abs(float(self.price) - float(other.price)) < 0.01 and  # Use float comparison for prices
            self.category_id == other.category_id
        )
        
        if not basic_equality:
            return False
            
        # Compare images
        images_match = False
        if self.image is None and other.image is None:
            images_match = True

        elif self.image is not None and other.image is not None:
            images_match = self.image == other.image

        # Compare image names only if images match
        if images_match and self.image is not None:
            return self.image_name == other.image_name
            
        return images_match
    

    def is_complete(self) -> bool:
        """Check if all required fields are filled"""
        return bool(
            self.name and
            self.description and
            self.price > 0 and
            self.category_id and
            self.image 
        )



###############################################################################
# DatabaseManager Class - Handles Database Connections and Queries
###############################################################################

class DatabaseManager:
    def __init__(self, config_path: str = None):
        self.connection = None
        if config_path is None:
            # Default path to the database configuration file
            base_dir = Path(__file__).resolve().parent.parent
            config_path = os.path.join(base_dir, 'db', 'config.json')
        
        self.config = self._load_config(config_path)
        self.connect()



    ###############################################################################
    # Connection and Configuration
    ###############################################################################

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load database configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Configuration file not found at {config_path}. Current working directory: {os.getcwd()}")
    

    def connect(self) -> None:
        """Establish a database connection."""
        try:
            self.connection = mysql.connector.connect(**self.config)
        except Error as e:
            raise Exception(f"Error connecting to database: {e}")


    def ensure_connection(self) -> None:
        """Ensure database connection is active; reconnect if necessary."""
        if not self.connection or not self.connection.is_connected():
            self.connect()

    
    ###############################################################################
    # CRUD Operations for Menu Items
    ###############################################################################

    def create_menu_item(self, item: MenuItem) -> int:
        """Create a new menu item in the database with validation"""

        if not item.is_complete():
            raise ValueError("All fields are required to create a menu item")
            
        self.ensure_connection()
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO menu_items 
                (name, description, price, category_id, image, image_name)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                item.name,
                item.description,
                item.price,
                item.category_id,
                item.image,
                item.image_name
            )
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.lastrowid
        
        except Error as e:
            self.connection.rollback()
            raise Exception(f"Error creating menu item: {e}")
        
        finally:
            cursor.close()


    def read_menu_item(self, item_id: int) -> Optional[MenuItem]:
        """Retrieve a menu item by ID."""

        self.ensure_connection()

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT m.*, c.name as category_name 
                FROM menu_items m
                JOIN categories c ON m.category_id = c.id
                WHERE m.id = %s
            """
            cursor.execute(query, (item_id,))
            result = cursor.fetchone()

            if result:
                return MenuItem(
                    id=result['id'],
                    name=result['name'],
                    description=result['description'],
                    price=float(result['price']),
                    category_id=result['category_id'],
                    image=result['image'],
                    image_name=result['image_name'],
                    category_name=result['category_name']
                )
            return None
        
        except Error as e:
            raise Exception(f"Error reading menu item: {e}")
        
        finally:
            cursor.close()
  

    def update_menu_item(self, item: MenuItem) -> bool:
        """Update an existing menu item if changes are detected"""

        if not item.id:
            raise ValueError("Item ID is required for update")
            
        self.ensure_connection()
        cursor = None

        try:
            if not self.has_changes(item.id, item):
                return False  
                
            cursor = self.connection.cursor()
            
            if not item.image:
                current_item = self.read_menu_item(item.id)
                if current_item:
                    item.image = current_item.image
                    item.image_name = current_item.image_name
            
            query = """
                UPDATE menu_items 
                SET name = %s, description = %s, price = %s, 
                    category_id = %s, image = %s, image_name = %s
                WHERE id = %s
            """
            values = (
                item.name,
                item.description,
                item.price,
                item.category_id,
                item.image,
                item.image_name,
                item.id
            )

            cursor.execute(query, values)
            self.connection.commit()
            return cursor.rowcount > 0
        
        except Error as e:
            if self.connection:
                self.connection.rollback()
            raise Exception(f"Error updating menu item: {e}")
        
        finally:
            if cursor:
                cursor.close()


    def delete_menu_item(self, item_id: int) -> bool:
        """Delete a menu item from the database."""

        if not item_id:
            raise ValueError("Item ID is required for deletion")
            
        self.ensure_connection()
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM menu_items WHERE id = %s"
            cursor.execute(query, (item_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        
        except Error as e:
            if self.connection:
                self.connection.rollback()
            raise Exception(f"Error deleting menu item: {e}")
        
        finally:
            if cursor:
                cursor.close()


    
    ###############################################################################
    # Data Retrieval and Search
    ###############################################################################

    def get_all_menu_items(self) -> List[MenuItem]:
        """Retrieve all menu items from the database."""

        self.ensure_connection()
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT m.*, c.name as category_name 
                FROM menu_items m
                JOIN categories c ON m.category_id = c.id
                ORDER BY m.name
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            return [
                MenuItem(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    price=float(row['price']),
                    category_id=row['category_id'],
                    image=row['image'],
                    image_name=row['image_name'],
                    category_name=row['category_name']
                )
                for row in results
            ]
        
        except Error as e:
            raise Exception(f"Error fetching menu items: {e}")
        
        finally:
            cursor.close()

   
    def get_categories(self) -> List[Tuple[int, str]]:
        """Retrieve all categories from the database."""

        self.ensure_connection()

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, name FROM categories ORDER BY name")
            return cursor.fetchall()
        
        except Error as e:
            raise Exception(f"Error fetching categories: {e}")
        
        finally:
            cursor.close()


    def search_menu_items(self, search_term: str) -> List[MenuItem]:
        """
        Search menu items by ID, name, or similar names using SOUNDEX and LIKE
        """
        
        self.ensure_connection()
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            try:
                item_id = int(search_term)
                id_condition = "m.id = %s"
                id_param = (item_id,)
            
            except ValueError:
                id_condition = "FALSE"
                id_param = ()

            query = """
                SELECT DISTINCT m.*, c.name as category_name 
                FROM menu_items m
                JOIN categories c ON m.category_id = c.id
                WHERE 
                    {id_condition}
                    OR m.name LIKE %s
                    OR SOUNDEX(m.name) = SOUNDEX(%s)
                ORDER BY 
                    CASE 
                        WHEN m.name LIKE %s THEN 1
                        WHEN SOUNDEX(m.name) = SOUNDEX(%s) THEN 2
                        ELSE 3
                    END,
                    m.name
            """.format(id_condition=id_condition)

            search_pattern = f"%{search_term}%"
            params = (
                *id_param,
                search_pattern,  
                search_term,     
                search_pattern,  
                search_term      
            )
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            return [
                MenuItem(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    price=float(row['price']),
                    category_id=row['category_id'],
                    image=row['image'],
                    image_name=row['image_name'],
                    category_name=row['category_name']
                )
                for row in results
            ]
        
        except Error as e:
            raise Exception(f"Error searching menu items: {e}")
        
        finally:
            cursor.close()


    
    ###############################################################################
    # Helper Methods
    ###############################################################################

    def has_changes(self, item_id: int, new_item: MenuItem) -> bool:
        """Check if the item has any changes compared to the database version"""
        
        self.ensure_connection()
        
        try:
            current_item = self.read_menu_item(item_id)
            if not current_item:
                return True
            
            # If no new image provided, use existing image for comparison
            if not new_item.image:
                new_item.image = current_item.image
                new_item.image_name = current_item.image_name
                
            return not current_item.equals(new_item)
        
        except Error as e:
            raise Exception(f"Error checking for changes: {e}")

       
        
    def close(self) -> None:
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
