-- ============================================
-- SALES INTELLIGENCE HUB
-- Sample Data Insertion
-- GUVI | HCL Project
-- ============================================

USE sales_management_system;

-- ─────────────────────────────────────────────
-- INSERT: branches
-- ─────────────────────────────────────────────
INSERT INTO branches (branch_name, branch_admin_name) VALUES
('Chennai', 'Ramesh Kumar'),
('Delhi', 'Priya Sharma'),
('Mumbai', 'Anil Mehta'),
('Bangalore', 'Sneha Reddy');

-- ─────────────────────────────────────────────
-- INSERT: users
-- ─────────────────────────────────────────────
INSERT INTO users (username, password, branch_id, role, email) VALUES
('superadmin', 'Admin@123', NULL, 'Super Admin', 'superadmin@sales.com'),
('chennai_admin', 'Admin@123', 1, 'Admin', 'chennai@sales.com'),
('delhi_admin', 'Admin@123', 2, 'Admin', 'delhi@sales.com'),
('mumbai_admin', 'Admin@123', 3, 'Admin', 'mumbai@sales.com'),
('bangalore_admin', 'Admin@123', 4, 'Admin', 'bangalore@sales.com');

-- ─────────────────────────────────────────────
-- INSERT: customer_sales
-- ─────────────────────────────────────────────
INSERT INTO customer_sales (branch_id, date, name, mobile_number, product_name, gross_sales, status) VALUES
(1, '2024-01-05', 'Arjun Raj', '9876543210', 'DS', 45000.00, 'Open'),
(1, '2024-01-10', 'Meena S', '9876543211', 'DA', 38000.00, 'Close'),
(1, '2024-02-03', 'Karthik V', '9876543212', 'BA', 52000.00, 'Open'),
(2, '2024-01-15', 'Rohit Gupta', '9876543213', 'FSD', 60000.00, 'Open'),
(2, '2024-02-20', 'Anjali Singh', '9876543214', 'DS', 41000.00, 'Close'),
(2, '2024-03-10', 'Vikram D', '9876543215', 'DA', 35000.00, 'Open'),
(3, '2024-01-22', 'Pooja Nair', '9876543216', 'BA', 48000.00, 'Open'),
(3, '2024-02-14', 'Suresh M', '9876543217', 'FSD', 55000.00, 'Close'),
(3, '2024-03-05', 'Deepa K', '9876543218', 'DS', 42000.00, 'Open'),
(4, '2024-01-30', 'Ravi Teja', '9876543219', 'DA', 39000.00, 'Open'),
(4, '2024-02-25', 'Lakshmi P', '9876543220', 'BA', 50000.00, 'Close'),
(4, '2024-03-15', 'Naveen R', '9876543221', 'FSD', 62000.00, 'Open');

-- ─────────────────────────────────────────────
-- INSERT: payment_splits
-- (Trigger will auto-update received_amount)
-- ─────────────────────────────────────────────
INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method) VALUES
(1, '2024-01-05', 20000.00, 'Cash'),
(1, '2024-01-20', 15000.00, 'UPI'),
(2, '2024-01-10', 38000.00, 'Card'),
(3, '2024-02-03', 25000.00, 'Cash'),
(3, '2024-02-20', 20000.00, 'UPI'),
(4, '2024-01-15', 30000.00, 'Card'),
(4, '2024-02-01', 20000.00, 'Cash'),
(5, '2024-02-20', 41000.00, 'UPI'),
(6, '2024-03-10', 15000.00, 'Cash'),
(7, '2024-01-22', 25000.00, 'UPI'),
(7, '2024-02-10', 15000.00, 'Card'),
(8, '2024-02-14', 55000.00, 'Cash'),
(9, '2024-03-05', 20000.00, 'UPI'),
(10, '2024-01-30', 20000.00, 'Card'),
(10, '2024-02-15', 12000.00, 'Cash'),
(11, '2024-02-25', 50000.00, 'UPI'),
(12, '2024-03-15', 30000.00, 'Card');

-- Verify data
SELECT 'Branches' AS Table_Name, COUNT(*) AS Total_Records FROM branches
UNION ALL
SELECT 'Users', COUNT(*) FROM users
UNION ALL
SELECT 'Customer Sales', COUNT(*) FROM customer_sales
UNION ALL
SELECT 'Payment Splits', COUNT(*) FROM payment_splits;
