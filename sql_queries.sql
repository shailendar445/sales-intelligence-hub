USE sales_management_system;
SELECT * FROM customer_sales;
SELECT * FROM branches;
SELECT * FROM payment_splits;
SELECT * FROM customer_sales
WHERE status = 'Open';
SELECT SUM(gross_sales) AS total_gross_sales
FROM customer_sales;
SELECT SUM(received_amount) AS total_received_amount
FROM customer_sales;
SELECT SUM(pending_amount) AS total_pending_amount
FROM customer_sales;
SELECT b.branch_name, COUNT(cs.sale_id) AS total_sales
FROM branches b
JOIN customer_sales cs ON b.branch_id = cs.branch_id
GROUP BY b.branch_name
ORDER BY total_sales DESC;
SELECT cs.sale_id, b.branch_name, cs.date, cs.name,
       cs.product_name, cs.gross_sales,
       cs.received_amount, cs.pending_amount, cs.status
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
ORDER BY cs.sale_id;
SELECT b.branch_name,
       SUM(cs.gross_sales) AS total_gross_sales,
       SUM(cs.received_amount) AS total_received,
       SUM(cs.pending_amount) AS total_pending
FROM branches b
JOIN customer_sales cs ON b.branch_id = cs.branch_id
GROUP BY b.branch_name
ORDER BY total_gross_sales DESC;
SELECT cs.sale_id, cs.name, cs.gross_sales,
       ps.payment_date, ps.amount_paid, ps.payment_method
FROM customer_sales cs
JOIN payment_splits ps ON cs.sale_id = ps.sale_id
ORDER BY cs.sale_id;
SELECT cs.sale_id, b.branch_name, cs.name,
       cs.gross_sales, cs.received_amount, cs.pending_amount
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
WHERE cs.pending_amount > 5000
ORDER BY cs.pending_amount DESC;
SELECT cs.sale_id, b.branch_name, cs.name,
       cs.product_name, cs.gross_sales
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
ORDER BY cs.gross_sales DESC
LIMIT 3;
SELECT b.branch_name,
       SUM(cs.gross_sales) AS total_sales
FROM branches b
JOIN customer_sales cs ON b.branch_id = cs.branch_id
GROUP BY b.branch_name
ORDER BY total_sales DESC
LIMIT 1;
SELECT payment_method,
       COUNT(*) AS total_transactions,
       SUM(amount_paid) AS total_collection
FROM payment_splits
GROUP BY payment_method
ORDER BY total_collection DESC;
