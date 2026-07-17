-- Use the bloodbank database


-- Insert more Users
INSERT INTO Users (username, password, role) VALUES
('admin_khushi', 'admin123', 'admin'),
('donor_devesh', 'pass123', 'donor'),
('donor_akshat', 'pass456', 'donor'),
('donor_radhika', 'pass789', 'donor'),
('donor_aman', 'pass111', 'donor'),
('recipient_kartik', 'pass222', 'recipient'),
('recipient_sanya', 'pass333', 'recipient'),
('recipient_mohit', 'pass444', 'recipient');

-- Insert Donors (user_ids 2-5)
INSERT INTO Donors (user_id, name, age, blood_group, contact, last_donation) VALUES
(2, 'Devesh Mehta', 30, 'A+', '9876543210', '2024-12-10'),
(3, 'Akshat Sharma', 27, 'O-', '9123456789', '2025-01-15'),
(4, 'Radhika Nair', 24, 'B+', '9001122334', '2025-03-20'),
(5, 'Aman Kapoor', 35, 'AB+', '9112233445', '2025-04-05');

-- Insert Recipients (user_ids 6-8)
INSERT INTO Recipients (user_id, name, age, blood_group, contact) VALUES
(6, 'Kartik Iyer', 45, 'A+', '9988776655'),
(7, 'Sanya Verma', 29, 'B-', '8877665544'),
(8, 'Mohit Rathi', 60, 'O+', '7788996655');

-- Update BloodInventory (simulate stock)
UPDATE BloodInventory SET units_available = 5 WHERE blood_group = 'A+';
UPDATE BloodInventory SET units_available = 2 WHERE blood_group = 'O-';
UPDATE BloodInventory SET units_available = 0 WHERE blood_group = 'B-';
UPDATE BloodInventory SET units_available = 4 WHERE blood_group = 'B+';
UPDATE BloodInventory SET units_available = 3 WHERE blood_group = 'AB+';
UPDATE BloodInventory SET units_available = 6 WHERE blood_group = 'O+';

-- Insert Requests
-- recipient_id = 1 → Kartik, 2 → Sanya, 3 → Mohit
INSERT INTO Requests (recipient_id, blood_group, units_needed, status, request_date) VALUES
(1, 'A+', 2, 'Pending', '2025-05-10'),
(2, 'B-', 3, 'Pending', '2025-05-11'),
(3, 'O+', 1, 'Fulfilled', '2025-04-20'),
(1, 'A+', 1, 'Fulfilled', '2025-03-18');

-- Insert BloodDonations
-- donor_id = 1 → Devesh, 2 → Akshat, 3 → Radhika, 4 → Aman
INSERT INTO BloodDonations (donor_id, donation_date, units_donated) VALUES
(1, '2024-12-10', 1),
(2, '2025-01-15', 1),
(3, '2025-03-20', 2),
(4, '2025-04-05', 1),
(1, '2025-04-25', 1),
(2, '2025-05-01', 1);
