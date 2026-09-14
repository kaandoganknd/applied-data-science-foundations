# Executed schemas and complete source records

## employee_projects_db.employee

```sql
CREATE TABLE `employee` (
  `enum` int NOT NULL,
  `ename` char(15) NOT NULL,
  `startdate` date DEFAULT NULL,
  `salary` decimal(7,2) DEFAULT NULL,
  `floor` tinyint DEFAULT NULL,
  PRIMARY KEY (`enum`),
  CONSTRAINT `employee_ch_salary` CHECK ((`salary` > 0)),
  CONSTRAINT `employee_ch_startdate` CHECK ((`startdate` >= _utf8mb4'2000-01-01'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

| enum | ename | startdate | salary | floor |
| --- | --- | --- | --- | --- |
| 852341 | Smith | 2019-01-12 | 15000.00 | 1 |
| 852358 | Jones | 2019-07-11 | 19000.00 | 3 |
| 852407 | Brown | 2020-03-03 | 16000.00 | 3 |
| 852455 | White | 2020-04-09 | 25100.00 | 2 |
| 852491 | Adams | 2018-07-12 | 30500.00 | 1 |
| 852514 | Doyle | 2018-11-12 | 11650.00 | 2 |
| 852530 | Evans | 2020-08-06 | 26980.00 | 4 |

## employee_projects_db.project

```sql
CREATE TABLE `project` (
  `pnum` int NOT NULL,
  `pname` char(15) NOT NULL,
  `leader` char(15) DEFAULT NULL,
  PRIMARY KEY (`pnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

| pnum | pname | leader |
| --- | --- | --- |
| 121 | IT | Gates |
| 135 | Design | Sinclair |
| 147 | Analysis | Einstein |
| 216 | Publicity | Saatchi |
| 227 | Theatre | Dench |
| 251 | Sport | Shearer |

## employee_projects_db.works_on

```sql
CREATE TABLE `works_on` (
  `enum` int NOT NULL,
  `pnum` int NOT NULL,
  `role` char(15) DEFAULT NULL,
  PRIMARY KEY (`enum`,`pnum`),
  KEY `workson_fk_pnum` (`pnum`),
  CONSTRAINT `workson_fk_enum` FOREIGN KEY (`enum`) REFERENCES `employee` (`enum`),
  CONSTRAINT `workson_fk_pnum` FOREIGN KEY (`pnum`) REFERENCES `project` (`pnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

| enum | pnum | role |
| --- | --- | --- |
| 852341 | 121 | Manager |
| 852341 | 135 | Designer |
| 852358 | 135 | Consultant |
| 852358 | 147 | Consultant |
| 852407 | 216 | Assistant |
| 852455 | 121 | Assistant |
| 852455 | 227 | Manager |
| 852491 | 135 | Designer |
| 852491 | 216 | Manager |
| 852514 | 121 | Assistant |
| 852514 | 216 | Consultant |
| 852514 | 251 | Manager |
| 852530 | 147 | Manager |

## employee_departments_db.location

```sql
CREATE TABLE `location` (
  `LocationID` char(4) NOT NULL,
  `Address1` varchar(40) DEFAULT NULL,
  `Address2` varchar(40) DEFAULT NULL,
  `City` varchar(40) DEFAULT NULL,
  `Postcode` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`LocationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

| LocationID | Address1 | Address2 | City | Postcode |
| --- | --- | --- | --- | --- |
| L101 | 11 | Live Street | Birmingham | B04 3LB |
| L102 | 110 | Mcdonald Road | Liverpool | L04 3LB |
| L103 | 22 | College Garden | London | B04 3LB |
| L104 | 20 | RoseHill Street | London | N11 3XS |
| L105 | 54 | Windmill Road | Liverpool | L14 3LB |

## employee_departments_db.department

```sql
CREATE TABLE `department` (
  `DeptID` char(4) NOT NULL,
  `DeptName` varchar(45) DEFAULT NULL,
  `LocationID` char(4) DEFAULT NULL,
  PRIMARY KEY (`DeptID`),
  KEY `department_fk_locationid` (`LocationID`),
  CONSTRAINT `department_fk_locationid` FOREIGN KEY (`LocationID`) REFERENCES `location` (`LocationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

| DeptID | DeptName | LocationID |
| --- | --- | --- |
| D101 | Department of Computing | L101 |
| D102 | Department of Mathematics | L102 |
| D103 | Department of Business | L101 |
| D104 | Department of Marketing | L103 |
| D105 | Department of Sales | L104 |
| D106 | Department of Resources | L103 |

## employee_departments_db.employee

```sql
CREATE TABLE `employee` (
  `EmployeeID` char(4) NOT NULL,
  `LastName` char(40) DEFAULT NULL,
  `FirstName` char(40) DEFAULT NULL,
  `Startdate` date DEFAULT NULL,
  `Salary` decimal(9,2) DEFAULT NULL,
  `DeptID` char(4) DEFAULT NULL,
  PRIMARY KEY (`EmployeeID`),
  KEY `employee_fk_deptid` (`DeptID`),
  CONSTRAINT `employee_fk_deptid` FOREIGN KEY (`DeptID`) REFERENCES `department` (`DeptID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

| EmployeeID | LastName | FirstName | Startdate | Salary | DeptID |
| --- | --- | --- | --- | --- | --- |
| 1001 | Klopp | Jurgen | 2017-03-20 | 39210.00 | D103 |
| 1002 | Alicia | Mann | 2015-05-17 | 43210.00 | D101 |
| 1003 | Thompson | Jane | 2016-03-07 | 33210.00 | D103 |
| 1004 | Jones | John | 2016-11-09 | 45710.00 | D102 |
| 1005 | Mullins | Paul | 2017-03-20 | 32210.00 | D104 |
| 1006 | Frank | Napp | 2016-03-14 | 22210.00 | D105 |

## floor_1_emp view

```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `floor_1_emp` (`employee_no`,`name`) AS select `employee`.`enum` AS `enum`,`employee`.`ename` AS `ename` from `employee` where (`employee`.`floor` = 1);
```
