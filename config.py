"""
==========================================================
Banking Management System
File : config.py
Python Version : 3.11.2
MySQL Version : 8.0.46
==========================================================
This file contains all configuration settings used by
the application.
==========================================================
"""

# ==========================
# DATABASE CONFIGURATION
# ==========================

import os

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "uTkArSh"),
    "database": os.environ.get("DB_DATABASE", "banking_management_system"),
    "autocommit": False
}


# ==========================
# BANK DETAILS
# ==========================

BANK_NAME = "Python National Bank"

BANK_SHORT_NAME = "PNB"

BANK_IFSC_PREFIX = "PNB000"

BANK_ADDRESS = "Main Branch, Delhi"


# ==========================
# ACCOUNT SETTINGS
# ==========================

MINIMUM_SAVINGS_BALANCE = 1000.00

MINIMUM_CURRENT_BALANCE = 5000.00

MAX_DAILY_WITHDRAWAL = 50000.00

MAX_DAILY_TRANSFER = 100000.00

DEFAULT_ACCOUNT_STATUS = "Active"

DEFAULT_ACCOUNT_TYPE = "Savings"


# ==========================
# ATM SETTINGS
# ==========================

ATM_PIN_LENGTH = 4

MAX_PIN_ATTEMPTS = 3


# ==========================
# PASSWORD SETTINGS
# ==========================

MIN_PASSWORD_LENGTH = 8

MAX_LOGIN_ATTEMPTS = 5


# ==========================
# LOAN SETTINGS
# ==========================

HOME_LOAN_INTEREST = 8.50

VEHICLE_LOAN_INTEREST = 9.25

EDUCATION_LOAN_INTEREST = 7.80

PERSONAL_LOAN_INTEREST = 12.50


# ==========================
# FD INTEREST RATES
# ==========================

FD_INTEREST = {
    12: 6.50,
    24: 6.90,
    36: 7.10,
    60: 7.50
}


# ==========================
# RD INTEREST RATES
# ==========================

RD_INTEREST = {
    12: 6.20,
    24: 6.60,
    36: 6.90,
    60: 7.20
}


# ==========================
# TRANSACTION TYPES
# ==========================

TRANSACTION_TYPES = (
    "Deposit",
    "Withdraw",
    "Transfer",
    "Loan",
    "FD",
    "RD"
)


# ==========================
# ACCOUNT TYPES
# ==========================

ACCOUNT_TYPES = (
    "Savings",
    "Current"
)


# ==========================
# ACCOUNT STATUS
# ==========================

ACCOUNT_STATUS = (
    "Active",
    "Frozen",
    "Closed"
)


# ==========================
# LOAN TYPES
# ==========================

LOAN_TYPES = (
    "Home",
    "Vehicle",
    "Education",
    "Personal"
)


# ==========================
# LOAN STATUS
# ==========================

LOAN_STATUS = (
    "Pending",
    "Approved",
    "Rejected"
)


# ==========================
# ADMIN DEFAULT LOGIN
# ==========================

DEFAULT_ADMIN_USERNAME = "admin"

DEFAULT_ADMIN_PASSWORD = "admin123"


# ==========================
# DATE FORMAT
# ==========================

DATE_FORMAT = "%Y-%m-%d"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# ==========================
# CURRENCY
# ==========================

CURRENCY_SYMBOL = "₹"

CURRENCY_NAME = "INR"


# ==========================
# APPLICATION VERSION
# ==========================

APP_NAME = "Banking Management System"

APP_VERSION = "1.0"

AUTHOR = "Utkarsh Kumar"


# ==========================
# END OF FILE
# ==========================
