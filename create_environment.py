#!/usr/bin/env python3

import os
import sqlite3
import hashlib
# let's first create connection to database.
def create_connection():
    """Creates and returns a database connection."""
    return sqlite3.connect("forks_and_folks")

def close_connection(conn):
    """Closes a database connection."""
    if conn:
        conn.close()

# Defining the function executes queries  for executing SQL queries
def execute_query(conn, query, params=None):
    """Executes a SQL query."""
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

""" notes:
Fetches all rows of data from the result set of a previously executed SQL query. 
   Returns None if the cursor is invalid.
"""
def fetch_all(cursor):
    """Fetches all results from a cursor."""
    if cursor:
        return cursor.fetchall()
    return None
    
def fetch_one(cursor):
    """ Fetches a single result from a cursor."""
    if cursor:
        return cursor.fetchone()
    return None

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_database():
    """Creates the database schema and populates it with dummy data."""
    conn = create_connection()
    cursor = conn.cursor()

 # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('Chef', 'Consumer'))
        )
    ''')
    
     cursor.execute('''
        CREATE TABLE IF NOT EXISTS Recipes (
            recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_name TEXT NOT NULL,
            ingredients TEXT,
            instructions TEXT,
            chef_id INTEGER,
            FOREIGN KEY (chef_id) REFERENCES Users(user_id)
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ingredients (
            ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_name TEXT NOT NULL,
            location TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Chefs (
            chef_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            portfolio_details TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Chef_Hires (
            hire_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chef_id INTEGER,
            consumer_id INTEGER,
            hire_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chef_id) REFERENCES Users(user_id),
            FOREIGN KEY (consumer_id) REFERENCES Users(user_id)
        )
    ''')

# Insert sample data
    cursor.execute("INSERT OR IGNORE INTO Users (username, password, role) VALUES ('Gabriella', ?, 'Consumer')", (hash_password('password'),))
    cursor.execute("INSERT OR IGNORE INTO Users (username, password, role) VALUES ('Jessica', ?, 'Consumer')", (hash_password('password'),))
    cursor.execute("INSERT OR IGNORE INTO Users (username, password, role) VALUES ('Santhiana', ?, 'Chef')", (hash_password('pass'),))
    cursor.execute("INSERT OR IGNORE INTO Users (username, password, role) VALUES ('Buke', ?, 'Chef')", (hash_password('pass'),))
    cursor.execute("INSERT OR IGNORE INTO Users (username, password, role) VALUES ('Janviere', ?, 'Consumer')", (hash_password('password'),))
    cursor.execute("INSERT OR IGNORE INTO Users (username, password, role) VALUES ('Thierry', ?, 'Chef')", (hash_password('pass'),))
    cursor.execute("INSERT OR IGNORE INTO Users (username, password, role) VALUES ('Dhieu', ?, 'Chef')", (hash_password('pass'),))
    cursor.execute("INSERT OR IGNORE INTO Users (username, password, role) VALUES ('Herve', ?, 'Consumer')", (hash_password('password'),))
    cursor.execute("INSERT OR IGNORE INTO Chefs (user_id, portfolio_details) VALUES (3, 'Specializes in Burundian cuisine.')")
    cursor.execute("INSERT OR IGNORE INTO Chefs (user_id, portfolio_details) VALUES (4, 'Specializes in Kenyan cuisine.')")
    cursor.execute("INSERT OR IGNORE INTO Chefs (user_id, portfolio_details) VALUES (6, 'Specializes in Rwandan cuisine.')")
    cursor.execute("INSERT OR IGNORE INTO Chefs (user_id, portfolio_details) VALUES (7, 'Specializes in Sudani cuisine.')")

 recipes = [
        ("Spaghetti Carbonara", "spaghetti, eggs, pecorino cheese, pancetta, black pepper", "1. Cook pasta\n2. Fry pancetta\n3. Mix eggs and cheese\n4. Combine all ingredients\n", 3),
        ("Classic Burger", "ground beef, burger buns, lettuce, tomato, onion, cheese", "1. Form patties\n2. Grill until done\n3. Assemble with toppings\n", 4),
        ("Caesar Salad", "romaine lettuce, croutons, parmesan, caesar dressing", "1. Chop lettuce\n2. Add croutons and cheese\n3. Toss with dressing\n", 6),
        ("Chocolate Chip Cookies", "flour, butter, sugar, eggs, chocolate chips", "1. Mix ingredients\n2. Form cookies\n3. Bake at 350F for 12 minutes\n", 7),
        ("Chicken Stir Fry", "chicken breast, vegetables, soy sauce, oil, garlic", "1. Cut chicken\n2. Stir fry vegetables\n3. Add chicken and sauce\n", 4)
    ]

    for recipe in recipes:
        cursor.execute('''
            INSERT OR IGNORE INTO Recipes (recipe_name, ingredients, instructions, chef_id)
            VALUES (?, ?, ?, ?)
        ''', recipe)

    ingredients = [
        ("Tomatoes", "Kimironko Market"),
        ("Spaghetti", "250 Stores"),
        ("Chicken Breast", "Farmer's Choice Butcher Shop"),
        ("Flour", "Simba Kisimenti Supermarket"),
        ("Lettuce", "Kimironko Market"),
        ("Croutons", "T2000 Supermarket"),
        ("Butter", "Zoe's Bakery"),
        ("Ground Beef", "Kimironko Market"),
        ("Cheese", "T2000 Supermarket"),
        ("Chocolate Chips", "Zoe's Bakery"),
        ("Buns", "250 Stores"),
        ("Soy Sauce", "Simba Kimironko")
    ]

  for ingredient in ingredients:
        cursor.execute('''
            INSERT OR IGNORE INTO Ingredients (ingredient_name, location)
            VALUES (?, ?)
        ''', ingredient)

    conn.commit()
    close_connection(conn)

def signup(username, password, role):
    """Registers a new user."""
    conn = create_connection()
    hashed_password = hash_password(password)
    query = "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)"
    params = (username, hashed_password, role)
    execute_query(conn, query, params)
    close_connection(conn)
    print("Signup successful!")


def login(username, password):
    """Logs in a user."""
    conn = create_connection()
    query = "SELECT user_id, username, password, role FROM Users WHERE username = ?"
    cursor = execute_query(conn, query, (username,))
    user = fetch_one(cursor)
    close_connection(conn)
    if user:
        user_id, username, stored_password, role = user
        if verify_password(stored_password, password):
            return user_id, username, role
    return None, None, None


def browse_recipes():
    """Allows users to browse recipes."""
    conn = create_connection()
    query = "SELECT recipe_name, ingredients, instructions FROM Recipes"
    cursor = execute_query(conn, query)
    recipes = fetch_all(cursor)
    close_connection(conn)

    if recipes:
        print("\nAvailable Recipes:")
        for i, (name, ingredients, instructions) in enumerate(recipes, 1):
            print(f"{i}. {name}")

        while True:
            choice = input("\nEnter recipe number to view details (or 'exit' to go back): ")
            if choice.lower() == 'exit':
                break
            if choice.isdigit() and 1 <= int(choice) <= len(recipes):
                recipe = recipes[int(choice) - 1]
                print(f"\nRecipe: {recipe[0]}")
                print(f"Ingredients: {recipe[1]}")
                print(f"Instructions:\n{recipe[2]}")
            else:
                print("Invalid choice. Please try again.")
    else:
        print("No recipes found.")

def browse_ingredients():
    """Allows users to browse ingredients."""
    conn = create_connection()
    query = "SELECT ingredient_name, location FROM Ingredients"
    cursor = execute_query(conn, query)
    ingredients = fetch_all(cursor)
    close_connection(conn)

    if ingredients:
        print("\nAvailable Ingredients:")
        for ingredient_name, location in ingredients:
            print(f"{ingredient_name} - Location: {location}")
    else:
        print("No ingredients found.")

def consumer_menu(username):
    """Displays the consumer menu."""
    while True:
        print("\nConsumer Menu:")
        print("1. Browse Recipes")
        print("2. Browse Ingredients")
        print("3. View Chef Portfolios and Hire")
        print("4. Exit")

        choice = input("What do you wish to do?: ")

        if choice == '1':
            browse_recipes()
        elif choice == '2':
            browse_ingredients()
        elif choice == '3':
            view_and_hire_chefs(username)
        elif choice == '4':
            print("Exiting consumer menu...")
            break
        else:
            print("Invalid choice! Try again.")

def view_and_hire_chefs(username):
    """Allows consumers to view chef portfolios and hire chefs."""
    conn = create_connection()
    query = '''
        SELECT Chefs.chef_id, Users.username, Chefs.portfolio_details
        FROM Chefs
        INNER JOIN Users ON Chefs.user_id = Users.user_id
    '''
    cursor = execute_query(conn, query)
    chefs = fetch_all(cursor)
    close_connection(conn)

if chefs:
        print("\nAvailable Chefs:")
        for chef_id, chef_name, portfolio in chefs:
            print(f"Chef ID: {chef_id}, Name: {chef_name}, Portfolio: {portfolio}")

        chef_id = input("\nEnter the Chef ID to hire (or 'exit' to go back): ")
        if chef_id.lower() == 'exit':
            return

conn = create_connection()
        consumer_query = "SELECT user_id FROM Users WHERE username = ?"
        consumer_cursor = execute_query(conn, consumer_query, (username,))
        consumer = fetch_one(consumer_cursor)

conn = create_connection()
        consumer_query = "SELECT user_id FROM Users WHERE username = ?"
        consumer_cursor = execute_query(conn, consumer_query, (username,))
        consumer = fetch_one(consumer_cursor)

if consumer:
            consumer_id = consumer[0]
            hire_query = "INSERT INTO Chef_Hires (chef_id, consumer_id) VALUES (?, ?)"
            execute_query(conn, hire_query, (chef_id, consumer_id))
            print("Chef hired successfully!")
    else:
            print("Consumer not found.")
        close_connection(conn)
    else:
        print("No chefs available.")
