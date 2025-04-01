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
