USE employee_projects_db;

-- P01: Floor-one roles: comma join (slides 7, 10 Mark 1)
SELECT ename, role
FROM employee, works_on
WHERE employee.enum = works_on.enum AND floor = 1;

-- P02: Floor-one roles: INNER JOIN ON (slides 7, 10 Mark 2)
SELECT ename, role
FROM employee
INNER JOIN works_on ON employee.enum = works_on.enum
WHERE floor = 1;

-- P03: Floor-one roles: USING (slides 7, 10 Mark 3)
SELECT ename, role
FROM employee
INNER JOIN works_on USING(enum)
WHERE floor = 1;

-- P04: Floor-one roles: JOIN ON; missing slide 7 filter restored (slides 7, 10 Mark 4)
SELECT ename, role
FROM employee
JOIN works_on ON employee.enum = works_on.enum
WHERE floor = 1;

-- P05: Floor-one roles: aliases (slides 7, 10 Mark 5)
SELECT e.ename, w.role
FROM employee e, works_on w
WHERE e.enum = w.enum AND e.floor = 1;

-- P06: Gates-led projects: comma join (slides 8, 9 Mark 1)
SELECT ename, salary
FROM employee, works_on, project
WHERE employee.enum = works_on.enum AND works_on.pnum = project.pnum AND leader = 'Gates';

-- P07: Gates-led projects: INNER JOIN ON (slide 9 Mark 2)
SELECT ename, salary
FROM employee
INNER JOIN works_on ON employee.enum = works_on.enum
INNER JOIN project ON works_on.pnum = project.pnum
WHERE leader = 'Gates';

-- P08: Gates-led projects: USING (slide 9 Mark 3)
SELECT ename, salary
FROM employee
INNER JOIN works_on USING(enum)
INNER JOIN project USING(pnum)
WHERE leader = 'Gates';

-- P09: Gates-led projects: requested alias solution (slide 9 question)
SELECT e.ename, e.salary
FROM employee e
JOIN works_on w ON e.enum = w.enum
JOIN project p ON w.pnum = p.pnum
WHERE p.leader = 'Gates';

-- P10: Consultant assignments: join retains duplicate names (slide 11)
SELECT ename
FROM employee, works_on
WHERE employee.enum = works_on.enum AND role = 'Consultant';

-- P11: Consultant employees: IN returns one row per employee (slide 11)
SELECT ename
FROM employee
WHERE enum IN (SELECT enum
FROM works_on
WHERE role = 'Consultant');

-- P12: Consultant employees: DISTINCT join comparison (supporting check for slide 11)
SELECT DISTINCT e.ename
FROM employee e
JOIN works_on w ON e.enum = w.enum
WHERE w.role = 'Consultant';

-- P13: Employees earning above the overall average (slide 12)
SELECT ename
FROM employee
WHERE salary > (SELECT AVG(salary)
FROM employee);

-- P14: Projects with fewer than two assignments: source example (slide 12)
SELECT COUNT(pnum) AS Num_Projects
FROM project
WHERE pnum IN (SELECT pnum
FROM works_on
GROUP BY pnum
HAVING COUNT(enum) < 2);

-- P15: Projects with fewer than two employees: includes zero-assignment projects
SELECT COUNT(*) AS Num_Projects
FROM (SELECT p.pnum
FROM project p
LEFT JOIN works_on w ON p.pnum = w.pnum
GROUP BY p.pnum
HAVING COUNT(w.enum) < 2) AS low_staff_projects;

-- P16: Consultant project numbers: lowest nested step (slide 22)
SELECT pnum
FROM works_on
WHERE role = 'Consultant';

-- P17: Assignments outside consultant projects: middle nested step (slide 22)
SELECT enum
FROM works_on
WHERE pnum NOT IN (SELECT pnum
FROM works_on
WHERE role = 'Consultant');

-- P18: Employees on at least one consultant-free project: source result (slide 22)
SELECT DISTINCT ename
FROM employee
WHERE enum IN (SELECT enum
FROM works_on
WHERE pnum NOT IN (SELECT pnum
FROM works_on
WHERE role = 'Consultant'));

-- P19: Employees on no consultant projects: strict reading of slide 22 question
SELECT e.ename
FROM employee e
WHERE NOT EXISTS (SELECT 1
FROM works_on assigned
JOIN works_on consultant ON assigned.pnum = consultant.pnum
WHERE assigned.enum = e.enum AND consultant.role = 'Consultant');

-- P20: Read the floor-one view (slide 23)
SELECT employee_no, name
FROM floor_1_emp ORDER BY employee_no;
