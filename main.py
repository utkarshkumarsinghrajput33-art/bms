"""
==============================================================
            BANKING MANAGEMENT SYSTEM
--------------------------------------------------------------
Python Version : 3.11.2
Database       : MySQL 8.0.46
IDE            : Visual Studio Code

Main Controller File

This file acts as the entry point of the Banking
Management System. It initializes all modules and
controls the navigation between Admin and Customer
operations.

==============================================================
"""

import sys

from database import db
from utils import Utils

from auth import Authentication
from admin import Admin
from customer import Customer
from account import Account
from transactions import Transaction
from loan import Loan
from fd import FixedDeposit
from rd import RecurringDeposit
from beneficiary import Beneficiary
from branch import Branch


class BankingManagementSystem:

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        try:

            if db.connection is None:

                db.connect()

        except Exception as e:

            print("\nUnable to connect to MySQL Database.")
            print(e)
            sys.exit()

        # -------------------------------------------------
        # Create Objects
        # -------------------------------------------------

        self.auth = Authentication()

        self.admin = Admin()

        self.customer = Customer()

        self.account = Account()

        self.transaction = Transaction()

        self.loan = Loan()

        self.fd = FixedDeposit()

        self.rd = RecurringDeposit()

        self.beneficiary = Beneficiary()

        self.branch = Branch()

        # -----------------------------
        # Session Variables
        # -----------------------------

        self.current_admin = None

        self.current_customer = None


    # =====================================================
    # Welcome Screen
    # =====================================================

    def welcome(self):

        Utils.clear_screen()

        print("=" * 70)

        print("            BANKING MANAGEMENT SYSTEM")

        print("=" * 70)

        print()

        print("Python  : 3.11.2")

        print("Database: MySQL 8.0.46")

        print()

        print("=" * 70)

    # =====================================================
    # Exit
    # =====================================================

    def exit_system(self):

        self.close_system()

        Utils.clear_screen()

        print("=" * 70)

        print("Thank You For Using Banking Management System")

        print()

        print("Project Developed Using")

        print("Python 3.11.2")

        print("MySQL 8.0.46")

        print("Visual Studio Code")

        print()

        print("=" * 70)

        sys.exit()

    # =====================================================
    # Main Menu
    # =====================================================

    def main_menu(self):

        while True:

            self.banner()

            print("1. Admin Login")

            print("2. Customer Login")

            print("3. About Project")

            print("4. Database Status")

            print("0. Exit")

            print()

            choice = input("Enter Choice : ").strip()

            if choice == "1":

                self.admin_login()

            elif choice == "2":

                self.customer_login()

            elif choice == "3":

                self.about()

            elif choice == "4":

                self.database_status()

            elif choice == "0":

                self.exit_system()

            else:

                print("\nInvalid Choice.")

                Utils.pause()

    # =====================================================
    # Admin Login
    # =====================================================

    def admin_login(self):

        pass


    # =====================================================
    # Customer Login
    # =====================================================

    def customer_login(self):

        pass




    # =====================================================
    # Admin Login
    # =====================================================

    def admin_login(self):

        Utils.clear_screen()

        print("=" * 70)
        print("                    ADMIN LOGIN")
        print("=" * 70)

        try:

            # Call auth.py
            login_success = self.auth.admin_login()

            if login_success:

                self.current_admin = login_success

                print("\nAuthentic pass.")

                Utils.pause()

                self.admin_dashboard()

            else:

                print("\nInvalid Username or Password.")

                Utils.pause()

        except Exception as e:

            print("\nLogin Failed.")

            print(e)

            Utils.pause()


    # =====================================================
    # Customer Login
    # =====================================================

    def customer_login(self):

        Utils.clear_screen()

        print("=" * 70)
        print("                 CUSTOMER LOGIN")
        print("=" * 70)

        try:

            # auth.py should return customer_id/account_no
            customer = self.auth.customer_login()

            if customer:

                self.current_customer = customer

                print("\nAuthentic pass.")

                Utils.pause()

                self.customer_dashboard(customer)

            else:

                print("\nInvalid Account Number or Password.")

                Utils.pause()

        except Exception as e:

            print("\nLogin Failed.")

            print(e)

            Utils.pause()


    # =====================================================
    # Admin Dashboard
    # =====================================================

    def admin_dashboard(self):

        while True:

            Utils.clear_screen()

            print("=" * 70)
            print("                 ADMIN DASHBOARD")
            print("=" * 70)

            print()

            print("1. Customer Management")

            print("2. Account Management")

            print("3. Transaction Management")

            print("4. Loan Management")

            print("5. Fixed Deposit")

            print("6. Recurring Deposit")

            print("7. Beneficiary Management")

            print("8. Branch Management")

            print("9. Logout")

            print()

            choice = input("Enter Choice : ").strip()

            if choice == "1":
                self.customer_management()
            elif choice == "2":
                self.account_management()
            elif choice == "3":
                self.transaction_management()
            elif choice == "4":
                self.loan_management()
            elif choice == "5":
                self.fixed_deposit_management()
            elif choice == "6":
                self.recurring_deposit_management()
            elif choice == "7":
                self.beneficiary_management()
            elif choice == "8":
                self.branch_management()
            elif choice == "9":
                self.logout()
                break
            else:
                print("\nInvalid Choice.")
                Utils.pause()
        else:

            print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Customer Dashboard
    # =====================================================

    def customer_dashboard(self, customer):

        while True:

            Utils.clear_screen()

            print("=" * 70)
            print("               CUSTOMER DASHBOARD")
            print("=" * 70)

            print()

            print("Welcome :", customer)

            print()

            print("1. My Account")

            print("2. Transactions")

            print("3. Loan")

            print("4. Fixed Deposit")

            print("5. Recurring Deposit")

            print("6. Beneficiaries")

            print("7. Logout")

            print()

            choice = input("Enter Choice : ").strip()
            if choice == "1":
                self.account_management()
            elif choice == "2":
                self.transaction_management()
            elif choice == "3":
                self.loan_management()
            elif choice == "4":
                self.fixed_deposit_management()
            elif choice == "5":
                self.recurring_deposit_management()
            elif choice == "6":
                self.beneficiary_management()
            elif choice == "7":
                self.logout()
                break
            else:
                print("\nInvalid Choice.")
                Utils.pause()
        else:

            print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Customer Management
    # =====================================================

    def customer_management(self):

        try:

            self.customer.menu()

        except Exception as e:

            print("\nCustomer Module Error")

            print(e)

            Utils.pause()


    # =====================================================
    # Account Management
    # =====================================================

    def account_management(self):

        try:

            self.account.menu()

        except Exception as e:

            print("\nAccount Module Error")

            print(e)

            Utils.pause()


    # =====================================================
    # Transaction Management
    # =====================================================

    def transaction_management(self):

        try:

            self.transaction.menu()

        except Exception as e:

            print("\nTransaction Module Error")

            print(e)

            Utils.pause()


    # =====================================================
    # Loan Management
    # =====================================================

    def loan_management(self):

        try:

            self.loan.menu()

        except Exception as e:

            print("\nLoan Module Error")

            print(e)

            Utils.pause()


    # =====================================================
    # Fixed Deposit Management
    # =====================================================

    def fixed_deposit_management(self):

        try:

            self.fd.menu()

        except Exception as e:

            print("\nFixed Deposit Module Error")

            print(e)

            Utils.pause()


    # =====================================================
    # Recurring Deposit Management
    # =====================================================

    def recurring_deposit_management(self):

        try:

            self.rd.menu()

        except Exception as e:

            print("\nRecurring Deposit Module Error")

            print(e)

            Utils.pause()


    # =====================================================
    # Beneficiary Management
    # =====================================================

    def beneficiary_management(self):

        try:

            self.beneficiary.menu()

        except Exception as e:

            print("\nBeneficiary Module Error")

            print(e)

            Utils.pause()


    # =====================================================
    # Branch Management
    # =====================================================

    def branch_management(self):

        try:

            self.branch.menu()

        except Exception as e:

            print("\nBranch Module Error")

            print(e)

            Utils.pause()




    # =====================================================
    # Project Information
    # =====================================================

    def about(self):

        Utils.clear_screen()

        print("=" * 70)

        print("              BANKING MANAGEMENT SYSTEM")

        print("=" * 70)

        print()

        print("Version          : 1.0")

        print("Language         : Python 3.11.2")

        print("Database         : MySQL 8.0.46")

        print("IDE              : Visual Studio Code")

        print("Application Type : Console Based")

        print("Future Upgrade   : Flask + HTML + CSS")

        print()

        Utils.pause()


    # =====================================================
    # Database Status
    # =====================================================

    def database_status(self):

        Utils.clear_screen()

        print("=" * 70)

        print("DATABASE STATUS")

        print("=" * 70)

        if db.connection is not None:

            print()

            print("Database Status : Connected")

        else:

            print()

            print("Database Status : Not Connected")

        print()

        Utils.pause()


    # =====================================================
    # Reload Objects
    # =====================================================

    def reload_modules(self):

        self.admin = Admin()

        self.customer = Customer()

        self.account = Account()

        self.transaction = Transaction()

        self.loan = Loan()

        self.fd = FixedDeposit()

        self.rd = RecurringDeposit()

        self.beneficiary = Beneficiary()

        self.branch = Branch()


    # =====================================================
    # Logout
    # =====================================================

    def logout(self):

        self.reset_session()

        print()

        print("Logging Out...")

        Utils.pause()


    # =====================================================
    # Project Modules
    # =====================================================

    def project_modules(self):

        Utils.clear_screen()

        print("=" * 70)

        print("AVAILABLE MODULES")

        print("=" * 70)

        print()

        print("1. Authenticationentication")

        print("2. Customer")

        print("3. Account")

        print("4. Transactions")

        print("5. Loan")

        print("6. Fixed Deposit")

        print("7. Recurring Deposit")

        print("8. Beneficiary")

        print("9. Branch")

        print()

        Utils.pause()


    # =====================================================
    # Initialize System
    # =====================================================

    def initialize(self):

        try:

            if db.connection is None:

                db.connect()

            self.reload_modules()

            return True

        except Exception as e:

            print("\nSystem Initialization Failed.")

            print(e)

            return False


    # =====================================================
    # Close System
    # =====================================================

    def close_system(self):

        try:

            if db.connection:

                db.connection.close()

                print("\nDatabase Connection Closed.")

        except Exception:

            pass

    # =====================================================
    # Banner
    # =====================================================

    def banner(self):

        Utils.clear_screen()

        print("=" * 70)

        print("        BANKING MANAGEMENT SYSTEM")

        print("=" * 70)

        print()

        print("Python   : 3.11.2")

        print("Database : MySQL 8.0.46")

        print()

        print("Designed for Banking Operations")

        print()

        print("=" * 70)

    # =====================================================
    # Run Application
    # =====================================================

    def run(self):

        try:

            if self.initialize():

                self.main_menu()

        except KeyboardInterrupt:

            print("\n\nApplication Interrupted by User.")

        except Exception as e:

            print("\nUnexpected Error.")

            print(e)

        finally:

            self.close_system()

            print("\nThank You For Using Banking Management System.")


    # =====================================================
    # Current Session
    # =====================================================

    def reset_session(self):

        self.current_admin = None

        self.current_customer = None


    # =====================================================
    # Database Connection Status
    # =====================================================

    def is_database_connected(self):

        return db.connection is not None


    # =====================================================
    # Reconnect Database
    # =====================================================

    def reconnect_database(self):

        try:

            if db.connection is None:

                db.connect()

                print("\nDatabase Reconnected Successfully.")

        except Exception as e:

            print("\nUnable to Reconnect Database.")

            print(e)


    # =====================================================
    # Refresh Application
    # =====================================================

    def refresh(self):

        self.reset_session()

        self.reload_modules()


    # =====================================================
    # Display Current User
    # =====================================================

    def current_user(self):

        if self.current_admin is not None:

            return "Administrator"

        elif self.current_customer is not None:

            return "Customer"

        return "Guest"

# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    system = BankingManagementSystem()

    system.run()

