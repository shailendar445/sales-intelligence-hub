import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Golden@0415",
        database="sales_management_system"
    )

st.set_page_config(page_title="Sales Intelligence Hub", page_icon="📊", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "branch_id" not in st.session_state:
    st.session_state.branch_id = None

def login_page():
    st.markdown("<h1 style='text-align:center;'>📊 Sales Intelligence Hub</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:gray;'>GUVI | HCL Project</h4>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
                user = cursor.fetchone()
                conn.close()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.role = user["role"]
                    st.session_state.branch_id = user["branch_id"]
                    st.success(f"Welcome, {user['username']}! ({user['role']})")
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
            except Exception as e:
                st.error(f"Connection error: {e}")

def get_branches():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM branches")
    branches = cursor.fetchall()
    conn.close()
    return branches

def dashboard():
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.markdown(f"**Role:** {st.session_state.role}")
        st.markdown("---")
        menu = st.radio("Navigation", [
            "🏠 Dashboard",
            "➕ Add Sale",
            "💳 Add Payment",
            "📋 View Sales",
            "💰 Pending Payments",
            "📊 Analytics",
            "🔍 SQL Queries"
        ])
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.session_state.branch_id = None
            st.rerun()

    if menu == "🏠 Dashboard":
        st.title("📊 Sales Intelligence Hub")
        st.markdown(f"Welcome back, **{st.session_state.username}**!")
        st.markdown("---")
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if st.session_state.role == "Super Admin":
            cursor.execute("SELECT SUM(gross_sales) as total, SUM(received_amount) as received, SUM(pending_amount) as pending FROM customer_sales")
        else:
            cursor.execute("SELECT SUM(gross_sales) as total, SUM(received_amount) as received, SUM(pending_amount) as pending FROM customer_sales WHERE branch_id=%s", (st.session_state.branch_id,))
        kpi = cursor.fetchone()
        conn.close()
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total Gross Sales", f"₹{kpi['total'] or 0:,.2f}")
        col2.metric("✅ Total Received", f"₹{kpi['received'] or 0:,.2f}")
        col3.metric("⏳ Total Pending", f"₹{kpi['pending'] or 0:,.2f}")

    elif menu == "➕ Add Sale":
        st.title("➕ Add New Sale")
        st.markdown("---")
        branches = get_branches()
        branch_dict = {b["branch_name"]: b["branch_id"] for b in branches}
        with st.form("add_sale_form"):
            if st.session_state.role == "Super Admin":
                branch_name = st.selectbox("Branch", list(branch_dict.keys()))
                selected_branch_id = branch_dict[branch_name]
            else:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT branch_name FROM branches WHERE branch_id=%s", (st.session_state.branch_id,))
                b = cursor.fetchone()
                conn.close()
                st.info(f"Branch: **{b['branch_name']}**")
                selected_branch_id = st.session_state.branch_id
            sale_date = st.date_input("Sale Date", value=date.today())
            name = st.text_input("Customer Name")
            mobile = st.text_input("Mobile Number")
            product = st.selectbox("Product", ["DS", "DA", "BA", "FSD"])
            gross_sales = st.number_input("Gross Sales Amount (₹)", min_value=0.0, step=100.0)
            status = st.selectbox("Status", ["Open", "Close"])
            submitted = st.form_submit_button("Add Sale")
            if submitted:
                if name and mobile and gross_sales > 0:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO customer_sales (branch_id, date, name, mobile_number, product_name, gross_sales, status) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                            (selected_branch_id, sale_date, name, mobile, product, gross_sales, status)
                        )
                        conn.commit()
                        conn.close()
                        st.success(f"✅ Sale added successfully for {name}!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please fill all fields!")

    elif menu == "💳 Add Payment":
        st.title("💳 Add Payment Split")
        st.markdown("---")
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if st.session_state.role == "Super Admin":
            cursor.execute("SELECT sale_id, name, gross_sales, pending_amount FROM customer_sales WHERE status='Open'")
        else:
            cursor.execute("SELECT sale_id, name, gross_sales, pending_amount FROM customer_sales WHERE branch_id=%s AND status='Open'", (st.session_state.branch_id,))
        sales = cursor.fetchall()
        conn.close()
        if not sales:
            st.info("No open sales found!")
        else:
            sale_options = {f"ID:{s['sale_id']} - {s['name']} (Pending: ₹{s['pending_amount']})": s['sale_id'] for s in sales}
            with st.form("add_payment_form"):
                selected_sale = st.selectbox("Select Sale", list(sale_options.keys()))
                payment_date = st.date_input("Payment Date", value=date.today())
                amount_paid = st.number_input("Amount Paid (₹)", min_value=0.0, step=100.0)
                payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Card"])
                submitted = st.form_submit_button("Add Payment")
                if submitted:
                    if amount_paid > 0:
                        try:
                            conn = get_connection()
                            cursor = conn.cursor()
                            sale_id = sale_options[selected_sale]
                            cursor.execute(
                                "INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method) VALUES (%s,%s,%s,%s)",
                                (sale_id, payment_date, amount_paid, payment_method)
                            )
                            conn.commit()
                            conn.close()
                            st.success("✅ Payment added successfully!")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.warning("Please enter a valid amount!")

    elif menu == "📋 View Sales":
        st.title("📋 Sales Report")
        st.markdown("---")
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if st.session_state.role == "Super Admin":
            branches = get_branches()
            branch_options = ["All Branches"] + [b["branch_name"] for b in branches]
            selected_branch = st.selectbox("Filter by Branch", branch_options)
            if selected_branch == "All Branches":
                cursor.execute("""
                    SELECT cs.sale_id, b.branch_name, cs.date, cs.name,
                           cs.mobile_number, cs.product_name, cs.gross_sales,
                           cs.received_amount, cs.pending_amount, cs.status
                    FROM customer_sales cs
                    JOIN branches b ON cs.branch_id = b.branch_id
                    ORDER BY cs.sale_id DESC
                """)
            else:
                cursor.execute("""
                    SELECT cs.sale_id, b.branch_name, cs.date, cs.name,
                           cs.mobile_number, cs.product_name, cs.gross_sales,
                           cs.received_amount, cs.pending_amount, cs.status
                    FROM customer_sales cs
                    JOIN branches b ON cs.branch_id = b.branch_id
                    WHERE b.branch_name = %s
                    ORDER BY cs.sale_id DESC
                """, (selected_branch,))
        else:
            cursor.execute("""
                SELECT cs.sale_id, b.branch_name, cs.date, cs.name,
                       cs.mobile_number, cs.product_name, cs.gross_sales,
                       cs.received_amount, cs.pending_amount, cs.status
                FROM customer_sales cs
                JOIN branches b ON cs.branch_id = b.branch_id
                WHERE cs.branch_id = %s
                ORDER BY cs.sale_id DESC
            """, (st.session_state.branch_id,))
        sales = cursor.fetchall()
        conn.close()
        if sales:
            df = pd.DataFrame(sales)
            st.dataframe(df, use_container_width=True)
            st.info(f"Total Records: {len(df)}")
        else:
            st.info("No sales records found!")

    elif menu == "💰 Pending Payments":
        st.title("💰 Pending Payments")
        st.markdown("---")
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if st.session_state.role == "Super Admin":
            cursor.execute("""
                SELECT cs.sale_id, b.branch_name, cs.name, cs.product_name,
                       cs.gross_sales, cs.received_amount, cs.pending_amount, cs.status
                FROM customer_sales cs
                JOIN branches b ON cs.branch_id = b.branch_id
                WHERE cs.pending_amount > 0
                ORDER BY cs.pending_amount DESC
            """)
        else:
            cursor.execute("""
                SELECT cs.sale_id, b.branch_name, cs.name, cs.product_name,
                       cs.gross_sales, cs.received_amount, cs.pending_amount, cs.status
                FROM customer_sales cs
                JOIN branches b ON cs.branch_id = b.branch_id
                WHERE cs.branch_id = %s AND cs.pending_amount > 0
                ORDER BY cs.pending_amount DESC
            """, (st.session_state.branch_id,))
        pending = cursor.fetchall()
        conn.close()
        if pending:
            df = pd.DataFrame(pending)
            st.dataframe(df, use_container_width=True)
            total_pending = df["pending_amount"].sum()
            st.error(f"Total Pending Amount: ₹{total_pending:,.2f}")
        else:
            st.success("No pending payments! 🎉")

    elif menu == "📊 Analytics":
        st.title("📊 Analytics & Insights")
        st.markdown("---")
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT b.branch_name,
                   SUM(cs.gross_sales) AS gross,
                   SUM(cs.received_amount) AS received,
                   SUM(cs.pending_amount) AS pending
            FROM branches b
            JOIN customer_sales cs ON b.branch_id = cs.branch_id
            GROUP BY b.branch_name
        """)
        branch_data = cursor.fetchall()
        cursor.execute("SELECT payment_method, SUM(amount_paid) AS total FROM payment_splits GROUP BY payment_method")
        payment_data = cursor.fetchall()
        cursor.execute("SELECT status, COUNT(*) AS count FROM customer_sales GROUP BY status")
        status_data = cursor.fetchall()
        conn.close()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🏢 Branch-wise Sales")
            if branch_data:
                df_branch = pd.DataFrame(branch_data)
                st.dataframe(df_branch, use_container_width=True)
                st.bar_chart(df_branch.set_index("branch_name")["gross"])
        with col2:
            st.subheader("💳 Payment Method Summary")
            if payment_data:
                df_pay = pd.DataFrame(payment_data)
                st.dataframe(df_pay, use_container_width=True)
        st.subheader("📈 Sales Status (Open vs Close)")
        if status_data:
            df_status = pd.DataFrame(status_data)
            st.dataframe(df_status, use_container_width=True)

    elif menu == "🔍 SQL Queries":
        st.title("🔍 Predefined SQL Queries")
        st.markdown("---")
        queries = {
            "1. All Customer Sales": "SELECT * FROM customer_sales",
            "2. All Branches": "SELECT * FROM branches",
            "3. All Payment Splits": "SELECT * FROM payment_splits",
            "4. Open Sales": "SELECT * FROM customer_sales WHERE status='Open'",
            "5. Total Gross Sales": "SELECT SUM(gross_sales) AS total_gross_sales FROM customer_sales",
            "6. Total Received Amount": "SELECT SUM(received_amount) AS total_received FROM customer_sales",
            "7. Total Pending Amount": "SELECT SUM(pending_amount) AS total_pending FROM customer_sales",
            "8. Sales Count Per Branch": "SELECT b.branch_name, COUNT(cs.sale_id) AS total_sales FROM branches b JOIN customer_sales cs ON b.branch_id=cs.branch_id GROUP BY b.branch_name",
            "9. Sales With Branch Name": "SELECT cs.sale_id, cs.name, cs.product_name, cs.gross_sales, cs.status, b.branch_name FROM customer_sales cs JOIN branches b ON cs.branch_id=b.branch_id",
            "10. Branch-wise Total Gross Sales": "SELECT b.branch_name, SUM(cs.gross_sales) AS total_gross FROM branches b JOIN customer_sales cs ON b.branch_id=cs.branch_id GROUP BY b.branch_name",
            "11. Sales With Payment Method": "SELECT cs.sale_id, cs.name, cs.gross_sales, ps.payment_method, ps.amount_paid FROM customer_sales cs JOIN payment_splits ps ON cs.sale_id=ps.sale_id",
            "12. Pending Amount > 5000": "SELECT sale_id, name, gross_sales, received_amount, pending_amount FROM customer_sales WHERE pending_amount > 5000",
            "13. Top 3 Highest Gross Sales": "SELECT sale_id, name, gross_sales FROM customer_sales ORDER BY gross_sales DESC LIMIT 3",
            "14. Branch With Highest Sales": "SELECT b.branch_name, SUM(cs.gross_sales) AS total_sales FROM branches b JOIN customer_sales cs ON b.branch_id=cs.branch_id GROUP BY b.branch_name ORDER BY total_sales DESC LIMIT 1",
            "15. Payment Method-wise Total Collection": "SELECT payment_method, SUM(amount_paid) AS total_collection FROM payment_splits GROUP BY payment_method"
        }
        selected_query = st.selectbox("Select a Query", list(queries.keys()))
        st.code(queries[selected_query], language="sql")
        if st.button("▶ Execute Query"):
            try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute(queries[selected_query])
                results = cursor.fetchall()
                conn.close()
                if results:
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True)
                    st.success(f"✅ {len(df)} rows returned")
                else:
                    st.info("No results found!")
            except Exception as e:
                st.error(f"Error: {e}")

if st.session_state.logged_in:
    dashboard()
else:
    login_page()
