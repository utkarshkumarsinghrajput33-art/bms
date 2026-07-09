"""
==========================================================
Banking Management System
File : customer.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================

Customer Management Module

Features
--------
1. Add Customer
2. View Customer
3. Search Customer
4. Update Customer
5. Delete Customer
6. Customer Statistics

==========================================================
"""

from database import db
from utils import Utils
from validations import Validator


class Customer:

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        if db.connection is None:
            db.connect()

    # =====================================================
    # Customer Exists
    # =====================================================

    def customer_exists(self, customer_id):

        query = """
        SELECT *
        FROM customer
        WHERE customer_id=%s
        """

        return db.fetch_one(query, (customer_id,))

    # =====================================================
    # Mobile Exists
    # =====================================================

    def mobile_exists(self, mobile):

        query = """
        SELECT customer_id
        FROM customer
        WHERE mobile=%s
        """

        return db.fetch_one(query, (mobile,))

    # =====================================================
    # Aadhaar Exists
    # =====================================================

    def aadhaar_exists(self, aadhaar):

        query = """
        SELECT customer_id
        FROM customer
        WHERE aadhaar=%s
        """

        return db.fetch_one(query, (aadhaar,))

    # =====================================================
    # PAN Exists
    # =====================================================

    def pan_exists(self, pan):

        query = """
        SELECT customer_id
        FROM customer
        WHERE pan=%s
        """

        return db.fetch_one(query, (pan,))
    # =====================================================
    # Add Customer
    # =====================================================

    def add_customer(self):

        Utils.print_header("ADD CUSTOMER")

        first_name = input(
            "First Name : "
        ).strip().title()

        last_name = input(
            "Last Name  : "
        ).strip().title()

        gender = input(
            "Gender (Male/Female/Other): "
        ).strip().title()

        dob = input(
            "Date of Birth (YYYY-MM-DD): "
        ).strip()

        mobile = input(
            "Mobile Number : "
        ).strip()

        if self.mobile_exists(mobile):

            print("\nMobile Number Already Registered.")
            return

        email = input(
            "Email : "
        ).strip()

        aadhaar = input(
            "Aadhaar Number : "
        ).strip()

        if self.aadhaar_exists(aadhaar):

            print("\nAadhaar Already Exists.")
            return

        pan = input(
            "PAN Number : "
        ).strip().upper()

        if self.pan_exists(pan):

            print("\nPAN Already Exists.")
            return

        address = input(
            "Address : "
        ).strip()

        city = input(
            "City : "
        ).strip().title()

        state = input(
            "State : "
        ).strip().title()

        pincode = input(
            "Pincode : "
        ).strip()

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
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
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

            print("=" * 60)

            print("CUSTOMER CREATED SUCCESSFULLY")

            print("=" * 60)

            print("Customer ID :", customer_id)

            print("Customer Name :", first_name, last_name)

            print("=" * 60)

        else:

            print("\nUnable to Create Customer.")


    # =====================================================
    # Get Customer by ID
    # =====================================================

    def get_customer(self, customer_id):

        query = """
        SELECT *
        FROM customer
        WHERE customer_id=%s
        """

        return db.fetch_one(query, (customer_id,))

    # =====================================================
    # Search Customer by Mobile
    # =====================================================

    def search_by_mobile(self):

        Utils.print_header("SEARCH CUSTOMER")

        mobile = input(
            "Enter Mobile Number : "
        ).strip()

        query = """
        SELECT *
        FROM customer
        WHERE mobile=%s
        """

        customer = db.fetch_one(query, (mobile,))

        if customer is None:

            print("\nCustomer Not Found.")
            return

        self.display_customer(customer)

    # =====================================================
    # Search Customer by Aadhaar
    # =====================================================

    def search_by_aadhaar(self):

        Utils.print_header("SEARCH CUSTOMER")

        aadhaar = input(
            "Enter Aadhaar Number : "
        ).strip()

        query = """
        SELECT *
        FROM customer
        WHERE aadhaar=%s
        """

        customer = db.fetch_one(query, (aadhaar,))

        if customer is None:

            print("\nCustomer Not Found.")
            return

        self.display_customer(customer)

    # =====================================================
    # Search Customer by PAN
    # =====================================================

    def search_by_pan(self):

        Utils.print_header("SEARCH CUSTOMER")

        pan = input(
            "Enter PAN Number : "
        ).strip().upper()

        query = """
        SELECT *
        FROM customer
        WHERE pan=%s
        """

        customer = db.fetch_one(query, (pan,))

        if customer is None:

            print("\nCustomer Not Found.")
            return

        self.display_customer(customer)

    # =====================================================
    # View Customer
    # =====================================================

    def view_customer(self):

        Utils.print_header("VIEW CUSTOMER")

        try:

            customer_id = int(
                input("Customer ID : ")
            )

        except ValueError:

            print("\nInvalid Customer ID.")
            return

        customer = self.get_customer(customer_id)

        if customer is None:

            print("\nCustomer Not Found.")
            return

        self.display_customer(customer)


    # =====================================================
    # Display Customer
    # =====================================================

    def display_customer(self, customer):

        print()

        print("=" * 65)

        print("CUSTOMER DETAILS")

        print("=" * 65)

        print(
            "Customer ID   :",
            customer["customer_id"]
        )

        print(
            "Name          :",
            f"{customer['first_name']} "
            f"{customer['last_name'] or ''}".strip()
        )

        print(
            "Gender        :",
            customer["gender"]
        )

        print(
            "Date of Birth :",
            customer["dob"]
        )

        print(
            "Mobile        :",
            customer["mobile"]
        )

        print(
            "Email         :",
            customer["email"]
        )

        print(
            "Aadhaar       :",
            customer["aadhaar"]
        )

        print(
            "PAN           :",
            customer["pan"]
        )

        print(
            "Address       :",
            customer["address"]
        )

        print(
            "City          :",
            customer["city"]
        )

        print(
            "State         :",
            customer["state"]
        )

        print(
            "Pincode       :",
            customer["pincode"]
        )

        print(
            "Created At    :",
            customer["created_at"]
        )

        print("=" * 65)


    # =====================================================
    # View All Customers
    # =====================================================

    def view_all_customers(self):

        Utils.print_header("ALL CUSTOMERS")

        query = """
        SELECT *
        FROM customer
        ORDER BY customer_id
        """

        customers = db.fetch_all(query)

        if not customers:

            print("\nNo Customers Found.")
            return

        print()

        print(
            "{:<6}{:<25}{:<15}{:<15}".format(
                "ID",
                "Name",
                "Mobile",
                "City"
            )
        )

        print("-" * 70)

        for customer in customers:

            full_name = (
                f"{customer['first_name']} "
                f"{customer['last_name'] or ''}"
            ).strip()

            print(
                "{:<6}{:<25}{:<15}{:<15}".format(
                    customer["customer_id"],
                    full_name,
                    customer["mobile"],
                    customer["city"]
                )
            )


    # =====================================================
    # Update Customer
    # =====================================================

    def update_customer(self):

        Utils.print_header("UPDATE CUSTOMER")

        try:

            customer_id = int(
                input("Customer ID : ")
            )

        except ValueError:

            print("\nInvalid Customer ID.")
            return

        customer = self.get_customer(customer_id)

        if customer is None:

            print("\nCustomer Not Found.")
            return

        print("\nPress ENTER to keep existing value.\n")

        first_name = input(
            f"First Name [{customer['first_name']}] : "
        ).strip()

        last_name = input(
            f"Last Name [{customer['last_name']}] : "
        ).strip()

        gender = input(
            f"Gender [{customer['gender']}] : "
        ).strip().title()

        dob = input(
            f"DOB [{customer['dob']}] : "
        ).strip()

        mobile = input(
            f"Mobile [{customer['mobile']}] : "
        ).strip()

        email = input(
            f"Email [{customer['email']}] : "
        ).strip()

        aadhaar = input(
            f"Aadhaar [{customer['aadhaar']}] : "
        ).strip()

        pan = input(
            f"PAN [{customer['pan']}] : "
        ).strip().upper()

        address = input(
            f"Address [{customer['address']}] : "
        ).strip()

        city = input(
            f"City [{customer['city']}] : "
        ).strip()

        state = input(
            f"State [{customer['state']}] : "
        ).strip()

        pincode = input(
            f"Pincode [{customer['pincode']}] : "
        ).strip()


        if mobile and mobile != customer["mobile"]:

            exists = self.mobile_exists(mobile)

            if exists:

                print("\nMobile Number Already Exists.")
                return

        if aadhaar and aadhaar != customer["aadhaar"]:

            exists = self.aadhaar_exists(aadhaar)

            if exists:

                print("\nAadhaar Already Exists.")
                return

        if pan and pan != customer["pan"]:

            exists = self.pan_exists(pan)

            if exists:

                print("\nPAN Already Exists.")
                return


        query = """
        UPDATE customer
        SET

        first_name=%s,
        last_name=%s,
        gender=%s,
        dob=%s,
        mobile=%s,
        email=%s,
        aadhaar=%s,
        pan=%s,
        address=%s,
        city=%s,
        state=%s,
        pincode=%s

        WHERE customer_id=%s
        """

        values = (

            first_name if first_name else customer["first_name"],

            last_name if last_name else customer["last_name"],

            gender if gender else customer["gender"],

            dob if dob else customer["dob"],

            mobile if mobile else customer["mobile"],

            email if email else customer["email"],

            aadhaar if aadhaar else customer["aadhaar"],

            pan if pan else customer["pan"],

            address if address else customer["address"],

            city if city else customer["city"],

            state if state else customer["state"],

            pincode if pincode else customer["pincode"],

            customer_id

        )

        if db.execute(query, values):

            print("\nCustomer Updated Successfully.")

        else:

            print("\nUnable to Update Customer.")


    # =====================================================
    # Update Customer Mobile
    # =====================================================

    def update_mobile(self, customer_id, mobile):

        query = """
        UPDATE customer
        SET mobile=%s
        WHERE customer_id=%s
        """

        return db.execute(
            query,
            (
                mobile,
                customer_id
            )
        )


    # =====================================================
    # Delete Customer
    # =====================================================

    def delete_customer(self):

        Utils.print_header("DELETE CUSTOMER")

        try:

            customer_id = int(
                input("Customer ID : ")
            )

        except ValueError:

            print("\nInvalid Customer ID.")
            return

        customer = self.get_customer(customer_id)

        if customer is None:

            print("\nCustomer Not Found.")
            return

        # Check if customer owns any account

        query = """
        SELECT COUNT(*) AS total
        FROM account
        WHERE customer_id=%s
        """

        row = db.fetch_one(
            query,
            (customer_id,)
        )

        if row["total"] > 0:

            print()

            print("Customer has active account(s).")

            print("Delete the accounts first.")

            return

        choice = input(
            "\nDelete this customer? (Y/N): "
        ).upper()

        if choice != "Y":

            print("\nOperation Cancelled.")

            return

        query = """
        DELETE FROM customer
        WHERE customer_id=%s
        """

        if db.execute(query, (customer_id,)):

            print("\nCustomer Deleted Successfully.")

        else:

            print("\nUnable to Delete Customer.")


    # =====================================================
    # Customer Profile
    # =====================================================

    def customer_profile(self):

        Utils.print_header("CUSTOMER PROFILE")

        try:

            customer_id = int(
                input("Customer ID : ")
            )

        except ValueError:

            print("Invalid Customer ID.")

            return

        query = """
        SELECT

        c.customer_id,
        c.first_name,
        c.last_name,
        c.mobile,
        c.email,
        c.city,
        c.state,

        a.account_number,
        a.account_type,
        a.balance,
        a.status

        FROM customer c

        LEFT JOIN account a

        ON c.customer_id=a.customer_id

        WHERE c.customer_id=%s
        """

        records = db.fetch_all(
            query,
            (customer_id,)
        )

        if not records:

            print("\nCustomer Not Found.")

            return

        customer = records[0]

        print()

        print("=" * 70)

        print("CUSTOMER PROFILE")

        print("=" * 70)

        print(
            "Customer ID :",
            customer["customer_id"]
        )

        print(
            "Name :",
            customer["first_name"],
            customer["last_name"] or ""
        )

        print(
            "Mobile :",
            customer["mobile"]
        )

        print(
            "Email :",
            customer["email"]
        )

        print(
            "City :",
            customer["city"]
        )

        print(
            "State :",
            customer["state"]
        )

        print()

        print("Accounts")

        print("-" * 70)

        for row in records:

            if row["account_number"] is None:
                continue

            print(
                f"A/C : {row['account_number']} | "
                f"{row['account_type']} | "
                f"Balance : {Utils.format_currency(row['balance'])} | "
                f"{row['status']}"
            )

        print("=" * 70)


    # =====================================================
    # Total Customers
    # =====================================================

    def total_customers(self):

        query = """
        SELECT COUNT(*) AS total
        FROM customer
        """

        row = db.fetch_one(query)

        if row:

            return row["total"]

        return 0


    # =====================================================
    # Search By City
    # =====================================================

    def search_by_city(self):

        Utils.print_header("SEARCH BY CITY")

        city = input(
            "City : "
        ).title()

        query = """
        SELECT *
        FROM customer
        WHERE city=%s
        ORDER BY first_name
        """

        customers = db.fetch_all(
            query,
            (city,)
        )

        if not customers:

            print("\nNo Customers Found.")

            return

        for customer in customers:

            print(
                customer["customer_id"],
                customer["first_name"],
                customer["last_name"],
                customer["mobile"]
            )


    # =====================================================
    # Search By State
    # =====================================================

    def search_by_state(self):

        Utils.print_header("SEARCH BY STATE")

        state = input(
            "State : "
        ).title()

        query = """
        SELECT *
        FROM customer
        WHERE state=%s
        ORDER BY first_name
        """

        customers = db.fetch_all(
            query,
            (state,)
        )

        if not customers:

            print("\nNo Customers Found.")

            return

        for customer in customers:

            print(
                customer["customer_id"],
                customer["first_name"],
                customer["last_name"],
                customer["mobile"]
            )


    # =====================================================
    # Customer Statistics
    # =====================================================

    def customer_statistics(self):

        Utils.print_header("CUSTOMER STATISTICS")

        print()

        print(
            "Total Customers :",
            self.total_customers()
        )

        # Male Customers
        query = """
        SELECT COUNT(*) AS total
        FROM customer
        WHERE gender='Male'
        """

        row = db.fetch_one(query)

        print(
            "Male Customers  :",
            row["total"] if row else 0
        )

        # Female Customers
        query = """
        SELECT COUNT(*) AS total
        FROM customer
        WHERE gender='Female'
        """

        row = db.fetch_one(query)

        print(
            "Female Customers:",
            row["total"] if row else 0
        )

        # Other Customers
        query = """
        SELECT COUNT(*) AS total
        FROM customer
        WHERE gender='Other'
        """

        row = db.fetch_one(query)

        print(
            "Other Customers :",
            row["total"] if row else 0
        )


    # =====================================================
    # Recently Added Customers
    # =====================================================

    def recent_customers(self):

        Utils.print_header("RECENT CUSTOMERS")

        query = """
        SELECT
        customer_id,
        first_name,
        last_name,
        mobile,
        created_at
        FROM customer
        ORDER BY created_at DESC
        LIMIT 10
        """

        customers = db.fetch_all(query)

        if not customers:

            print("\nNo Records Found.")
            return

        print()

        print(
            "{:<6}{:<25}{:<15}{:<20}".format(
                "ID",
                "Name",
                "Mobile",
                "Created"
            )
        )

        print("-" * 75)

        for customer in customers:

            name = (
                f"{customer['first_name']} "
                f"{customer['last_name'] or ''}"
            ).strip()

            print(
                "{:<6}{:<25}{:<15}{:<20}".format(
                    customer["customer_id"],
                    name,
                    customer["mobile"],
                    str(customer["created_at"])
                )
            )


    # =====================================================
    # Customer Dashboard
    # =====================================================

    def dashboard(self):

        Utils.print_header("CUSTOMER DASHBOARD")

        print()

        print(
            "Total Customers :",
            self.total_customers()
        )

        # Total Accounts
        query = """
        SELECT COUNT(*) AS total
        FROM account
        """

        row = db.fetch_one(query)

        print(
            "Total Accounts  :",
            row["total"] if row else 0
        )

        # Active Accounts
        query = """
        SELECT COUNT(*) AS total
        FROM account
        WHERE status='Active'
        """

        row = db.fetch_one(query)

        print(
            "Active Accounts :",
            row["total"] if row else 0
        )

        print()


    # =====================================================
    # Customer Account Summary
    # =====================================================

    def account_summary(self, customer_id):

        query = """
        SELECT

        COUNT(*) AS accounts,

        IFNULL(SUM(balance),0) AS balance

        FROM account

        WHERE customer_id=%s
        """

        row = db.fetch_one(
            query,
            (customer_id,)
        )

        if row:

            return {

                "accounts": row["accounts"],

                "balance": float(row["balance"])

            }

        return {

            "accounts": 0,

            "balance": 0.0

        }


    # =====================================================
    # Customer Report
    # =====================================================

    def customer_report(self):

        query = """
        SELECT

        customer_id,

        first_name,

        last_name,

        mobile,

        city,

        state

        FROM customer

        ORDER BY customer_id
        """

        return db.fetch_all(query)


    # =====================================================
    # Search By Email
    # =====================================================

    def search_by_email(self):

        Utils.print_header("SEARCH CUSTOMER BY EMAIL")

        email = input(
            "Email : "
        ).strip().lower()

        query = """
        SELECT *
        FROM customer
        WHERE email=%s
        """

        customer = db.fetch_one(query, (email,))

        if customer is None:

            print("\nCustomer Not Found.")
            return

        self.display_customer(customer)


    # =====================================================
    # Search By Name
    # =====================================================

    def search_by_name(self):

        Utils.print_header("SEARCH CUSTOMER BY NAME")

        name = input(
            "Enter First Name : "
        ).strip()

        query = """
        SELECT *
        FROM customer
        WHERE first_name LIKE %s
        ORDER BY first_name,last_name
        """

        customers = db.fetch_all(
            query,
            (f"%{name}%",)
        )

        if not customers:

            print("\nNo Customer Found.")
            return

        print()

        print(
            "{:<6}{:<25}{:<15}{:<20}".format(
                "ID",
                "Customer Name",
                "Mobile",
                "City"
            )
        )

        print("-" * 75)

        for customer in customers:

            full_name = (
                f"{customer['first_name']} "
                f"{customer['last_name'] or ''}"
            ).strip()

            print(
                "{:<6}{:<25}{:<15}{:<20}".format(
                    customer["customer_id"],
                    full_name,
                    customer["mobile"],
                    customer["city"]
                )
            )


    # =====================================================
    # Customers Having Multiple Accounts
    # =====================================================

    def multiple_accounts(self):

        Utils.print_header(
            "CUSTOMERS HAVING MULTIPLE ACCOUNTS"
        )

        query = """
        SELECT

        c.customer_id,
        c.first_name,
        c.last_name,

        COUNT(a.account_number) AS accounts

        FROM customer c

        INNER JOIN account a

        ON c.customer_id=a.customer_id

        GROUP BY c.customer_id

        HAVING COUNT(a.account_number)>1

        ORDER BY accounts DESC
        """

        rows = db.fetch_all(query)

        if not rows:

            print("\nNo Records Found.")
            return

        print()

        print(
            "{:<8}{:<30}{:<10}".format(
                "ID",
                "Customer Name",
                "Accounts"
            )
        )

        print("-" * 55)

        for row in rows:

            name = (
                f"{row['first_name']} "
                f"{row['last_name'] or ''}"
            ).strip()

            print(
                "{:<8}{:<30}{:<10}".format(
                    row["customer_id"],
                    name,
                    row["accounts"]
                )
            )


    # =====================================================
    # Customers Without Accounts
    # =====================================================

    def customers_without_accounts(self):

        Utils.print_header(
            "CUSTOMERS WITHOUT ACCOUNTS"
        )

        query = """
        SELECT

        c.customer_id,
        c.first_name,
        c.last_name,
        c.mobile

        FROM customer c

        LEFT JOIN account a

        ON c.customer_id=a.customer_id

        WHERE a.account_number IS NULL

        ORDER BY c.customer_id
        """

        rows = db.fetch_all(query)

        if not rows:

            print("\nAll Customers Have Accounts.")
            return

        print()

        print(
            "{:<8}{:<30}{:<15}".format(
                "ID",
                "Customer Name",
                "Mobile"
            )
        )

        print("-" * 60)

        for row in rows:

            name = (
                f"{row['first_name']} "
                f"{row['last_name'] or ''}"
            ).strip()

            print(
                "{:<8}{:<30}{:<15}".format(
                    row["customer_id"],
                    name,
                    row["mobile"]
                )
            )


    # =====================================================
    # Print Customer Receipt
    # =====================================================

    def print_receipt(self, customer_id):

        customer = self.get_customer(customer_id)

        if customer is None:

            print("\nCustomer Not Found.")
            return

        Utils.print_header("CUSTOMER RECEIPT")

        print(
            "Customer ID :",
            customer["customer_id"]
        )

        print(
            "Customer Name :",
            f"{customer['first_name']} "
            f"{customer['last_name'] or ''}"
        )

        print(
            "Mobile :",
            customer["mobile"]
        )

        print(
            "Email :",
            customer["email"]
        )

        print(
            "City :",
            customer["city"]
        )

        print(
            "State :",
            customer["state"]
        )

        summary = self.account_summary(
            customer_id
        )

        print()

        print(
            "Total Accounts :",
            summary["accounts"]
        )

        print(
            "Total Balance :",
            Utils.format_currency(
                summary["balance"]
            )
        )

        print("=" * 60)


    # =====================================================
    # Get Customer List
    # =====================================================

    def get_customer_list(self):

        query = """
        SELECT *
        FROM customer
        ORDER BY customer_id
        """

        return db.fetch_all(query)


    # =====================================================
    # Dashboard Summary
    # =====================================================

    def dashboard_summary(self):

        Utils.print_header("CUSTOMER DASHBOARD")

        print()

        print(
            "Total Customers :",
            self.total_customers()
        )

        query = """
        SELECT COUNT(*) AS total
        FROM account
        """

        row = db.fetch_one(query)

        total_accounts = row["total"] if row else 0

        print(
            "Total Accounts  :",
            total_accounts
        )

        query = """
        SELECT IFNULL(SUM(balance),0) AS total
        FROM account
        """

        row = db.fetch_one(query)

        total_balance = float(row["total"]) if row else 0

        print(
            "Total Deposits  :",
            Utils.format_currency(total_balance)
        )

        print()


    # =====================================================
    # Refresh Database Connection
    # =====================================================

    def reconnect(self):

        if db.connection is None:

            db.connect()


    # =====================================================
    # Customers Count by City
    # =====================================================

    def customers_by_city(self):

        query = """
        SELECT city,
               COUNT(*) AS total
        FROM customer
        GROUP BY city
        ORDER BY city
        """

        return db.fetch_all(query)


    # =====================================================
    # Customers Count by State
    # =====================================================

    def customers_by_state(self):

        query = """
        SELECT state,
               COUNT(*) AS total
        FROM customer
        GROUP BY state
        ORDER BY state
        """

        return db.fetch_all(query)




    # =====================================================
    # Get Customer Full Name
    # =====================================================

    def get_customer_name(self, customer_id):

        customer = self.get_customer(customer_id)

        if customer is None:

            return None

        return (
            f"{customer['first_name']} "
            f"{customer['last_name'] or ''}"
        ).strip()


    # =====================================================
    # Customer Exists (Boolean)
    # =====================================================

    def exists(self, customer_id):

        return self.get_customer(customer_id) is not None


    # =====================================================
    # Customer Status
    # =====================================================

    def customer_status(self, customer_id):

        query = """
        SELECT COUNT(*) AS total
        FROM account
        WHERE customer_id=%s
        """

        row = db.fetch_one(query, (customer_id,))

        if row["total"] > 0:

            return "Active"

        return "Inactive"


    # =====================================================
    # Complete Customer Summary
    # =====================================================

    def summary(self, customer_id):

        customer = self.get_customer(customer_id)

        if customer is None:

            return None

        summary = self.account_summary(customer_id)

        return {

            "customer_id": customer["customer_id"],

            "name": self.get_customer_name(customer_id),

            "mobile": customer["mobile"],

            "city": customer["city"],

            "accounts": summary["accounts"],

            "balance": summary["balance"],

            "status": self.customer_status(customer_id)

        }


    # =====================================================
    # Export Customer Data
    # =====================================================

    def export_data(self):

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

        return db.fetch_all(query)


    # =====================================================
    # Destructor
    # =====================================================

    def delete_customer(self):
        customer_id = int(input("Enter the Customer ID to delete: "))

        sql = "DELETE FROM Customer WHERE CustomerID = %s"
        self.cursor.execute(sql, (customer_id,))
        self.conn.commit()

        print(f"{self.cursor.rowcount} record(s) deleted.")
        obj = Customer(conn)
        obj.delete_customer()

    # =====================================================
    # Customer Menu
    # =====================================================

    def menu(self):

        while True:

            Utils.print_header("CUSTOMER MENU")

            print("1. Add Customer")
            print("2. View Customer")
            print("3. View All Customers")
            print("4. Update Customer")
            print("5. Delete Customer")
            print("6. Customer Profile")
            print("7. Search by Mobile")
            print("8. Search by Aadhaar")
            print("9. Search by PAN")
            print("10. Search by Email")
            print("11. Search by Name")
            print("12. Search by City")
            print("13. Search by State")
            print("14. Multiple Account Customers")
            print("15. Customers Without Accounts")
            print("16. Customer Statistics")
            print("17. Recent Customers")
            print("18. Dashboard")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.add_customer()

            elif choice == "2":

                self.view_customer()

            elif choice == "3":

                self.view_all_customers()

            elif choice == "4":

                self.update_customer()

            elif choice == "5":

                self.delete_customer()

            elif choice == "6":

                self.customer_profile()

            elif choice == "7":

                self.search_by_mobile()

            elif choice == "8":

                self.search_by_aadhaar()

            elif choice == "9":

                self.search_by_pan()

            elif choice == "10":

                self.search_by_email()

            elif choice == "11":

                self.search_by_name()

            elif choice == "12":

                self.search_by_city()

            elif choice == "13":

                self.search_by_state()

            elif choice == "14":

                self.multiple_accounts()

            elif choice == "15":

                self.customers_without_accounts()

            elif choice == "16":

                self.customer_statistics()

            elif choice == "17":

                self.recent_customers()

            elif choice == "18":

                self.dashboard()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


        pass
