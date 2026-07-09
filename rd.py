"""
==========================================================
Banking Management System
File : recurring_deposit.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================

Handles

1. Open Recurring Deposit
2. RD Maturity Calculation
3. View RD
4. Search RD
5. RD Statistics

==========================================================
"""

from datetime import timedelta

from database import db
from utils import Utils
from validations import Validator
from account import Account
from transactions import Transaction

from config import RD_INTEREST


class RecurringDeposit:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        if db.connection is None:
            db.connect()

        self.account = Account()
        self.transaction = Transaction()

    # ======================================================
    # Check RD Exists
    # ======================================================

    def rd_exists(self, rd_id):

        query = """
        SELECT *
        FROM recurring_deposit
        WHERE rd_id=%s
        """

        return db.fetch_one(query, (rd_id,))

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
    # Calculate Maturity Date
    # ======================================================

    def calculate_maturity_date(self, months):

        return Utils.current_date_object() + timedelta(days=months * 30)

    # ======================================================
    # Calculate RD Maturity
    # ======================================================

    def calculate_rd_maturity(
        self,
        monthly_amount,
        interest_rate,
        tenure
    ):

        total_deposit = monthly_amount * tenure

        interest = (
            total_deposit *
            interest_rate *
            tenure
        ) / (12 * 100)

        return total_deposit + interest

    # ======================================================
    # Open Recurring Deposit
    # ======================================================

    def open_rd(self):

        Utils.print_header("OPEN RECURRING DEPOSIT")

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

        try:

            monthly_amount = float(
                input("Monthly Installment : ")
            )

        except ValueError:

            print("Invalid Amount.")
            return

        if not Validator.validate_amount(monthly_amount):

            print("Invalid Amount.")
            return

        try:

            tenure = int(
                input("Tenure (Months) : ")
            )

        except ValueError:

            print("Invalid Tenure.")
            return

        if not Validator.validate_tenure(tenure):

            print("Invalid Tenure.")
            return

        current_balance = float(
            account["balance"]
        )

        minimum_balance = 1000

        if account["account_type"] == "Current":
            minimum_balance = 5000

        if current_balance - monthly_amount < minimum_balance:

            print()

            print("Insufficient Balance.")

            print(
                f"Minimum balance of "
                f"{Utils.format_currency(minimum_balance)} "
                f"must be maintained."
            )

            return

        interest_rate = RD_INTEREST_RATE

        maturity_amount = self.calculate_rd_maturity(

            monthly_amount,

            interest_rate,

            tenure

        )

        maturity_date = self.calculate_maturity_date(
            tenure
        )

        print()

        print("=" * 55)

        print("RECURRING DEPOSIT SUMMARY")

        print("=" * 55)

        print(
            "Monthly Installment :",
            Utils.format_currency(monthly_amount)
        )

        print(
            "Interest Rate       :",
            f"{interest_rate}%"
        )

        print(
            "Tenure              :",
            tenure,
            "Months"
        )

        print(
            "Total Deposit       :",
            Utils.format_currency(
                monthly_amount * tenure
            )
        )

        print(
            "Maturity Amount     :",
            Utils.format_currency(
                maturity_amount
            )
        )

        print(
            "Maturity Date       :",
            maturity_date
        )

        print("=" * 55)

        choice = input(
            "\nProceed? (Y/N): "
        ).upper()

        if choice != "Y":

            print("\nRecurring Deposit Cancelled.")
            return
        # ==================================================
        # Deduct First Monthly Installment
        # ==================================================

        new_balance = current_balance - monthly_amount

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

            print("\nUnable to Update Account.")
            return

        # ==================================================
        # Create Recurring Deposit
        # ==================================================

        insert_query = """
        INSERT INTO recurring_deposit
        (
            account_number,
            monthly_amount,
            interest_rate,
            tenure_months,
            start_date,
            maturity_date,
            maturity_amount
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            CURDATE(),
            %s,
            %s
        )
        """

        values = (

            account_number,

            monthly_amount,

            interest_rate,

            tenure,

            maturity_date,

            maturity_amount

        )

        if not db.execute(insert_query, values):

            print("\nUnable to Create Recurring Deposit.")
            return

        rd_id = db.last_insert_id()

        # ==================================================
        # Record Transaction
        # ==================================================

        self.transaction.record_transaction(

            account_number=account_number,

            transaction_type="RD",

            amount=monthly_amount,

            balance=new_balance,

            description=f"Recurring Deposit #{rd_id}"

        )

        # ==================================================
        # Success Receipt
        # ==================================================

        Utils.print_header("RECURRING DEPOSIT CREATED")

        print("RD Number            :", rd_id)

        print("Account Number       :", account_number)

        print(
            "Monthly Installment  :",
            Utils.format_currency(monthly_amount)
        )

        print(
            "Interest Rate        :",
            f"{interest_rate}%"
        )

        print(
            "Tenure               :",
            tenure,
            "Months"
        )

        print(
            "Start Date           :",
            Utils.current_date()
        )

        print(
            "Maturity Date        :",
            maturity_date
        )

        print(
            "Maturity Amount      :",
            Utils.format_currency(
                maturity_amount
            )
        )

        print(
            "Available Balance    :",
            Utils.format_currency(
                new_balance
            )
        )

        print()

        print("Recurring Deposit Created Successfully.")

    # ======================================================
    # Search RD
    # ======================================================

    def search_rd(self, rd_id):

        query = """
        SELECT *
        FROM recurring_deposit
        WHERE rd_id=%s
        """

        return db.fetch_one(
            query,
            (rd_id,)
        )

    # ======================================================
    # View RD Details
    # ======================================================

    def view_rd(self):

        Utils.print_header("VIEW RECURRING DEPOSIT")

        try:

            rd_id = int(
                input("RD Number : ")
            )

        except ValueError:

            print("Invalid RD Number.")
            return

        rd = self.search_rd(rd_id)

        if rd is None:

            print("\nRecurring Deposit Not Found.")
            return

        print()

        print("=" * 60)

        print("RECURRING DEPOSIT DETAILS")

        print("=" * 60)

        print("RD Number           :", rd["rd_id"])

        print(
            "Account Number      :",
            rd["account_number"]
        )

        print(
            "Monthly Installment :",
            Utils.format_currency(
                rd["monthly_amount"]
            )
        )

        print(
            "Interest Rate       :",
            f"{rd['interest_rate']}%"
        )

        print(
            "Tenure              :",
            rd["tenure_months"],
            "Months"
        )

        print(
            "Opening Date        :",
            rd["start_date"]
        )

        print(
            "Maturity Date       :",
            rd["maturity_date"]
        )

        print(
            "Maturity Amount     :",
            Utils.format_currency(
                rd["maturity_amount"]
            )
        )

        print("=" * 60)
    # ======================================================
    # View All Recurring Deposits
    # ======================================================

    def view_all_rd(self):

        Utils.print_header("ALL RECURRING DEPOSITS")

        query = """
        SELECT *
        FROM recurring_deposit
        ORDER BY start_date DESC
        """

        records = db.fetch_all(query)

        if not records:

            print("\nNo Recurring Deposits Found.")
            return

        print()

        print(
            "{:<8}{:<15}{:<15}{:<10}{:<15}".format(
                "RD ID",
                "Account",
                "Monthly",
                "Rate",
                "Maturity"
            )
        )

        print("-" * 75)

        for rd in records:

            print(
                "{:<8}{:<15}{:<15}{:<10}{:<15}".format(
                    rd["rd_id"],
                    rd["account_number"],
                    f"₹{rd['monthly_amount']}",
                    f"{rd['interest_rate']}%",
                    str(rd["maturity_date"])
                )
            )

    # ======================================================
    # View Account RD
    # ======================================================

    def view_account_rd(self):

        Utils.print_header("ACCOUNT RECURRING DEPOSITS")

        account_number = input(
            "Account Number : "
        ).strip()

        account = self.account_exists(account_number)

        if account is None:

            print("\nAccount Not Found.")
            return

        query = """
        SELECT *
        FROM recurring_deposit
        WHERE account_number=%s
        ORDER BY start_date DESC
        """

        records = db.fetch_all(
            query,
            (account_number,)
        )

        if not records:

            print("\nNo Recurring Deposits Found.")
            return

        print()

        print(
            "{:<8}{:<15}{:<12}{:<12}{:<15}".format(
                "RD ID",
                "Monthly",
                "Rate",
                "Months",
                "Maturity"
            )
        )

        print("-" * 80)

        for rd in records:

            print(
                "{:<8}{:<15}{:<12}{:<12}{:<15}".format(
                    rd["rd_id"],
                    f"₹{rd['monthly_amount']}",
                    f"{rd['interest_rate']}%",
                    rd["tenure_months"],
                    str(rd["maturity_date"])
                )
            )

    # ======================================================
    # Search RD By Account
    # ======================================================

    def search_rd_by_account(self):

        Utils.print_header("SEARCH RECURRING DEPOSIT")

        account_number = input(
            "Account Number : "
        ).strip()

        query = """
        SELECT *
        FROM recurring_deposit
        WHERE account_number=%s
        ORDER BY start_date DESC
        """

        records = db.fetch_all(
            query,
            (account_number,)
        )

        if not records:

            print("\nNo Records Found.")
            return

        for rd in records:

            print()

            print("=" * 60)

            print("RD Number          :", rd["rd_id"])

            print(
                "Monthly Amount     :",
                Utils.format_currency(
                    rd["monthly_amount"]
                )
            )

            print(
                "Interest Rate      :",
                f"{rd['interest_rate']}%"
            )

            print(
                "Tenure             :",
                rd["tenure_months"],
                "Months"
            )

            print(
                "Opening Date       :",
                rd["start_date"]
            )

            print(
                "Maturity Date      :",
                rd["maturity_date"]
            )

            print(
                "Maturity Amount    :",
                Utils.format_currency(
                    rd["maturity_amount"]
                )
            )

        print("=" * 60)

    # ======================================================
    # Total RD Accounts
    # ======================================================

    def total_rd(self):

        query = """
        SELECT COUNT(*) AS total
        FROM recurring_deposit
        """

        row = db.fetch_one(query)

        if row:

            return row["total"]

        return 0

    # ======================================================
    # Total RD Investment
    # ======================================================

    def total_rd_amount(self):

        query = """
        SELECT SUM(monthly_amount * tenure_months) AS total
        FROM recurring_deposit
        """

        row = db.fetch_one(query)

        if row and row["total"] is not None:

            return float(row["total"])

        return 0.0
    # ======================================================
    # RD Statistics
    # ======================================================

    def rd_statistics(self):

        Utils.print_header("RECURRING DEPOSIT STATISTICS")

        print()

        print(
            "Total RD Accounts     :",
            self.total_rd()
        )

        print(
            "Total Investment      :",
            Utils.format_currency(
                self.total_rd_amount()
            )
        )

        query = """
        SELECT AVG(monthly_amount) AS average_amount
        FROM recurring_deposit
        """

        row = db.fetch_one(query)

        average = 0

        if row and row["average_amount"] is not None:

            average = float(row["average_amount"])

        print(
            "Average Monthly RD    :",
            Utils.format_currency(average)
        )

        print()

    # ======================================================
    # RD Maturity Calculator
    # ======================================================

    def maturity_calculator(self):

        Utils.print_header("RD MATURITY CALCULATOR")

        try:

            monthly_amount = float(
                input("Monthly Installment : ")
            )

            if not Validator.validate_amount(monthly_amount):

                print("Invalid Amount.")
                return

            tenure = int(
                input("Tenure (Months) : ")
            )

            if not Validator.validate_tenure(tenure):

                print("Invalid Tenure.")
                return

        except ValueError:

            print("Invalid Input.")
            return

        maturity = self.calculate_rd_maturity(

            monthly_amount,

            RD_INTEREST_RATE,

            tenure

        )

        total_deposit = monthly_amount * tenure

        print()

        print("=" * 55)

        print("RD MATURITY DETAILS")

        print("=" * 55)

        print(
            "Monthly Installment :",
            Utils.format_currency(monthly_amount)
        )

        print(
            "Interest Rate       :",
            f"{RD_INTEREST_RATE}%"
        )

        print(
            "Tenure              :",
            tenure,
            "Months"
        )

        print(
            "Total Deposit       :",
            Utils.format_currency(total_deposit)
        )

        print(
            "Maturity Amount     :",
            Utils.format_currency(maturity)
        )

        print("=" * 55)

    # ======================================================
    # Display RD Interest Rate
    # ======================================================

    def display_interest_rate(self):

        Utils.print_header("RD INTEREST RATE")

        print()

        print(
            f"Current RD Interest Rate : "
            f"{RD_INTEREST}%"
        )

        print()

    # ======================================================
    # RD Summary
    # ======================================================

    def summary(self):

        Utils.print_header("RECURRING DEPOSIT SUMMARY")

        print(
            "Total RD Accounts :",
            self.total_rd()
        )

        print(
            "Total Investment  :",
            Utils.format_currency(
                self.total_rd_amount()
            )
        )

    # ======================================================
    # Get Total RD
    # ======================================================

    def get_total_rd(self):

        return self.total_rd()

    # ======================================================
    # Get Total RD Investment
    # ======================================================

    def get_total_investment(self):

        return self.total_rd_amount()

    # ======================================================
    # RD Menu
    # ======================================================

    def menu(self):

        while True:

            Utils.print_header("RECURRING DEPOSIT MENU")

            print("1. Open Recurring Deposit")
            print("2. View RD Details")
            print("3. View All RD Accounts")
            print("4. View Account RD")
            print("5. Search RD By Account")
            print("6. RD Statistics")
            print("7. Maturity Calculator")
            print("8. Interest Rate")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.open_rd()

            elif choice == "2":

                self.view_rd()

            elif choice == "3":

                self.view_all_rd()

            elif choice == "4":

                self.view_account_rd()

            elif choice == "5":

                self.search_rd_by_account()

            elif choice == "6":

                self.rd_statistics()

            elif choice == "7":

                self.maturity_calculator()

            elif choice == "8":

                self.display_interest_rate()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()
    # ======================================================
    # Get RD Details
    # ======================================================

    def get_rd(self, rd_id):

        query = """
        SELECT *
        FROM recurring_deposit
        WHERE rd_id=%s
        """

        return db.fetch_one(query, (rd_id,))

    # ======================================================
    # Check Whether Account Has RD
    # ======================================================

    def account_has_rd(self, account_number):

        query = """
        SELECT COUNT(*) AS total
        FROM recurring_deposit
        WHERE account_number=%s
        """

        row = db.fetch_one(query, (account_number,))

        if row:
            return row["total"] > 0

        return False

    # ======================================================
    # Get Maturity Amount
    # ======================================================

    def get_maturity_amount(self, rd_id):

        rd = self.get_rd(rd_id)

        if rd is None:
            return None

        return float(rd["maturity_amount"])

    # ======================================================
    # Get Maturity Date
    # ======================================================

    def get_maturity_date(self, rd_id):

        rd = self.get_rd(rd_id)

        if rd is None:
            return None

        return rd["maturity_date"]

    # ======================================================
    # Print RD Receipt
    # ======================================================

    def print_receipt(self, rd_id):

        rd = self.get_rd(rd_id)

        if rd is None:

            print("\nRecurring Deposit Not Found.")
            return

        Utils.print_header("RECURRING DEPOSIT RECEIPT")

        print("RD Number            :", rd["rd_id"])

        print("Account Number       :", rd["account_number"])

        print(
            "Monthly Installment  :",
            Utils.format_currency(
                rd["monthly_amount"]
            )
        )

        print(
            "Interest Rate        :",
            f"{rd['interest_rate']}%"
        )

        print(
            "Tenure               :",
            rd["tenure_months"],
            "Months"
        )

        print(
            "Opening Date         :",
            rd["start_date"]
        )

        print(
            "Maturity Date        :",
            rd["maturity_date"]
        )

        print(
            "Maturity Amount      :",
            Utils.format_currency(
                rd["maturity_amount"]
            )
        )

        print("=" * 60)

    # ======================================================
    # Dashboard Summary
    # ======================================================

    def dashboard_summary(self):

        print()

        print("=" * 50)

        print("RECURRING DEPOSIT SUMMARY")

        print("=" * 50)

        print(
            "Total RD Accounts :",
            self.total_rd()
        )

        print(
            "Total Investment  :",
            Utils.format_currency(
                self.total_rd_amount()
            )
        )

        print("=" * 50)

    # ======================================================
    # Refresh Database Connection
    # ======================================================

    def reconnect(self):

        if db.connection is None:

            db.connect()

    # ======================================================
    # Destructor
    # ======================================================

    def __del__(self):

        pass
