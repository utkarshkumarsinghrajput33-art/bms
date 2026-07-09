"""
==========================================================
Banking Management System
File : loan.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================

Handles

1. Apply Loan
2. Loan Approval (Automatic)
3. EMI Calculation
4. Search Loan
5. View Loan Details
6. View All Loans

==========================================================
"""

from database import db
from validations import Validator
from utils import Utils
from transactions import Transaction
from account import Account
from config import (
    HOME_LOAN_INTEREST,
    VEHICLE_LOAN_INTEREST,
    EDUCATION_LOAN_INTEREST,
    PERSONAL_LOAN_INTEREST
)


class Loan:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        if db.connection is None:
            db.connect()

        self.transactions = Transaction()
        self.account = Account()

    # ======================================================
    # Check Loan Exists
    # ======================================================

    def loan_exists(self, loan_id):

        query = """
        SELECT loan_id
        FROM loan
        WHERE loan_id=%s
        """

        return db.record_exists(query, (loan_id,))

    # ======================================================
    # Check Account Exists
    # ======================================================

    def account_exists(self, account_number):

        query = """
        SELECT *
        FROM account
        WHERE account_number=%s
        """

        return db.fetch_one(query, (account_number,))

    # ======================================================
    # Interest Rate
    # ======================================================

    def get_interest_rate(self, loan_type):

        loan_type = loan_type.capitalize()

        if loan_type == "Home":
            return HOME_LOAN_INTEREST

        elif loan_type == "Vehicle":
            return VEHICLE_LOAN_INTEREST

        elif loan_type == "Education":
            return EDUCATION_LOAN_INTEREST

        elif loan_type == "Personal":
            return PERSONAL_LOAN_INTEREST

        return None

    # ======================================================
    # EMI Calculation
    # ======================================================

    def calculate_emi(self, amount, rate, months):

        return Utils.calculate_emi(
            amount,
            rate,
            months
        )

    # ======================================================
    # Apply Loan
    # ======================================================

    def apply_loan(self):

        Utils.print_header("LOAN APPLICATION")

        account_number = input(
            "Account Number : "
        ).strip()

        account = self.account_exists(account_number)

        if account is None:
            print("\nAccount Not Found.")
            return

        if account["status"] != "Active":
            print("\nAccount is not Active.")
            return

        print()

        print("Loan Types")

        print("1. Home")
        print("2. Vehicle")
        print("3. Education")
        print("4. Personal")

        choice = input(
            "\nSelect Loan Type : "
        ).strip()

        loan_map = {
            "1": "Home",
            "2": "Vehicle",
            "3": "Education",
            "4": "Personal"
        }

        if choice not in loan_map:
            print("\nInvalid Choice.")
            return

        loan_type = loan_map[choice]

        try:

            amount = float(
                input("Loan Amount : ")
            )

            if not Validator.validate_amount(amount):
                print("Invalid Amount.")
                return

        except ValueError:
            print("Invalid Amount.")
            return

        try:

            tenure = int(
                input("Loan Tenure (Months): ")
            )

            if not Validator.validate_tenure(tenure):
                print("Invalid Tenure.")
                return

        except ValueError:
            print("Invalid Tenure.")
            return

        interest_rate = self.get_interest_rate(
            loan_type
        )

        emi = self.calculate_emi(
            amount,
            interest_rate,
            tenure
        )

        print()

        print("=" * 50)
        print("LOAN SUMMARY")
        print("=" * 50)

        print("Loan Type       :", loan_type)
        print(
            "Loan Amount     :",
            Utils.format_currency(amount)
        )
        print(
            "Interest Rate   :",
            f"{interest_rate}%"
        )
        print(
            "Tenure          :",
            tenure,
            "Months"
        )
        print(
            "Monthly EMI     :",
            Utils.format_currency(emi)
        )

        print("=" * 50)

        confirm = input(
            "\nProceed? (Y/N): "
        ).upper()

        if confirm != "Y":
            print("\nLoan Cancelled.")
            return
        # ==================================================
        # Automatically Approve Loan
        # ==================================================

        status = "Approved"

        insert_query = """
        INSERT INTO loan
        (
            account_number,
            loan_type,
            amount,
            interest_rate,
            tenure_months,
            status,
            applied_date
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            CURDATE()
        )
        """

        values = (
            account_number,
            loan_type,
            amount,
            interest_rate,
            tenure,
            status
        )

        if not db.execute(insert_query, values):

            print("\nUnable to Process Loan.")
            return

        loan_id = db.last_insert_id()

        # ==================================================
        # Credit Loan Amount
        # ==================================================

        current_balance = float(account["balance"])

        new_balance = current_balance + amount

        update_query = """
        UPDATE account
        SET balance=%s
        WHERE account_number=%s
        """

        if not db.execute(
            update_query,
            (
                new_balance,
                account_number
            )
        ):

            print("\nUnable to Credit Loan Amount.")
            return

        # ==================================================
        # Record Transaction
        # ==================================================

        self.transactions.record_transaction(

            account_number=account_number,

            transaction_type="Loan",

            amount=amount,

            balance=new_balance,

            description=f"{loan_type} Loan Credited"

        )

        # ==================================================
        # Success Message
        # ==================================================

        Utils.print_header("LOAN APPROVED")

        print("Loan ID           :", loan_id)

        print("Account Number    :", account_number)

        print("Loan Type         :", loan_type)

        print(
            "Loan Amount       :",
            Utils.format_currency(amount)
        )

        print(
            "Interest Rate     :",
            f"{interest_rate}%"
        )

        print(
            "Loan Tenure       :",
            tenure,
            "Months"
        )

        print(
            "Monthly EMI       :",
            Utils.format_currency(emi)
        )

        print("Status            : Approved")

        print(
            "New Balance       :",
            Utils.format_currency(new_balance)
        )

        print("\nLoan Amount has been credited successfully.")

    # ======================================================
    # Search Loan
    # ======================================================

    def search_loan(self, loan_id):

        query = """
        SELECT *
        FROM loan
        WHERE loan_id=%s
        """

        return db.fetch_one(
            query,
            (loan_id,)
        )

    # ======================================================
    # View Loan Details
    # ======================================================

    def view_loan(self):

        Utils.print_header("VIEW LOAN DETAILS")

        try:

            loan_id = int(
                input("Loan ID : ")
            )

        except ValueError:

            print("Invalid Loan ID.")
            return

        loan = self.search_loan(loan_id)

        if loan is None:

            print("\nLoan Not Found.")
            return

        account = self.account_exists(
            loan["account_number"]
        )

        print()

        print("=" * 60)
        print("LOAN DETAILS")
        print("=" * 60)

        print("Loan ID          :", loan["loan_id"])

        print(
            "Account Number   :",
            loan["account_number"]
        )

        print(
            "Loan Type        :",
            loan["loan_type"]
        )

        print(
            "Loan Amount      :",
            Utils.format_currency(
                loan["amount"]
            )
        )

        print(
            "Interest Rate    :",
            f"{loan['interest_rate']}%"
        )

        print(
            "Tenure           :",
            loan["tenure_months"],
            "Months"
        )

        emi = self.calculate_emi(

            float(loan["amount"]),

            float(loan["interest_rate"]),

            int(loan["tenure_months"])

        )

        print(
            "Monthly EMI      :",
            Utils.format_currency(emi)
        )

        print(
            "Status           :",
            loan["status"]
        )

        print(
            "Applied Date     :",
            loan["applied_date"]
        )

        if account:

            print(
                "Current Balance  :",
                Utils.format_currency(
                    account["balance"]
                )
            )

        print("=" * 60)

    # ======================================================
    # View All Loans
    # ======================================================

    def view_all_loans(self):

        Utils.print_header("ALL LOANS")

        query = """
        SELECT *
        FROM loan
        ORDER BY applied_date DESC
        """

        loans = db.fetch_all(query)

        if not loans:
            print("\nNo Loan Records Found.")
            return

        print(
            "{:<8}{:<15}{:<15}{:<15}{:<12}{:<12}".format(
                "ID",
                "Account",
                "Type",
                "Amount",
                "Status",
                "Applied"
            )
        )

        print("-" * 80)

        for loan in loans:

            print(
                "{:<8}{:<15}{:<15}{:<15}{:<12}{:<12}".format(
                    loan["loan_id"],
                    loan["account_number"],
                    loan["loan_type"],
                    f"₹{loan['amount']}",
                    loan["status"],
                    str(loan["applied_date"])
                )
            )

    # ======================================================
    # View Loans of an Account
    # ======================================================

    def view_account_loans(self):

        Utils.print_header("ACCOUNT LOANS")

        account_number = input(
            "Account Number : "
        ).strip()

        account = self.account_exists(account_number)

        if account is None:

            print("\nAccount Not Found.")
            return

        query = """
        SELECT *
        FROM loan
        WHERE account_number=%s
        ORDER BY applied_date DESC
        """

        loans = db.fetch_all(
            query,
            (account_number,)
        )

        if not loans:

            print("\nNo Loan Found.")
            return

        print()

        print(
            "{:<8}{:<12}{:<15}{:<10}{:<15}".format(
                "Loan ID",
                "Type",
                "Amount",
                "Status",
                "Applied"
            )
        )

        print("-" * 70)

        for loan in loans:

            print(
                "{:<8}{:<12}{:<15}{:<10}{:<15}".format(
                    loan["loan_id"],
                    loan["loan_type"],
                    f"₹{loan['amount']}",
                    loan["status"],
                    str(loan["applied_date"])
                )
            )

    # ======================================================
    # View Loans By Type
    # ======================================================

    def view_loans_by_type(self):

        Utils.print_header("LOANS BY TYPE")

        print("1. Home")
        print("2. Vehicle")
        print("3. Education")
        print("4. Personal")

        option = input(
            "\nSelect Loan Type : "
        ).strip()

        loan_map = {

            "1": "Home",

            "2": "Vehicle",

            "3": "Education",

            "4": "Personal"

        }

        if option not in loan_map:

            print("\nInvalid Choice.")
            return

        loan_type = loan_map[option]

        query = """
        SELECT *
        FROM loan
        WHERE loan_type=%s
        ORDER BY applied_date DESC
        """

        loans = db.fetch_all(
            query,
            (loan_type,)
        )

        if not loans:

            print("\nNo Loan Found.")
            return

        print()

        print(
            "{:<8}{:<15}{:<15}{:<15}{:<12}".format(
                "ID",
                "Account",
                "Amount",
                "Status",
                "Applied"
            )
        )

        print("-" * 75)

        for loan in loans:

            print(
                "{:<8}{:<15}{:<15}{:<15}{:<12}".format(
                    loan["loan_id"],
                    loan["account_number"],
                    f"₹{loan['amount']}",
                    loan["status"],
                    str(loan["applied_date"])
                )
            )

    # ======================================================
    # View Approved Loans
    # ======================================================

    def view_approved_loans(self):

        Utils.print_header("APPROVED LOANS")

        query = """
        SELECT *
        FROM loan
        WHERE status='Approved'
        ORDER BY applied_date DESC
        """

        loans = db.fetch_all(query)

        if not loans:

            print("\nNo Approved Loans.")
            return

        for loan in loans:

            print("=" * 60)

            print("Loan ID        :", loan["loan_id"])

            print("Account Number :", loan["account_number"])

            print("Loan Type      :", loan["loan_type"])

            print(
                "Amount         :",
                Utils.format_currency(
                    loan["amount"]
                )
            )

            print(
                "Interest       :",
                f"{loan['interest_rate']}%"
            )

            print(
                "Tenure         :",
                loan["tenure_months"],
                "Months"
            )

            print(
                "Applied Date   :",
                loan["applied_date"]
            )

        print("=" * 60)

    # ======================================================
    # View Pending Loans
    # ======================================================

    def view_pending_loans(self):

        Utils.print_header("PENDING LOANS")

        query = """
        SELECT *
        FROM loan
        WHERE status='Pending'
        ORDER BY applied_date DESC
        """

        loans = db.fetch_all(query)

        if not loans:

            print("\nNo Pending Loans.")
            return

        for loan in loans:

            print("=" * 60)

            print("Loan ID        :", loan["loan_id"])

            print("Account Number :", loan["account_number"])

            print("Loan Type      :", loan["loan_type"])

            print(
                "Amount         :",
                Utils.format_currency(
                    loan["amount"]
                )
            )

            print(
                "Applied Date   :",
                loan["applied_date"]
            )

        print("=" * 60)

    # ======================================================
    # Count Total Loans
    # ======================================================

    def total_loans(self):

        query = """
        SELECT COUNT(*) AS total
        FROM loan
        """

        row = db.fetch_one(query)

        if row:
            return row["total"]

        return 0

    # ======================================================
    # Total Loan Amount
    # ======================================================

    def total_loan_amount(self):

        query = """
        SELECT SUM(amount) AS total
        FROM loan
        WHERE status='Approved'
        """

        row = db.fetch_one(query)

        if row and row["total"] is not None:
            return float(row["total"])

        return 0.0

    # ======================================================
    # Count Loans By Type
    # ======================================================

    def total_loans_by_type(self, loan_type):

        query = """
        SELECT COUNT(*) AS total
        FROM loan
        WHERE loan_type=%s
        """

        row = db.fetch_one(
            query,
            (loan_type,)
        )

        if row:
            return row["total"]

        return 0

    # ======================================================
    # Search Loans using Account Number
    # ======================================================

    def search_by_account(self):

        Utils.print_header("SEARCH LOANS")

        account_number = input(
            "Account Number : "
        ).strip()

        query = """
        SELECT *
        FROM loan
        WHERE account_number=%s
        ORDER BY applied_date DESC
        """

        loans = db.fetch_all(
            query,
            (account_number,)
        )

        if not loans:

            print("\nNo Loan Records Found.")
            return

        print()

        print(
            "{:<8}{:<12}{:<15}{:<10}{:<15}".format(
                "Loan ID",
                "Type",
                "Amount",
                "Status",
                "Applied"
            )
        )

        print("-" * 70)

        for loan in loans:

            print(
                "{:<8}{:<12}{:<15}{:<10}{:<15}".format(
                    loan["loan_id"],
                    loan["loan_type"],
                    f"₹{loan['amount']}",
                    loan["status"],
                    str(loan["applied_date"])
                )
            )

    # ======================================================
    # Display Loan Statistics
    # ======================================================

    def loan_statistics(self):

        Utils.print_header("LOAN STATISTICS")

        home = self.total_loans_by_type("Home")
        vehicle = self.total_loans_by_type("Vehicle")
        education = self.total_loans_by_type("Education")
        personal = self.total_loans_by_type("Personal")

        print(f"Total Loans          : {self.total_loans()}")

        print(
            "Total Loan Amount    :",
            Utils.format_currency(
                self.total_loan_amount()
            )
        )

        print()

        print("Loan Type Distribution")

        print("-" * 40)

        print(f"Home Loans       : {home}")

        print(f"Vehicle Loans    : {vehicle}")

        print(f"Education Loans  : {education}")

        print(f"Personal Loans   : {personal}")

        print("-" * 40)

    # ======================================================
    # Display Interest Rates
    # ======================================================

    def display_interest_rates(self):

        Utils.print_header("LOAN INTEREST RATES")

        print(
            f"Home Loan       : {HOME_LOAN_INTEREST}%"
        )

        print(
            f"Vehicle Loan    : {VEHICLE_LOAN_INTEREST}%"
        )

        print(
            f"Education Loan  : {EDUCATION_LOAN_INTEREST}%"
        )

        print(
            f"Personal Loan   : {PERSONAL_LOAN_INTEREST}%"
        )

    # ======================================================
    # Loan Menu
    # ======================================================

    def menu(self):

        while True:

            Utils.print_header("LOAN MANAGEMENT")

            print("1. Apply Loan")
            print("2. View Loan Details")
            print("3. View All Loans")
            print("4. View Account Loans")
            print("5. Search Loan By Account")
            print("6. View Loans By Type")
            print("7. View Approved Loans")
            print("8. View Pending Loans")
            print("9. Loan Statistics")
            print("10. Interest Rates")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":
                self.apply_loan()

            elif choice == "2":
                self.view_loan()

            elif choice == "3":
                self.view_all_loans()

            elif choice == "4":
                self.view_account_loans()

            elif choice == "5":
                self.search_by_account()

            elif choice == "6":
                self.view_loans_by_type()

            elif choice == "7":
                self.view_approved_loans()

            elif choice == "8":
                self.view_pending_loans()

            elif choice == "9":
                self.loan_statistics()

            elif choice == "10":
                self.display_interest_rates()

            elif choice == "0":
                break

            else:
                print("\nInvalid Choice.")

            Utils.pause()

    # ======================================================
    # Get Loan Details by ID
    # ======================================================

    def get_loan(self, loan_id):

        query = """
        SELECT *
        FROM loan
        WHERE loan_id=%s
        """

        return db.fetch_one(query, (loan_id,))

    # ======================================================
    # Check Existing Loan
    # ======================================================

    def customer_has_loan(self, account_number):

        query = """
        SELECT COUNT(*) AS total
        FROM loan
        WHERE account_number=%s
        """

        row = db.fetch_one(query, (account_number,))

        if row:
            return row["total"] > 0

        return False

    # ======================================================
    # Display EMI Calculator
    # ======================================================

    def emi_calculator(self):

        Utils.print_header("EMI CALCULATOR")

        try:

            amount = float(
                input("Loan Amount : ")
            )

            if not Validator.validate_amount(amount):
                print("Invalid Amount.")
                return

            rate = float(
                input("Interest Rate (%) : ")
            )

            months = int(
                input("Tenure (Months) : ")
            )

            if not Validator.validate_tenure(months):
                print("Invalid Tenure.")
                return

        except ValueError:

            print("Invalid Input.")
            return

        emi = Utils.calculate_emi(
            amount,
            rate,
            months
        )

        total_payment = emi * months

        total_interest = total_payment - amount

        print()

        print("=" * 50)

        print("EMI DETAILS")

        print("=" * 50)

        print(
            "Loan Amount      :",
            Utils.format_currency(amount)
        )

        print(
            "Interest Rate    :",
            f"{rate}%"
        )

        print(
            "Tenure           :",
            months,
            "Months"
        )

        print(
            "Monthly EMI      :",
            Utils.format_currency(emi)
        )

        print(
            "Total Interest   :",
            Utils.format_currency(total_interest)
        )

        print(
            "Total Payment    :",
            Utils.format_currency(total_payment)
        )

        print("=" * 50)

    # ======================================================
    # Get Loan Count
    # ======================================================

    def get_total_loans(self):

        return self.total_loans()

    # ======================================================
    # Get Total Approved Amount
    # ======================================================

    def get_total_disbursed(self):

        return self.total_loan_amount()

    # ======================================================
    # Loan Summary
    # ======================================================

    def summary(self):

        Utils.print_header("LOAN SUMMARY")

        print(
            "Total Loans :",
            self.get_total_loans()
        )

        print(
            "Total Amount Disbursed :",
            Utils.format_currency(
                self.get_total_disbursed()
            )
        )

    # ======================================================
    # Admin Loan Approval Methods
    # ======================================================

    def pending_loans(self):
        self.view_pending_loans()

    def approve_loan(self):
        Utils.print_header("APPROVE LOAN")
        try:
            loan_id = int(input("Enter Loan ID to Approve : ").strip())
        except ValueError:
            print("Invalid Loan ID.")
            return

        query = "SELECT * FROM loan WHERE loan_id=%s"
        loan = db.fetch_one(query, (loan_id,))

        if not loan:
            print("Loan application not found.")
            return

        if loan["status"] != "Pending":
            print(f"Loan application is already {loan['status']}.")
            return

        account_query = "SELECT * FROM account WHERE account_number=%s"
        account = db.fetch_one(account_query, (loan["account_number"],))
        if not account:
            print("Account associated with loan not found.")
            return

        update_loan = "UPDATE loan SET status='Approved' WHERE loan_id=%s"
        if db.execute(update_loan, (loan_id,)):
            current_balance = float(account["balance"])
            amount = float(loan["amount"])
            new_balance = current_balance + amount

            update_acc = "UPDATE account SET balance=%s WHERE account_number=%s"
            if db.execute(update_acc, (new_balance, loan["account_number"])):
                self.transactions.record_transaction(
                    account_number=loan["account_number"],
                    transaction_type="Loan",
                    amount=amount,
                    balance=new_balance,
                    description=f"{loan['loan_type']} Loan Approved & Credited"
                )
                print(f"\nLoan ID {loan_id} Approved Successfully. Amount Credited.")
            else:
                print("Failed to credit amount to customer account.")
        else:
            print("Failed to update loan status.")

    def reject_loan(self):
        Utils.print_header("REJECT LOAN")
        try:
            loan_id = int(input("Enter Loan ID to Reject : ").strip())
        except ValueError:
            print("Invalid Loan ID.")
            return

        query = "SELECT * FROM loan WHERE loan_id=%s"
        loan = db.fetch_one(query, (loan_id,))

        if not loan:
            print("Loan application not found.")
            return

        if loan["status"] != "Pending":
            print(f"Loan application is already {loan['status']}.")
            return

        update_loan = "UPDATE loan SET status='Rejected' WHERE loan_id=%s"
        if db.execute(update_loan, (loan_id,)):
            print(f"\nLoan ID {loan_id} Rejected Successfully.")
        else:
            print("Failed to update loan status.")

    # ======================================================
    # End of Loan Module
    # ======================================================
