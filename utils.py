"""
==========================================================
Banking Management System
File : utils.py
Python Version : 3.11.2
==========================================================
Common helper functions used throughout the project.
==========================================================
"""

import os
import random
import uuid
from datetime import datetime


class Utils:

    # ======================================================
    # Screen
    # ======================================================

    @staticmethod
    def clear_screen():
        """
        Clears the console screen.
        """
        os.system("cls" if os.name == "nt" else "clear")

    # ======================================================
    # Header
    # ======================================================

    @staticmethod
    def print_header(title: str):
        """
        Prints a formatted section header.
        """
        print("\n" + "=" * 60)
        print(title.center(60))
        print("=" * 60)

    # ======================================================
    # Pause
    # ======================================================

    @staticmethod
    def pause():
        """
        Wait for user input.
        """
        input("\nPress Enter to continue...")

    # ======================================================
    # Current Date
    # ======================================================

    @staticmethod
    def current_date():
        return datetime.now().strftime("%Y-%m-%d")

    # ======================================================
    # Current Time
    # ======================================================

    @staticmethod
    def current_time():
        return datetime.now().strftime("%H:%M:%S")

    # ======================================================
    # Current DateTime
    # ======================================================

    @staticmethod
    def current_datetime():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ======================================================
    # Currency Formatter
    # ======================================================

    @staticmethod
    def format_currency(amount):
        """
        Returns amount formatted in Indian Rupees.
        Example:
        ₹12,500.50
        """
        return f"₹{amount:,.2f}"

    # ======================================================
    # Generate Account Number
    # ======================================================

    @staticmethod
    def generate_account_number():
        """
        Generates a random 12-digit account number.
        """
        return random.randint(100000000000, 999999999999)

    # ======================================================
    # Generate Transaction Reference
    # ======================================================

    @staticmethod
    def generate_transaction_reference():
        """
        Example:
        TXN-20260707123055-1A2B3C
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique = uuid.uuid4().hex[:6].upper()
        return f"TXN-{timestamp}-{unique}"

    # ======================================================
    # Generate Loan Number
    # ======================================================

    @staticmethod
    def generate_loan_number():
        return "LN" + datetime.now().strftime("%Y%m%d%H%M%S")

    # ======================================================
    # Generate FD Number
    # ======================================================

    @staticmethod
    def generate_fd_number():
        return "FD" + datetime.now().strftime("%Y%m%d%H%M%S")

    # ======================================================
    # Generate RD Number
    # ======================================================

    @staticmethod
    def generate_rd_number():
        return "RD" + datetime.now().strftime("%Y%m%d%H%M%S")

    # ======================================================
    # Receipt Number
    # ======================================================

    @staticmethod
    def generate_receipt_number():
        return "RCPT-" + uuid.uuid4().hex[:10].upper()

    # ======================================================
    # FD Maturity Calculation (Simple Interest)
    # ======================================================

    @staticmethod
    def calculate_fd_maturity(principal, rate, months):
        years = months / 12
        maturity = principal + ((principal * rate * years) / 100)
        return round(maturity, 2)

    # ======================================================
    # RD Maturity Calculation (Approximate)
    # ======================================================

    @staticmethod
    def calculate_rd_maturity(monthly_amount, rate, months):
        total = monthly_amount * months
        years = months / 12
        interest = (total * rate * years) / 100
        return round(total + interest, 2)

    # ======================================================
    # EMI Calculator
    # ======================================================

    @staticmethod
    def calculate_emi(principal, annual_rate, months):
        """
        Standard EMI Formula.
        """
        monthly_rate = annual_rate / (12 * 100)

        if monthly_rate == 0:
            return round(principal / months, 2)

        emi = (
            principal
            * monthly_rate
            * ((1 + monthly_rate) ** months)
        ) / (
            ((1 + monthly_rate) ** months) - 1
        )

        return round(emi, 2)

    # ======================================================
    # Mask Aadhaar
    # ======================================================

    @staticmethod
    def mask_aadhaar(aadhaar):
        return "XXXXXXXX" + aadhaar[-4:]

    # ======================================================
    # Mask Mobile
    # ======================================================

    @staticmethod
    def mask_mobile(mobile):
        return "XXXXXX" + mobile[-4:]

    # ======================================================
    # Mask Account Number
    # ======================================================

    @staticmethod
    def mask_account(account_number):
        account_number = str(account_number)
        return "XXXXXXXX" + account_number[-4:]

    # ======================================================
    # Yes / No Confirmation
    # ======================================================

    @staticmethod
    def confirm(message):
        choice = input(f"{message} (Y/N): ").strip().upper()
        return choice == "Y"

    # ======================================================
    # Read Integer
    # ======================================================

    @staticmethod
    def read_int(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Please enter a valid integer.")

    # ======================================================
    # Read Float
    # ======================================================

    @staticmethod
    def read_float(prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Please enter a valid number.")

    # ======================================================
    # Read Non-empty String
    # ======================================================

    @staticmethod
    def read_string(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty.")

    # ======================================================
    # Display Menu
    # ======================================================

    @staticmethod
    def display_menu(title, options):
        """
        Displays a numbered menu.

        Example:
            Utils.display_menu(
                "Customer Menu",
                [
                    "Deposit",
                    "Withdraw",
                    "Balance",
                    "Logout"
                ]
            )
        """
        Utils.print_header(title)

        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")

        print("-" * 60)


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    Utils.print_header("UTILS MODULE TEST")

    print("Current Date :", Utils.current_date())
    print("Current Time :", Utils.current_time())
    print("Current DateTime :", Utils.current_datetime())

    print("\nAccount Number :", Utils.generate_account_number())
    print("Transaction Ref :", Utils.generate_transaction_reference())
    print("Loan Number :", Utils.generate_loan_number())
    print("FD Number :", Utils.generate_fd_number())
    print("RD Number :", Utils.generate_rd_number())
    print("Receipt :", Utils.generate_receipt_number())

    print("\nCurrency :", Utils.format_currency(152340.75))

    print("FD Maturity :", Utils.calculate_fd_maturity(100000, 7.5, 36))
    print("RD Maturity :", Utils.calculate_rd_maturity(5000, 7.2, 24))
    print("EMI :", Utils.calculate_emi(500000, 9.5, 60))

    print("\nMasked Aadhaar :", Utils.mask_aadhaar("123412341234"))
    print("Masked Mobile :", Utils.mask_mobile("9876543210"))
    print("Masked Account :", Utils.mask_account("123456789012"))
