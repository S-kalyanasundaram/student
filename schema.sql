-- Create the target database (run from a superuser or postgres user)
CREATE DATABASE student_db;

\c student_db

CREATE TABLE IF NOT EXISTS student_profile (
    id SERIAL PRIMARY KEY,
    name VARCHAR(26) NOT NULL,
    student_id VARCHAR(20) UNIQUE,
    relation_name VARCHAR(26),
    date_of_birth DATE,
    aadhaar_number VARCHAR(12) UNIQUE,
    city VARCHAR(100),
    pin_code VARCHAR(6),
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO student_profile (name, student_id, relation_name, date_of_birth, aadhaar_number, city, pin_code, is_active)
VALUES
    ('Rahul Sharma', 'STU1001', 'Sunita Sharma', '2004-05-12', '123456789012', 'Mumbai', '400001', TRUE),
    ('Anita Singh', 'STU1002', 'Raj Singh', '2005-08-24', '234567890123', 'Delhi', '110001', TRUE)
ON CONFLICT DO NOTHING;
