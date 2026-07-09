"""
==========================================================
Banking Management System
File : admin.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================

Admin Management Module

Features
--------
1. Admin Login
2. Dashboard
3. Customer Management
4. Account Management
5. Loan Approval
6. Reports
7. Audit Support

==========================================================
"""

from database import db
from utils import Utils
from customer import Customer
from account import Account
from loan import Loan
from fd import FixedDeposit
from rd import RecurringDeposit
from beneficiary import Beneficiary
from transactions import Transaction


class Admin:

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        if db.connection is None:
            db.connect()

        self.customer = Customer()
        self.account = Account()
        self.loan = Loan()
        self.fd = FixedDeposit()
        self.rd = RecurringDeposit()
        self.beneficiary = Beneficiary()
        self.transactions = Transaction()

        self.admin_data = None


    # =====================================================
    # Admin Login
    # =====================================================

    def login(self):

        Utils.print_header("ADMIN LOGIN")

        username = input(
            "Username : "
        ).strip()

        password = input(
            "Password : "
        ).strip()

        query = """
        SELECT *
        FROM admin
        WHERE username=%s
        """

        admin = db.fetch_one(
            query,
            (username,)
        )

        if admin is None:

            print("\nInvalid Username.")

            return False

        # Simple password check
        # Replace with bcrypt verification if using hashed passwords

        if admin["password"] != password:

            print("\nInvalid Password.")

            return False

        self.admin_data = admin

        

        self.add_audit_log("Admin Login")

        print()

        print(
            f"Welcome, {admin['full_name']}!"
        )

        return True


    # =====================================================
    # Logout
    # =====================================================

    def logout(self):

        

        self.add_audit_log("Admin Logout")

        self.admin_data = None

        print("\nLogged Out Successfully.")


    # =====================================================
    # Admin Profile
    # =====================================================

    def profile(self):

        if self.admin_data is None:

            print("\nNo Admin Logged In.")

            return

        Utils.print_header("ADMIN PROFILE")

        print(
            "Admin ID :",
            self.admin_data["admin_id"]
        )

        print(
            "Name :",
            self.admin_data["full_name"]
        )

        print(
            "Username :",
            self.admin_data["username"]
        )

        print(
            "Mobile :",
            self.admin_data["mobile"]
        )

        print(
            "Email :",
            self.admin_data["email"]
        )

        print(
            "Created :",
            self.admin_data["created_at"]
        )


    # =====================================================
    # Admin Dashboard
    # =====================================================

    def dashboard(self):

        Utils.print_header("ADMIN DASHBOARD")

        print()

        print("Logged In As :", self.admin_data["full_name"])

        print("-" * 60)

        print(
            "Total Customers :",
            self.customer.total_customers()
        )

        query = """
        SELECT COUNT(*) AS total
        FROM account
        """

        row = db.fetch_one(query)

        print(
            "Total Accounts  :",
            row["total"] if row else 0
        )

        query = """
        SELECT IFNULL(SUM(balance),0) AS total
        FROM account
        """

        row = db.fetch_one(query)

        print(
            "Total Deposits  :",
            Utils.format_currency(
                row["total"] if row else 0
            )
        )

        query = """
        SELECT COUNT(*) AS total
        FROM loan
        WHERE status='Pending'
        """

        row = db.fetch_one(query)

        print(
            "Pending Loans   :",
            row["total"] if row else 0
        )

        print("-" * 60)


    # =====================================================
    # Customer Management
    # =====================================================

    def customer_management(self):

        while True:

            Utils.print_header(
                "CUSTOMER MANAGEMENT"
            )

            print("1. Add Customer")
            print("2. View Customer")
            print("3. View All Customers")
            print("4. Update Customer")
            print("5. Delete Customer")
            print("6. Customer Statistics")
            print("7. Customer Dashboard")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.customer.add_customer()

            elif choice == "2":

                self.customer.view_customer()

            elif choice == "3":

                self.customer.view_all_customers()

            elif choice == "4":

                self.customer.update_customer()

            elif choice == "5":

                self.customer.delete_customer()

            elif choice == "6":

                self.customer.customer_statistics()

            elif choice == "7":

                self.customer.dashboard()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Account Management
    # =====================================================

    def account_management(self):

        while True:

            Utils.print_header(
                "ACCOUNT MANAGEMENT"
            )

            print("1. Open Account")
            print("2. View Account")
            print("3. View All Accounts")
            print("4. Deposit")
            print("5. Withdraw")
            print("6. Transfer")
            print("7. Freeze Account")
            print("8. Unfreeze Account")
            print("9. Close Account")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.account.create_account()

            elif choice == "2":

                self.account.view_account()

            elif choice == "3":

                self.account.view_all_accounts()

            elif choice == "4":

                self.account.deposit()

            elif choice == "5":

                self.account.withdraw()

            elif choice == "6":

                self.account.transfer()

            elif choice == "7":

                self.account.freeze_account()

            elif choice == "8":

                self.account.unfreeze_account()

            elif choice == "9":

                self.account.close_account()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Loan Management
    # =====================================================

    def loan_management(self):

        while True:

            Utils.print_header(
                "LOAN MANAGEMENT"
            )

            print("1. Apply Loan")
            print("2. View Loan")
            print("3. View All Loans")
            print("4. Pending Loans")
            print("5. Approve Loan")
            print("6. Reject Loan")
            print("7. Loan Statistics")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.loan.apply_loan()

            elif choice == "2":

                self.loan.view_loan()

            elif choice == "3":

                self.loan.view_all_loans()

            elif choice == "4":

                self.loan.pending_loans()

            elif choice == "5":

                self.loan.approve_loan()

            elif choice == "6":

                self.loan.reject_loan()

            elif choice == "7":

                self.loan.loan_statistics()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Fixed Deposit Management
    # =====================================================

    def fd_management(self):

        while True:

            Utils.print_header(
                "FIXED DEPOSIT MANAGEMENT"
            )

            print("1. Open Fixed Deposit")
            print("2. View Fixed Deposit")
            print("3. View All Fixed Deposits")
            print("4. Search Fixed Deposit")
            print("5. FD Statistics")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.fd.create_fd()

            elif choice == "2":

                self.fd.view_fd()

            elif choice == "3":

                self.fd.view_all_fd()

            elif choice == "4":

                self.fd.search_fd()

            elif choice == "5":

                self.fd.fd_statistics()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Recurring Deposit Management
    # =====================================================

    def rd_management(self):

        while True:

            Utils.print_header(
                "RECURRING DEPOSIT MANAGEMENT"
            )

            print("1. Open RD")
            print("2. View RD")
            print("3. View All RD")
            print("4. Search RD")
            print("5. RD Statistics")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.rd.create_rd()

            elif choice == "2":

                self.rd.view_rd()

            elif choice == "3":

                self.rd.view_all_rd()

            elif choice == "4":

                self.rd.search_rd()

            elif choice == "5":

                self.rd.rd_statistics()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Beneficiary Management
    # =====================================================

    def beneficiary_management(self):

        while True:

            Utils.print_header(
                "BENEFICIARY MANAGEMENT"
            )

            print("1. Add Beneficiary")
            print("2. View Beneficiary")
            print("3. View All Beneficiaries")
            print("4. Delete Beneficiary")
            print("5. Beneficiary Statistics")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.beneficiary.add_beneficiary()

            elif choice == "2":

                self.beneficiary.view_beneficiary()

            elif choice == "3":

                self.beneficiary.view_all_beneficiaries()

            elif choice == "4":

                self.beneficiary.delete_beneficiary()

            elif choice == "5":

                self.beneficiary.beneficiary_statistics()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Transaction Management
    # =====================================================

    def transactions_management(self):

        while True:

            Utils.print_header(
                "TRANSACTION MANAGEMENT"
            )

            print("1. Deposit")
            print("2. Withdraw")
            print("3. Transfer")
            print("4. Transaction History")
            print("5. Daily Transactions")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.transactions.deposit()

            elif choice == "2":

                self.transactions.withdraw()

            elif choice == "3":

                self.transactions.transfer()

            elif choice == "4":

                self.transactions.transactions_history()

            elif choice == "5":

                self.transactions.daily_transactionss()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Freeze / Unfreeze Account
    # =====================================================

    def account_status_management(self):

        while True:

            Utils.print_header(
                "ACCOUNT STATUS MANAGEMENT"
            )

            print("1. Freeze Account")
            print("2. Unfreeze Account")
            print("3. Close Account")
            print("0. Back")

            choice = input("\nEnter Choice : ").strip()

            if choice == "1":

                self.account.freeze_account()

            elif choice == "2":

                self.account.unfreeze_account()

            elif choice == "3":

                self.account.close_account()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Pending Loan Approval
    # =====================================================

    def pending_loan_approval(self):

        while True:

            Utils.print_header(
                "LOAN APPROVAL"
            )

            print("1. View Pending Loans")
            print("2. Approve Loan")
            print("3. Reject Loan")
            print("0. Back")

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.loan.pending_loans()

            elif choice == "2":

                self.loan.approve_loan()

            elif choice == "3":

                self.loan.reject_loan()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Banking Summary
    # =====================================================

    def banking_summary(self):

        Utils.print_header("BANK SUMMARY")

        print()

        print(
            "Customers :",
            self.customer.total_customers()
        )

        account_count = db.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM account
            """
        )

        print(
            "Accounts  :",
            account_count["total"]
        )

        loan_count = db.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM loan
            """
        )

        print(
            "Loans     :",
            loan_count["total"]
        )

        fd_count = db.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM fd
            """
        )

        print(
            "FDs       :",
            fd_count["total"]
        )

        rd_count = db.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM rd
            """
        )

        print(
            "RDs       :",
            rd_count["total"]
        )

        ben_count = db.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM beneficiary
            """
        )

        print(
            "Beneficiaries :",
            ben_count["total"]
        )

        print("-" * 60)


    # =====================================================
    # Admin Details
    # =====================================================

    def admin_details(self):

        Utils.print_header("ADMIN DETAILS")

        query = """
        SELECT *

        FROM admin

        ORDER BY admin_id
        """

        admins = db.fetch_all(query)

        if not admins:

            print("\nNo Admin Found.")

            return

        print()

        print(
            "{:<5}{:<20}{:<15}{:<25}".format(
                "ID",
                "Name",
                "Username",
                "Email"
            )
        )

        print("-" * 75)

        for admin in admins:

            print(
                "{:<5}{:<20}{:<15}{:<25}".format(
                    admin["admin_id"],
                    admin["full_name"],
                    admin["username"],
                    admin["email"] or ""
                )
            )


    # =====================================================
    # Refresh Connection
    # =====================================================

    def reconnect(self):

        if db.connection is None:

            db.connect()


    # =====================================================
    # Audit Log
    # =====================================================

    def view_audit_log(self):

        Utils.print_header("AUDIT LOG")

        query = """
        SELECT *
        FROM audit_log
        ORDER BY log_id DESC
        LIMIT 50
        """

        logs = db.fetch_all(query)

        if not logs:

            print("\nNo Audit Records Found.")

            return

        print()

        print(
            "{:<6}{:<10}{:<20}{:<25}".format(
                "ID",
                "Admin",
                "Action",
                "Date"
            )
        )

        print("-" * 80)

        for log in logs:

            print(
                "{:<6}{:<10}{:<20}{:<25}".format(
                    log["log_id"],
                    log["admin_id"],
                    log["action"],
                    str(log["created_at"])
                )
            )


    # =====================================================
    # Login History
    # =====================================================

    def view_login_history(self):

        Utils.print_header("LOGIN HISTORY")

        query = """
        SELECT *
        FROM login_history
        ORDER BY login_time DESC
        LIMIT 50
        """

        history = db.fetch_all(query)

        if not history:

            print("\nNo Login History Found.")

            return

        print()

        print(
            "{:<8}{:<15}{:<25}".format(
                "ID",
                "User",
                "Login Time"
            )
        )

        print("-" * 60)

        for row in history:

            print(
                "{:<8}{:<15}{:<25}".format(
                    row["login_id"],
                    row["username"],
                    str(row["login_time"])
                )
            )


    # =====================================================
    # View Branches
    # =====================================================

    def view_branches(self):

        Utils.print_header("BRANCH DETAILS")

        query = """
        SELECT *
        FROM branch
        ORDER BY branch_id
        """

        branches = db.fetch_all(query)

        if not branches:

            print("\nNo Branch Found.")

            return

        print()

        print(
            "{:<6}{:<30}{:<20}".format(
                "ID",
                "Branch Name",
                "City"
            )
        )

        print("-" * 70)

        for branch in branches:

            print(
                "{:<6}{:<30}{:<20}".format(
                    branch["branch_id"],
                    branch["branch_name"],
                    branch["city"]
                )
            )


    # =====================================================
    # Admin Statistics
    # =====================================================

    def admin_statistics(self):

        Utils.print_header("ADMIN STATISTICS")

        query = """
        SELECT COUNT(*) AS total
        FROM admin
        """

        row = db.fetch_one(query)

        print()

        print(
            "Total Admins :",
            row["total"] if row else 0
        )

        print(
            "Current Admin :",
            self.admin_data["full_name"]
        )


    # =====================================================
    # Dashboard Summary
    # =====================================================

    def dashboard_summary(self):

        Utils.print_header("SYSTEM DASHBOARD")

        self.dashboard()

        print()

        self.banking_summary()

        print()

        self.admin_statistics()


    # =====================================================
    # Branch Statistics
    # =====================================================

    def branch_statistics(self):

        Utils.print_header("BRANCH STATISTICS")

        query = """
        SELECT COUNT(*) AS total
        FROM branch
        """

        row = db.fetch_one(query)

        print()

        print("Total Branches :", row["total"])

        print()

        query = """
        SELECT
        state,
        COUNT(*) AS total
        FROM branch
        GROUP BY state
        ORDER BY state
        """

        rows = db.fetch_all(query)

        if rows:

            print("{:<20}{:<10}".format(
                "State",
                "Branches"
            ))

            print("-"*35)

            for branch in rows:

                print(
                    "{:<20}{:<10}".format(
                        branch["state"],
                        branch["total"]
                    )
                )


    # =====================================================
    # View Complete Branch Details
    # =====================================================

    def branch_details(self):

        Utils.print_header("BRANCH DETAILS")

        query = """
        SELECT *
        FROM branch
        ORDER BY branch_name
        """

        branches = db.fetch_all(query)

        if not branches:

            print("\nNo Branch Found.")

            return

        for branch in branches:

            print("="*70)

            print("Branch ID    :", branch["branch_id"])

            print("Branch Name  :", branch["branch_name"])

            print("Branch Code  :", branch["branch_code"])

            print("IFSC Code    :", branch["ifsc_code"])

            print("Address      :", branch["address"])

            print("City         :", branch["city"])

            print("State        :", branch["state"])

            print("Pincode      :", branch["pincode"])

        print("="*70)


    # =====================================================
    # Recent Audit Logs
    # =====================================================

    def recent_audit_logs(self):

        Utils.print_header("RECENT AUDIT LOGS")

        query = """
        SELECT *
        FROM audit_log
        ORDER BY action_time DESC
        LIMIT 20
        """

        logs = db.fetch_all(query)

        if not logs:

            print("\nNo Audit Records.")

            return

        print()

        print("{:<8}{:<10}{:<25}{:<25}".format(
            "Log ID",
            "Admin",
            "Action",
            "Time"
        ))

        print("-"*75)

        for log in logs:

            print(
                "{:<8}{:<10}{:<25}{:<25}".format(
                    log["log_id"],
                    log["admin_id"],
                    log["action"],
                    str(log["action_time"])
                )
            )


    # =====================================================
    # Recent Login History
    # =====================================================

    def recent_login_history(self):

        Utils.print_header("LOGIN HISTORY")

        query = """
        SELECT *
        FROM login_history
        ORDER BY login_time DESC
        LIMIT 20
        """

        history = db.fetch_all(query)

        if not history:

            print("\nNo Login Records.")

            return

        print()

        print("{:<15}{:<25}{:<18}".format(
            "Account",
            "Login Time",
            "IP Address"
        ))

        print("-"*70)

        for row in history:

            print(
                "{:<15}{:<25}{:<18}".format(
                    row["account_number"],
                    str(row["login_time"]),
                    row["ip_address"] or "-"
                )
            )


    # =====================================================
    # System Health
    # =====================================================

    def system_health(self):

        Utils.print_header("SYSTEM HEALTH")

        print()

        print("Database Connection : Connected")

        print(
            "Customers :",
            self.customer.total_customers()
        )

        print(
            "Loans :",
            self.loan.total_loans()
        )

        print(
            "Fixed Deposits :",
            self.fd.total_fd()
        )

        print(
            "Recurring Deposits :",
            self.rd.total_rd()
        )

        print(
            "Beneficiaries :",
            self.beneficiary.total_beneficiaries()
        )

        print("-"*60)


    # =====================================================
    # Admin Main Menu
    # =====================================================

    def menu(self):

        while True:

            Utils.print_header("BANK ADMIN PANEL")

            print("Logged In :", self.admin_data["full_name"])

            print("\n========== MAIN MENU ==========\n")

            print("1. Dashboard")

            print("2. Customer Management")

            print("3. Account Management")

            print("4. Transaction Management")

            print("5. Loan Management")

            print("6. Fixed Deposit Management")

            print("7. Recurring Deposit Management")

            print("8. Beneficiary Management")

            print("9. Branch Details")

            print("10. Banking Summary")

            print("11. Audit Logs")

            print("12. Login History")

            print("13. Admin Profile")

            print("14. System Health")

            print("15. Branch Statistics")

            print("16. Admin Statistics")

            print("0. Logout")

            choice = input("\nEnter Choice : ").strip()

            if choice == "1":

                self.dashboard()

            elif choice == "2":

                self.customer_management()

            elif choice == "3":

                self.account_management()

            elif choice == "4":

                self.transactions_management()

            elif choice == "5":

                self.loan_management()

            elif choice == "6":

                self.fd_management()

            elif choice == "7":

                self.rd_management()

            elif choice == "8":

                self.beneficiary_management()

            elif choice == "9":

                self.branch_details()

            elif choice == "10":

                self.banking_summary()

            elif choice == "11":

                self.recent_audit_logs()

            elif choice == "12":

                self.recent_login_history()

            elif choice == "13":

                self.profile()

            elif choice == "14":

                self.system_health()

            elif choice == "15":

                self.branch_statistics()

            elif choice == "16":

                self.admin_statistics()

            elif choice == "0":

                self.logout()

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Check Login Status
    # =====================================================

    def is_logged_in(self):

        return self.admin_data is not None


    # =====================================================
    # Current Admin
    # =====================================================

    def current_admin(self):

        return self.admin_data


    # =====================================================
    # Get Admin Name
    # =====================================================

    def admin_name(self):

        if self.admin_data:

            return self.admin_data["full_name"]

        return None


    # =====================================================
    # Record Audit Log
    # =====================================================

    def add_audit_log(self, action):

        if self.admin_data is None:

            return

        query = """
        INSERT INTO audit_log
        (
            admin_id,
            action
        )
        VALUES
        (
            %s,
            %s
        )
        """

        db.execute(

            query,

            (

                self.admin_data["admin_id"],

                action

            )

        )


    # =====================================================
    # Record Login History
    # =====================================================

    def record_login(self, account_number=0, ip_address="127.0.0.1"):

        query = """
        INSERT INTO login_history
        (
            account_number,
            ip_address
        )
        VALUES
        (
            %s,
            %s
        )
        """

        db.execute(
            query,
            (
                account_number,
                ip_address
            )
        )


    # =====================================================
    # Record Logout
    # =====================================================

    def record_logout(self, account_number=0):

        query = """
        UPDATE login_history

        SET logout_time = NOW()

        WHERE account_number=%s

        ORDER BY login_id DESC

        LIMIT 1
        """

        db.execute(
            query,
            (
                account_number,
            )
        )


    # =====================================================
    # Change Admin Password
    # =====================================================

    def change_password(self):

        Utils.print_header("CHANGE PASSWORD")

        old_password = input("Old Password : ").strip()

        if old_password != self.admin_data["password"]:

            print("\nIncorrect Password.")

            return

        new_password = input("New Password : ").strip()

        confirm = input("Confirm Password : ").strip()

        if new_password != confirm:

            print("\nPasswords do not match.")

            return

        query = """
        UPDATE admin

        SET password=%s

        WHERE admin_id=%s
        """

        db.execute(
            query,
            (
                new_password,
                self.admin_data["admin_id"]
            )
        )

        self.admin_data["password"] = new_password

        self.add_audit_log("Changed Password")

        print("\nPassword Updated Successfully.")


    # =====================================================
    # Refresh Admin Information
    # =====================================================

    def refresh(self):

        if self.admin_data is None:

            return

        query = """
        SELECT *

        FROM admin

        WHERE admin_id=%s
        """

        self.admin_data = db.fetch_one(
            query,
            (
                self.admin_data["admin_id"],
            )
        )


    # =====================================================
    # Destructor
    # =====================================================

    def __del__(self):

        pass
