# ============================================
# SALES INTELLIGENCE HUB
# Python - MySQL Connection Script
# GUVI | HCL Project
# ============================================

import mysql.connector
from mysql.connector import Error

# ─────────────────────────────────────────────
# DATABASE CONFIGURATION
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Golden@0415",
    "database": "sales_management_system"
}

# ─────────────────────────────────────────────
# GET CONNECTION
# ─────────────────────────────────────────────
def get_connection():
    """Create and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ─────────────────────────────────────────────
# EXECUTE QUERY (SELECT)
# ─────────────────────────────────────────────
def execute_query(query, params=None):
    """Execute a SELECT query and return results as list of dicts."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Query error: {e}")
        return []
    finally:
        conn.close()

# ─────────────────────────────────────────────
# EXECUTE INSERT / UPDATE / DELETE
# ─────────────────────────────────────────────
def execute_update(query, params=None):
    """Execute INSERT, UPDATE or DELETE query."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except Error as e:
        print(f"Update error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# ─────────────────────────────────────────────
# AUTHENTICATION
# ─────────────────────────────────────────────
def authenticate_user(username, password):
    """Validate user credentials and return user details."""
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    results = execute_query(query, (username, password))
    return results[0] if results else None

# ─────────────────────────────────────────────
# BRANCH FUNCTIONS
# ─────────────────────────────────────────────
def get_all_branches():
    """Fetch all branches."""
    return execute_query("SELECT * FROM branches")

def get_branch_by_id(branch_id):
    """Fetch a specific branch by ID."""
    results = execute_query("SELECT * FROM branches WHERE branch_id=%s", (branch_id,))
    return results[0] if results else None

# ─────────────────────────────────────────────
# SALES FUNCTIONS
# ─────────────────────────────────────────────
def get_all_sales():
    """Fetch all sales with branch name."""
    query = """
        SELECT cs.*, b.branch_name
        FROM customer_sales cs
        JOIN branches b ON cs.branch_id = b.branch_id
        ORDER BY cs.sale_id DESC
    """
    return execute_query(query)

def get_sales_by_branch(branch_id):
    """Fetch sales for a specific branch."""
    query = """
        SELECT cs.*, b.branch_name
        FROM customer_sales cs
        JOIN branches b ON cs.branch_id = b.branch_id
        WHERE cs.branch_id = %s
        ORDER BY cs.sale_id DESC
    """
    return execute_query(query, (branch_id,))

def add_sale(branch_id, date, name, mobile, product, gross_sales, status):
    """Insert a new sale record."""
    query = """
        INSERT INTO customer_sales
        (branch_id, date, name, mobile_number, product_name, gross_sales, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return execute_update(query, (branch_id, date, name, mobile, product, gross_sales, status))

# ─────────────────────────────────────────────
# PAYMENT FUNCTIONS
# ─────────────────────────────────────────────
def get_all_payments():
    """Fetch all payment splits."""
    return execute_query("SELECT * FROM payment_splits ORDER BY payment_id DESC")

def add_payment(sale_id, payment_date, amount_paid, payment_method):
    """Insert a new payment split (trigger auto-updates received_amount)."""
    query = """
        INSERT INTO payment_splits
        (sale_id, payment_date, amount_paid, payment_method)
        VALUES (%s, %s, %s, %s)
    """
    return execute_update(query, (sale_id, payment_date, amount_paid, payment_method))

# ─────────────────────────────────────────────
# KPI / ANALYTICS FUNCTIONS
# ─────────────────────────────────────────────
def get_financial_kpi(branch_id=None):
    """Get total gross, received, and pending amounts."""
    if branch_id:
        query = """
            SELECT SUM(gross_sales) AS total,
                   SUM(received_amount) AS received,
                   SUM(pending_amount) AS pending
            FROM customer_sales WHERE branch_id=%s
        """
        results = execute_query(query, (branch_id,))
    else:
        query = """
            SELECT SUM(gross_sales) AS total,
                   SUM(received_amount) AS received,
                   SUM(pending_amount) AS pending
            FROM customer_sales
        """
        results = execute_query(query)
    return results[0] if results else {"total": 0, "received": 0, "pending": 0}

def get_branch_wise_sales():
    """Get branch-wise sales summary."""
    query = """
        SELECT b.branch_name,
               SUM(cs.gross_sales) AS gross,
               SUM(cs.received_amount) AS received,
               SUM(cs.pending_amount) AS pending
        FROM branches b
        JOIN customer_sales cs ON b.branch_id = cs.branch_id
        GROUP BY b.branch_name
    """
    return execute_query(query)

def get_payment_method_summary():
    """Get payment method-wise total collection."""
    query = """
        SELECT payment_method, SUM(amount_paid) AS total
        FROM payment_splits
        GROUP BY payment_method
    """
    return execute_query(query)

def get_pending_sales(branch_id=None):
    """Get sales with pending amounts."""
    if branch_id:
        query = """
            SELECT cs.sale_id, b.branch_name, cs.name, cs.product_name,
                   cs.gross_sales, cs.received_amount, cs.pending_amount, cs.status
            FROM customer_sales cs
            JOIN branches b ON cs.branch_id = b.branch_id
            WHERE cs.pending_amount > 0 AND cs.branch_id = %s
            ORDER BY cs.pending_amount DESC
        """
        return execute_query(query, (branch_id,))
    else:
        query = """
            SELECT cs.sale_id, b.branch_name, cs.name, cs.product_name,
                   cs.gross_sales, cs.received_amount, cs.pending_amount, cs.status
            FROM customer_sales cs
            JOIN branches b ON cs.branch_id = b.branch_id
            WHERE cs.pending_amount > 0
            ORDER BY cs.pending_amount DESC
        """
        return execute_query(query)

# ─────────────────────────────────────────────
# TEST CONNECTION
# ─────────────────────────────────────────────
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("✅ MySQL Connection Successful!")
        print(f"   Host: {DB_CONFIG['host']}")
        print(f"   Database: {DB_CONFIG['database']}")
        conn.close()

        # Test KPI
        kpi = get_financial_kpi()
        print(f"\n📊 Financial KPI Summary:")
        print(f"   Total Gross Sales : ₹{kpi['total']:,.2f}")
        print(f"   Total Received    : ₹{kpi['received']:,.2f}")
        print(f"   Total Pending     : ₹{kpi['pending']:,.2f}")

        # Test branches
        branches = get_all_branches()
        print(f"\n🏢 Branches ({len(branches)} total):")
        for b in branches:
            print(f"   - {b['branch_name']} (Admin: {b['branch_admin_name']})")
    else:
        print("❌ Connection Failed! Check your MySQL credentials.")
