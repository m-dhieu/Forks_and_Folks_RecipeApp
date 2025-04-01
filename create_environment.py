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




