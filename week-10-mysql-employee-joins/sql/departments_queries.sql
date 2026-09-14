USE employee_departments_db;

-- D01: Cartesian product: all employee-department pairs (slide 15)
SELECT e.LastName, d.DeptName
FROM employee e, department d;

-- D02: Employee departments: table-qualified comma join (slide 15 Mark 1)
SELECT employee.LastName, department.DeptName
FROM employee, department
WHERE employee.DeptID = department.DeptID;

-- D03: Employee departments: defined aliases (slide 15 Mark 2 corrected)
SELECT e.LastName, d.DeptName
FROM employee e, department d
WHERE e.DeptID = d.DeptID;

-- D04: Employee departments: JOIN with WHERE (slide 15 Mark 3)
SELECT e.LastName, d.DeptName
FROM employee e
JOIN department d
WHERE e.DeptID = d.DeptID;

-- D05: Employee departments: INNER JOIN with WHERE (slide 15 Mark 4)
SELECT e.LastName, d.DeptName
FROM employee e
INNER JOIN department d
WHERE e.DeptID = d.DeptID;

-- D06: Employee departments: INNER JOIN ON (slide 15 Mark 5)
SELECT e.LastName, d.DeptName
FROM employee e
INNER JOIN department d ON e.DeptID = d.DeptID;

-- D07: Employee departments: USING (slide 15 Mark 6)
SELECT e.LastName, d.DeptName
FROM employee e
INNER JOIN department d USING(DeptID);

-- D08: Employee departments and city: comma join (slide 16 Mark 1)
SELECT employee.LastName, department.DeptName, location.City
FROM employee, department, location
WHERE employee.DeptID = department.DeptID AND location.LocationID = department.LocationID;

-- D09: Employee departments and city: aliases (slide 16 Mark 2)
SELECT e.LastName, d.DeptName, l.City
FROM employee e, department d, location l
WHERE e.DeptID = d.DeptID AND l.LocationID = d.LocationID;

-- D10: Employee departments and city: JOIN with WHERE (slide 16 Mark 3)
SELECT e.LastName, d.DeptName, l.City
FROM employee e
JOIN department d
JOIN location l
WHERE e.DeptID = d.DeptID AND l.LocationID = d.LocationID;

-- D11: Employee departments and city: missing City restored (slide 16 Mark 4)
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d
INNER JOIN location l
WHERE e.DeptID = d.DeptID AND l.LocationID = d.LocationID;

-- D12: Employee departments and city: corrected ON equality and City (slide 16 Mark 5)
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d ON e.DeptID = d.DeptID
INNER JOIN location l ON d.LocationID = l.LocationID;

-- D13: Employee departments and city: USING with City restored (slide 16 Mark 6)
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d USING(DeptID)
INNER JOIN location l USING(LocationID);

-- D14: Salary above 34000: ON joins (slide 17 Mark 1)
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d ON e.DeptID = d.DeptID
INNER JOIN location l ON l.LocationID = d.LocationID
WHERE e.Salary > 34000;

-- D15: Salary above 34000: USING joins (slide 17 Mark 6)
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d USING(DeptID)
INNER JOIN location l USING(LocationID)
WHERE e.Salary > 34000;

-- D16: Salary above 34000: comma joins (slide 17 Mark 2)
SELECT e.LastName, d.DeptName, l.City
FROM employee e, department d, location l
WHERE e.DeptID = d.DeptID AND l.LocationID = d.LocationID AND e.Salary > 34000;

-- D17: Salary above 34000: INNER JOIN with WHERE (slide 17 Mark 4)
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d
INNER JOIN location l
WHERE e.DeptID = d.DeptID AND l.LocationID = d.LocationID AND e.Salary > 34000;

-- D18: Left join: ON (slide 18)
SELECT e.LastName, d.DeptName
FROM employee e
LEFT JOIN department d ON e.DeptID = d.DeptID;

-- D19: Left outer join: ON (slide 18)
SELECT e.LastName, d.DeptName
FROM employee e
LEFT OUTER JOIN department d ON e.DeptID = d.DeptID;

-- D20: Left outer join: USING (slide 18)
SELECT e.LastName, d.DeptName
FROM employee e
LEFT OUTER JOIN department d USING(DeptID);

-- D21: Right join: ON (slide 19)
SELECT e.LastName, d.DeptName
FROM employee e
RIGHT JOIN department d ON e.DeptID = d.DeptID;

-- D22: Right outer join: ON (slide 19)
SELECT e.LastName, d.DeptName
FROM employee e
RIGHT OUTER JOIN department d ON e.DeptID = d.DeptID;

-- D23: Right outer join: USING (slide 19)
SELECT e.LastName, d.DeptName
FROM employee e
RIGHT OUTER JOIN department d USING(DeptID);

-- D24: Full outer join emulation: UNION source example (slide 20)
SELECT e.LastName, d.DeptName
FROM employee e
LEFT JOIN department d USING(DeptID)
UNION
SELECT e.LastName, d.DeptName
FROM employee e
RIGHT JOIN department d USING(DeptID);

-- D25: Full outer join emulation: UNION ALL plus unmatched right rows
SELECT e.LastName, d.DeptName
FROM employee e
LEFT JOIN department d ON e.DeptID = d.DeptID
UNION ALL
SELECT e.LastName, d.DeptName
FROM employee e
RIGHT JOIN department d ON e.DeptID = d.DeptID
WHERE e.EmployeeID IS NULL;
