"""
==========================================================
Banking Management System
File : transaction.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================
Handles:
1. Balance Enquiry
2. Deposit
3. Transaction Logging
==========================================================
"""

from database import db
from utils import Utils
from validations import Validator
from account import Account


class Transaction:

    def __init__(self):

        if db.connection is None:
            db.connect()

        self.account = Account()

    # ==================================================
    # Check Account
    # ==================================================

    def account_exists(self, account_number):

        query = """
        SELECT *
        FROM account
        WHERE account_number=%s
        """

        return db.fetch_one(query, (account_number,))

    # ==================================================
    # Current Balance
    # ==================================================

    def get_balance(self, account_number):

        query = """
        SELECT balance
        FROM account
        WHERE account_number=%s
        """

        row = db.fetch_one(query, (account_number,))

        if row:
            return float(row["balance"])

        return None

    # ==================================================
    # Balance Enquiry
    # ==================================================

    def balance_enquiry(self, account_number):

        account = self.account_exists(account_number)

        if account is None:

            print("\nAccount Not Found.")

            return

        Utils.print_header("BALANCE ENQUIRY")

        print("Account Number :", account_number)

        print(
            "Available Balance :",
            Utils.format_currency(account["balance"])
        )

    # ==================================================
    # Deposit Amount
    # ==================================================

    def deposit(self):

        Utils.print_header("DEPOSIT MONEY")

        account_number = input("Account Number : ").strip()

        account = self.account_exists(account_number)

        if account is None:

            print("\nAccount Not Found.")

            return

        if account["status"] != "Active":

            print("\nAccount is not active.")

            return

        amount = float(input("Deposit Amount : "))

        if not Validator.validate_amount(amount):

            print("Invalid Amount.")

            return

        current_balance = float(account["balance"])

        new_balance = current_balance + amount

        update_query = """
        UPDATE account
        SET balance=%s
        WHERE account_number=%s
        """

        if db.execute(update_query, (new_balance, account_number)):

            self.record_transaction(
                account_number=account_number,
                transaction_type="Deposit",
                amount=amount,
                balance=new_balance,
                description="Cash Deposit"
            )

            print()

            print("=" * 50)
            print("DEPOSIT SUCCESSFUL")
            print("=" * 50)

            print("Deposited Amount :",
                  Utils.format_currency(amount))

            print("Current Balance  :",
                  Utils.format_currency(new_balance))

            print("=" * 50)

        else:

            print("Unable to Deposit Amount.")

    # ==================================================
    # Record Transaction
    # ==================================================

    def record_transaction(
            self,
            account_number,
            transaction_type,
            amount,
            balance,
            description
    ):

        query = """
        INSERT INTO transactions
        (
            account_number,
            transaction_type,
            amount,
            balance_after,
            description
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        values = (
            account_number,
            transaction_type,
            amount,
            balance,
            description
        )

        db.execute(query, values)

    # ==================================================
    # Print Deposit Receipt
    # ==================================================

    def print_receipt(
            self,
            account_number,
            transaction_type,
            amount,
            balance
    ):

        Utils.print_header("TRANSACTION RECEIPT")

        print("Receipt No      :", Utils.generate_receipt_number())
        print("Transaction     :", transaction_type)
        print("Account Number  :", account_number)
        print("Amount          :", Utils.format_currency(amount))
        print("Balance         :", Utils.format_currency(balance))
        print("Date            :", Utils.current_date())
        print("Time            :", Utils.current_time())

        print("=" * 50)

    # ==================================================
    # Deposit With Receipt
    # ==================================================

    def deposit_with_receipt(self):

        Utils.print_header("DEPOSIT MONEY")

        account_number = input("Account Number : ").strip()

        account = self.account_exists(account_number)

        if account is None:

            print("Account Not Found.")

            return

        amount = float(input("Deposit Amount : "))

        if not Validator.validate_amount(amount):

            print("Invalid Amount.")

            return

        current_balance = float(account["balance"])

        new_balance = current_balance + amount

        query = """
        UPDATE account
        SET balance=%s
        WHERE account_number=%s
        """

        if db.execute(query, (new_balance, account_number)):

            self.record_transaction(
                account_number,
                "Deposit",
                amount,
                new_balance,
                "Cash Deposit"
            )

            self.print_receipt(
                account_number,
                "Deposit",
                amount,
                new_balance
            )

        else:

            print("Transaction Failed.")
    # ==================================================
    # Withdraw Amount
    # ==================================================

    def withdraw(self):

        Utils.print_header("WITHDRAW MONEY")

        account_number = input("Account Number : ").strip()

        account = self.account_exists(account_number)

        if account is None:

            print("\nAccount Not Found.")

            return

        if account["status"] != "Active":

            print("\nAccount is not Active.")

            return

        amount = float(input("Withdrawal Amount : "))

        if not Validator.validate_amount(amount):

            print("Invalid Amount.")

            return

        current_balance = float(account["balance"])

        # Minimum balance check

        if account["account_type"] == "Savings":

            minimum_balance = 1000

        else:

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

        new_balance = current_balance - amount

        update_query = """
        UPDATE account
        SET balance=%s
        WHERE account_number=%s
        """

        if db.execute(update_query, (new_balance, account_number)):

            self.record_transaction(
                account_number,
                "Withdraw",
                amount,
                new_balance,
                "Cash Withdrawal"
            )

            self.print_receipt(
                account_number,
                "Withdrawal",
                amount,
                new_balance
            )

            print("\nWithdrawal Successful.")

        else:

            print("Transaction Failed.")

    # ==================================================
    # Fund Transfer
    # ==================================================

    def transfer(self):

        Utils.print_header("FUND TRANSFER")

        sender = input("Sender Account Number : ").strip()

        sender_account = self.account_exists(sender)

        if sender_account is None:

            print("Sender Account Not Found.")

            return

        if sender_account["status"] != "Active":

            print("Sender Account is not Active.")

            return

        receiver = input("Receiver Account Number : ").strip()

        receiver_account = self.account_exists(receiver)

        if receiver_account is None:

            print("Receiver Account Not Found.")

            return

        if receiver_account["status"] != "Active":

            print("Receiver Account is not Active.")

            return

        if sender == receiver:

            print("Cannot transfer to the same account.")

            return

        amount = float(input("Transfer Amount : "))

        if not Validator.validate_amount(amount):

            print("Invalid Amount.")

            return

        sender_balance = float(sender_account["balance"])

        receiver_balance = float(receiver_account["balance"])

        if sender_account["account_type"] == "Savings":

            minimum_balance = 1000

        else:

            minimum_balance = 5000

        if sender_balance - amount < minimum_balance:

            print()

            print("Insufficient Balance.")

            return

        new_sender_balance = sender_balance - amount

        new_receiver_balance = receiver_balance + amount

        try:

            db.begin()

            db.execute(
                """
                UPDATE account
                SET balance=%s
                WHERE account_number=%s
                """,
                (
                    new_sender_balance,
                    sender
                )
            )

            db.execute(
                """
                UPDATE account
                SET balance=%s
                WHERE account_number=%s
                """,
                (
                    new_receiver_balance,
                    receiver
                )
            )

            self.record_transaction(
                sender,
                "Transfer",
                amount,
                new_sender_balance,
                f"Transferred to {receiver}"
            )

            self.record_transaction(
                receiver,
                "Deposit",
                amount,
                new_receiver_balance,
                f"Received from {sender}"
            )

            db.commit()

            print()

            print("=" * 55)
            print("FUND TRANSFER SUCCESSFUL")
            print("=" * 55)

            print("From Account :", sender)

            print("To Account   :", receiver)

            print(
                "Amount       :",
                Utils.format_currency(amount)
            )

            print(
                "Remaining Balance :",
                Utils.format_currency(new_sender_balance)
            )

            print("=" * 55)

        except Exception as e:

            db.rollback()

            print("Transfer Failed.")

            print(e)

    # ==================================================
    # Internal Balance Update
    # ==================================================

    def update_balance(
            self,
            account_number,
            new_balance
    ):

        query = """
        UPDATE account
        SET balance=%s
        WHERE account_number=%s
        """

        return db.execute(
            query,
            (
                new_balance,
                account_number
            )
        )

    # ==================================================
    # Get Customer Name
    # ==================================================

    def get_customer_name(self, account_number):

        query = """
        SELECT

            c.first_name,
            c.last_name

        FROM customer c

        INNER JOIN account a

        ON c.customer_id = a.customer_id

        WHERE a.account_number=%s
        """

        row = db.fetch_one(
            query,
            (
                account_number,
            )
        )

        if row:

            return (
                row["first_name"]
                + " "
                + row["last_name"]
            )

        return ""

    # ==================================================
    # Transfer Receipt
    # ==================================================

    def transfer_receipt(
            self,
            sender,
            receiver,
            amount,
            balance
    ):

        Utils.print_header("TRANSFER RECEIPT")

        print(
            "Receipt No     :",
            Utils.generate_receipt_number()
        )

        print("Sender         :", sender)

        print("Receiver       :", receiver)

        print("Amount         :", Utils.format_currency(amount))

        print(
            "Balance        :",
            Utils.format_currency(balance)
        )

        print("Date           :", Utils.current_date())

        print("Time           :", Utils.current_time())

        print("=" * 60)
