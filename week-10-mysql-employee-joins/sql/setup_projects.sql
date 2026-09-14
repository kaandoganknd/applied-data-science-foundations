CREATE DATABASE IF NOT EXISTS employee_projects_db;

USE employee_projects_db;

CREATE TABLE IF NOT EXISTS employee (
	enum INT PRIMARY KEY,
	ename CHAR(15) NOT NULL,
	startdate DATE,
	salary DECIMAL(7,2),
	floor TINYINT,
	CONSTRAINT employee_ch_salary CHECK (salary > 0),
	CONSTRAINT employee_ch_startdate CHECK (startdate >= '2000-01-01')
);

CREATE TABLE IF NOT EXISTS project (
	pnum INT PRIMARY KEY,
	pname CHAR(15) NOT NULL,
	leader CHAR(15)
);

CREATE TABLE IF NOT EXISTS works_on (
	enum INT NOT NULL,
	pnum INT NOT NULL,
	role CHAR(15),
	CONSTRAINT workson_pk PRIMARY KEY (enum, pnum),
	CONSTRAINT workson_fk_enum FOREIGN KEY (enum) REFERENCES employee(enum),
	CONSTRAINT workson_fk_pnum FOREIGN KEY (pnum) REFERENCES project(pnum)
);

INSERT INTO employee VALUES
(852341, 'Smith', '2019-01-12', 15000, 1),
(852358, 'Jones', '2019-07-11', 19000, 3),
(852407, 'Brown', '2020-03-03', 16000, 3),
(852455, 'White', '2020-04-09', 25100, 2),
(852491, 'Adams', '2018-07-12', 30500, 1),
(852514, 'Doyle', '2018-11-12', 11650, 2),
(852530, 'Evans', '2020-08-06', 26980, 4);

INSERT INTO project VALUES
(121, 'IT', 'Gates'),
(135, 'Design', 'Sinclair'),
(147, 'Analysis', 'Einstein'),
(216, 'Publicity', 'Saatchi'),
(227, 'Theatre', 'Dench'),
(251, 'Sport', 'Shearer');

INSERT INTO works_on VALUES
(852341, 121, 'Manager'),
(852341, 135, 'Designer'),
(852358, 147, 'Consultant'),
(852358, 135, 'Consultant'),
(852407, 216, 'Assistant'),
(852455, 121, 'Assistant'),
(852455, 227, 'Manager'),
(852491, 135, 'Designer'),
(852491, 216, 'Manager'),
(852514, 121, 'Assistant'),
(852514, 216, 'Consultant'),
(852514, 251, 'Manager'),
(852530, 147, 'Manager');