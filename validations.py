"""
==========================================================
Banking Management System
File : validations.py
Python Version : 3.11.2
==========================================================
Contains all input validation methods.
==========================================================
"""

import re
from datetime import datetime, date


class Validator:

    # ------------------------------------------------------
    # Name Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Allows alphabets and spaces only.
        Length: 2 to 50 characters.
        """
        pattern = r"^[A-Za-z ]{2,50}$"
        return bool(re.fullmatch(pattern, name.strip()))

    # ------------------------------------------------------
    # Mobile Number Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_mobile(mobile: str) -> bool:
        """
        Indian mobile number validation.
        Starts with 6-9 and contains exactly 10 digits.
        """
        pattern = r"^[6-9][0-9]{9}$"
        return bool(re.fullmatch(pattern, mobile))

    # ------------------------------------------------------
    # Email Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Standard email validation.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$"
        return bool(re.fullmatch(pattern, email))

    # ------------------------------------------------------
    # Aadhaar Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_aadhaar(aadhaar: str) -> bool:
        """
        Aadhaar must contain exactly 12 digits.
        """
        pattern = r"^\d{12}$"
        return bool(re.fullmatch(pattern, aadhaar))

    # ------------------------------------------------------
    # PAN Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_pan(pan: str) -> bool:
        """
        PAN Format:
        ABCDE1234F
        """
        pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
        return bool(re.fullmatch(pattern, pan.upper()))

    # ------------------------------------------------------
    # Pincode Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_pincode(pincode: str) -> bool:
        """
        Indian PIN code.
        """
        pattern = r"^[1-9][0-9]{5}$"
        return bool(re.fullmatch(pattern, pincode))

    # ------------------------------------------------------
    # Password Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Password Rules:
        Minimum 8 characters
        At least one uppercase
        At least one lowercase
        At least one number
        At least one special character
        """
        pattern = (
            r"^(?=.*[a-z])"
            r"(?=.*[A-Z])"
            r"(?=.*\d)"
            r"(?=.*[@$!%*?&])"
            r"[A-Za-z\d@$!%*?&]{8,}$"
        )

        return bool(re.fullmatch(pattern, password))

    # ------------------------------------------------------
    # ATM PIN Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_atm_pin(pin: str) -> bool:
        """
        ATM PIN must contain exactly 4 digits.
        """
        pattern = r"^\d{4}$"
        return bool(re.fullmatch(pattern, pin))

    # ------------------------------------------------------
    # Account Number Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_account_number(account_number: str) -> bool:
        """
        Account number:
        10 to 18 digits.
        """
        pattern = r"^\d{10,18}$"
        return bool(re.fullmatch(pattern, account_number))

    # ------------------------------------------------------
    # IFSC Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_ifsc(ifsc: str) -> bool:
        """
        IFSC Example:
        SBIN0001234
        """
        pattern = r"^[A-Z]{4}0[A-Z0-9]{6}$"
        return bool(re.fullmatch(pattern, ifsc.upper()))

    # ------------------------------------------------------
    # Date Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_date(date_string: str) -> bool:
        """
        Format:
        YYYY-MM-DD
        """
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # ------------------------------------------------------
    # DOB Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_dob(date_string: str) -> bool:
        """
        Customer must be at least 18 years old.
        """
        try:
            dob = datetime.strptime(date_string, "%Y-%m-%d").date()

            today = date.today()

            age = (
                today.year
                - dob.year
                - (
                    (today.month, today.day)
                    < (dob.month, dob.day)
                )
            )

            return age >= 18

        except ValueError:
            return False

    # ------------------------------------------------------
    # Gender Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_gender(gender: str) -> bool:

        return gender.capitalize() in (
            "Male",
            "Female",
            "Other"
        )

    # ------------------------------------------------------
    # Amount Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_amount(amount) -> bool:
        """
        Amount must be greater than zero.
        """
        try:
            amount = float(amount)
            return amount > 0
        except ValueError:
            return False

    # ------------------------------------------------------
    # Interest Rate Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_interest(rate) -> bool:

        try:
            rate = float(rate)
            return 0 <= rate <= 100
        except ValueError:
            return False

    # ------------------------------------------------------
    # Loan Tenure Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_tenure(months) -> bool:

        try:
            months = int(months)
            return months > 0
        except ValueError:
            return False

    # ------------------------------------------------------
    # Transaction Type Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_transaction_type(transaction_type: str) -> bool:

        transaction_types = (
            "Deposit",
            "Withdraw",
            "Transfer",
            "Loan",
            "FD",
            "RD"
        )

        return transaction_type in transaction_types

    # ------------------------------------------------------
    # Account Type Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_account_type(account_type: str) -> bool:

        return account_type.capitalize() in (
            "Savings",
            "Current"
        )

    # ------------------------------------------------------
    # Branch Code Validation
    # ------------------------------------------------------

    @staticmethod
    def validate_branch_code(branch_code: str) -> bool:
        """
        Example:
        B001
        """
        pattern = r"^B\d{3}$"
        return bool(re.fullmatch(pattern, branch_code.upper()))

    # ------------------------------------------------------
    # Empty String Validation
    # ------------------------------------------------------

    @staticmethod
    def is_not_empty(value: str) -> bool:

        return bool(value.strip())


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    print("Validation Testing")
    print("-" * 40)

    print("Name:", Validator.validate_name("Rahul Sharma"))

    print("Mobile:", Validator.validate_mobile("9876543210"))

    print("Email:", Validator.validate_email("rahul@gmail.com"))

    print("Aadhaar:", Validator.validate_aadhaar("123412341234"))

    print("PAN:", Validator.validate_pan("ABCDE1234F"))

    print("PIN:", Validator.validate_atm_pin("1234"))

    print("Password:", Validator.validate_password("Rahul@123"))

    print("DOB:", Validator.validate_dob("2000-01-15"))

    print("Amount:", Validator.validate_amount(5000))

    print("IFSC:", Validator.validate_ifsc("SBIN0123456"))
