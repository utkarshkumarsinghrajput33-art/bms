"""
==========================================================
Banking Management System
File : database.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================
Handles all database operations.
==========================================================
"""

import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG


class Database:
    """
    Database class for handling all MySQL operations.
    """

    def __init__(self):
        self.connection = None
        self.cursor = None

    # ------------------------------------------------------
    # Connect to Database
    # ------------------------------------------------------

    def connect(self):
        """
        Establish connection with MySQL.
        """

        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)

            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True

        except Error as e:
            print("\nDatabase Connection Error")
            print(e)

        return False

    # ------------------------------------------------------
    # Disconnect
    # ------------------------------------------------------

    def disconnect(self):
        """
        Close cursor and database connection.
        """

        try:

            if self.cursor:
                self.cursor.close()

            if self.connection:
                self.connection.close()

        except Error as e:
            print(e)

    # ------------------------------------------------------
    # Execute INSERT / UPDATE / DELETE
    # ------------------------------------------------------

    def execute(self, query, values=None):
        """
        Execute INSERT, UPDATE or DELETE query.

        Returns True if successful.
        """

        try:

            self.cursor.execute(query, values)

            self.connection.commit()

            return True

        except Error as e:

            self.connection.rollback()

            print("\nDatabase Error")

            print(e)

            return False

    # ------------------------------------------------------
    # Execute SELECT ONE
    # ------------------------------------------------------

    def fetch_one(self, query, values=None):
        """
        Returns one row.
        """

        try:

            self.cursor.execute(query, values)

            return self.cursor.fetchone()

        except Error as e:

            print(e)

            return None

    # ------------------------------------------------------
    # Execute SELECT ALL
    # ------------------------------------------------------

    def fetch_all(self, query, values=None):
        """
        Returns all rows.
        """

        try:

            self.cursor.execute(query, values)

            return self.cursor.fetchall()

        except Error as e:

            print(e)

            return []

    # ------------------------------------------------------
    # Check Record Exists
    # ------------------------------------------------------

    def record_exists(self, query, values=None):

        row = self.fetch_one(query, values)

        return row is not None

    # ------------------------------------------------------
    # Return Last Insert ID
    # ------------------------------------------------------

    def last_insert_id(self):

        return self.cursor.lastrowid

    # ------------------------------------------------------
    # Transaction Handling
    # ------------------------------------------------------

    def begin(self):

        self.connection.start_transaction()

    def commit(self):

        self.connection.commit()

    def rollback(self):

        self.connection.rollback()


# ==========================================================
# Singleton Database Object
# ==========================================================

db = Database()


# ==========================================================
# Connection Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 50)
    print("BANKING MANAGEMENT SYSTEM")
    print("=" * 50)

    if db.connect():

        print("Database Connected Successfully.")

        print()

        version = db.fetch_one("SELECT VERSION() AS version")

        print("MySQL Version :", version["version"])

        database = db.fetch_one("SELECT DATABASE() AS db")

        print("Current Database :", database["db"])

        db.disconnect()

    else:

        print("Connection Failed.")
