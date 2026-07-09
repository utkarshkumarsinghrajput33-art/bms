"""
==========================================================
Banking Management System
File : auth.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================
Handles:
1. Admin Login
2. Customer Login
3. Change Password
4. Login History
==========================================================
"""

from database import db


class Authentication:

    # ============================================
    # Admin Login
    # ============================================

    @staticmethod
    def admin_login():

        print("\n========== ADMIN LOGIN ==========")

        username = input("Username : ").strip()

        password = input("Password : ").strip()

        query = """
        SELECT *
        FROM admin
        WHERE username=%s
        AND password=%s
        """

        admin = db.fetch_one(query, (username, password))

        if admin:

            print("\nLogin Successful.")

            return admin

        print("\nInvalid Username or Password.")

        return None

    # ============================================
    # Customer Login
    # ============================================

    @staticmethod
    def customer_login():

        print("\n========== CUSTOMER LOGIN ==========")

        account_number = input("Account Number : ").strip()

        password = input("Password : ").strip()

        query = """
        SELECT *
        FROM account
        WHERE account_number=%s
        AND login_password=%s
        """

        account = db.fetch_one(query, (account_number, password))

        if account is None:

            print("\nInvalid Account Number or Password.")

            return None

        if account["status"] != "Active":

            print("\nYour account is not active.")

            return None

        #Authentication.add_login_history(account_number)

        print("\nLogin Successful.")

        return account

    # ============================================
    # Change Password
    # ============================================

    @staticmethod
    def change_password(account_number):

        print("\n========== CHANGE PASSWORD ==========")

        old_password = input("Old Password : ")

        query = """
        SELECT login_password
        FROM account
        WHERE account_number=%s
        """

        row = db.fetch_one(query, (account_number,))

        if row is None:

            print("Account Not Found.")

            return

        if row["login_password"] != old_password:

            print("Old Password Incorrect.")

            return

        new_password = input("New Password : ")

        confirm_password = input("Confirm Password : ")

        if new_password != confirm_password:

            print("Passwords Do Not Match.")

            return

        update_query = """
        UPDATE account
        SET login_password=%s
        WHERE account_number=%s
        """

        if db.execute(update_query, (new_password, account_number)):

            print("Password Changed Successfully.")

        else:

            print("Unable to Change Password.")

    # ============================================
    # Login History
    # ============================================

    @staticmethod
    def add_login_history(account_number):

        query = """
        INSERT INTO login_history
        (
            account_number,
            ip_address
        )
        VALUES
        (
            %s,
            %s
        )
        """

        db.execute(query, (account_number, "LOCALHOST"))

    # ============================================
    # Logout
    # ============================================

    @staticmethod
    def logout(account_number):

        query = """
        UPDATE login_history
        SET logout_time=NOW()
        WHERE account_number=%s
        ORDER BY login_id DESC
        LIMIT 1
        """

        db.execute(query, (account_number,))

        print("\nLogged Out Successfully.")
