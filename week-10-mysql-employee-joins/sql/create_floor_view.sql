USE employee_projects_db;

-- Slide 23: create once on the exercise schema.
CREATE VIEW floor_1_emp (employee_no, name)
AS SELECT enum, ename
FROM employee
WHERE floor = 1;
