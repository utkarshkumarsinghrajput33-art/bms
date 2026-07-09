import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import db
from validations import Validator
from config import (
    FD_INTEREST,
    RD_INTEREST,
    HOME_LOAN_INTEREST,
    VEHICLE_LOAN_INTEREST,
    EDUCATION_LOAN_INTEREST,
    PERSONAL_LOAN_INTEREST
)

app = Flask(__name__)
app.secret_key = 'super_secret_pnb_portal_key_change_in_production'

# ==========================================
# Database Connection Checker
# ==========================================
@app.before_request
def ensure_db_connection():
    try:
        if db.connection is None or not db.connection.is_connected():
            db.connect()
    except Exception:
        db.connect()

# ==========================================
# Root Route
# ==========================================
@app.route('/')
def index():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif session['role'] == 'customer':
            return redirect(url_for('customer_dashboard'))
    return redirect(url_for('login'))

# ==========================================
# Login Route
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        
        if role == 'admin':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            query = "SELECT * FROM admin WHERE username=%s AND password=%s"
            admin = db.fetch_one(query, (username, password))
            
            if admin:
                session['role'] = 'admin'
                session['username'] = admin['username']
                session['full_name'] = admin['full_name']
                session['admin_id'] = admin['admin_id']
                flash('Successfully logged in to Admin Portal.', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid Username or Password.', 'error')
                
        elif role == 'customer':
            account_number = request.form.get('account_number', '').strip()
            password = request.form.get('password', '').strip()
            
            query = """
            SELECT a.*, c.first_name, c.last_name, c.email, c.mobile
            FROM account a
            JOIN customer c ON a.customer_id = c.customer_id
            WHERE a.account_number=%s AND a.login_password=%s
            """
            account = db.fetch_one(query, (account_number, password))
            
            if account:
                if account['status'] != 'Active':
                    flash(f'Login failed: Your account status is {account["status"]}.', 'error')
                    return redirect(url_for('login'))
                
                session['role'] = 'customer'
                session['account_number'] = account['account_number']
                session['customer_id'] = account['customer_id']
                session['full_name'] = f"{account['first_name']} {account['last_name'] or ''}".strip()
                flash('Successfully logged in to Customer Portal.', 'success')
                return redirect(url_for('customer_dashboard'))
            else:
                flash('Invalid Account Number or Password.', 'error')
                
        return redirect(url_for('login'))
        
    return render_template('login.html')

# ==========================================
# Logout Route
# ==========================================
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# ==========================================
# ADMIN DASHBOARD
# ==========================================
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Unauthorized Access. Please login as Administrator.', 'error')
        return redirect(url_for('login'))
        
    # Get statistics
    cust_count = db.fetch_one("SELECT COUNT(*) AS count FROM customer")['count']
    acc_count = db.fetch_one("SELECT COUNT(*) AS count FROM account")['count']
    total_balance = db.fetch_one("SELECT SUM(balance) AS total FROM account")['total'] or 0.0
    pending_loans = db.fetch_one("SELECT COUNT(*) AS count FROM loan WHERE status='Pending'")['count']
    branch_count = db.fetch_one("SELECT COUNT(*) AS count FROM branch")['count']
    
    stats = {
        'customers': cust_count,
        'accounts': acc_count,
        'total_deposits': float(total_balance),
        'pending_loans': pending_loans,
        'branches': branch_count
    }
    
    # Recent global transactions
    recent_tx = db.fetch_all("""
        SELECT t.*, c.first_name, c.last_name
        FROM transactions t
        JOIN account a ON t.account_number = a.account_number
        JOIN customer c ON a.customer_id = c.customer_id
        ORDER BY t.transaction_time DESC
        LIMIT 5
    """)
    
    # Branches list
    branches = db.fetch_all("SELECT * FROM branch ORDER BY branch_name ASC")
    
    return render_template('admin_dashboard.html', active_page='admin_dashboard', stats=stats, recent_transactions=recent_tx, branches=branches)

# ==========================================
# ADMIN BRANCH MANAGEMENT
# ==========================================
@app.route('/admin/branches', methods=['GET', 'POST'])
def admin_branches():
    if session.get('role') != 'admin':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form.get('branch_name', '').strip()
        code = request.form.get('branch_code', '').strip().upper()
        ifsc = request.form.get('ifsc_code', '').strip().upper()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        pincode = request.form.get('pincode', '').strip()
        
        if not Validator.validate_branch_code(code):
            flash('Invalid Branch Code. Must match format: B + 3 digits (e.g. B001).', 'error')
            return redirect(url_for('admin_branches'))
            
        if not Validator.validate_ifsc(ifsc):
            flash('Invalid IFSC Code (e.g. PNB0001234).', 'error')
            return redirect(url_for('admin_branches'))
            
        if not Validator.validate_pincode(pincode):
            flash('Invalid Pincode. Must be exactly 6 digits.', 'error')
            return redirect(url_for('admin_branches'))
            
        # Duplicate Checks
        dup = db.fetch_one("SELECT * FROM branch WHERE branch_code=%s OR ifsc_code=%s", (code, ifsc))
        if dup:
            flash('Branch Code or IFSC Code already registered.', 'error')
            return redirect(url_for('admin_branches'))
            
        # Insert branch
        query = """
        INSERT INTO branch (branch_name, branch_code, ifsc_code, address, city, state, pincode)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        if db.execute(query, (name, code, ifsc, address, city, state, pincode)):
            flash(f'Branch "{name}" registered successfully.', 'success')
        else:
            flash('Error registering branch in database.', 'error')
            
        return redirect(url_for('admin_branches'))
        
    branches = db.fetch_all("SELECT * FROM branch ORDER BY branch_id DESC")
    return render_template('admin_branches.html', active_page='admin_branches', branches=branches)

# ==========================================
# ADMIN CUSTOMER MANAGEMENT
# ==========================================
@app.route('/admin/customers', methods=['GET', 'POST'])
def admin_customers():
    if session.get('role') != 'admin':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip().title()
        last_name = request.form.get('last_name', '').strip().title()
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        mobile = request.form.get('mobile', '').strip()
        email = request.form.get('email', '').strip()
        aadhaar = request.form.get('aadhaar', '').strip()
        pan = request.form.get('pan', '').strip().upper()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip().title()
        state = request.form.get('state', '').strip().title()
        pincode = request.form.get('pincode', '').strip()
        
        # Validate inputs
        if not Validator.validate_name(first_name):
            flash('Invalid Name. Alphabets only, between 2 and 50 characters.', 'error')
            return redirect(url_for('admin_customers'))
        if last_name and not Validator.validate_name(last_name):
            flash('Invalid Last Name.', 'error')
            return redirect(url_for('admin_customers'))
        if not Validator.validate_dob(dob):
            flash('Customer must be at least 18 years old.', 'error')
            return redirect(url_for('admin_customers'))
        if not Validator.validate_mobile(mobile):
            flash('Invalid Indian Mobile Number (10 digits starting with 6-9).', 'error')
            return redirect(url_for('admin_customers'))
        if not Validator.validate_email(email):
            flash('Invalid Email Address.', 'error')
            return redirect(url_for('admin_customers'))
        if not Validator.validate_aadhaar(aadhaar):
            flash('Invalid Aadhaar (exactly 12 digits).', 'error')
            return redirect(url_for('admin_customers'))
        if not Validator.validate_pan(pan):
            flash('Invalid PAN Number (format: ABCDE1234F).', 'error')
            return redirect(url_for('admin_customers'))
        if not Validator.validate_pincode(pincode):
            flash('Invalid Pincode (6 digits).', 'error')
            return redirect(url_for('admin_customers'))
            
        # Duplicate Checks
        dup = db.fetch_one("""
            SELECT * FROM customer 
            WHERE mobile=%s OR email=%s OR aadhaar=%s OR pan=%s
        """, (mobile, email, aadhaar, pan))
        
        if dup:
            flash('Customer already registered with this Mobile, Email, Aadhaar, or PAN.', 'error')
            return redirect(url_for('admin_customers'))
            
        # Insert
        query = """
        INSERT INTO customer (first_name, last_name, gender, dob, mobile, email, aadhaar, pan, address, city, state, pincode)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        if db.execute(query, (first_name, last_name, gender, dob, mobile, email, aadhaar, pan, address, city, state, pincode)):
            flash(f'Customer "{first_name} {last_name}" registered successfully.', 'success')
        else:
            flash('Error inserting customer details.', 'error')
            
        return redirect(url_for('admin_customers'))
        
    customers = db.fetch_all("SELECT * FROM customer ORDER BY customer_id DESC")
    return render_template('admin_customers.html', active_page='admin_customers', customers=customers)

# ==========================================
# ADMIN ACCOUNT MANAGEMENT
# ==========================================
@app.route('/admin/accounts', methods=['GET', 'POST'])
def admin_accounts():
    if session.get('role') != 'admin':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        branch_id = request.form.get('branch_id')
        account_type = request.form.get('account_type')
        balance_str = request.form.get('balance', '0')
        atm_pin = request.form.get('atm_pin', '').strip()
        login_password = request.form.get('login_password', '').strip()
        
        try:
            balance = float(balance_str)
        except ValueError:
            flash('Opening balance must be a number.', 'error')
            return redirect(url_for('admin_accounts'))
            
        if not Validator.validate_amount(balance):
            flash('Invalid Balance amount.', 'error')
            return redirect(url_for('admin_accounts'))
            
        if account_type == 'Savings' and balance < 1000.0:
            flash('Minimum balance for Savings Account is ₹1,000.00.', 'error')
            return redirect(url_for('admin_accounts'))
        elif account_type == 'Current' and balance < 5000.0:
            flash('Minimum balance for Current Account is ₹5,000.00.', 'error')
            return redirect(url_for('admin_accounts'))
            
        if not Validator.validate_atm_pin(atm_pin):
            flash('ATM PIN must be exactly 4 digits.', 'error')
            return redirect(url_for('admin_accounts'))
            
        if not Validator.is_not_empty(login_password):
            flash('Login password cannot be empty.', 'error')
            return redirect(url_for('admin_accounts'))
            
        # Unique Account number generation
        account_number = None
        while True:
            candidate = random.randint(100000000000, 999999999999)
            if not db.fetch_one("SELECT account_number FROM account WHERE account_number=%s", (candidate,)):
                account_number = candidate
                break
                
        # Insert Account
        query = """
        INSERT INTO account (account_number, customer_id, branch_id, account_type, balance, opening_date, status, atm_pin, login_password)
        VALUES (%s, %s, %s, %s, %s, CURDATE(), 'Active', %s, %s)
        """
        
        try:
            db.begin()
            if db.execute(query, (account_number, customer_id, branch_id, account_type, balance, atm_pin, login_password)):
                # Record Opening transaction
                db.execute("""
                    INSERT INTO transactions (account_number, transaction_type, amount, balance_after, description)
                    VALUES (%s, 'Deposit', %s, %s, 'Opening Balance')
                """, (account_number, balance, balance))
                db.commit()
                flash(f'Account {account_number} opened successfully.', 'success')
            else:
                db.rollback()
                flash('Failed to create account.', 'error')
        except Exception as e:
            db.rollback()
            flash(f'Database Error: {e}', 'error')
            
        return redirect(url_for('admin_accounts'))
        
    accounts = db.fetch_all("""
        SELECT a.*, c.first_name, c.last_name, b.branch_name
        FROM account a
        JOIN customer c ON a.customer_id = c.customer_id
        JOIN branch b ON a.branch_id = b.branch_id
        ORDER BY a.opening_date DESC
    """)
    customers = db.fetch_all("SELECT customer_id, first_name, last_name, mobile FROM customer ORDER BY first_name ASC")
    branches = db.fetch_all("SELECT branch_id, branch_name, ifsc_code FROM branch ORDER BY branch_name ASC")
    
    return render_template('admin_accounts.html', active_page='admin_accounts', accounts=accounts, customers=customers, branches=branches)

# ==========================================
# ADMIN LOANS APPROVAL BOARD
# ==========================================
@app.route('/admin/loans')
def admin_loans():
    if session.get('role') != 'admin':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    loans = db.fetch_all("""
        SELECT l.*, c.first_name, c.last_name
        FROM loan l
        JOIN account a ON l.account_number = a.account_number
        JOIN customer c ON a.customer_id = c.customer_id
        ORDER BY l.applied_date DESC
    """)
    return render_template('admin_loans.html', active_page='admin_loans', loans=loans)

@app.route('/admin/loans/action/<int:loan_id>', methods=['POST'])
def admin_loan_action(loan_id):
    if session.get('role') != 'admin':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    action = request.form.get('action')
    loan = db.fetch_one("SELECT * FROM loan WHERE loan_id=%s", (loan_id,))
    
    if not loan:
        flash('Loan application not found.', 'error')
        return redirect(url_for('admin_loans'))
        
    if loan['status'] != 'Pending':
        flash(f'Loan application has already been reviewed ({loan["status"]}).', 'warning')
        return redirect(url_for('admin_loans'))
        
    if action == 'approve':
        # Approve loan and credit account balance
        account = db.fetch_one("SELECT * FROM account WHERE account_number=%s", (loan['account_number'],))
        if not account:
            flash('Customer account linked to loan not found.', 'error')
            return redirect(url_for('admin_loans'))
            
        try:
            db.begin()
            # Update status
            db.execute("UPDATE loan SET status='Approved' WHERE loan_id=%s", (loan_id,))
            
            # Credit balance
            new_balance = float(account['balance']) + float(loan['amount'])
            db.execute("UPDATE account SET balance=%s WHERE account_number=%s", (new_balance, loan['account_number']))
            
            # Log transaction
            db.execute("""
                INSERT INTO transactions (account_number, transaction_type, amount, balance_after, description)
                VALUES (%s, 'Loan', %s, %s, %s)
            """, (loan['account_number'], loan['amount'], new_balance, f"{loan['loan_type']} Loan Approved"))
            
            db.commit()
            flash(f'Loan ID #{loan_id} successfully approved and credited.', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Error processing approval: {e}', 'error')
            
    elif action == 'reject':
        if db.execute("UPDATE loan SET status='Rejected' WHERE loan_id=%s", (loan_id,)):
            flash(f'Loan ID #{loan_id} application rejected.', 'info')
        else:
            flash('Error rejecting loan.', 'error')
            
    return redirect(url_for('admin_loans'))

# ==========================================
# ADMIN TRANSACTION AUDIT
# ==========================================
@app.route('/admin/transactions')
def admin_transactions():
    if session.get('role') != 'admin':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    transactions = db.fetch_all("""
        SELECT t.*, c.first_name, c.last_name
        FROM transactions t
        JOIN account a ON t.account_number = a.account_number
        JOIN customer c ON a.customer_id = c.customer_id
        ORDER BY t.transaction_time DESC
    """)
    return render_template('admin_transactions.html', active_page='admin_transactions', transactions=transactions)


# ==========================================
# CUSTOMER DASHBOARD
# ==========================================
@app.route('/customer/dashboard')
def customer_dashboard():
    if session.get('role') != 'customer':
        flash('Unauthorized Access. Please login as Customer.', 'error')
        return redirect(url_for('login'))
        
    account_number = session['account_number']
    
    # Get complete account & branch & customer details
    account = db.fetch_one("""
        SELECT a.*, c.first_name, c.last_name, b.branch_name, b.branch_code, b.ifsc_code, b.address, b.city, b.state
        FROM account a
        JOIN customer c ON a.customer_id = c.customer_id
        JOIN branch b ON a.branch_id = b.branch_id
        WHERE a.account_number=%s
    """, (account_number,))
    
    # Recent 5 transactions
    transactions = db.fetch_all("""
        SELECT * FROM transactions
        WHERE account_number=%s
        ORDER BY transaction_time DESC
        LIMIT 5
    """, (account_number,))
    
    return render_template('customer_dashboard.html', active_page='customer_dashboard', account=account, transactions=transactions)

# ==========================================
# CUSTOMER CASH SIMULATOR ROUTE
# ==========================================
@app.route('/customer/cash-action', methods=['POST'])
def customer_cash_action():
    if session.get('role') != 'customer':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    account_number = session['account_number']
    operation = request.form.get('operation')
    amount_str = request.form.get('amount', '0')
    
    try:
        amount = float(amount_str)
    except ValueError:
        flash('Amount must be a valid number.', 'error')
        return redirect(url_for('customer_dashboard'))
        
    if not Validator.validate_amount(amount):
        flash('Invalid transaction amount.', 'error')
        return redirect(url_for('customer_dashboard'))
        
    # Fetch current account balance details
    account = db.fetch_one("SELECT balance, account_type FROM account WHERE account_number=%s", (account_number,))
    if not account:
        flash('Account details not found.', 'error')
        return redirect(url_for('customer_dashboard'))
        
    current_balance = float(account['balance'])
    
    if operation == 'Deposit':
        new_balance = current_balance + amount
        
        try:
            db.begin()
            db.execute("UPDATE account SET balance=%s WHERE account_number=%s", (new_balance, account_number))
            db.execute("""
                INSERT INTO transactions (account_number, transaction_type, amount, balance_after, description)
                VALUES (%s, 'Deposit', %s, %s, 'Simulated Cash Deposit')
            """, (account_number, amount, new_balance))
            db.commit()
            flash(f'Simulated Deposit of ₹{amount:,.2f} completed successfully.', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Deposit failed: {e}', 'error')
            
    elif operation == 'Withdraw':
        min_balance = 1000.0 if account['account_type'] == 'Savings' else 5000.0
        
        if current_balance - amount < min_balance:
            flash(f'Withdrawal failed: Insufficient balance. A minimum balance of ₹{min_balance:,.2f} must be maintained.', 'error')
            return redirect(url_for('customer_dashboard'))
            
        new_balance = current_balance - amount
        
        try:
            db.begin()
            db.execute("UPDATE account SET balance=%s WHERE account_number=%s", (new_balance, account_number))
            db.execute("""
                INSERT INTO transactions (account_number, transaction_type, amount, balance_after, description)
                VALUES (%s, 'Withdraw', %s, %s, 'Simulated Cash Withdrawal')
            """, (account_number, amount, new_balance))
            db.commit()
            flash(f'Simulated Withdrawal of ₹{amount:,.2f} completed successfully.', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Withdrawal failed: {e}', 'error')
            
    return redirect(url_for('customer_dashboard'))

# ==========================================
# CUSTOMER FUND TRANSFER
# ==========================================
@app.route('/customer/transfer', methods=['GET', 'POST'])
def customer_transfer():
    if session.get('role') != 'customer':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    account_number = session['account_number']
    
    if request.method == 'POST':
        dest_account = request.form.get('direct_account') or request.form.get('beneficiary_account')
        amount_str = request.form.get('amount', '0')
        description = request.form.get('description', '').strip() or 'Fund Transfer'
        
        if not dest_account:
            flash('Please specify destination recipient account.', 'error')
            return redirect(url_for('customer_transfer'))
            
        dest_account = dest_account.strip()
        
        try:
            amount = float(amount_str)
        except ValueError:
            flash('Transfer amount must be a number.', 'error')
            return redirect(url_for('customer_transfer'))
            
        if not Validator.validate_amount(amount):
            flash('Invalid transfer amount.', 'error')
            return redirect(url_for('customer_transfer'))
            
        if dest_account == str(account_number):
            flash('Cannot transfer funds to the same account.', 'error')
            return redirect(url_for('customer_transfer'))
            
        # Get accounts
        sender = db.fetch_one("SELECT balance, account_type FROM account WHERE account_number=%s", (account_number,))
        receiver = db.fetch_one("SELECT balance, status FROM account WHERE account_number=%s", (dest_account,))
        
        if not sender:
            flash('Sender details error.', 'error')
            return redirect(url_for('customer_transfer'))
            
        if not receiver:
            flash(f'Recipient Account number {dest_account} not found.', 'error')
            return redirect(url_for('customer_transfer'))
            
        if receiver['status'] != 'Active':
            flash(f'Cannot transfer: Recipient account status is currently {receiver["status"]}.', 'error')
            return redirect(url_for('customer_transfer'))
            
        # Check limits
        min_balance = 1000.0 if sender['account_type'] == 'Savings' else 5000.0
        sender_balance = float(sender['balance'])
        receiver_balance = float(receiver['balance'])
        
        if sender_balance - amount < min_balance:
            flash(f'Transfer failed: Insufficient balance. You must maintain minimum ₹{min_balance:,.2f} in your account.', 'error')
            return redirect(url_for('customer_transfer'))
            
        # Perform Transfer
        new_sender_balance = sender_balance - amount
        new_receiver_balance = receiver_balance + amount
        
        try:
            db.begin()
            db.execute("UPDATE account SET balance=%s WHERE account_number=%s", (new_sender_balance, account_number))
            db.execute("UPDATE account SET balance=%s WHERE account_number=%s", (new_receiver_balance, dest_account))
            
            # Logs
            db.execute("""
                INSERT INTO transactions (account_number, transaction_type, amount, balance_after, description)
                VALUES (%s, 'Transfer', %s, %s, %s)
            """, (account_number, amount, new_sender_balance, f"Transfer to A/C: {dest_account} ({description})"))
            
            db.execute("""
                INSERT INTO transactions (account_number, transaction_type, amount, balance_after, description)
                VALUES (%s, 'Deposit', %s, %s, %s)
            """, (dest_account, amount, new_receiver_balance, f"Fund Transfer received from A/C: {account_number}"))
            
            db.commit()
            flash(f'Transferred ₹{amount:,.2f} successfully to Account {dest_account}.', 'success')
            return redirect(url_for('customer_dashboard'))
        except Exception as e:
            db.rollback()
            flash(f'Transfer failed due to system error: {e}', 'error')
            return redirect(url_for('customer_transfer'))
            
    # Get beneficiaries list & sender balance
    beneficiaries = db.fetch_all("SELECT * FROM beneficiary WHERE account_number=%s", (account_number,))
    account = db.fetch_one("SELECT balance, account_type FROM account WHERE account_number=%s", (account_number,))
    
    return render_template('customer_transfer.html', active_page='customer_transfer', beneficiaries=beneficiaries, account=account)

# ==========================================
# CUSTOMER BENEFICIARY MANAGEMENT
# ==========================================
@app.route('/customer/beneficiary', methods=['GET', 'POST'])
def customer_beneficiary():
    if session.get('role') != 'customer':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    account_number = session['account_number']
    
    if request.method == 'POST':
        beneficiary_acc = request.form.get('beneficiary_account', '').strip()
        beneficiary_name = request.form.get('beneficiary_name', '').strip()
        
        if not beneficiary_acc or not beneficiary_name:
            flash('All beneficiary input fields are required.', 'error')
            return redirect(url_for('customer_beneficiary'))
            
        if beneficiary_acc == str(account_number):
            flash('Cannot add your own account as beneficiary.', 'error')
            return redirect(url_for('customer_beneficiary'))
            
        # Check if recipient account exists
        recipient = db.fetch_one("SELECT account_number FROM account WHERE account_number=%s", (beneficiary_acc,))
        if not recipient:
            flash(f'Recipient Account {beneficiary_acc} does not exist.', 'error')
            return redirect(url_for('customer_beneficiary'))
            
        # Check duplicates
        dup = db.fetch_one("SELECT * FROM beneficiary WHERE account_number=%s AND beneficiary_account=%s", (account_number, beneficiary_acc))
        if dup:
            flash('Beneficiary already registered for this account.', 'error')
            return redirect(url_for('customer_beneficiary'))
            
        # Save beneficiary
        query = """
        INSERT INTO beneficiary (account_number, beneficiary_account, beneficiary_name, added_date)
        VALUES (%s, %s, %s, CURDATE())
        """
        if db.execute(query, (account_number, beneficiary_acc, beneficiary_name)):
            flash(f'Beneficiary "{beneficiary_name}" registered successfully.', 'success')
        else:
            flash('Error registering beneficiary.', 'error')
            
        return redirect(url_for('customer_beneficiary'))
        
    beneficiaries = db.fetch_all("SELECT * FROM beneficiary WHERE account_number=%s", (account_number,))
    return render_template('customer_beneficiary.html', active_page='customer_beneficiary', beneficiaries=beneficiaries)

# ==========================================
# CUSTOMER LOANS BOARD
# ==========================================
@app.route('/customer/loans', methods=['GET', 'POST'])
def customer_loans():
    if session.get('role') != 'customer':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    account_number = session['account_number']
    
    if request.method == 'POST':
        loan_type = request.form.get('loan_type')
        amount_str = request.form.get('amount', '0')
        tenure_str = request.form.get('tenure', '0')
        
        try:
            amount = float(amount_str)
            tenure = int(tenure_str)
        except ValueError:
            flash('Amount and tenure must be valid numbers.', 'error')
            return redirect(url_for('customer_loans'))
            
        if not Validator.validate_amount(amount):
            flash('Invalid Loan Amount requested.', 'error')
            return redirect(url_for('customer_loans'))
            
        if not Validator.validate_tenure(tenure):
            flash('Invalid Tenure request (months must be positive).', 'error')
            return redirect(url_for('customer_loans'))
            
        # Map interest rate
        rates = {
            'Home': HOME_LOAN_INTEREST,
            'Vehicle': VEHICLE_LOAN_INTEREST,
            'Education': EDUCATION_LOAN_INTEREST,
            'Personal': PERSONAL_LOAN_INTEREST
        }
        interest_rate = rates.get(loan_type, 10.0)
        
        # Insert Loan application with status 'Pending'
        query = """
        INSERT INTO loan (account_number, loan_type, amount, interest_rate, tenure_months, status, applied_date)
        VALUES (%s, %s, %s, %s, %s, 'Pending', CURDATE())
        """
        if db.execute(query, (account_number, loan_type, amount, interest_rate, tenure)):
            flash(f'Loan Application for ₹{amount:,.2f} submitted successfully to review.', 'success')
        else:
            flash('Error submitting loan request.', 'error')
            
        return redirect(url_for('customer_loans'))
        
    loans = db.fetch_all("SELECT * FROM loan WHERE account_number=%s ORDER BY applied_date DESC", (account_number,))
    return render_template('customer_loans.html', active_page='customer_loans', loans=loans)

# ==========================================
# CUSTOMER FIXED DEPOSIT Vault
# ==========================================
@app.route('/customer/fd', methods=['GET', 'POST'])
def customer_fd():
    if session.get('role') != 'customer':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    account_number = session['account_number']
    
    if request.method == 'POST':
        amount_str = request.form.get('amount', '0')
        tenure_str = request.form.get('tenure', '0')
        
        try:
            amount = float(amount_str)
            tenure = int(tenure_str)
        except ValueError:
            flash('Amount and tenure must be numbers.', 'error')
            return redirect(url_for('customer_fd'))
            
        if amount < 5000:
            flash('Minimum principal for Fixed Deposit is ₹5,000.00.', 'error')
            return redirect(url_for('customer_fd'))
            
        rate = FD_INTEREST.get(tenure)
        if not rate:
            flash('Invalid tenure duration chosen.', 'error')
            return redirect(url_for('customer_fd'))
            
        # Get current balance
        account = db.fetch_one("SELECT balance, account_type FROM account WHERE account_number=%s", (account_number,))
        if not account:
            flash('Sender details error.', 'error')
            return redirect(url_for('customer_fd'))
            
        current_balance = float(account['balance'])
        min_balance = 1000.0 if account['account_type'] == 'Savings' else 5000.0
        
        if current_balance - amount < min_balance:
            flash(f'Unable to open FD: Insufficient account balance. You must maintain ₹{min_balance:,.2f} in your account.', 'error')
            return redirect(url_for('customer_fd'))
            
        # Calculate Maturity
        t = tenure / 12.0
        r = rate / 100.0
        # Compounding quarterly
        maturity_amount = amount * ((1 + r/4)**(4 * t))
        
        # Calculate Maturity Date
        maturity_date = (datetime.now() + timedelta(days=tenure*30)).strftime('%Y-%m-%d')
        
        new_balance = current_balance - amount
        
        # DB Transactions
        try:
            db.begin()
            # Deduct balance
            db.execute("UPDATE account SET balance=%s WHERE account_number=%s", (new_balance, account_number))
            
            # Create FD
            db.execute("""
                INSERT INTO fixed_deposit (account_number, amount, interest_rate, tenure_months, start_date, maturity_date, maturity_amount)
                VALUES (%s, %s, %s, %s, CURDATE(), %s, %s)
            """, (account_number, amount, rate, tenure, maturity_date, maturity_amount))
            
            # Log transaction
            db.execute("""
                INSERT INTO transactions (account_number, transaction_type, amount, balance_after, description)
                VALUES (%s, 'FD', %s, %s, %s)
            """, (account_number, amount, new_balance, f"Fixed Deposit Opened (Maturity Date: {maturity_date})"))
            
            db.commit()
            flash(f'Fixed Deposit account of ₹{amount:,.2f} opened successfully.', 'success')
            return redirect(url_for('customer_fd'))
        except Exception as e:
            db.rollback()
            flash(f'Error opening Fixed Deposit: {e}', 'error')
            return redirect(url_for('customer_fd'))
            
    fds = db.fetch_all("SELECT * FROM fixed_deposit WHERE account_number=%s ORDER BY start_date DESC", (account_number,))
    return render_template('customer_fd.html', active_page='customer_fd', fds=fds)

# ==========================================
# CUSTOMER RECURRING DEPOSIT Vault
# ==========================================
@app.route('/customer/rd', methods=['GET', 'POST'])
def customer_rd():
    if session.get('role') != 'customer':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    account_number = session['account_number']
    
    if request.method == 'POST':
        amount_str = request.form.get('amount', '0')
        tenure_str = request.form.get('tenure', '0')
        
        try:
            amount = float(amount_str)
            tenure = int(tenure_str)
        except ValueError:
            flash('Amount and tenure must be numbers.', 'error')
            return redirect(url_for('customer_rd'))
            
        if amount < 500:
            flash('Minimum monthly investment for Recurring Deposit is ₹500.00.', 'error')
            return redirect(url_for('customer_rd'))
            
        rate = RD_INTEREST.get(tenure)
        if not rate:
            flash('Invalid tenure duration chosen.', 'error')
            return redirect(url_for('customer_rd'))
            
        # Get current balance (first installment deducted immediately!)
        account = db.fetch_one("SELECT balance, account_type FROM account WHERE account_number=%s", (account_number,))
        if not account:
            flash('Sender details error.', 'error')
            return redirect(url_for('customer_rd'))
            
        current_balance = float(account['balance'])
        min_balance = 1000.0 if account['account_type'] == 'Savings' else 5000.0
        
        if current_balance - amount < min_balance:
            flash(f'Unable to open RD: Insufficient account balance. You must maintain ₹{min_balance:,.2f} in your account to cover the first installment.', 'error')
            return redirect(url_for('customer_rd'))
            
        # Calculate maturity
        r = rate / 100.0
        n = 4.0 # compounded quarterly
        maturity_amount = 0.0
        for i in range(1, tenure + 1):
            comp_time = (tenure - i + 1) / 12.0
            maturity_amount += amount * ((1 + r/n)**(n * comp_time))
            
        # Calculate Maturity Date
        maturity_date = (datetime.now() + timedelta(days=tenure*30)).strftime('%Y-%m-%d')
        
        new_balance = current_balance - amount
        
        # DB Transactions
        try:
            db.begin()
            # Deduct balance
            db.execute("UPDATE account SET balance=%s WHERE account_number=%s", (new_balance, account_number))
            
            # Create RD
            db.execute("""
                INSERT INTO recurring_deposit (account_number, monthly_amount, interest_rate, tenure_months, start_date, maturity_date, maturity_amount)
                VALUES (%s, %s, %s, %s, CURDATE(), %s, %s)
            """, (account_number, amount, rate, tenure, maturity_date, maturity_amount))
            
            # Log transaction
            db.execute("""
                INSERT INTO transactions (account_number, transaction_type, amount, balance_after, description)
                VALUES (%s, 'RD', %s, %s, %s)
            """, (account_number, amount, new_balance, f"Recurring Deposit Opened (Maturity Date: {maturity_date})"))
            
            db.commit()
            flash(f'Recurring Deposit account with ₹{amount:,.2f} monthly contribution opened successfully.', 'success')
            return redirect(url_for('customer_rd'))
        except Exception as e:
            db.rollback()
            flash(f'Error opening Recurring Deposit: {e}', 'error')
            return redirect(url_for('customer_rd'))
            
    rds = db.fetch_all("SELECT * FROM recurring_deposit WHERE account_number=%s ORDER BY start_date DESC", (account_number,))
    return render_template('customer_rd.html', active_page='customer_rd', rds=rds)

# ==========================================
# CUSTOMER DETAILED TRANSACTION STATEMENT
# ==========================================
@app.route('/customer/transactions')
def customer_transactions():
    if session.get('role') != 'customer':
        flash('Unauthorized Access.', 'error')
        return redirect(url_for('login'))
        
    account_number = session['account_number']
    
    # Fetch account
    account = db.fetch_one("SELECT account_number FROM account WHERE account_number=%s", (account_number,))
    
    # All transactions
    transactions = db.fetch_all("""
        SELECT * FROM transactions
        WHERE account_number=%s
        ORDER BY transaction_time DESC
    """, (account_number,))
    
    return render_template('customer_transactions.html', active_page='customer_transactions', account=account, transactions=transactions)

# ==========================================
# Run application
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
