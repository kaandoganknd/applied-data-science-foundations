# Departments: complete query results

MySQL 9.7.1. Every result row is retained. Queries without ORDER BY have no guaranteed display order.

## D01: Cartesian product: all employee-department pairs (slide 15)

```sql
SELECT e.LastName, d.DeptName
FROM employee e, department d;
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Resources |
| Klopp | Department of Sales |
| Klopp | Department of Marketing |
| Klopp | Department of Business |
| Klopp | Department of Mathematics |
| Klopp | Department of Computing |
| Alicia | Department of Resources |
| Alicia | Department of Sales |
| Alicia | Department of Marketing |
| Alicia | Department of Business |
| Alicia | Department of Mathematics |
| Alicia | Department of Computing |
| Thompson | Department of Resources |
| Thompson | Department of Sales |
| Thompson | Department of Marketing |
| Thompson | Department of Business |
| Thompson | Department of Mathematics |
| Thompson | Department of Computing |
| Jones | Department of Resources |
| Jones | Department of Sales |
| Jones | Department of Marketing |
| Jones | Department of Business |
| Jones | Department of Mathematics |
| Jones | Department of Computing |
| Mullins | Department of Resources |
| Mullins | Department of Sales |
| Mullins | Department of Marketing |
| Mullins | Department of Business |
| Mullins | Department of Mathematics |
| Mullins | Department of Computing |
| Frank | Department of Resources |
| Frank | Department of Sales |
| Frank | Department of Marketing |
| Frank | Department of Business |
| Frank | Department of Mathematics |
| Frank | Department of Computing |

Rows returned: 36.

## D02: Employee departments: table-qualified comma join (slide 15 Mark 1)

```sql
SELECT employee.LastName, department.DeptName
FROM employee, department
WHERE employee.DeptID = department.DeptID;
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |

Rows returned: 6.

## D03: Employee departments: defined aliases (slide 15 Mark 2 corrected)

```sql
SELECT e.LastName, d.DeptName
FROM employee e, department d
WHERE e.DeptID = d.DeptID;
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |

Rows returned: 6.

## D04: Employee departments: JOIN with WHERE (slide 15 Mark 3)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
JOIN department d
WHERE e.DeptID = d.DeptID;
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |

Rows returned: 6.

## D05: Employee departments: INNER JOIN with WHERE (slide 15 Mark 4)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
INNER JOIN department d
WHERE e.DeptID = d.DeptID;
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |

Rows returned: 6.

## D06: Employee departments: INNER JOIN ON (slide 15 Mark 5)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
INNER JOIN department d ON e.DeptID = d.DeptID;
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |

Rows returned: 6.

## D07: Employee departments: USING (slide 15 Mark 6)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
INNER JOIN department d USING(DeptID);
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |

Rows returned: 6.

## D08: Employee departments and city: comma join (slide 16 Mark 1)

```sql
SELECT employee.LastName, department.DeptName, location.City
FROM employee, department, location
WHERE employee.DeptID = department.DeptID AND location.LocationID = department.LocationID;
```

| LastName | DeptName | City |
| --- | --- | --- |
| Klopp | Department of Business | Birmingham |
| Alicia | Department of Computing | Birmingham |
| Thompson | Department of Business | Birmingham |
| Jones | Department of Mathematics | Liverpool |
| Mullins | Department of Marketing | London |
| Frank | Department of Sales | London |

Rows returned: 6.

## D09: Employee departments and city: aliases (slide 16 Mark 2)

```sql
SELECT e.LastName, d.DeptName, l.City
FROM employee e, department d, location l
WHERE e.DeptID = d.DeptID AND l.LocationID = d.LocationID;
```

| LastName | DeptName | City |
| --- | --- | --- |
| Klopp | Department of Business | Birmingham |
| Alicia | Department of Computing | Birmingham |
| Thompson | Department of Business | Birmingham |
| Jones | Department of Mathematics | Liverpool |
| Mullins | Department of Marketing | London |
| Frank | Department of Sales | London |

Rows returned: 6.

## D10: Employee departments and city: JOIN with WHERE (slide 16 Mark 3)

```sql
SELECT e.LastName, d.DeptName, l.City
FROM employee e
JOIN department d
JOIN location l
WHERE e.DeptID = d.DeptID AND l.LocationID = d.LocationID;
```

| LastName | DeptName | City |
| --- | --- | --- |
| Klopp | Department of Business | Birmingham |
| Alicia | Department of Computing | Birmingham |
| Thompson | Department of Business | Birmingham |
| Jones | Department of Mathematics | Liverpool |
| Mullins | Department of Marketing | London |
| Frank | Department of Sales | London |

Rows returned: 6.

## D11: Employee departments and city: missing City restored (slide 16 Mark 4)

```sql
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d
INNER JOIN location l
WHERE e.DeptID = d.DeptID AND l.LocationID = d.LocationID;
```

| LastName | DeptName | City |
| --- | --- | --- |
| Klopp | Department of Business | Birmingham |
| Alicia | Department of Computing | Birmingham |
| Thompson | Department of Business | Birmingham |
| Jones | Department of Mathematics | Liverpool |
| Mullins | Department of Marketing | London |
| Frank | Department of Sales | London |

Rows returned: 6.

## D12: Employee departments and city: corrected ON equality and City (slide 16 Mark 5)

```sql
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d ON e.DeptID = d.DeptID
INNER JOIN location l ON d.LocationID = l.LocationID;
```

| LastName | DeptName | City |
| --- | --- | --- |
| Klopp | Department of Business | Birmingham |
| Alicia | Department of Computing | Birmingham |
| Thompson | Department of Business | Birmingham |
| Jones | Department of Mathematics | Liverpool |
| Mullins | Department of Marketing | London |
| Frank | Department of Sales | London |

Rows returned: 6.

## D13: Employee departments and city: USING with City restored (slide 16 Mark 6)

```sql
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d USING(DeptID)
INNER JOIN location l USING(LocationID);
```

| LastName | DeptName | City |
| --- | --- | --- |
| Klopp | Department of Business | Birmingham |
| Alicia | Department of Computing | Birmingham |
| Thompson | Department of Business | Birmingham |
| Jones | Department of Mathematics | Liverpool |
| Mullins | Department of Marketing | London |
| Frank | Department of Sales | London |

Rows returned: 6.

## D14: Salary above 34000: ON joins (slide 17 Mark 1)

```sql
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d ON e.DeptID = d.DeptID
INNER JOIN location l ON l.LocationID = d.LocationID
WHERE e.Salary > 34000;
```

| LastName | DeptName | City |
| --- | --- | --- |
| Klopp | Department of Business | Birmingham |
| Alicia | Department of Computing | Birmingham |
| Jones | Department of Mathematics | Liverpool |

Rows returned: 3.

## D15: Salary above 34000: USING joins (slide 17 Mark 6)

```sql
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d USING(DeptID)
INNER JOIN location l USING(LocationID)
WHERE e.Salary > 34000;
```

| LastName | DeptName | City |
| --- | --- | --- |
| Klopp | Department of Business | Birmingham |
| Alicia | Department of Computing | Birmingham |
| Jones | Department of Mathematics | Liverpool |

Rows returned: 3.

## D16: Salary above 34000: comma joins (slide 17 Mark 2)

```sql
SELECT e.LastName, d.DeptName, l.City
FROM employee e, department d, location l
WHERE e.DeptID = d.DeptID AND l.LocationID = d.LocationID AND e.Salary > 34000;
```

| LastName | DeptName | City |
| --- | --- | --- |
| Klopp | Department of Business | Birmingham |
| Alicia | Department of Computing | Birmingham |
| Jones | Department of Mathematics | Liverpool |

Rows returned: 3.

## D17: Salary above 34000: INNER JOIN with WHERE (slide 17 Mark 4)

```sql
SELECT e.LastName, d.DeptName, l.City
FROM employee e
INNER JOIN department d
INNER JOIN location l
WHERE e.DeptID = d.DeptID AND l.LocationID = d.LocationID AND e.Salary > 34000;
```

| LastName | DeptName | City |
| --- | --- | --- |
| Klopp | Department of Business | Birmingham |
| Alicia | Department of Computing | Birmingham |
| Jones | Department of Mathematics | Liverpool |

Rows returned: 3.

## D18: Left join: ON (slide 18)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
LEFT JOIN department d ON e.DeptID = d.DeptID;
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |

Rows returned: 6.

## D19: Left outer join: ON (slide 18)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
LEFT OUTER JOIN department d ON e.DeptID = d.DeptID;
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |

Rows returned: 6.

## D20: Left outer join: USING (slide 18)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
LEFT OUTER JOIN department d USING(DeptID);
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |

Rows returned: 6.

## D21: Right join: ON (slide 19)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
RIGHT JOIN department d ON e.DeptID = d.DeptID;
```

| LastName | DeptName |
| --- | --- |
| Alicia | Department of Computing |
| Jones | Department of Mathematics |
| Klopp | Department of Business |
| Thompson | Department of Business |
| Mullins | Department of Marketing |
| Frank | Department of Sales |
| NULL | Department of Resources |

Rows returned: 7.

## D22: Right outer join: ON (slide 19)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
RIGHT OUTER JOIN department d ON e.DeptID = d.DeptID;
```

| LastName | DeptName |
| --- | --- |
| Alicia | Department of Computing |
| Jones | Department of Mathematics |
| Klopp | Department of Business |
| Thompson | Department of Business |
| Mullins | Department of Marketing |
| Frank | Department of Sales |
| NULL | Department of Resources |

Rows returned: 7.

## D23: Right outer join: USING (slide 19)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
RIGHT OUTER JOIN department d USING(DeptID);
```

| LastName | DeptName |
| --- | --- |
| Alicia | Department of Computing |
| Jones | Department of Mathematics |
| Klopp | Department of Business |
| Thompson | Department of Business |
| Mullins | Department of Marketing |
| Frank | Department of Sales |
| NULL | Department of Resources |

Rows returned: 7.

## D24: Full outer join emulation: UNION source example (slide 20)

```sql
SELECT e.LastName, d.DeptName
FROM employee e
LEFT JOIN department d USING(DeptID)
UNION
SELECT e.LastName, d.DeptName
FROM employee e
RIGHT JOIN department d USING(DeptID);
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |
| NULL | Department of Resources |

Rows returned: 7.

## D25: Full outer join emulation: UNION ALL plus unmatched right rows

```sql
SELECT e.LastName, d.DeptName
FROM employee e
LEFT JOIN department d ON e.DeptID = d.DeptID
UNION ALL
SELECT e.LastName, d.DeptName
FROM employee e
RIGHT JOIN department d ON e.DeptID = d.DeptID
WHERE e.EmployeeID IS NULL;
```

| LastName | DeptName |
| --- | --- |
| Klopp | Department of Business |
| Alicia | Department of Computing |
| Thompson | Department of Business |
| Jones | Department of Mathematics |
| Mullins | Department of Marketing |
| Frank | Department of Sales |
| NULL | Department of Resources |

Rows returned: 7.
