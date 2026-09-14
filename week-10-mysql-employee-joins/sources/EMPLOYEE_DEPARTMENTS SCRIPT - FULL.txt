CREATE DATABASE IF NOT EXISTS employee_departments_db;

USE employee_departments_db;

CREATE TABLE IF NOT EXISTS location (
	LocationID CHAR(4) PRIMARY KEY,
	Address1 VARCHAR(40),
	Address2 VARCHAR(40),
	City VARCHAR(40),
	Postcode VARCHAR(7)
);

CREATE TABLE IF NOT EXISTS department (
	DeptID CHAR(4) PRIMARY KEY,
	DeptName VARCHAR(45),
	LocationID CHAR(4),
	CONSTRAINT department_fk_locationid FOREIGN KEY (LocationID) REFERENCES location(LocationID)
);

CREATE TABLE IF NOT EXISTS employee (
	EmployeeID CHAR(4) PRIMARY KEY,
	LastName CHAR(40),
	FirstName CHAR(40),
	Startdate DATE,
	Salary DECIMAL(9,2),
	DeptID CHAR(4),
	CONSTRAINT employee_fk_deptid FOREIGN KEY (DeptID) REFERENCES department(DeptID)
);

INSERT INTO location VALUES
("L101", "11", "Live Street", "Birmingham", "B04 3LB"),
("L102", "110", "Mcdonald Road", "Liverpool", "L04 3LB"),
("L103", "22", "College Garden", "London", "B04 3LB"),
("L104", "20", "RoseHill Street", "London", "N11 3XS"),
("L105", "54", "Windmill Road", "Liverpool", "L14 3LB");

INSERT INTO department VALUES
('D101', 'Department of Computing', 'L101'),
('D102', 'Department of Mathematics', 'L102'),
('D103', 'Department of Business', 'L101'),
('D104', 'Department of Marketing', 'L103'),
('D105', 'Department of Sales', 'L104'),
('D106', 'Department of Resources', 'L103');

INSERT INTO employee VALUES
('1001', 'Klopp', 'Jurgen', '2017-03-20', 39210.00, 'D103'),
('1002', 'Alicia', 'Mann', '2015-05-17', 43210.00, 'D101'),
('1003', 'Thompson', 'Jane', '2016-03-07', 33210.00, 'D103'),
('1004', 'Jones', 'John', '2016-11-09', 45710.00, 'D102'),
('1005', 'Mullins', 'Paul', '2017-03-20', 32210.00, 'D104'),
('1006', 'Frank', 'Napp', '2016-03-14', 22210.00, 'D105');