# Slide text extraction

Text and native table cells in source XML order. Original formatting, images, diagrams, and layout remain in the unchanged PowerPoint file.

## Slide 1

MySQL Exercises

## Slide 2

Employee Project
Create tables: Employee, Project and Works_on
Insert data into tables (you can use Employee_Projects Script.txt file)

## Slide 3

EMPLOYEE_PROJECTS
enum
pnum
role
852341
121
Manager
852341
135
Designer
852358
147
Consultant
852358
135
Consultant
852407
216
Assistant
852455
121
Assistant
852455
227
Manager
852491
135
Designer
852491
216
Manager
852514
121
Assistant
852514
216
Consultant
852514
251
Manager
852530
147
Manager
pnum
pname
leader
121
IT
Gates
135
Design
Sinclair
147
Analysis
Einstein
216
Publicity
Saatchi
227
Theatre
Dench
251
Sport
Shearer
enum
ename
sdate
salary
floor
852341
Smith
2019/01/12
15000
1
852358
Jones
2019/07/11
19000
3
852407
Brown
2020/03/03
16000
3
852455
White
2020/04/09
25100
2
852491
Adams
2018/07/12
30500
1
852514
Doyle
2018/11/12
11650
2
852530
Evans
2020/08/06
26980
4
Consider the following relational schema:     EMPLOYEE (enum , ename, sdate, salary, floor)
                                                                               PROJECT (pnum , pname, leader)
                                                                               WORKS_ON (enum* , pnum* , role)
With sample data as shown
EMPLOYEE
WORKS_ON
PROJECT
Notice the PKs and FKs, and how the tables will be linked
Can an attribute be NULL?
Decide on the Data Types
CREATE DATABASE DATABASENAME;

## Slide 4

SQL – Example Database
1. Create the EMPLOYEE Table
EMPLOYEE (enum , ename, salary, floor)
EMPLOYEE
CREATE TABLE EMPLOYEE (
enum  int  not null,
ename char (15),
sdate date,
salary decimal (7,2),
floor tinyint,
CONSTRAINT pk_emp PRIMARY KEY (enum)
);
Don’t waste storage space – choose data types that are just large enough.
In this example, pk_emp is the name given to the Primary Key Constraint
Primary Key Constraint – can be added when the table is created, or added later using an ALTER TABLE statement.
Entity Integrity - no attributes participating in the primary key of a relation can accept null values.
SQL Style Guide:
Table names and SQL Reserved words – ALL CAPS, words separated by underscore (_)
Attribute names – meaningful, all lowercase, words separated by underscore (_)
Layout – generally, one SQL clause per line
enum
ename
sdate
salary
floor
852341
Smith
2019/01/12
15000
1
852358
Jones
2019/07/11
19000
3
852407
Brown
2020/03/03
16000
3
852455
White
2020/04/09
25100
2
852491
Adams
2018/07/12
30500
1
852514
Doyle
2018/11/12
11650
2
852530
Evans
2020/08/06
26980
4

## Slide 5

SQL – Example Database
CREATE TABLE EMPLOYEE (
enum  int  not null,
ename char (15),
sdate date,
salary decimal (7,2),
floor tinyint,
CONSTRAINT pk_emp PRIMARY KEY (enum)
);
Table level constraint
CREATE TABLE EMPLOYEE (
enum  int  PRIMARY KEY,
ename char (15),
sdate date,
salary decimal (7,2),
floor tinyint,
);
column level constraint
CONSTRAINT in SQL can be
created at:
Table level
Column level
And finally use the
Alter statement
ALTER TABLE WORKS_ON
ADD CONSTRAINT fk_wo2 FOREIGN KEY (enum) REFERENCES EMPLOYEE (enum);
ALTER TABLE EMPLOYEE
ADD CONSTRAINT fk_wo1 PRIMARY KEY (enum);

## Slide 6

SQL – Example Database
3. Create the PROJECT Table
PROJECT (pnum , pname, leader)
enum
pnum
role
852341
121
Manager
852341
135
Designer
852358
147
Consultant
852358
135
Consultant
852407
216
Assistant
852455
121
Assistant
852455
227
Manager
852491
135
Designer
852491
216
Manager
852514
121
Assistant
852514
216
Consultant
852514
251
Manager
852530
147
Manager
PROJECT
CREATE TABLE PROJECT (
pnum  smallint  not null,
pname  char(15),
leader  char(15),
CONSTRAINT  pk_proj PRIMARY KEY (pnum)
);
pnum
pname
leader
121
IT
Gates
135
Design
Sinclair
147
Analysis
Einstein
216
Publicity
Saatchi
227
Theatre
Dench
251
Sport
Shearer
WORKS_ON
2. Create the WORK_ON Table
WORKS_ON (enum* , pnum* , role)
CREATE TABLE WORKS_ON (
enum  int  not null,
pnum smallint not null,
role char(15),
CONSTRAINT  pk_wo PRIMARY KEY (enum, pnum)
);
We will use an ALTER TABLE statement to make enum and pnum FKs
Data Types must be the same as PKs in corresponding tables

## Slide 7

SQL – Multiple Table Queries
Mark 2 Joins - Alternative method for SQL joins
all relations participating in the join are listed in the FROM clause
Use of INNER JOIN/ EQUI JOIN as the join operator
e.g.	Get the names of employees and the roles they have performed for employees on the 1st floor.
Mark 1
SELECT ename, role
FROM EMPLOYEE, WORKS_ON
WHERE EMPLOYEE.enum = WORKS_ON.enum
AND floor = 1;
There are a number of different JOIN operators – see later
Mark 2
SELECT ename, role
FROM EMPLOYEE INNER JOIN WORKS_ON
ON EMPLOYEE.enum = WORKS_ON.enum
WHERE floor = 1;
Mark 3
SELECT ename, role
FROM EMPLOYEE INNER JOIN WORKS_ON
USING(enum)
WHERE floor = 1;
Mark 4
SELECT ename, role
FROM EMPLOYEE JOIN WORKS_ON
ON EMPLOYEE.enum = WORKS_ON.enum
WHERE floor = 1;
Mark 5
SELECT e.ename, w.role
FROM EMPLOYEE e, WORKS_ON w
WHERE e.enum = w.enum
AND floor = 1;
	Use of aliases

## Slide 8

SQL – Multiple Table Queries
Natural Language Query:	Get the names and salaries of employees who work on projects led by ‘Gates’
SELECT ename, salary
FROM EMPLOYEE, WORKS_ON, PROJECT
WHERE EMPLOYEE.enum = WORKS_ON.enum
AND WORKS_ON.pnum = PROJECT.pnum
AND leader = ‘Gates';
Requires attributes from all three tables
enum
pnum
role
852341
121
Manager
852341
135
Designer
852358
147
Consultant
852358
135
Consultant
852407
216
Assistant
852455
121
Assistant
852455
227
Manager
852491
135
Designer
852491
216
Manager
852514
121
Assistant
852514
216
Consultant
852514
251
Manager
852530
147
Manager
pnum
pname
leader
121
IT
Gates
135
Design
Sinclair
147
Analysis
Einstein
216
Publicity
Saatchi
227
Theatre
Dench
251
Sport
Shearer
enum
ename
salary
floor
852341
Smith
15000
1
852358
Jones
19000
3
852407
Brown
16000
3
852455
White
25100
2
852491
Adams
30500
1
852514
Doyle
11650
2
852530
Evans
26980
4
EMPLOYEE
WORKS_ON
PROJECT
Mark 1 Join onPK/FK match
Result Table
ename
salary
Smith
15000
White
25100
Doyle
11650
WORKS_ON.pnum = PROJECT.pnum
Second example

## Slide 9

SQL – Multiple Table Queries
e.g.	Get the names and salaries of employees who work on projects led by ‘Gates’
Mark 1
SELECT ename, salary
FROM EMPLOYEE, WORKS_ON, PROJECT
WHERE EMPLOYEE.enum = WORKS_ON.enum
AND WORKS_ON.pnum = PROJECT.pnum
AND leader = ‘Gates’;
Mark 3
SELECT ename, salary
FROM EMPLOYEE
INNER JOIN WORKS_ON
USING(enum)
INNER JOIN PROJECT
USING(pnum)
WHERE leader = 'Gates';
Question: Use aliases to get the names and salaries of employees who work on project led by ‘Gates’.
Mark 2
SELECT ename, salary
FROM EMPLOYEE INNER JOIN WORKS_ON
ON EMPLOYEE.enum = WORKS_ON.enum
INNER JOIN PROJECT
ON WORKS_ON.pnum = PROJECT.pnum
WHERE leader = ’Gates’;

## Slide 10

SQL – Multiple Table Queries
Mark 2 Joins - Alternative method for SQL joins
all relations participating in the join are listed in the FROM clause
Use of INNER JOIN/ EQUI JOIN as the join operator
e.g.	Get the names of employees and the roles they have performed for employees on the 1st floor.
Mark 1
SELECT ename, role
FROM EMPLOYEE, WORKS_ON
WHERE EMPLOYEE.enum = WORKS_ON.enum
AND floor = 1;
There are a number of different JOIN operators – see later
Mark 2
SELECT ename, role
FROM EMPLOYEE INNER JOIN WORKS_ON
ON EMPLOYEE.enum = WORKS_ON.enum
WHERE floor = 1;
Mark 3
SELECT ename, role
FROM EMPLOYEE INNER JOIN WORKS_ON
USING(enum)
WHERE floor = 1;
Mark 4
SELECT ename, role
FROM EMPLOYEE JOIN WORKS_ON
ON EMPLOYEE.enum = WORKS_ON.enum
WHERE floor = 1;
Mark 5
SELECT e.ename, w.role
FROM EMPLOYEE e, WORKS_ON w
WHERE e.enum = w.enum
AND floor = 1;
	Use of aliases

## Slide 11

SQL – Multiple Table Queries
Nested Queries
Join queries can be formulated as a set of nested queries whenever:
the SELECT clause contains attributes from only one relation
extra information is required for comparison in the WHERE clause	e.g. an aggregate function, or a list of attributes from another table
Links between the query blocks can be achieved:
using the IN predicate if multiple values may be returned from the lower clause
using >,>=,<,<=,=,<> whenever only one value will be returned from the lower clause
e.g.  Get the names of employees who have worked in the role of 'Consultant'.
As Mark 1 Join:
SELECT ename
FROM EMPLOYEE, WORKS_ON
WHERE EMPLOYEE.enum = WORKS_ON.enum
AND role = ‘Consultant’;
As a Nested Query:
SELECT ename
FROM EMPLOYEE
WHERE enum IN
	(SELECT enum
	FROM WORKS_ON
	WHERE role = ‘Consultant’);
The nested SELECT clause returns a list of enum of staff who are consultants
So, WHERE clause is equivalent to:
WHERE enum IN (852358, 852514);
ename
Jones
Jones
Doyle
Result Table

## Slide 12

SQL – Multiple Table Queries
e.g.	Get the employee names for employees earning salaries above the average salary for all employees
SELECT ename
FROM EMPLOYEE
WHERE salary >
(SELECT AVG (salary)
FROM EMPLOYEE);
e.g.	How many projects have less than 2 people working on them?
SELECT COUNT (pnum) AS Num_Projects
FROM PROJECT
WHERE pnum IN
(SELECT pnum
FROM WORKS_ON
GROUP BY pnum
HAVING COUNT(enum) < 2);
The query is evaluated backwards as:
subquery:	get the pnums of those projects having less than 2 employeesand pass them upwards into the top query
top query:	get the number of projects (pnums) passed into the IN list
ename
White
Adams
Evans
Result Table
The nested SELECT clause returns a single value – average salary
RECALL: Aggregate functions can only appear in SELECT or HAVING clauses
Num_Projects
2
Result Table
The subclause AS <columnname>, where columnname contains NO spaces, is used to give the result table a meaningful name

## Slide 13

Employee Departments
Create tables: location, department, employee
Insert data into tables using the Employee_Departments script. txt

## Slide 14

In the examples that follow the LOCATION, DEPARTMENT, EMPLOYEE database is used -
LOCATION (LocationID , Address1, Address2, Postcode)
DEPARTMENT((DeptID, Department, LocationID*)
EMPLOYEE(EmployeeID, LastName, Firstname, Startdate, Salary, DeptID*)
EMPLOYEE_DEPARTMENTS
LocationID
Address1
Address2
City
Postcode
L101
11
Live Street
Birmingham
BA04 3LB
L102
110
McDonald Road
Liverpool
L04 3LB
L103
22
College Garden
London
BA04 3LB
L104
20
Rose Hill Street
London
N11 3XS
L105
54
Windmill Road
Liverpool
L14 3LB
LOCATION
DeptID
DeptName
Locationid
D101
Department of Computing
L101
D102
Department of Mathematics
L102
D103
Department of Business
L101
D104
Department of Marketing
L103
D105
Department of Sales
L104
D106
Department of Resources
L103
DEPARTMENT
EmployeeID
LastName
FirstName
Startdate
Salary
DeptID
1001
Klopp
Jurgen
2017/03/20
39210.00
D103
1002
Alicia
Mann
2015/05/17
43210.00
D101
1003
Thompson
Jane
2016/03/07
33210.00
D103
1004
Jones
John
2016/11/09
45710.00
D102
1005
Mullins
Paul
2017/03/20
32210.00
D104
1006
Frank
Napp
2016/03/14
22210.00
D105
EMPLOYEE

## Slide 15

SQL – Multiple Table Queries
CARTESIAN JOIN
SELECT e.lastname, d.deptname
FROM EMPLOYEE e, DEPARTMENT d
______________________________
A product of two tables
EQUIJOIN involving of two tables
Get the names of all employees and the department they work
Mark 1
SELECT employee. lastname,
department.deptName
FROM EMPLOYEE, DEPARTMENT
WHERE employee.deptID = department. deptID
Mark 3
SELECT e.lastname, d.deptName
FROM employee e JOIN department d
WHERE e.deptID = d. deptID
Mark 4
SELECT e.lastname, d.deptName
FROM employee e INNER JOIN department d
WHERE e.deptID = d. deptID
Mark 2
SELECT e. lastname, d.deptName
FROM EMPLOYEE, DEPARTMENT
WHERE e.deptID = d. deptID
Mark 5
SELECT e.lastname, d.deptName
FROM employee e INNER JOIN department d
ON e.deptID = d. deptID
Mark 6
SELECT e.lastname, d.deptName
FROM employee e INNER JOIN department d
USING (deptID)

## Slide 16

SQL – Multiple Table Queries
EQUIJOIN involving of three tables
Get the names of all employees and the department
they work as well as the City they are based.
Mark 1
SELECT employee. lastname,
department.deptName, location.city
FROM EMPLOYEE, DEPARTMENT, LOCATION
WHERE employee.deptID = department. deptID
AND location.locationid = department.locationid
Mark 3
SELECT e.lastname, d.deptName, l.city
FROM employee e JOIN department d
JOIN LOCATION l
WHERE e.deptID = d. deptID
AND l.locationid = d.locationid
Mark 4
SELECT e.lastname, d.deptName
FROM EMPLOYEE e INNER JOIN DEPARTMENT d
INNER JOIN LOCATION l
WHERE e.deptID = d. deptID
AND l.locationid = d.locationid
Mark 2
SELECT e. lastname, d.deptName, l.city
FROM EMPLOYEE e, DEPARTMENT d, LOCATION l
WHERE e.deptID = d. deptID
AND l.locationid = d.locationid
Mark 5
SELECT e.lastname, d.deptName
FROM employee e INNER JOIN department d
ON e.deptID = d. deptID
INNER JOIN LOCATION L
ON d.locationid – L.locationid
Mark 6
SELECT e.lastname, d.deptName
FROM employee e INNER JOIN department d
USING (deptID)
INNER JOIN Location L
USING(locationid)

## Slide 17

SQL – Multiple Table Queries
EQUIJOIN involving of three tables
Get the employee names, department and the city of all employees who earn more than 34000.
Mark 1
SELECT e.lastname, d.deptName, l.city
FROM employee e INNER JOIN department d
ON e.deptID = d. deptID
INNER JOIN location L
ON l.locationid = d.locationid
WHERE e.salary > 34000
Mark 6
SELECT e.lastname, d.deptName, l.city
FROM employee e INNER JOIN department d
USING (deptID)
INNER JOIN location l
USING (locationid)
WHERE e.salary > 34000
Mark 2
SELECT e. lastname, d.deptName, l.city
FROM EMPLOYEE e, DEPARTMENT d, LOCATION l
WHERE e.deptID = d. deptID
AND l.locationid = d.locationid
AND e.salary > 34000
Mark 4
SELECT e.lastname, d.deptName, l.city
FROM EMPLOYEE e INNER JOIN DEPARTMENT d
INNER JOIN LOCATION l
WHERE e.deptID = d. deptID
AND l.locationid = d.locationid
AND e.salary > 34000

## Slide 18

Further SQL – More Operators and JOIN Queries
TABLE_A
TABLE_B
TABLE_B
SELECT e.lastname, d.deptname
FROM employee e LEFT JOIN department d
ON e.deptid = d.deptid
SELECT e.lastname, d.deptname
FROM employee e LEFT OUTER JOIN department d
ON e.deptid = d.deptid
SELECT e.lastname, d.deptname
FROM employee e LEFT OUTER JOIN department d
USING (deptid)
Note: A LEFT JOIN returns all the values from the left  table,
plus, matched values from the right table  or NULL in case of no matching join predicate.

## Slide 19

Further SQL – More Operators and JOIN Queries
TABLE_A
TABLE_B
TABLE_B
SELECT e.lastname, d.deptname
FROM employee e RIGHT JOIN department d
ON e.deptid = d.deptid
SELECT e.lastname, d.deptname
FROM employee e RIGHT OUTER JOIN department d
ON e.deptid = d.deptid
SELECT e.lastname, d.deptname
FROM employee e RIGHT OUTER JOIN department d
USING (deptid)
Note: A RIGHT JOIN is similar to a LEFT JOIN, but  with the treatment of the tables reversed.
 Returns all the values from the right table, plus  matched values from the left table or NULL
 in  case of no matching join predicate.

## Slide 20

Further SQL – More Operators and JOIN Queries
TABLE_A
TABLE_B
TABLE_B
A FULL OUTER JOIN is NOT supported in MYSQL
SOLUTION: UNION(see later slides)
SELECT e.lastname, d.deptname
FROM EMPLOYEE e LEFT JOIN DEPARTMENT d
USING (deptid)
UNION
SELECT e.lastname, d.deptname
FROM EMPLOYEE e RIGHT JOIN DEPARTMENT d
USING (DEPTID)

## Slide 21

Multiple Table Quires

## Slide 22

SQL – Multiple Table Queries
Get the names of employees NOT working on projects that have a consultant on them
lowest subquery: 	Get the projects which have consultants working on them
SELECT pnum FROM WORKS_ON
WHERE role = 'Consultant'
middle subquery: 	Get the employee numbers for projects not in this list
SELECT enum
FROM  WORKS_ON
WHERE pnum NOT IN
(SELECT pnum FROM WORKS_ON
WHERE role = 'Consultant')
top query:	Get the employee names of employees from this employee list
SELECT DISTINCT ename
FROM EMPLOYEE
WHERE enum IN
(SELECT enum
FROM  WORKS_ON
WHERE pnum NOT IN
(SELECT pnum FROM WORKS_ON
WHERE role = 'Consultant')) ;
ename
Smith
White
Doyle
Result Table

## Slide 23

SQL – Multiple Table Queries
Views
A view is a virtual table defined as a subset of one or more tables and stored in the data dictionary
It is only materialized (actually created as a table) at run time from the base table(s)
Views can be manipulated mostly as though it were a base table (from user perspective)
SQL View Syntax:
CREATE VIEW viewname  (<new attribute list>)
AS SELECT <attribute list>
FROM <table list>
[ other clauses];
e.g.	CREATE VIEW FLOOR_1_EMP (employee_no, name)
	AS SELECT enum, ename
FROM EMPLOYEE
WHERE floor = 1;
Views can be used in queries,
just like any other table
enum
ename
salary
floor
852341
Smith
15000
1
852358
Jones
19000
3
852407
Brown
16000
3
852455
White
25100
2
852491
Adams
30500
1
852514
Doyle
11650
2
852530
Evans
26980
4
EMPLOYEE
FLOOR_1_EMP
employee_no
name
852341
Smith
852491
Adams
Can give the attributes new names
