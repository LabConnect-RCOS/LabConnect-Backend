-- rpi_departments relation
CREATE TABLE rpi_departments (
    name VARCHAR(255) PRIMARY KEY,
    description TEXT
);

-- contact_links relation
CREATE TABLE contact_links (
    contact_link VARCHAR(255) PRIMARY KEY,
    contact_type VARCHAR(255)
);

-- lab_runner relation
CREATE TABLE lab_runner (
    rcs_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255)
);

-- opportunities relation
CREATE TABLE opportunities (
    name VARCHAR(255) PRIMARY KEY,
    description TEXT,
    active_status BOOLEAN
);

-- courses relation
CREATE TABLE courses (
    course_code VARCHAR(255) PRIMARY KEY,
    course_name VARCHAR(255)
);

-- majors relation
CREATE TABLE majors (
    major VARCHAR(255) PRIMARY KEY
);

-- experiences relation
CREATE TABLE experiences (
    description TEXT PRIMARY KEY
);

-- class_years relation
CREATE TABLE class_years (
    class_year_id INT PRIMARY KEY IDENTITY(1, 1),
    class_year_name VARCHAR(255)
);

-- application_due_dates relation
CREATE TABLE application_due_dates (
    due_date_id INT PRIMARY KEY IDENTITY(1, 1),
    due_date DATE
);

-- semesters relation
CREATE TABLE semesters (
    semester_id INT PRIMARY KEY IDENTITY(1, 1),
    semester_name VARCHAR(255)
);

-- pay_compensation_info relation
CREATE TABLE pay_compensation_info (
    pay_info_id INT PRIMARY KEY IDENTITY(1, 1),
    pay_info TEXT
);

-- credit_compensation_info relation
CREATE TABLE credit_compensation_info (
    credit_info_id INT PRIMARY KEY IDENTITY(1, 1),
    credit_info TEXT
);
