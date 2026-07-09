"""
==========================================================
Banking Management System
File : beneficiary.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================

Beneficiary Management

1. Add Beneficiary
2. Delete Beneficiary
3. View Beneficiaries
4. Search Beneficiary
5. Verify Beneficiary
6. Transfer Validation

==========================================================
"""

from database import db
from utils import Utils
from validations import Validator
from account import Account


class Beneficiary:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        if db.connection is None:
            db.connect()

        self.account = Account()

    # ======================================================
    # Check Beneficiary Exists
    # ======================================================

    def beneficiary_exists(
        self,
        account_number,
        beneficiary_account
    ):

        query = """
        SELECT *
        FROM beneficiary
        WHERE account_number=%s
        AND beneficiary_account=%s
        """

        return db.fetch_one(
            query,
            (
                account_number,
                beneficiary_account
            )
        )

    # ======================================================
    # Verify Account Exists
    # ======================================================

    def account_exists(
        self,
        account_number
    ):

        query = """
        SELECT *
        FROM account
        WHERE account_number=%s
        """

        return db.fetch_one(
            query,
            (account_number,)
        )

    # ======================================================
    # Add Beneficiary
    # ======================================================

    def add_beneficiary(self):

        Utils.print_header(
            "ADD BENEFICIARY"
        )

        owner_account = input(
            "Your Account Number : "
        ).strip()

        owner = self.account_exists(
            owner_account
        )

        if owner is None:

            print("\nAccount Not Found.")
            return

        beneficiary_account = input(
            "Beneficiary Account Number : "
        ).strip()

        if beneficiary_account == owner_account:

            print(
                "\nCannot Add Own Account."
            )

            return

        beneficiary = self.account_exists(
            beneficiary_account
        )

        if beneficiary is None:

            print(
                "\nBeneficiary Account Does Not Exist."
            )

            return

        if self.beneficiary_exists(
            owner_account,
            beneficiary_account
        ):

            print(
                "\nBeneficiary Already Exists."
            )

            return

        query = """
SELECT first_name,
       last_name
FROM customer
WHERE customer_id=%s
"""

        row = db.fetch_one(
        query,
        (beneficiary["customer_id"],)
        )
        if row is None:
            print("\nCustomer Record Not Found.")
            return
        beneficiary_name = (
            f"{row['first_name']} "
            f"{row['last_name'] or ''}"
            ).strip()
        print()
        print("=" * 50)
        print("BENEFICIARY DETAILS")
        print("=" * 50)
        print(
            "Account Number :",
            beneficiary_account
            )
        print(
            "Name           :",
            beneficiary_name
            )
        print("=" * 50)
        choice = input(
            "\nConfirm Add? (Y/N): "
            ).upper()
        if choice != "Y":
            print("\nOperation Cancelled.")
            return
        insert_query = """
        INSERT INTO beneficiary
        (
            account_number,
            beneficiary_account,
            beneficiary_name,
            added_date
        )
        VALUES
        (
            %s,
            %s,
            %s,
            CURDATE()
        )
        """
        values = (

            owner_account,

            beneficiary_account,

            beneficiary_name
            )
        if not db.execute(insert_query, values):
            print("\nUnable to Add Beneficiary.")
            return
        beneficiary_id = db.last_insert_id()
        Utils.print_header("BENEFICIARY ADDED")
        print("Beneficiary ID     :", beneficiary_id)
        print("Owner Account      :", owner_account)
        print("Beneficiary Account:", beneficiary_account)
        print("Beneficiary Name   :", beneficiary_name)
        print("Added Date         :", Utils.current_date())
        print()
        print("Beneficiary Added Successfully.")

    # ======================================================
    # Search Beneficiary
    # ======================================================

def search_beneficiary(self, beneficiary_id):

        query = """
        SELECT *
        FROM beneficiary
        WHERE beneficiary_id=%s
        """

        return db.fetch_one(query, (beneficiary_id,))

    # ======================================================
    # View Beneficiary
    # ======================================================

def view_beneficiary(self):

        Utils.print_header("VIEW BENEFICIARY")

        try:

            beneficiary_id = int(
                input("Beneficiary ID : ")
            )

        except ValueError:

            print("Invalid Beneficiary ID.")
            return

        beneficiary = self.search_beneficiary(
            beneficiary_id
        )

        if beneficiary is None:

            print("\nBeneficiary Not Found.")
            return

        print()

        print("=" * 60)

        print("BENEFICIARY DETAILS")

        print("=" * 60)

        print(
            "Beneficiary ID     :",
            beneficiary["beneficiary_id"]
        )

        print(
            "Owner Account      :",
            beneficiary["account_number"]
        )

        print(
            "Beneficiary Account:",
            beneficiary["beneficiary_account"]
        )

        print(
            "Beneficiary Name   :",
            beneficiary["beneficiary_name"]
        )

        print(
            "Added Date         :",
            beneficiary["added_date"]
        )

        print("=" * 60)

    # ======================================================
    # Delete Beneficiary
    # ======================================================

def delete_beneficiary(self):

        Utils.print_header("DELETE BENEFICIARY")

        try:

            beneficiary_id = int(
                input("Beneficiary ID : ")
            )

        except ValueError:

            print("Invalid Beneficiary ID.")
            return

        beneficiary = self.search_beneficiary(
            beneficiary_id
        )

        if beneficiary is None:

            print("\nBeneficiary Not Found.")
            return

        choice = input(
            "\nDelete this Beneficiary? (Y/N): "
        ).upper()

        if choice != "Y":

            print("\nOperation Cancelled.")
            return

        query = """
        DELETE FROM beneficiary
        WHERE beneficiary_id=%s
        """

        if db.execute(query, (beneficiary_id,)):

            print("\nBeneficiary Deleted Successfully.")

        else:

            print("\nUnable to Delete Beneficiary.")
    # ======================================================
    # View All Beneficiaries
    # ======================================================

def view_all_beneficiaries(self):

        Utils.print_header("ALL BENEFICIARIES")

        query = """
        SELECT *
        FROM beneficiary
        ORDER BY added_date DESC
        """

        beneficiaries = db.fetch_all(query)

        if not beneficiaries:

            print("\nNo Beneficiaries Found.")
            return

        print()

        print(
            "{:<8}{:<15}{:<15}{:<20}".format(
                "ID",
                "Owner A/C",
                "Beneficiary",
                "Name"
            )
        )

        print("-" * 70)

        for beneficiary in beneficiaries:

            print(
                "{:<8}{:<15}{:<15}{:<20}".format(
                    beneficiary["beneficiary_id"],
                    beneficiary["account_number"],
                    beneficiary["beneficiary_account"],
                    beneficiary["beneficiary_name"]
                )
            )

    # ======================================================
    # View Beneficiaries of an Account
    # ======================================================

def view_account_beneficiaries(self):

        Utils.print_header("ACCOUNT BENEFICIARIES")

        account_number = input(
            "Account Number : "
        ).strip()

        if self.account_exists(account_number) is None:

            print("\nAccount Not Found.")
            return

        query = """
        SELECT *
        FROM beneficiary
        WHERE account_number=%s
        ORDER BY beneficiary_name
        """

        beneficiaries = db.fetch_all(
            query,
            (account_number,)
        )

        if not beneficiaries:

            print("\nNo Beneficiaries Found.")
            return

        print()

        print(
            "{:<8}{:<18}{:<25}".format(
                "ID",
                "Beneficiary A/C",
                "Name"
            )
        )

        print("-" * 60)

        for beneficiary in beneficiaries:

            print(
                "{:<8}{:<18}{:<25}".format(
                    beneficiary["beneficiary_id"],
                    beneficiary["beneficiary_account"],
                    beneficiary["beneficiary_name"]
                )
            )

    # ======================================================
    # Search Beneficiaries by Account
    # ======================================================

def search_by_account(self):

        Utils.print_header("SEARCH BENEFICIARIES")

        account_number = input(
            "Account Number : "
        ).strip()

        query = """
        SELECT *
        FROM beneficiary
        WHERE account_number=%s
        """

        records = db.fetch_all(
            query,
            (account_number,)
        )

        if not records:

            print("\nNo Beneficiaries Found.")
            return

        print()

        for beneficiary in records:

            print("=" * 60)

            print(
                "Beneficiary ID      :",
                beneficiary["beneficiary_id"]
            )

            print(
                "Beneficiary Account :",
                beneficiary["beneficiary_account"]
            )

            print(
                "Beneficiary Name    :",
                beneficiary["beneficiary_name"]
            )

            print(
                "Added Date          :",
                beneficiary["added_date"]
            )

        print("=" * 60)

    # ======================================================
    # Verify Beneficiary
    # ======================================================

def verify_beneficiary(
        self,
        account_number,
        beneficiary_account
    ):

        query = """
        SELECT *
        FROM beneficiary
        WHERE account_number=%s
        AND beneficiary_account=%s
        """

        beneficiary = db.fetch_one(
            query,
            (
                account_number,
                beneficiary_account
            )
        )

        return beneficiary is not None

    # ======================================================
    # Total Beneficiaries
    # ======================================================

def total_beneficiaries(self):

        query = """
        SELECT COUNT(*) AS total
        FROM beneficiary
        """

        row = db.fetch_one(query)

        if row:

            return row["total"]

        return 0


    # ======================================================
    # Get Beneficiary Details
    # ======================================================

def get_beneficiary(self, beneficiary_id):

        return self.search_beneficiary(
            beneficiary_id
        )

    # ======================================================
    # Check Whether Account Has Beneficiaries
    # ======================================================

def account_has_beneficiary(
        self,
        account_number
    ):

        return (
            self.total_account_beneficiaries(
                account_number
            ) > 0
        )

    # ======================================================
    # Print Beneficiary Receipt
    # ======================================================

def print_receipt(
        self,
        beneficiary_id
    ):

        beneficiary = self.get_beneficiary(
            beneficiary_id
        )

        if beneficiary is None:

            print("\nBeneficiary Not Found.")

            return

        Utils.print_header(
            "BENEFICIARY RECEIPT"
        )

        print(
            "Beneficiary ID      :",
            beneficiary["beneficiary_id"]
        )

        print(
            "Owner Account       :",
            beneficiary["account_number"]
        )

        print(
            "Beneficiary Account :",
            beneficiary["beneficiary_account"]
        )

        print(
            "Beneficiary Name    :",
            beneficiary["beneficiary_name"]
        )

        print(
            "Added Date          :",
            beneficiary["added_date"]
        )

        print("=" * 60)

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
