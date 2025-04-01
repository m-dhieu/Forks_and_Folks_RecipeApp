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

# Fetches a single row of data from the result set of a previously executed SQL query.
def fetch_all(cursor):
    """Fetches all results from a cursor."""
    if cursor:
        return cursor.fetchall()
    return None

# Fetches a single row of data from the result set of a previously executed SQL query.   
def fetch_one(cursor):
    """ Fetches a single result from a cursor."""
    if cursor:
        return cursor.fetchone()
    return None
 # Hashes a password using SHA-256.
def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

#   Verifies a hashed password against a provided password.
def verify_password(stored_password, provided_password):
    """Verifies a hashed password."""
    hashed_provided_password = hash_password(provided_password)
    return stored_password == hashed_provided_password

# Creates the database schema and populates it with dummy data.
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
     # Create the Recipes table
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

# Create the Ingredients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ingredients (
            ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_name TEXT NOT NULL,
            location TEXT
        )
    ''')

# Create the Chefs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Chefs (
            chef_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            portfolio_details TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')

# Create the Chef_Hires table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Chef_Hires (
            hire_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chef_id INTEGER,
            consumer_id INTEGER,
            hire_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            response TEXT,
            message TEXT,            
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

# Insert sample recipes
    recipes = [
        ("Spaghetti Carbonara", "spaghetti, eggs, pecorino cheese, pancetta, black pepper", "1. Cook pasta\n2. Fry pancetta\n3. Mix eggs and cheese\n4. Combine all ingredients\n", 3),
        ("Classic Burger", "ground beef, burger buns, lettuce, tomato, onion, cheese", "1. Form patties\n2. Grill until done\n3. Assemble with toppings\n", 4),
        ("Caesar Salad", "romaine lettuce, croutons, parmesan, caesar dressing", "1. Chop lettuce\n2. Add croutons and cheese\n3. Toss with dressing\n", 6),
        ("Chocolate Chip Cookies", "flour, butter, sugar, eggs, chocolate chips", "1. Mix ingredients\n2. Form cookies\n3. Bake at 350F for 12 minutes\n", 7),
        ("Chicken Stir Fry", "chicken breast, vegetables, soy sauce, oil, garlic", "1. Cut chicken\n2. Stir fry vegetables\n3. Add chicken and sauce\n", 4)
    ]

# Insert sample recipes
    for recipe in recipes:
        cursor.execute('''
            INSERT OR IGNORE INTO Recipes (recipe_name, ingredients, instructions, chef_id)
            VALUES (?, ?, ?, ?)
        ''', recipe)

# Insert sample ingredients
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

# Insert sample ingredients
    for ingredient in ingredients:
        cursor.execute('''
            INSERT OR IGNORE INTO Ingredients (ingredient_name, location)
            VALUES (?, ?)
        ''', ingredient)

    conn.commit()
    close_connection(conn)

# Registers a new user in the database.
def signup(username, password, role):
    """Registers a new user."""
    conn = create_connection()
    hashed_password = hash_password(password)
    query = "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)"
    params = (username, hashed_password, role)
    execute_query(conn, query, params)
    
    # Prompt for portfolio details, if the user signs up as a chef.
    if role.lower() == "chef":
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM Users WHERE username = ?", (username,))
        user = fetch_one(cursor)
        if user:
            user_id = user[0]
            portfolio_details = input("Enter your portfolio details (e.g., specialties, experience): ")
            chef_query = "INSERT INTO Chefs (user_id, portfolio_details) VALUES (?, ?)"
            execute_query(conn, chef_query, (user_id, portfolio_details))
            print("Portfolio created successfully!")
    
    close_connection(conn)
    print("Signup successful!")

# Logs in a user and returns their user ID, username, and role.
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

# Allow saving of data
def save_to_file(data, filename):
    """Saves data to a file."""
    try:
        with open(filename, 'w') as file:
            file.write(data)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to file: {e}")
        
# Allows consumers to browse recipes and view details.
def browse_recipes():
    """Allows users to browse recipes and save them."""
    conn = create_connection()
    query = "SELECT recipe_name, ingredients, instructions FROM Recipes"
    cursor = execute_query(conn, query)
    recipes = fetch_all(cursor)
    close_connection(conn)

    # Display available recipes
    if recipes:
        print("\nAvailable Recipes:")
        for i, (name, ingredients, instructions) in enumerate(recipes, 1):
            print(f"{i}. {name}")
        
        # Allow user to select a recipe to view details
        while True:
            choice = input("\nEnter recipe number to view details (or 'exit' to go back): ")
            if choice.lower() == 'exit':
                break
            if choice.isdigit() and 1 <= int(choice) <= len(recipes):
                recipe = recipes[int(choice) - 1]
                print(f"\nRecipe: {recipe[0]}")
                print(f"Ingredients: {recipe[1]}")
                print(f"Instructions:\n{recipe[2]}")
                # Prompt to save the recipe
                save_choice = input("Do you want to save this recipe to a file? (yes/no): ").lower()
                if save_choice == 'yes':
                    data = f"Recipe: {recipe[0]}\nIngredients: {recipe[1]}\nInstructions:\n{recipe[2]}"
                    save_to_file(data, f"{recipe[0].replace(' ', '_')}_recipe.txt")
            else:
                print("Invalid choice. Please try again.")
    else:
        print("No recipes found.")

# Allows consumers to browse ingredients and view their locations.
def browse_ingredients():
    """Allows users to browse ingredients' locations and save them."""
    conn = create_connection()
    query = "SELECT ingredient_name, location FROM Ingredients"
    cursor = execute_query(conn, query)
    ingredients = fetch_all(cursor)
    close_connection(conn)
    
    # Display available ingredients
    if ingredients:
        print("\nAvailable Ingredients:")
        for i, (ingredient_name, location) in enumerate(ingredients, 1):
            print(f"{i}. {ingredient_name} - Location: {location}")

        while True:
            choice = input("\nEnter ingredient number to view details (or 'exit' to go back): ")
            if choice.lower() == 'exit':
                break
            if choice.isdigit() and 1 <= int(choice) <= len(ingredients):
                ingredient = ingredients[int(choice) - 1]
                print(f"\nIngredient: {ingredient[0]}")
                print(f"Location: {ingredient[1]}")

                # Prompt to save the ingredient location
                save_choice = input("Do you want to save this ingredient location to a file? (yes/no): ").lower()
                if save_choice == 'yes':
                    data = f"Ingredient: {ingredient[0]}\nLocation: {ingredient[1]}"
                    save_to_file(data, f"{ingredient[0].replace(' ', '_')}_location.txt")
            else:
                print("Invalid choice! Please try again.")
    else:
        print("No ingredients found.")

# Displays the consumer menu and allows them to choose actions.
def consumer_menu(username):
    """Displays the consumer menu."""
    while True:
        print("\nConsumer Menu:")
        print("1. Browse Recipes")
        print("2. Browse Ingredients")
        print("3. View Chef Portfolios and Hire")
        print("4. View Hiring Request Status")
        print("5. Exit")
        
        # Prompt user for action
        choice = input("What do you wish to do?: ")

        if choice == '1':
            browse_recipes()
        elif choice == '2':
            browse_ingredients()
        elif choice == '3':
            view_and_hire_chefs(username)
        elif choice == '4':
            view_hiring_status(username)
        elif choice == '5':
            print("Exiting consumer menu...")
            break
        else:
            print("Invalid choice! Try again.")

# Allows consumers to view chef portfolios and hire chefs.
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
    
    # Display available chefs
    if chefs:
        print("\nAvailable Chefs:")
        for chef_id, chef_name, portfolio in chefs:
            print(f"Chef ID: {chef_id}, Name: {chef_name}, Portfolio: {portfolio}")

        chef_id = input("\nEnter the Chef ID to hire (or 'exit' to go back): ")

        # Allow user to hire a chef
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

       #Check if the chef ID is valid
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

# Displays the chef menu and allows them to choose actions.
def chef_menu(username):
    """Displays the chef menu."""

    # This function displays the chef menu and allows chefs to create recipes, view/edit their portfolio, and view hiring notifications.
    while True:
        print("\nChef Menu:")
        print("1. Create Recipe")
        print("2. View/Edit Portfolio")
        print("3. View Hiring Notifications")
        print("4. Exit")

        choice = input("What do you wish to do?: ")
        
        # Prompt user for action
        if choice == '1':
            create_recipe(username)
        elif choice == '2':
            view_edit_portfolio(username)
        elif choice == '3':
            view_hiring_notifications(username)
        elif choice == '4':
            print("Exiting chef menu...")
            break
        else:
            print("Invalid choice! Try again.")

# Allows chefs to create a new recipe.
def create_recipe(username):
    """Allows chefs to create a recipe."""
    conn = create_connection()
    query = "SELECT user_id FROM Users WHERE username = ?"
    cursor = execute_query(conn, query, (username,))
    user = fetch_one(cursor)
    
    # Check if the user is a chef
    if user:
        chef_id = user[0]
        recipe_name = input("Enter recipe name: ")
        ingredients = input("Enter ingredients (comma-separated): ")
        instructions = input("Enter instructions: ")

        recipe_query = "INSERT INTO Recipes (recipe_name, ingredients, instructions, chef_id) VALUES (?, ?, ?, ?)"
        execute_query(conn, recipe_query, (recipe_name, ingredients, instructions, chef_id))
        print("Recipe created successfully!")

    # Check if the user is a chef
    else:
        print("Chef not found.")
    close_connection(conn)

# Allows chefs to view or edit their portfolio.
def view_edit_portfolio(username):
    """Allows chefs to view or edit their portfolio."""
    conn = create_connection()
    query = '''
        SELECT Chefs.portfolio_details
        FROM Chefs
        INNER JOIN Users ON Chefs.user_id = Users.user_id
        WHERE Users.username = ?
    '''
    cursor = execute_query(conn, query, (username,))
    portfolio = fetch_one(cursor)

    # Check if the user is a chef
    if portfolio:
        print(f"\nYour Portfolio: {portfolio[0]}")
        edit_choice = input("Do you want to edit your portfolio? (yes/no): ").lower()
        if edit_choice == 'yes':
            new_portfolio = input("Enter new portfolio details: ")
            update_query = '''
                UPDATE Chefs
                SET portfolio_details = ?
                WHERE user_id = (SELECT user_id FROM Users WHERE username = ?)
            '''
            execute_query(conn, update_query, (new_portfolio, username))
            print("Portfolio updated successfully!")
    
    # Check if the user is a chef
    else:
        print("Portfolio not found.")
    close_connection(conn)

# Allows chefs to view hiring notifications.
def view_hiring_notifications(username):
    """Allows chefs to view hiring notifications."""
    conn = create_connection()
    query = '''
        SELECT Users.username, Chef_Hires.hire_date
        FROM Chef_Hires
        INNER JOIN Users ON Chef_Hires.consumer_id = Users.user_id
        WHERE Chef_Hires.chef_id = (SELECT chef_id FROM Chefs INNER JOIN Users ON Chefs.user_id = Users.user_id WHERE Users.username = ?)
    '''
    cursor = execute_query(conn, query, (username,))
    hires = fetch_all(cursor)
    close_connection(conn)
    
    # Check if the user is a chef
    if hires:
        print("\nHiring Notifications:")
        for consumer_name, hire_date in hires:
            print(f"Consumer: {consumer_name}, Hire Date: {hire_date}")
    
    # Check if the user is a chef
    else:
        print("No hiring notifications found.")

# Main function to handle user interaction.
def main():
        """Main function to handle user interaction."""
        print("Welcome to Forks and Folks Recipe App!")
        
        # Create the database and tables if they don't exist
        create_database()
        
        # Main loop for user interaction
        while True:
            print("\n1. Signup")
            print("2. Login")
            print("3. Exit")
        
            choice = input("Enter your choice: ")

            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                role = input("Enter role (Chef or Consumer): ").capitalize()
                
                if role in ["Chef", "Consumer"]:
                    signup(username, password, role)
                else:
                    print("Invalid role. Please enter 'Chef' or 'Consumer'.")
            
            elif choice == '2':
                username = input("Enter username: ")
                password = input("Enter password: ")
                user_id, username, role = login(username, password)
                if user_id:
                    print(f"Welcome, {username} as a ({role})!")
                    if role == "Consumer":
                        consumer_menu(username)
                    elif role == "Chef":
                        chef_menu(username)
                else:
                    print("Invalid username or password. Please try again.")
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice! Please try again.")

# The main function is the entry point of the program.
if __name__ == "__main__":
    main()
