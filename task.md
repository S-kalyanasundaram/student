# Task: Student Profile Management System

## Objective

Build a Student Profile Management System using:

-   **Database:** PostgreSQL
-   **Frontend:** Python (Streamlit or Tkinter)
-   **Backend:** Python with PostgreSQL integration using `psycopg2` or
    `SQLAlchemy`

------------------------------------------------------------------------

## Database Design

### Table: `student_profile`

  Column Name      Data Type      Constraint
  ---------------- -------------- --------------
  id               SERIAL         PRIMARY KEY
  name             VARCHAR(26)    NOT NULL
  student_id       VARCHAR(20)    UNIQUE
  relation_name    VARCHAR(26)    
  date_of_birth    DATE           
  aadhaar_number   VARCHAR(12)    UNIQUE
  city             VARCHAR(100)   
  pin_code         VARCHAR(6)     
  is_active        BOOLEAN        DEFAULT TRUE

------------------------------------------------------------------------

## PostgreSQL Tasks

-   [ ] Install PostgreSQL.
-   [ ] Create a database named `student_db`.
-   [ ] Create the `student_profile` table.
-   [ ] Add constraints for unique fields.
-   [ ] Insert sample student records.

------------------------------------------------------------------------

## Python Frontend Tasks

### Student Registration Form

Create a form with the following fields:

-   [ ] Name
-   [ ] Student ID
-   [ ] Relation Name
-   [ ] Date of Birth
-   [ ] Aadhaar Number
-   [ ] City
-   [ ] PIN Code
-   [ ] Active Status (Checkbox)

------------------------------------------------------------------------

## Functional Requirements

-   [ ] Add new student records.
-   [ ] View all student records.
-   [ ] Search students by Name or Student ID.
-   [ ] Update student information.
-   [ ] Delete student records.
-   [ ] Validate Aadhaar Number and PIN Code length.
-   [ ] Display success and error messages.

------------------------------------------------------------------------

## Technologies

-   Python 3.x
-   PostgreSQL
-   psycopg2 / SQLAlchemy
-   Streamlit or Tkinter

------------------------------------------------------------------------

## Deliverables

1.  PostgreSQL database schema.
2.  Python frontend application.
3.  Database connection module.
4.  CRUD functionality.
5.  Project documentation.
