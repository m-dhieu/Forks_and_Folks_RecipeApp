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
