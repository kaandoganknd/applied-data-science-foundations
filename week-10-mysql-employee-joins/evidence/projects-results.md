# Projects: complete query results

MySQL 9.7.1. Every result row is retained. Queries without ORDER BY have no guaranteed display order.

## P01: Floor-one roles: comma join (slides 7, 10 Mark 1)

```sql
SELECT ename, role
FROM employee, works_on
WHERE employee.enum = works_on.enum AND floor = 1;
```

| ename | role |
| --- | --- |
| Smith | Manager |
| Smith | Designer |
| Adams | Designer |
| Adams | Manager |

Rows returned: 4.

## P02: Floor-one roles: INNER JOIN ON (slides 7, 10 Mark 2)

```sql
SELECT ename, role
FROM employee
INNER JOIN works_on ON employee.enum = works_on.enum
WHERE floor = 1;
```

| ename | role |
| --- | --- |
| Smith | Manager |
| Smith | Designer |
| Adams | Designer |
| Adams | Manager |

Rows returned: 4.

## P03: Floor-one roles: USING (slides 7, 10 Mark 3)

```sql
SELECT ename, role
FROM employee
INNER JOIN works_on USING(enum)
WHERE floor = 1;
```

| ename | role |
| --- | --- |
| Smith | Manager |
| Smith | Designer |
| Adams | Designer |
| Adams | Manager |

Rows returned: 4.

## P04: Floor-one roles: JOIN ON; missing slide 7 filter restored (slides 7, 10 Mark 4)

```sql
SELECT ename, role
FROM employee
JOIN works_on ON employee.enum = works_on.enum
WHERE floor = 1;
```

| ename | role |
| --- | --- |
| Smith | Manager |
| Smith | Designer |
| Adams | Designer |
| Adams | Manager |

Rows returned: 4.

## P05: Floor-one roles: aliases (slides 7, 10 Mark 5)

```sql
SELECT e.ename, w.role
FROM employee e, works_on w
WHERE e.enum = w.enum AND e.floor = 1;
```

| ename | role |
| --- | --- |
| Smith | Manager |
| Smith | Designer |
| Adams | Designer |
| Adams | Manager |

Rows returned: 4.

## P06: Gates-led projects: comma join (slides 8, 9 Mark 1)

```sql
SELECT ename, salary
FROM employee, works_on, project
WHERE employee.enum = works_on.enum AND works_on.pnum = project.pnum AND leader = 'Gates';
```

| ename | salary |
| --- | --- |
| Smith | 15000.00 |
| White | 25100.00 |
| Doyle | 11650.00 |

Rows returned: 3.

## P07: Gates-led projects: INNER JOIN ON (slide 9 Mark 2)

```sql
SELECT ename, salary
FROM employee
INNER JOIN works_on ON employee.enum = works_on.enum
INNER JOIN project ON works_on.pnum = project.pnum
WHERE leader = 'Gates';
```

| ename | salary |
| --- | --- |
| Smith | 15000.00 |
| White | 25100.00 |
| Doyle | 11650.00 |

Rows returned: 3.

## P08: Gates-led projects: USING (slide 9 Mark 3)

```sql
SELECT ename, salary
FROM employee
INNER JOIN works_on USING(enum)
INNER JOIN project USING(pnum)
WHERE leader = 'Gates';
```

| ename | salary |
| --- | --- |
| Smith | 15000.00 |
| White | 25100.00 |
| Doyle | 11650.00 |

Rows returned: 3.

## P09: Gates-led projects: requested alias solution (slide 9 question)

```sql
SELECT e.ename, e.salary
FROM employee e
JOIN works_on w ON e.enum = w.enum
JOIN project p ON w.pnum = p.pnum
WHERE p.leader = 'Gates';
```

| ename | salary |
| --- | --- |
| Smith | 15000.00 |
| White | 25100.00 |
| Doyle | 11650.00 |

Rows returned: 3.

## P10: Consultant assignments: join retains duplicate names (slide 11)

```sql
SELECT ename
FROM employee, works_on
WHERE employee.enum = works_on.enum AND role = 'Consultant';
```

| ename |
| --- |
| Jones |
| Jones |
| Doyle |

Rows returned: 3.

## P11: Consultant employees: IN returns one row per employee (slide 11)

```sql
SELECT ename
FROM employee
WHERE enum IN (SELECT enum
FROM works_on
WHERE role = 'Consultant');
```

| ename |
| --- |
| Jones |
| Doyle |

Rows returned: 2.

## P12: Consultant employees: DISTINCT join comparison (supporting check for slide 11)

```sql
SELECT DISTINCT e.ename
FROM employee e
JOIN works_on w ON e.enum = w.enum
WHERE w.role = 'Consultant';
```

| ename |
| --- |
| Jones |
| Doyle |

Rows returned: 2.

## P13: Employees earning above the overall average (slide 12)

```sql
SELECT ename
FROM employee
WHERE salary > (SELECT AVG(salary)
FROM employee);
```

| ename |
| --- |
| White |
| Adams |
| Evans |

Rows returned: 3.

## P14: Projects with fewer than two assignments: source example (slide 12)

```sql
SELECT COUNT(pnum) AS Num_Projects
FROM project
WHERE pnum IN (SELECT pnum
FROM works_on
GROUP BY pnum
HAVING COUNT(enum) < 2);
```

| Num_Projects |
| --- |
| 2 |

Rows returned: 1.

## P15: Projects with fewer than two employees: includes zero-assignment projects

```sql
SELECT COUNT(*) AS Num_Projects
FROM (SELECT p.pnum
FROM project p
LEFT JOIN works_on w ON p.pnum = w.pnum
GROUP BY p.pnum
HAVING COUNT(w.enum) < 2) AS low_staff_projects;
```

| Num_Projects |
| --- |
| 2 |

Rows returned: 1.

## P16: Consultant project numbers: lowest nested step (slide 22)

```sql
SELECT pnum
FROM works_on
WHERE role = 'Consultant';
```

| pnum |
| --- |
| 135 |
| 147 |
| 216 |

Rows returned: 3.

## P17: Assignments outside consultant projects: middle nested step (slide 22)

```sql
SELECT enum
FROM works_on
WHERE pnum NOT IN (SELECT pnum
FROM works_on
WHERE role = 'Consultant');
```

| enum |
| --- |
| 852341 |
| 852455 |
| 852514 |
| 852455 |
| 852514 |

Rows returned: 5.

## P18: Employees on at least one consultant-free project: source result (slide 22)

```sql
SELECT DISTINCT ename
FROM employee
WHERE enum IN (SELECT enum
FROM works_on
WHERE pnum NOT IN (SELECT pnum
FROM works_on
WHERE role = 'Consultant'));
```

| ename |
| --- |
| Smith |
| White |
| Doyle |

Rows returned: 3.

## P19: Employees on no consultant projects: strict reading of slide 22 question

```sql
SELECT e.ename
FROM employee e
WHERE NOT EXISTS (SELECT 1
FROM works_on assigned
JOIN works_on consultant ON assigned.pnum = consultant.pnum
WHERE assigned.enum = e.enum AND consultant.role = 'Consultant');
```

| ename |
| --- |
| White |

Rows returned: 1.

## P20: Read the floor-one view (slide 23)

```sql
SELECT employee_no, name
FROM floor_1_emp ORDER BY employee_no;
```

| employee_no | name |
| --- | --- |
| 852341 | Smith |
| 852491 | Adams |

Rows returned: 2.
