-- =======================================
-- 1️⃣ Customers
-- =======================================
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT NOT NULL,
    signup_date DATE NOT NULL
);

INSERT INTO customers (name, region, signup_date) VALUES
('Alice Smith', 'North', '2024-01-10'),
('Bob Johnson', 'South', '2024-01-15'),
('Charlie Lee', 'East', '2024-02-01'),
('Diana Patel', 'West', '2024-02-05'),
('Ethan Brown', 'North', '2024-02-12'),
('Fiona White', 'South', '2024-02-20'),
('George Kim', 'East', '2024-03-01'),
('Hannah Cruz', 'West', '2024-03-03'),
('Ian Davis', 'North', '2024-03-10'),
('Jane Wilson', 'South', '2024-03-15');

-- =======================================
-- 2️⃣ Products
-- =======================================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price NUMERIC NOT NULL
);

INSERT INTO products (name, category, price) VALUES
('Laptop Pro 14', 'Electronics', 1200),
('Laptop Air 13', 'Electronics', 900),
('Smartphone X', 'Electronics', 700),
('Office Chair', 'Furniture', 150),
('Desk Lamp', 'Furniture', 40),
('Coffee Machine', 'Appliances', 120),
('Blender', 'Appliances', 60),
('Running Shoes', 'Apparel', 80),
('T-Shirt', 'Apparel', 25),
('Jeans', 'Apparel', 50);

-- =======================================
-- 3️⃣ Orders
-- =======================================
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    product_id INT REFERENCES products(id),
    order_date DATE NOT NULL,
    quantity INT NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO orders (customer_id, product_id, order_date, quantity, status) VALUES
(1, 1, '2024-03-01', 1, 'completed'),
(2, 3, '2024-03-02', 2, 'completed'),
(3, 5, '2024-03-03', 1, 'cancelled'),
(4, 2, '2024-03-04', 1, 'completed'),
(5, 6, '2024-03-05', 1, 'completed'),
(6, 7, '2024-03-06', 3, 'completed'),
(7, 8, '2024-03-07', 2, 'completed'),
(8, 4, '2024-03-08', 1, 'completed'),
(9, 9, '2024-03-09', 5, 'completed'),
(10, 10, '2024-03-10', 2, 'completed');

-- =======================================
-- 4️⃣ Payments
-- =======================================
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    payment_date DATE NOT NULL,
    amount NUMERIC NOT NULL,
    method TEXT NOT NULL
);

INSERT INTO payments (order_id, payment_date, amount, method) VALUES
(1, '2024-03-01', 1200, 'credit'),
(2, '2024-03-02', 1400, 'debit'),
(4, '2024-03-04', 900, 'credit'),
(5, '2024-03-05', 120, 'paypal'),
(6, '2024-03-06', 180, 'credit'),
(7, '2024-03-07', 160, 'debit'),
(8, '2024-03-08', 150, 'credit'),
(9, '2024-03-09', 125, 'paypal'),
(10, '2024-03-10', 100, 'credit');

-- =======================================
-- 5️⃣ Inventory
-- =======================================
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    stock_quantity INT NOT NULL,
    warehouse TEXT NOT NULL
);

INSERT INTO inventory (product_id, stock_quantity, warehouse) VALUES
(1, 10, 'North'),
(2, 8, 'East'),
(3, 15, 'South'),
(4, 20, 'West'),
(5, 30, 'North'),
(6, 12, 'East'),
(7, 25, 'South'),
(8, 50, 'West'),
(9, 40, 'North'),
(10, 35, 'East');
