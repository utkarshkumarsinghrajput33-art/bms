"""
==========================================================
Banking Management System
File : account.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================
Handles:
1. Customer Creation
2. Account Creation
3. Account Search
4. Customer Search
==========================================================
"""

from database import db
from validations import Validator
from utils import Utils


class Account:

    def __init__(self):

        if db.connection is None:
            db.connect()

    # ==================================================
    # Generate Unique Account Number
    # ==================================================

    def generate_account_number(self):

        while True:

            account_number = Utils.generate_account_number()

            query = """
            SELECT account_number
            FROM account
            WHERE account_number=%s
            """

            row = db.fetch_one(query, (account_number,))

            if row is None:
                return account_number

    # ==================================================
    # Create Customer
    # ==================================================

    def create_customer(self):

        Utils.print_header("CREATE NEW CUSTOMER")

        first_name = input("First Name          : ").strip()

        if not Validator.validate_name(first_name):
            print("Invalid First Name.")
            return None

        last_name = input("Last Name           : ").strip()

        if not Validator.validate_name(last_name):
            print("Invalid Last Name.")
            return None

        gender = input("Gender (Male/Female/Other): ").strip()

        if not Validator.validate_gender(gender):
            print("Invalid Gender.")
            return None

        dob = input("Date of Birth (YYYY-MM-DD): ").strip()

        if not Validator.validate_dob(dob):
            print("Customer must be at least 18 years old.")
            return None

        mobile = input("Mobile Number       : ").strip()

        if not Validator.validate_mobile(mobile):
            print("Invalid Mobile Number.")
            return None

        email = input("Email               : ").strip()

        if not Validator.validate_email(email):
            print("Invalid Email.")
            return None

        aadhaar = input("Aadhaar Number      : ").strip()

        if not Validator.validate_aadhaar(aadhaar):
            print("Invalid Aadhaar Number.")
            return None

        pan = input("PAN Number          : ").strip().upper()

        if not Validator.validate_pan(pan):
            print("Invalid PAN Number.")
            return None

        address = input("Address             : ").strip()

        city = input("City                : ").strip()

        state = input("State               : ").strip()

        pincode = input("Pincode             : ").strip()

        if not Validator.validate_pincode(pincode):
            print("Invalid Pincode.")
            return None

        # --------------------------------------------
        # Duplicate Checks
        # --------------------------------------------

        query = """
        SELECT customer_id
        FROM customer
        WHERE mobile=%s
        OR email=%s
        OR aadhaar=%s
        OR pan=%s
        """

        duplicate = db.fetch_one(
            query,
            (
                mobile,
                email,
                aadhaar,
                pan
            )
        )

        if duplicate:

            print("\nCustomer already exists.")

            return None

        # --------------------------------------------
        # Insert Customer
        # --------------------------------------------

        query = """
        INSERT INTO customer
        (
            first_name,
            last_name,
            gender,
            dob,
            mobile,
            email,
            aadhaar,
            pan,
            address,
            city,
            state,
            pincode
        )

        VALUES
        (
            %s,%s,%s,%s,
            %s,%s,%s,%s,
            %s,%s,%s,%s
        )
        """

        values = (
            first_name,
            last_name,
            gender,
            dob,
            mobile,
            email,
            aadhaar,
            pan,
            address,
            city,
            state,
            pincode
        )

        if db.execute(query, values):

            customer_id = db.last_insert_id()

            print()

            print("Customer Created Successfully.")

            print("Customer ID :", customer_id)

            return customer_id

        print("Unable to Create Customer.")

        return None

    # ==================================================
    # Create Account
    # ==================================================

    def create_account(self):

        Utils.print_header("CREATE NEW ACCOUNT")

        customer_id = self.create_customer()

        if customer_id is None:
            return

        print()

        print("Available Branches")

        branches = db.fetch_all(
            """
            SELECT *
            FROM branch
            ORDER BY branch_id
            """
        )

        for branch in branches:

            print(
                f"{branch['branch_id']}. "
                f"{branch['branch_name']} "
                f"({branch['ifsc_code']})"
            )

        print()

        branch_id = int(input("Branch ID : "))

        account_type = input(
            "Account Type (Savings/Current): "
        ).capitalize()

        if not Validator.validate_account_type(account_type):

            print("Invalid Account Type.")

            return

        opening_balance = float(
            input("Opening Balance : ")
        )

        if not Validator.validate_amount(opening_balance):

            print("Invalid Amount.")

            return

        atm_pin = input("ATM PIN (4 digits): ")

        if not Validator.validate_atm_pin(atm_pin):

            print("Invalid ATM PIN.")

            return

        password = input("Login Password : ")

        if not Validator.is_not_empty(password):
            print("Password cannot be empty.")
            return

            print("Password does not satisfy requirements.")

            return

        account_number = self.generate_account_number()

        query = """
        INSERT INTO account
        (
            account_number,
            customer_id,
            branch_id,
            account_type,
            balance,
            opening_date,
            status,
            atm_pin,
            login_password
        )

        VALUES
        (
            %s,%s,%s,%s,
            %s,CURDATE(),
            'Active',
            %s,%s
        )
        """

        values = (
            account_number,
            customer_id,
            branch_id,
            account_type,
            opening_balance,
            atm_pin,
            password
        )

        if db.execute(query, values):

            db.execute(
                """
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
                    'Deposit',
                    %s,
                    %s,
                    'Opening Balance'
                )
                """,
                (
                    account_number,
                    opening_balance,
                    opening_balance
                )
            )

            print()

            print("=" * 45)

            print("ACCOUNT CREATED SUCCESSFULLY")

            print("=" * 45)

            print("Customer ID   :", customer_id)

            print("Account No    :", account_number)

            print("Account Type  :", account_type)

            print(
                "Balance       :",
                Utils.format_currency(opening_balance)
            )

            print("=" * 45)

        else:

            print("Unable to Create Account.")

    # ==================================================
    # Search Account
    # ==================================================

    def search_account(self, account_number):

        query = """
        SELECT *
        FROM account
        WHERE account_number=%s
        """

        return db.fetch_one(
            query,
            (account_number,)
        )

    # ==================================================
    # Search Customer
    # ==================================================

    def search_customer(self, customer_id):

        query = """
        SELECT *
        FROM customer
        WHERE customer_id=%s
        """

        return db.fetch_one(
            query,
            (customer_id,)
        )
    # ==================================================
    # View Complete Account Details
    # ==================================================

    def view_account(self, account_number):

        query = """
        SELECT
            a.account_number,
            a.account_type,
            a.balance,
            a.status,
            a.opening_date,
            a.atm_pin,

            c.customer_id,
            c.first_name,
            c.last_name,
            c.gender,
            c.dob,
            c.mobile,
            c.email,
            c.aadhaar,
            c.pan,
            c.address,
            c.city,
            c.state,
            c.pincode,

            b.branch_name,
            b.ifsc_code

        FROM account a

        INNER JOIN customer c
        ON a.customer_id = c.customer_id

        INNER JOIN branch b
        ON a.branch_id = b.branch_id

        WHERE a.account_number=%s
        """

        account = db.fetch_one(query, (account_number,))

        if account is None:

            print("\nAccount Not Found.")

            return

        Utils.print_header("ACCOUNT DETAILS")

        print(f"Customer ID        : {account['customer_id']}")
        print(f"Customer Name      : {account['first_name']} {account['last_name']}")
        print(f"Gender             : {account['gender']}")
        print(f"DOB                : {account['dob']}")
        print(f"Mobile             : {account['mobile']}")
        print(f"Email              : {account['email']}")
        print(f"Aadhaar            : {account['aadhaar']}")
        print(f"PAN                : {account['pan']}")
        print(f"Address            : {account['address']}")
        print(f"City               : {account['city']}")
        print(f"State              : {account['state']}")
        print(f"Pincode            : {account['pincode']}")

        print("-" * 60)

        print(f"Account Number     : {account['account_number']}")
        print(f"Account Type       : {account['account_type']}")
        print(f"Opening Date       : {account['opening_date']}")
        print(f"Balance            : {Utils.format_currency(account['balance'])}")
        print(f"Status             : {account['status']}")
        print(f"Branch             : {account['branch_name']}")
        print(f"IFSC               : {account['ifsc_code']}")

    # ==================================================
    # Update Customer Details
    # ==================================================

    def update_customer(self, customer_id):

        customer = self.search_customer(customer_id)

        if customer is None:

            print("Customer Not Found.")

            return

        Utils.print_header("UPDATE CUSTOMER")

        mobile = input(
            f"Mobile [{customer['mobile']}]: "
        ).strip()

        email = input(
            f"Email [{customer['email']}]: "
        ).strip()

        address = input(
            f"Address [{customer['address']}]: "
        ).strip()

        city = input(
            f"City [{customer['city']}]: "
        ).strip()

        state = input(
            f"State [{customer['state']}]: "
        ).strip()

        pincode = input(
            f"Pincode [{customer['pincode']}]: "
        ).strip()

        if mobile:

            if not Validator.validate_mobile(mobile):

                print("Invalid Mobile Number.")

                return

        else:
            mobile = customer["mobile"]

        if email:

            if not Validator.validate_email(email):

                print("Invalid Email.")

                return

        else:
            email = customer["email"]

        if not address:
            address = customer["address"]

        if not city:
            city = customer["city"]

        if not state:
            state = customer["state"]

        if pincode:

            if not Validator.validate_pincode(pincode):

                print("Invalid Pincode.")

                return

        else:
            pincode = customer["pincode"]

        query = """
        UPDATE customer

        SET

        mobile=%s,
        email=%s,
        address=%s,
        city=%s,
        state=%s,
        pincode=%s

        WHERE customer_id=%s
        """

        values = (
            mobile,
            email,
            address,
            city,
            state,
            pincode,
            customer_id
        )

        if db.execute(query, values):

            print("\nCustomer Updated Successfully.")

        else:

            print("\nUnable to Update Customer.")

    # ==================================================
    # Freeze Account
    # ==================================================

    def freeze_account(self, account_number):

        account = self.search_account(account_number)

        if account is None:

            print("Account Not Found.")

            return

        if account["status"] == "Frozen":

            print("Account Already Frozen.")

            return

        query = """
        UPDATE account
        SET status='Frozen'
        WHERE account_number=%s
        """

        if db.execute(query, (account_number,)):

            print("Account Frozen Successfully.")

    # ==================================================
    # Activate Account
    # ==================================================

    def activate_account(self, account_number):

        account = self.search_account(account_number)

        if account is None:

            print("Account Not Found.")

            return

        if account["status"] == "Active":

            print("Account Already Active.")

            return

        query = """
        UPDATE account
        SET status='Active'
        WHERE account_number=%s
        """

        if db.execute(query, (account_number,)):

            print("Account Activated Successfully.")

    # ==================================================
    # Close Account
    # ==================================================

    def close_account(self, account_number):

        account = self.search_account(account_number)

        if account is None:

            print("Account Not Found.")

            return

        if account["balance"] > 0:

            print()

            print(
                "Account cannot be closed."

            )

            print(
                "Please withdraw remaining balance first."

            )

            return

        query = """
        UPDATE account
        SET status='Closed'
        WHERE account_number=%s
        """

        if db.execute(query, (account_number,)):

            print("Account Closed Successfully.")

    # ==================================================
    # Delete Customer Account
    # ==================================================

    def delete_account(self, account_number):

        account = self.search_account(account_number)

        if account is None:

            print("Account Not Found.")

            return

        if not Utils.confirm(
            "Are you sure you want to delete this account?"
        ):

            print("Operation Cancelled.")

            return

        query = """
        DELETE FROM account
        WHERE account_number=%s
        """

        if db.execute(query, (account_number,)):

            print("Account Deleted Successfully.")

    # ==================================================
    # Check Account Exists
    # ==================================================

    def account_exists(self, account_number):

        query = """
        SELECT account_number
        FROM account
        WHERE account_number=%s
        """

        return db.record_exists(query, (account_number,))

    # ==================================================
    # Check Customer Exists
    # ==================================================

    def customer_exists(self, customer_id):

        query = """
        SELECT customer_id
        FROM customer
        WHERE customer_id=%s
        """

        return db.record_exists(query, (customer_id,))
    # ==================================================
    # View All Customers
    # ==================================================

    def view_all_customers(self):

        query = """
        SELECT
            customer_id,
            first_name,
            last_name,
            mobile,
            email,
            city,
            state
        FROM customer
        ORDER BY customer_id
        """

        customers = db.fetch_all(query)

        if not customers:

            print("\nNo Customers Found.")
            return

        Utils.print_header("CUSTOMER LIST")

        print(
            "{:<6} {:<25} {:<12} {:<30} {:<15}".format(
                "ID",
                "Customer Name",
                "Mobile",
                "Email",
                "City"
            )
        )

        print("-" * 95)

        for customer in customers:

            full_name = (
                customer["first_name"] + " " +
                customer["last_name"]
            )

            print(
                "{:<6} {:<25} {:<12} {:<30} {:<15}".format(
                    customer["customer_id"],
                    full_name,
                    customer["mobile"],
                    customer["email"],
                    customer["city"]
                )
            )

    # ==================================================
    # View All Accounts
    # ==================================================

    def view_all_accounts(self):

        query = """
        SELECT

            a.account_number,
            a.account_type,
            a.balance,
            a.status,

            c.first_name,
            c.last_name

        FROM account a

        INNER JOIN customer c

        ON a.customer_id = c.customer_id

        ORDER BY a.account_number
        """

        accounts = db.fetch_all(query)

        if not accounts:

            print("\nNo Accounts Found.")
            return

        Utils.print_header("ACCOUNT LIST")

        print(
            "{:<15} {:<25} {:<10} {:<15} {:<10}".format(
                "Account No",
                "Customer",
                "Type",
                "Balance",
                "Status"
            )
        )

        print("-" * 90)

        for account in accounts:

            name = (
                account["first_name"] +
                " " +
                account["last_name"]
            )

            print(
                "{:<15} {:<25} {:<10} {:<15} {:<10}".format(
                    account["account_number"],
                    name,
                    account["account_type"],
                    Utils.format_currency(account["balance"]),
                    account["status"]
                )
            )

    # ==================================================
    # Search by Mobile
    # ==================================================

    def search_by_mobile(self, mobile):

        query = """
        SELECT *
        FROM customer
        WHERE mobile=%s
        """

        return db.fetch_one(query, (mobile,))

    # ==================================================
    # Search by Aadhaar
    # ==================================================

    def search_by_aadhaar(self, aadhaar):

        query = """
        SELECT *
        FROM customer
        WHERE aadhaar=%s
        """

        return db.fetch_one(query, (aadhaar,))

    # ==================================================
    # Search by PAN
    # ==================================================

    def search_by_pan(self, pan):

        query = """
        SELECT *
        FROM customer
        WHERE pan=%s
        """

        return db.fetch_one(query, (pan.upper(),))

    # ==================================================
    # Search by Name
    # ==================================================

    def search_by_name(self, keyword):

        query = """
        SELECT *

        FROM customer

        WHERE first_name LIKE %s

        OR last_name LIKE %s

        ORDER BY first_name
        """

        value = "%" + keyword + "%"

        customers = db.fetch_all(query, (value, value))

        if not customers:

            print("\nNo Matching Customer Found.")

            return

        Utils.print_header("SEARCH RESULT")

        for customer in customers:

            print("-" * 60)

            print("Customer ID :", customer["customer_id"])
            print(
                "Name        :",
                customer["first_name"],
                customer["last_name"]
            )
            print("Mobile      :", customer["mobile"])
            print("Email       :", customer["email"])
            print("City        :", customer["city"])

    # ==================================================
    # Branch Wise Accounts
    # ==================================================

    def branch_accounts(self, branch_id):

        query = """
        SELECT

            a.account_number,
            c.first_name,
            c.last_name,
            a.balance,
            a.status

        FROM account a

        INNER JOIN customer c

        ON a.customer_id = c.customer_id

        WHERE a.branch_id=%s

        ORDER BY c.first_name
        """

        accounts = db.fetch_all(query, (branch_id,))

        if not accounts:

            print("\nNo Accounts Found.")

            return

        Utils.print_header("BRANCH ACCOUNT LIST")

        for account in accounts:

            print("-" * 50)

            print("Account :", account["account_number"])
            print(
                "Customer:",
                account["first_name"],
                account["last_name"]
            )
            print(
                "Balance :",
                Utils.format_currency(account["balance"])
            )
            print("Status  :", account["status"])

    # ==================================================
    # Account Summary
    # ==================================================

    def account_summary(self):

        query = """
        SELECT

            COUNT(*) AS total_accounts,

            SUM(
                CASE
                    WHEN status='Active'
                    THEN 1
                    ELSE 0
                END
            ) AS active_accounts,

            SUM(
                CASE
                    WHEN status='Frozen'
                    THEN 1
                    ELSE 0
                END
            ) AS frozen_accounts,

            SUM(
                CASE
                    WHEN status='Closed'
                    THEN 1
                    ELSE 0
                END
            ) AS closed_accounts,

            SUM(balance) AS total_balance

        FROM account
        """

        summary = db.fetch_one(query)

        Utils.print_header("ACCOUNT SUMMARY")

        print("Total Accounts :", summary["total_accounts"])
        print("Active Accounts:", summary["active_accounts"])
        print("Frozen Accounts:", summary["frozen_accounts"])
        print("Closed Accounts:", summary["closed_accounts"])

        balance = summary["total_balance"] or 0

        print("Total Deposits :", Utils.format_currency(balance))
# ==================================================
# Testing
# ==================================================

if __name__ == "__main__":

    if db.connect():

        account = Account()

        while True:

            Utils.print_header("ACCOUNT MODULE TEST")

            print("1. Create Customer & Account")
            print("2. View Account")
            print("3. View All Customers")
            print("4. View All Accounts")
            print("5. Account Summary")
            print("6. Freeze Account")
            print("7. Activate Account")
            print("8. Exit")

            choice = input("\nEnter Choice : ")

            if choice == "1":

                account.create_account()

            elif choice == "2":

                number = input("Account Number : ")

                account.view_account(number)

            elif choice == "3":

                account.view_all_customers()

            elif choice == "4":

                account.view_all_accounts()

            elif choice == "5":

                account.account_summary()

            elif choice == "6":

                number = input("Account Number : ")

                account.freeze_account(number)

            elif choice == "7":

                number = input("Account Number : ")

                account.activate_account(number)

            elif choice == "8":

                print("\nThank You.")

                break

            else:

                print("Invalid Choice.")

            Utils.pause()

        db.disconnect()

    else:

        print("Database Connection Failed.")
