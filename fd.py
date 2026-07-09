"""
==========================================================
Banking Management System
File : fixed_deposit.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================

Handles

1. Open Fixed Deposit
2. Calculate Maturity Amount
3. View Fixed Deposit
4. Search Fixed Deposit
5. FD Statistics

==========================================================
"""

from datetime import timedelta

from database import db
from utils import Utils
from validations import Validator
from account import Account
from transactions import Transaction

from config import FD_INTEREST


class FixedDeposit:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        if db.connection is None:
            db.connect()

        self.account = Account()
        self.transaction = Transaction()

    # ======================================================
    # Check FD Exists
    # ======================================================

    def fd_exists(self, fd_id):

        query = """
        SELECT *
        FROM fixed_deposit
        WHERE fd_id=%s
        """

        return db.fetch_one(query, (fd_id,))

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

        days = months * 30

        return Utils.current_date_object() + timedelta(days=days)

    # ======================================================
    # Open Fixed Deposit
    # ======================================================

    def open_fd(self):

        Utils.print_header("OPEN FIXED DEPOSIT")

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

            amount = float(
                input("FD Amount : ")
            )

        except ValueError:

            print("Invalid Amount.")
            return

        if not Validator.validate_amount(amount):

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

        current_balance = float(account["balance"])

        minimum_balance = 1000

        if account["account_type"] == "Current":
            minimum_balance = 5000

        if current_balance - amount < minimum_balance:

            print()

            print("Insufficient Balance.")

            print(
                f"Minimum balance of "
                f"{Utils.format_currency(minimum_balance)} "
                f"must be maintained."
            )

            return

        interest_rate = FD_INTEREST_RATE

        maturity_amount = Utils.calculate_fd_maturity(

            amount,

            interest_rate,

            tenure

        )

        maturity_date = self.calculate_maturity_date(
            tenure
        )

        print()

        print("=" * 50)

        print("FIXED DEPOSIT SUMMARY")

        print("=" * 50)

        print(
            "Deposit Amount :",
            Utils.format_currency(amount)
        )

        print(
            "Interest Rate  :",
            f"{interest_rate}%"
        )

        print(
            "Tenure         :",
            tenure,
            "Months"
        )

        print(
            "Maturity Amount:",
            Utils.format_currency(
                maturity_amount
            )
        )

        print(
            "Maturity Date  :",
            maturity_date
        )

        print("=" * 50)

        choice = input(
            "\nProceed? (Y/N): "
        ).upper()

        if choice != "Y":

            print("\nFixed Deposit Cancelled.")
            return
        # ==================================================
        # Deduct Amount from Account
        # ==================================================

        new_balance = current_balance - amount

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
        # Insert Fixed Deposit
        # ==================================================

        insert_query = """
        INSERT INTO fixed_deposit
        (
            account_number,
            amount,
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

            amount,

            interest_rate,

            tenure,

            maturity_date,

            maturity_amount

        )

        if not db.execute(insert_query, values):

            print("\nUnable to Create Fixed Deposit.")
            return

        fd_id = db.last_insert_id()

        # ==================================================
        # Record Transaction
        # ==================================================

        self.transaction.record_transaction(

            account_number=account_number,

            transaction_type="FD",

            amount=amount,

            balance=new_balance,

            description=f"Fixed Deposit #{fd_id}"

        )

        # ==================================================
        # FD Receipt
        # ==================================================

        Utils.print_header("FIXED DEPOSIT CREATED")

        print("FD Number          :", fd_id)

        print("Account Number     :", account_number)

        print(
            "Deposit Amount     :",
            Utils.format_currency(amount)
        )

        print(
            "Interest Rate      :",
            f"{interest_rate}%"
        )

        print(
            "Tenure             :",
            tenure,
            "Months"
        )

        print(
            "Start Date         :",
            Utils.current_date()
        )

        print(
            "Maturity Date      :",
            maturity_date
        )

        print(
            "Maturity Amount    :",
            Utils.format_currency(
                maturity_amount
            )
        )

        print(
            "Available Balance  :",
            Utils.format_currency(
                new_balance
            )
        )

        print()

        print("Fixed Deposit Created Successfully.")

    # ======================================================
    # Search FD
    # ======================================================

    def search_fd(self, fd_id):

        query = """
        SELECT *
        FROM fixed_deposit
        WHERE fd_id=%s
        """

        return db.fetch_one(
            query,
            (fd_id,)
        )

    # ======================================================
    # View FD Details
    # ======================================================

    def view_fd(self):

        Utils.print_header("VIEW FIXED DEPOSIT")

        try:

            fd_id = int(
                input("FD Number : ")
            )

        except ValueError:

            print("Invalid FD Number.")
            return

        fd = self.search_fd(fd_id)

        if fd is None:

            print("\nFixed Deposit Not Found.")
            return

        print()

        print("=" * 60)

        print("FIXED DEPOSIT DETAILS")

        print("=" * 60)

        print("FD Number          :", fd["fd_id"])

        print(
            "Account Number     :",
            fd["account_number"]
        )

        print(
            "Deposit Amount     :",
            Utils.format_currency(
                fd["amount"]
            )
        )

        print(
            "Interest Rate      :",
            f"{fd['interest_rate']}%"
        )

        print(
            "Tenure             :",
            fd["tenure_months"],
            "Months"
        )

        print(
            "Opening Date       :",
            fd["start_date"]
        )

        print(
            "Maturity Date      :",
            fd["maturity_date"]
        )

        print(
            "Maturity Amount    :",
            Utils.format_currency(
                fd["maturity_amount"]
            )
        )

        print("=" * 60)
    # ======================================================
    # View All Fixed Deposits
    # ======================================================

    def view_all_fd(self):

        Utils.print_header("ALL FIXED DEPOSITS")

        query = """
        SELECT *
        FROM fixed_deposit
        ORDER BY start_date DESC
        """

        fds = db.fetch_all(query)

        if not fds:

            print("\nNo Fixed Deposits Found.")
            return

        print()

        print(
            "{:<8}{:<15}{:<15}{:<10}{:<15}".format(
                "FD ID",
                "Account",
                "Amount",
                "Rate",
                "Maturity"
            )
        )

        print("-" * 75)

        for fd in fds:

            print(
                "{:<8}{:<15}{:<15}{:<10}{:<15}".format(
                    fd["fd_id"],
                    fd["account_number"],
                    f"₹{fd['amount']}",
                    f"{fd['interest_rate']}%",
                    str(fd["maturity_date"])
                )
            )

    # ======================================================
    # View Account Fixed Deposits
    # ======================================================

    def view_account_fd(self):

        Utils.print_header("ACCOUNT FIXED DEPOSITS")

        account_number = input(
            "Account Number : "
        ).strip()

        account = self.account_exists(account_number)

        if account is None:

            print("\nAccount Not Found.")
            return

        query = """
        SELECT *
        FROM fixed_deposit
        WHERE account_number=%s
        ORDER BY start_date DESC
        """

        fds = db.fetch_all(
            query,
            (account_number,)
        )

        if not fds:

            print("\nNo Fixed Deposits Found.")
            return

        print()

        print(
            "{:<8}{:<15}{:<15}{:<10}{:<15}".format(
                "FD ID",
                "Amount",
                "Rate",
                "Months",
                "Maturity"
            )
        )

        print("-" * 75)

        for fd in fds:

            print(
                "{:<8}{:<15}{:<10}{:<10}{:<15}".format(
                    fd["fd_id"],
                    f"₹{fd['amount']}",
                    f"{fd['interest_rate']}%",
                    fd["tenure_months"],
                    str(fd["maturity_date"])
                )
            )

    # ======================================================
    # Search Fixed Deposits using Account Number
    # ======================================================

    def search_fd_by_account(self):

        Utils.print_header("SEARCH FIXED DEPOSITS")

        account_number = input(
            "Account Number : "
        ).strip()

        query = """
        SELECT *
        FROM fixed_deposit
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

        print()

        for fd in records:

            print("=" * 60)

            print("FD Number        :", fd["fd_id"])

            print("Amount           :",
                  Utils.format_currency(fd["amount"]))

            print("Interest Rate    :",
                  f"{fd['interest_rate']}%")

            print("Tenure           :",
                  fd["tenure_months"], "Months")

            print("Start Date       :",
                  fd["start_date"])

            print("Maturity Date    :",
                  fd["maturity_date"])

            print("Maturity Amount  :",
                  Utils.format_currency(
                      fd["maturity_amount"]
                  ))

        print("=" * 60)

    # ======================================================
    # Total Fixed Deposits
    # ======================================================

    def total_fd(self):

        query = """
        SELECT COUNT(*) AS total
        FROM fixed_deposit
        """

        row = db.fetch_one(query)

        if row:
            return row["total"]

        return 0

    # ======================================================
    # Total FD Amount
    # ======================================================

    def total_fd_amount(self):

        query = """
        SELECT SUM(amount) AS total
        FROM fixed_deposit
        """

        row = db.fetch_one(query)

        if row and row["total"] is not None:
            return float(row["total"])

        return 0.0
    # ======================================================
    # FD Statistics
    # ======================================================

    def fd_statistics(self):

        Utils.print_header("FIXED DEPOSIT STATISTICS")

        print()

        print("Total Fixed Deposits :",
              self.total_fd())

        print(
            "Total Investment     :",
            Utils.format_currency(
                self.total_fd_amount()
            )
        )

        query = """
        SELECT AVG(amount) AS average_amount
        FROM fixed_deposit
        """

        row = db.fetch_one(query)

        average = 0

        if row and row["average_amount"] is not None:
            average = float(row["average_amount"])

        print(
            "Average FD Amount    :",
            Utils.format_currency(average)
        )

        print()

    # ======================================================
    # FD Maturity Calculator
    # ======================================================

    def maturity_calculator(self):

        Utils.print_header("FD MATURITY CALCULATOR")

        try:

            amount = float(
                input("Deposit Amount : ")
            )

            if not Validator.validate_amount(amount):
                print("Invalid Amount.")
                return

            months = int(
                input("Tenure (Months) : ")
            )

            if not Validator.validate_tenure(months):
                print("Invalid Tenure.")
                return

        except ValueError:

            print("Invalid Input.")
            return

        maturity = Utils.calculate_fd_maturity(
            amount,
            FD_INTEREST_RATE,
            months
        )

        print()

        print("=" * 50)

        print("FD CALCULATION")

        print("=" * 50)

        print(
            "Deposit Amount :",
            Utils.format_currency(amount)
        )

        print(
            "Interest Rate  :",
            f"{FD_INTEREST_RATE}%"
        )

        print(
            "Tenure         :",
            months,
            "Months"
        )

        print(
            "Maturity Value :",
            Utils.format_currency(maturity)
        )

        print("=" * 50)

    # ======================================================
    # Display Interest Rate
    # ======================================================

    def display_interest_rate(self):

        Utils.print_header("FIXED DEPOSIT INTEREST RATE")

        print()

        print(
            f"Current FD Interest Rate : "
            f"{FD_INTEREST_RATE}%"
        )

        print()

    # ======================================================
    # Admin Summary
    # ======================================================

    def summary(self):

        Utils.print_header("FD SUMMARY")

        print(
            "Total FD Accounts :",
            self.total_fd()
        )

        print(
            "Total Investment  :",
            Utils.format_currency(
                self.total_fd_amount()
            )
        )

    # ======================================================
    # Get Total FD Count
    # ======================================================

    def get_total_fd(self):

        return self.total_fd()

    # ======================================================
    # Get Total FD Investment
    # ======================================================

    def get_total_investment(self):

        return self.total_fd_amount()

    # ======================================================
    # FD Menu
    # ======================================================

    def menu(self):

        while True:

            Utils.print_header("FIXED DEPOSIT MENU")

            print("1. Open Fixed Deposit")
            print("2. View Fixed Deposit")
            print("3. View All Fixed Deposits")
            print("4. View Account Fixed Deposits")
            print("5. Search FD By Account")
            print("6. FD Statistics")
            print("7. Maturity Calculator")
            print("8. Interest Rate")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.open_fd()

            elif choice == "2":

                self.view_fd()

            elif choice == "3":

                self.view_all_fd()

            elif choice == "4":

                self.view_account_fd()

            elif choice == "5":

                self.search_fd_by_account()

            elif choice == "6":

                self.fd_statistics()

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
    # Get FD Details
    # ======================================================

    def get_fd(self, fd_id):

        query = """
        SELECT *
        FROM fixed_deposit
        WHERE fd_id=%s
        """

        return db.fetch_one(query, (fd_id,))

    # ======================================================
    # Check Whether Account Has FD
    # ======================================================

    def account_has_fd(self, account_number):

        query = """
        SELECT COUNT(*) AS total
        FROM fixed_deposit
        WHERE account_number=%s
        """

        row = db.fetch_one(query, (account_number,))

        if row:
            return row["total"] > 0

        return False

    # ======================================================
    # Get Maturity Amount
    # ======================================================

    def get_maturity_amount(self, fd_id):

        fd = self.get_fd(fd_id)

        if fd is None:
            return None

        return float(fd["maturity_amount"])

    # ======================================================
    # Get Maturity Date
    # ======================================================

    def get_maturity_date(self, fd_id):

        fd = self.get_fd(fd_id)

        if fd is None:
            return None

        return fd["maturity_date"]

    # ======================================================
    # Display FD Receipt
    # ======================================================

    def print_receipt(self, fd_id):

        fd = self.get_fd(fd_id)

        if fd is None:

            print("\nFixed Deposit Not Found.")
            return

        Utils.print_header("FIXED DEPOSIT RECEIPT")

        print("FD Number         :", fd["fd_id"])

        print("Account Number    :", fd["account_number"])

        print(
            "Deposit Amount    :",
            Utils.format_currency(
                fd["amount"]
            )
        )

        print(
            "Interest Rate     :",
            f"{fd['interest_rate']}%"
        )

        print(
            "Tenure            :",
            fd["tenure_months"],
            "Months"
        )

        print(
            "Opening Date      :",
            fd["start_date"]
        )

        print(
            "Maturity Date     :",
            fd["maturity_date"]
        )

        print(
            "Maturity Amount   :",
            Utils.format_currency(
                fd["maturity_amount"]
            )
        )

        print("=" * 60)

    # ======================================================
    # Dashboard Summary
    # ======================================================

    def dashboard_summary(self):

        print()

        print("=" * 50)

        print("FIXED DEPOSIT SUMMARY")

        print("=" * 50)

        print(
            "Total FD Accounts :",
            self.total_fd()
        )

        print(
            "Total Investment  :",
            Utils.format_currency(
                self.total_fd_amount()
            )
        )

        print("=" * 50)

    # ======================================================
    # Refresh Connection
    # ======================================================

    def reconnect(self):

        if db.connection is None:

            db.connect()

    # ======================================================
    # Destructor
    # ======================================================

    def __del__(self):

        pass


if __name__ == "__main__":

    fd = FixedDeposit()

    fd.menu()
