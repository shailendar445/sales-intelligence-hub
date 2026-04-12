-- ============================================
-- SALES INTELLIGENCE HUB
-- SQL Analytical Queries (15 Queries)
-- GUVI | HCL Project
-- ============================================

USE sales_management_system;

-- ─────────────────────────────────────────────
-- BASIC QUERIES
-- ─────────────────────────────────────────────

-- Q1: Retrieve all records from customer_sales
SELECT * FROM customer_sales;

-- Q2: Retrieve all records from branches
SELECT * FROM branches;

-- Q3: Retrieve all records from payment_splits
SELECT * FROM payment_splits;

-- Q4: Display all sales with status = 'Open'
SELECT * FROM customer_sales
WHERE status = 'Open';

-- ─────────────────────────────────────────────
-- AGGREGATION QUERIES
-- ─────────────────────────────────────────────

-- Q5: Calculate total gross sales across all branches
SELECT SUM(gross_sales) AS total_gross_sales
FROM customer_sales;

-- Q6: Calculate total received amount across all sales
SELECT SUM(received_amount) AS total_received_amount
FROM customer_sales;

-- Q7: Calculate total pending amount across all sales
SELECT SUM(pending_amount) AS total_pending_amount
FROM customer_sales;

-- Q8: Count total number of sales per branch
SELECT b.branch_name, COUNT(cs.sale_id) AS total_sales
FROM branches b
JOIN customer_sales cs ON b.branch_id = cs.branch_id
GROUP BY b.branch_name
ORDER BY total_sales DESC;

-- ─────────────────────────────────────────────
-- JOIN-BASED QUERIES
-- ─────────────────────────────────────────────

-- Q9: Retrieve sales details along with the branch name
SELECT cs.sale_id, b.branch_name, cs.date, cs.name,
       cs.product_name, cs.gross_sales,
       cs.received_amount, cs.pending_amount, cs.status
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
ORDER BY cs.sale_id;

-- Q10: Show branch-wise total gross sales (JOIN & GROUP BY)
SELECT b.branch_name,
       SUM(cs.gross_sales) AS total_gross_sales,
       SUM(cs.received_amount) AS total_received,
       SUM(cs.pending_amount) AS total_pending
FROM branches b
JOIN customer_sales cs ON b.branch_id = cs.branch_id
GROUP BY b.branch_name
ORDER BY total_gross_sales DESC;

-- Q11: Display sales along with payment method used
SELECT cs.sale_id, cs.name, cs.gross_sales,
       ps.payment_date, ps.amount_paid, ps.payment_method
FROM customer_sales cs
JOIN payment_splits ps ON cs.sale_id = ps.sale_id
ORDER BY cs.sale_id;

-- ─────────────────────────────────────────────
-- FINANCIAL TRACKING QUERIES
-- ─────────────────────────────────────────────

-- Q12: Find sales where pending amount > 5000
SELECT cs.sale_id, b.branch_name, cs.name,
       cs.gross_sales, cs.received_amount, cs.pending_amount
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
WHERE cs.pending_amount > 5000
ORDER BY cs.pending_amount DESC;

-- Q13: Retrieve top 3 highest gross sales
SELECT cs.sale_id, b.branch_name, cs.name,
       cs.product_name, cs.gross_sales
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
ORDER BY cs.gross_sales DESC
LIMIT 3;

-- Q14: Find the branch with highest total gross sales
SELECT b.branch_name,
       SUM(cs.gross_sales) AS total_sales
FROM branches b
JOIN customer_sales cs ON b.branch_id = cs.branch_id
GROUP BY b.branch_name
ORDER BY total_sales DESC
LIMIT 1;

-- Q15: Calculate payment method-wise total collection
SELECT payment_method,
       COUNT(*) AS total_transactions,
       SUM(amount_paid) AS total_collection
FROM payment_splits
GROUP BY payment_method
ORDER BY total_collection DESC;
