"""
==========================================================
Banking Management System
File : branch.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================
"""

from database import db
from utils import Utils
from validations import Validator


class Branch:

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        if db.connection is None:
            db.connect()


    # =====================================================
    # Add Branch
    # =====================================================

    def add_branch(self):

        Utils.print_header("ADD NEW BRANCH")

        branch_name = input("Branch Name : ").strip()

        branch_code = input("Branch Code : ").strip().upper()

        ifsc_code = input("IFSC Code : ").strip().upper()

        address = input("Address : ").strip()

        city = input("City : ").strip()

        state = input("State : ").strip()

        pincode = input("Pincode : ").strip()

        query = """
        INSERT INTO branch
        (
            branch_name,
            branch_code,
            ifsc_code,
            address,
            city,
            state,
            pincode
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s
        )
        """

        db.execute(
            query,
            (
                branch_name,
                branch_code,
                ifsc_code,
                address,
                city,
                state,
                pincode
            )
        )

        print("\nBranch Added Successfully.")


    # =====================================================
    # View Branch
    # =====================================================

    def view_branch(self):

        Utils.print_header("VIEW BRANCH")

        branch_id = input("Enter Branch ID : ").strip()

        query = """
        SELECT *
        FROM branch
        WHERE branch_id=%s
        """

        branch = db.fetch_one(query, (branch_id,))

        if not branch:

            print("\nBranch Not Found.")

            return

        print("\nBranch Details")

        print("-"*50)

        print("Branch ID   :", branch["branch_id"])

        print("Branch Name :", branch["branch_name"])

        print("Branch Code :", branch["branch_code"])

        print("IFSC Code   :", branch["ifsc_code"])

        print("Address     :", branch["address"])

        print("City        :", branch["city"])

        print("State       :", branch["state"])

        print("Pincode     :", branch["pincode"])


    # =====================================================
    # View All Branches
    # =====================================================

    def view_all_branches(self):

        Utils.print_header("ALL BRANCHES")

        query = """
        SELECT *
        FROM branch
        ORDER BY branch_name
        """

        branches = db.fetch_all(query)

        if not branches:

            print("\nNo Branches Found.")

            return

        print()

        print(
            "{:<5}{:<25}{:<12}{:<15}{:<15}".format(
                "ID",
                "Branch Name",
                "Code",
                "City",
                "State"
            )
        )

        print("-" * 75)

        for branch in branches:

            print(
                "{:<5}{:<25}{:<12}{:<15}{:<15}".format(
                    branch["branch_id"],
                    branch["branch_name"],
                    branch["branch_code"],
                    branch["city"],
                    branch["state"]
                )
            )


    # =====================================================
    # Search Branch by Branch Code
    # =====================================================

    def search_branch_code(self):

        Utils.print_header("SEARCH BRANCH")

        code = input(
            "Enter Branch Code : "
        ).strip().upper()

        query = """
        SELECT *
        FROM branch
        WHERE branch_code=%s
        """

        branch = db.fetch_one(
            query,
            (code,)
        )

        if not branch:

            print("\nBranch Not Found.")

            return

        print()

        print("Branch ID   :", branch["branch_id"])

        print("Branch Name :", branch["branch_name"])

        print("Branch Code :", branch["branch_code"])

        print("IFSC Code   :", branch["ifsc_code"])

        print("Address     :", branch["address"])

        print("City        :", branch["city"])

        print("State       :", branch["state"])

        print("Pincode     :", branch["pincode"])


    # =====================================================
    # Search Branch by IFSC
    # =====================================================

    def search_ifsc(self):

        Utils.print_header("SEARCH IFSC")

        ifsc = input(
            "Enter IFSC Code : "
        ).strip().upper()

        query = """
        SELECT *
        FROM branch
        WHERE ifsc_code=%s
        """

        branch = db.fetch_one(
            query,
            (ifsc,)
        )

        if not branch:

            print("\nBranch Not Found.")

            return

        print()

        print("Branch ID   :", branch["branch_id"])

        print("Branch Name :", branch["branch_name"])

        print("Branch Code :", branch["branch_code"])

        print("IFSC Code   :", branch["ifsc_code"])

        print("Address     :", branch["address"])

        print("City        :", branch["city"])

        print("State       :", branch["state"])

        print("Pincode     :", branch["pincode"])


    # =====================================================
    # Search Branches by City
    # =====================================================

    def search_city(self):

        Utils.print_header("SEARCH BY CITY")

        city = input(
            "Enter City : "
        ).strip()

        query = """
        SELECT *
        FROM branch
        WHERE city=%s
        ORDER BY branch_name
        """

        branches = db.fetch_all(
            query,
            (city,)
        )

        if not branches:

            print("\nNo Branch Found.")

            return

        print()

        print(
            "{:<5}{:<25}{:<12}{:<15}".format(
                "ID",
                "Branch Name",
                "Code",
                "IFSC"
            )
        )

        print("-" * 65)

        for branch in branches:

            print(
                "{:<5}{:<25}{:<12}{:<15}".format(
                    branch["branch_id"],
                    branch["branch_name"],
                    branch["branch_code"],
                    branch["ifsc_code"]
                )
            )


    # =====================================================
    # Update Branch
    # =====================================================

    def update_branch(self):

        Utils.print_header("UPDATE BRANCH")

        branch_id = input(
            "Enter Branch ID : "
        ).strip()

        query = """
        SELECT *
        FROM branch
        WHERE branch_id=%s
        """

        branch = db.fetch_one(
            query,
            (branch_id,)
        )

        if not branch:

            print("\nBranch Not Found.")

            return

        print("\nLeave blank to keep existing value.\n")

        branch_name = input(
            f"Branch Name [{branch['branch_name']}] : "
        ).strip()

        branch_code = input(
            f"Branch Code [{branch['branch_code']}] : "
        ).strip().upper()

        ifsc_code = input(
            f"IFSC Code [{branch['ifsc_code']}] : "
        ).strip().upper()

        address = input(
            f"Address [{branch['address']}] : "
        ).strip()

        city = input(
            f"City [{branch['city']}] : "
        ).strip()

        state = input(
            f"State [{branch['state']}] : "
        ).strip()

        pincode = input(
            f"Pincode [{branch['pincode']}] : "
        ).strip()

        query = """
        UPDATE branch
        SET
            branch_name=%s,
            branch_code=%s,
            ifsc_code=%s,
            address=%s,
            city=%s,
            state=%s,
            pincode=%s
        WHERE branch_id=%s
        """

        db.execute(
            query,
            (
                branch_name if branch_name else branch["branch_name"],
                branch_code if branch_code else branch["branch_code"],
                ifsc_code if ifsc_code else branch["ifsc_code"],
                address if address else branch["address"],
                city if city else branch["city"],
                state if state else branch["state"],
                pincode if pincode else branch["pincode"],
                branch_id
            )
        )

        print("\nBranch Updated Successfully.")


    # =====================================================
    # Delete Branch
    # =====================================================

    def delete_branch(self):

        Utils.print_header("DELETE BRANCH")

        branch_id = input(
            "Enter Branch ID : "
        ).strip()

        query = """
        SELECT *
        FROM branch
        WHERE branch_id=%s
        """

        branch = db.fetch_one(
            query,
            (branch_id,)
        )

        if not branch:

            print("\nBranch Not Found.")

            return

        confirm = input(
            "\nDelete this branch? (Y/N): "
        ).strip().upper()

        if confirm != "Y":

            print("\nDeletion Cancelled.")

            return

        query = """
        DELETE FROM branch
        WHERE branch_id=%s
        """

        db.execute(
            query,
            (branch_id,)
        )

        print("\nBranch Deleted Successfully.")


    # =====================================================
    # Total Branches
    # =====================================================

    def total_branches(self):

        query = """
        SELECT COUNT(*) AS total
        FROM branch
        """

        row = db.fetch_one(query)

        return row["total"]


    # =====================================================
    # Branch Statistics
    # =====================================================

    def branch_statistics(self):

        Utils.print_header("BRANCH STATISTICS")

        print()

        print(
            "Total Branches :",
            self.total_branches()
        )

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

            print(
                "{:<20}{:<10}".format(
                    "State",
                    "Branches"
                )
            )

            print("-" * 35)

            for row in rows:

                print(
                    "{:<20}{:<10}".format(
                        row["state"],
                        row["total"]
                    )
                )


    # =====================================================
    # Search Branches by State
    # =====================================================

    def search_state(self):

        Utils.print_header("SEARCH BRANCH BY STATE")

        state = input(
            "Enter State : "
        ).strip()

        query = """
        SELECT *
        FROM branch
        WHERE state=%s
        ORDER BY branch_name
        """

        branches = db.fetch_all(
            query,
            (state,)
        )

        if not branches:

            print("\nNo Branch Found.")

            return

        print()

        print(
            "{:<5}{:<25}{:<15}{:<15}".format(
                "ID",
                "Branch Name",
                "City",
                "Code"
            )
        )

        print("-" * 70)

        for branch in branches:

            print(
                "{:<5}{:<25}{:<15}{:<15}".format(
                    branch["branch_id"],
                    branch["branch_name"],
                    branch["city"],
                    branch["branch_code"]
                )
            )


    # =====================================================
    # Search Branch by Pincode
    # =====================================================

    def search_pincode(self):

        Utils.print_header("SEARCH BRANCH BY PINCODE")

        pincode = input(
            "Enter Pincode : "
        ).strip()

        query = """
        SELECT *
        FROM branch
        WHERE pincode=%s
        ORDER BY branch_name
        """

        branches = db.fetch_all(
            query,
            (pincode,)
        )

        if not branches:

            print("\nNo Branch Found.")

            return

        print()

        for branch in branches:

            print("-" * 60)

            print("Branch ID   :", branch["branch_id"])

            print("Branch Name :", branch["branch_name"])

            print("Branch Code :", branch["branch_code"])

            print("IFSC Code   :", branch["ifsc_code"])

            print("City        :", branch["city"])

            print("State       :", branch["state"])


    # =====================================================
    # Search Branch by Name
    # =====================================================

    def search_branch_name(self):

        Utils.print_header("SEARCH BRANCH NAME")

        name = input(
            "Enter Branch Name : "
        ).strip()

        query = """
        SELECT *
        FROM branch
        WHERE branch_name LIKE %s
        ORDER BY branch_name
        """

        branches = db.fetch_all(
            query,
            ("%" + name + "%",)
        )

        if not branches:

            print("\nNo Branch Found.")

            return

        print()

        print(
            "{:<5}{:<30}{:<15}{:<15}".format(
                "ID",
                "Branch Name",
                "City",
                "State"
            )
        )

        print("-" * 70)

        for branch in branches:

            print(
                "{:<5}{:<30}{:<15}{:<15}".format(
                    branch["branch_id"],
                    branch["branch_name"],
                    branch["city"],
                    branch["state"]
                )
            )


    # =====================================================
    # Check Branch Exists
    # =====================================================

    def branch_exists(self, branch_id):

        query = """
        SELECT branch_id
        FROM branch
        WHERE branch_id=%s
        """

        branch = db.fetch_one(
            query,
            (branch_id,)
        )

        return branch is not None


    # =====================================================
    # Get Branch Details
    # =====================================================

    def get_branch(self, branch_id):

        query = """
        SELECT *
        FROM branch
        WHERE branch_id=%s
        """

        return db.fetch_one(
            query,
            (branch_id,)
        )


    # =====================================================
    # View Branch by IFSC Code
    # =====================================================

    def view_branch_by_ifsc(self):

        Utils.print_header("VIEW BRANCH BY IFSC")

        ifsc = input(
            "Enter IFSC Code : "
        ).strip().upper()

        query = """
        SELECT *
        FROM branch
        WHERE ifsc_code=%s
        """

        branch = db.fetch_one(
            query,
            (ifsc,)
        )

        if not branch:

            print("\nBranch Not Found.")

            return

        print("\nBranch Details")

        print("-" * 60)

        print("Branch ID   :", branch["branch_id"])
        print("Branch Name :", branch["branch_name"])
        print("Branch Code :", branch["branch_code"])
        print("IFSC Code   :", branch["ifsc_code"])
        print("Address     :", branch["address"])
        print("City        :", branch["city"])
        print("State       :", branch["state"])
        print("Pincode     :", branch["pincode"])


    # =====================================================
    # View Branch by Branch Code
    # =====================================================

    def view_branch_by_code(self):

        Utils.print_header("VIEW BRANCH BY CODE")

        code = input(
            "Enter Branch Code : "
        ).strip().upper()

        query = """
        SELECT *
        FROM branch
        WHERE branch_code=%s
        """

        branch = db.fetch_one(
            query,
            (code,)
        )

        if not branch:

            print("\nBranch Not Found.")

            return

        print("\nBranch Details")

        print("-" * 60)

        print("Branch ID   :", branch["branch_id"])
        print("Branch Name :", branch["branch_name"])
        print("Branch Code :", branch["branch_code"])
        print("IFSC Code   :", branch["ifsc_code"])
        print("Address     :", branch["address"])
        print("City        :", branch["city"])
        print("State       :", branch["state"])
        print("Pincode     :", branch["pincode"])


    # =====================================================
    # List Available Cities
    # =====================================================

    def list_cities(self):

        Utils.print_header("CITIES WITH BRANCHES")

        query = """
        SELECT DISTINCT city
        FROM branch
        ORDER BY city
        """

        rows = db.fetch_all(query)

        if not rows:

            print("\nNo Records Found.")

            return

        print()

        for i, row in enumerate(rows, start=1):

            print(f"{i}. {row['city']}")


    # =====================================================
    # List Available States
    # =====================================================

    def list_states(self):

        Utils.print_header("STATES WITH BRANCHES")

        query = """
        SELECT DISTINCT state
        FROM branch
        ORDER BY state
        """

        rows = db.fetch_all(query)

        if not rows:

            print("\nNo Records Found.")

            return

        print()

        for i, row in enumerate(rows, start=1):

            print(f"{i}. {row['state']}")


    # =====================================================
    # Branch Summary
    # =====================================================

    def branch_summary(self):

        Utils.print_header("BRANCH SUMMARY")

        total = self.total_branches()

        print()

        print("Total Branches :", total)

        print()

        query = """
        SELECT
            state,
            COUNT(*) AS total
        FROM branch
        GROUP BY state
        ORDER BY total DESC
        """

        rows = db.fetch_all(query)

        if rows:

            print(
                "{:<20}{:<10}".format(
                    "State",
                    "Branches"
                )
            )

            print("-" * 35)

            for row in rows:

                print(
                    "{:<20}{:<10}".format(
                        row["state"],
                        row["total"]
                    )
                )


    # =====================================================
    # Get Branch Name
    # =====================================================

    def get_branch_name(self, branch_id):

        query = """
        SELECT branch_name
        FROM branch
        WHERE branch_id=%s
        """

        branch = db.fetch_one(
            query,
            (branch_id,)
        )

        if branch:

            return branch["branch_name"]

        return None


    # =====================================================
    # Get Branch Code
    # =====================================================

    def get_branch_code(self, branch_id):

        query = """
        SELECT branch_code
        FROM branch
        WHERE branch_id=%s
        """

        branch = db.fetch_one(
            query,
            (branch_id,)
        )

        if branch:

            return branch["branch_code"]

        return Nonev


    # =====================================================
    # Get IFSC Code
    # =====================================================

    def get_ifsc_code(self, branch_id):

        query = """
        SELECT ifsc_code
        FROM branch
        WHERE branch_id=%s
        """

        branch = db.fetch_one(
            query,
            (branch_id,)
        )

        if branch:

            return branch["ifsc_code"]

        return None


    # =====================================================
    # Get City
    # =====================================================

    def get_city(self, branch_id):

        query = """
        SELECT city
        FROM branch
        WHERE branch_id=%s
        """

        branch = db.fetch_one(
            query,
            (branch_id,)
        )

        if branch:

            return branch["city"]

        return None


    # =====================================================
    # Get State
    # =====================================================

    def get_state(self, branch_id):

        query = """
        SELECT state
        FROM branch
        WHERE branch_id=%s
        """

        branch = db.fetch_one(
            query,
            (branch_id,)
        )

        if branch:

            return branch["state"]

        return None


    # =====================================================
    # Get Complete Address
    # =====================================================

    def get_complete_address(self, branch_id):

        query = """
        SELECT *
        FROM branch
        WHERE branch_id=%s
        """

        branch = db.fetch_one(
            query,
            (branch_id,)
        )

        if not branch:

            return None

        return (
            f"{branch['address']}, "
            f"{branch['city']}, "
            f"{branch['state']} - "
            f"{branch['pincode']}"
        )


    # =====================================================
    # Check Duplicate Branch Code
    # =====================================================

    def branch_code_exists(self, branch_code):

        query = """
        SELECT branch_id
        FROM branch
        WHERE branch_code=%s
        """

        branch = db.fetch_one(
            query,
            (branch_code.upper(),)
        )

        return branch is not None


    # =====================================================
    # Check Duplicate IFSC Code
    # =====================================================

    def ifsc_exists(self, ifsc_code):

        query = """
        SELECT branch_id
        FROM branch
        WHERE ifsc_code=%s
        """

        branch = db.fetch_one(
            query,
            (ifsc_code.upper(),)
        )

        return branch is not None


    # =====================================================
    # Check Branch Exists Using Branch Code
    # =====================================================

    def branch_exists_by_code(self, branch_code):

        query = """
        SELECT *
        FROM branch
        WHERE branch_code=%s
        """

        return db.fetch_one(
            query,
            (branch_code.upper(),)
        )


    # =====================================================
    # Check Branch Exists Using IFSC
    # =====================================================

    def branch_exists_by_ifsc(self, ifsc_code):

        query = """
        SELECT *
        FROM branch
        WHERE ifsc_code=%s
        """

        return db.fetch_one(
            query,
            (ifsc_code.upper(),)
        )


    # =====================================================
    # Get Branch ID Using Branch Code
    # =====================================================

    def get_branch_id(self, branch_code):

        query = """
        SELECT branch_id
        FROM branch
        WHERE branch_code=%s
        """

        branch = db.fetch_one(
            query,
            (branch_code.upper(),)
        )

        if branch:

            return branch["branch_id"]

        return None


    # =====================================================
    # Select Branch
    # =====================================================

    def select_branch(self):

        self.view_all_branches()

        print()

        branch_id = input(
            "Enter Branch ID : "
        ).strip()

        if not self.branch_exists(branch_id):

            print("\nInvalid Branch ID.")

            return None

        return int(branch_id)


    # =====================================================
    # Can Delete Branch?
    # =====================================================

    def can_delete_branch(self, branch_id):

        query = """
        SELECT COUNT(*) AS total
        FROM account
        WHERE branch_id=%s
        """

        row = db.fetch_one(
            query,
            (branch_id,)
        )

        return row["total"] == 0


    # =====================================================
    # Branch Management Menu
    # =====================================================

    def menu(self):

        while True:

            Utils.print_header("BRANCH MANAGEMENT")

            print("1. Add Branch")
            print("2. View Branch")
            print("3. View All Branches")
            print("4. Update Branch")
            print("5. Delete Branch")
            print("6. Search Branch by Name")
            print("7. Search Branch by Code")
            print("8. Search Branch by IFSC")
            print("9. Search Branch by City")
            print("10. Search Branch by State")
            print("11. Search Branch by Pincode")
            print("12. Branch Statistics")
            print("13. Branch Summary")
            print("14. List Cities")
            print("15. List States")
            print("0. Back")

            choice = input("\nEnter Choice : ").strip()

            if choice == "1":

                self.add_branch()

            elif choice == "2":

                self.view_branch()

            elif choice == "3":

                self.view_all_branches()

            elif choice == "4":

                self.update_branch()

            elif choice == "5":

                self.delete_branch()

            elif choice == "6":

                self.search_branch_name()

            elif choice == "7":

                self.search_branch_code()

            elif choice == "8":

                self.search_ifsc()

            elif choice == "9":

                self.search_city()

            elif choice == "10":

                self.search_state()

            elif choice == "11":

                self.search_pincode()

            elif choice == "12":

                self.branch_statistics()

            elif choice == "13":

                self.branch_summary()

            elif choice == "14":

                self.list_cities()

            elif choice == "15":

                self.list_states()

            elif choice == "0":

                break

            else:

                print("\nInvalid Choice.")

            Utils.pause()


    # =====================================================
    # Branch Dashboard
    # =====================================================

    def dashboard(self):

        Utils.print_header("BRANCH DASHBOARD")

        print()

        print(
            "Total Branches :",
            self.total_branches()
        )

        print()

        query = """
        SELECT
            state,
            COUNT(*) AS total
        FROM branch
        GROUP BY state
        ORDER BY total DESC
        LIMIT 5
        """

        rows = db.fetch_all(query)

        if rows:

            print("{:<20}{:<10}".format(
                "State",
                "Branches"
            ))

            print("-" * 35)

            for row in rows:

                print(
                    "{:<20}{:<10}".format(
                        row["state"],
                        row["total"]
                    )
                )


    # =====================================================
    # Refresh Database Connection
    # =====================================================

    def reconnect(self):

        if db.connection is None:

            db.connect()


    # =====================================================
    # Reset Object
    # =====================================================

    def reset(self):

        self.reconnect()


    # =====================================================
    # Destructor
    # =====================================================

    def __del__(self):

        pass


# =====================================================
# Test Module
# =====================================================

if __name__ == "__main__":

    branch = Branch()

    branch.menu()
