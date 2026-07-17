

-- USERS table for login and role-based access
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role TEXT NOT NULL
);

-- DONORS table
CREATE TABLE IF NOT EXISTS Donors (
    donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT UNIQUE,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    blood_group TEXT NOT NULL,
    contact VARCHAR(15),
    last_donation DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- RECIPIENTS table
CREATE TABLE IF NOT EXISTS Recipients (
    recipient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT UNIQUE,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    blood_group TEXT NOT NULL,
    contact VARCHAR(15),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- BLOOD INVENTORY table
CREATE TABLE IF NOT EXISTS BloodInventory (
    blood_group TEXT PRIMARY KEY,
    units_available INT DEFAULT 0
);

-- Prepopulate inventory with all blood groups
INSERT OR IGNORE INTO BloodInventory (blood_group, units_available) VALUES
('A+', 0), ('A-', 0), ('B+', 0), ('B-', 0),
('AB+', 0), ('AB-', 0), ('O+', 0), ('O-', 0);

-- REQUESTS table for recipients
CREATE TABLE IF NOT EXISTS Requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_id INT NOT NULL,
    blood_group TEXT NOT NULL,
    units_needed INT NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    request_date DATE,
    FOREIGN KEY (recipient_id) REFERENCES Recipients(recipient_id) ON DELETE CASCADE
);

-- BLOOD DONATIONS table (donation history)
CREATE TABLE IF NOT EXISTS BloodDonations (
    donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_id INT NOT NULL,
    donation_date DATE,
    units_donated INT DEFAULT 1,
    FOREIGN KEY (donor_id) REFERENCES Donors(donor_id) ON DELETE CASCADE
);
