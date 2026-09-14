# Employee joins, subqueries, and views in MySQL

The Week 10 class exercises use two separate relational databases: employee/project assignments and employee/department locations. This project implements the examples across all 23 slides of the supplied presentation, including alternative JOIN forms, intermediate nested-query steps, and the floor-one view.

The original PowerPoint and both full setup scripts remain unchanged. The runnable setup files are byte-for-byte copies of those scripts. Query examples use the supplied schemas, with corrections and interpretation differences recorded in [source notes](docs/source-notes.md).

## Queries and complete outputs

| Database | Runnable queries | Executed results |
|---|---|---|
| Employee Projects | [20 query variants](sql/projects_queries.sql) | [Every result table](evidence/projects-results.md) |
| Employee Departments | [25 query variants](sql/departments_queries.sql) | [Every result table](evidence/departments-results.md) |
| Floor-one view | [CREATE VIEW](sql/create_floor_view.sql) | P20 in the Projects results |

Each query also has a separate CSV in `evidence/`. [Schemas and all source records](evidence/schemas-and-records.md), [constraint tests](evidence/constraint-tests.md), and the [validation record](evidence/validation.json) are included. See the [slide-by-slide coverage map](docs/coverage.md) for the location of every example. Repeated examples on slides 7 and 10 share the same runnable variants; both original slides remain in the source.

## Source tables

| Database | Table | Records | Relationship |
|---|---|---|---|
| employee_projects_db | employee | 7 | Primary key: enum |
| employee_projects_db | project | 6 | Primary key: pnum |
| employee_projects_db | works_on | 13 | Composite primary key: enum + pnum; two foreign keys |
| employee_departments_db | location | 5 | Primary key: LocationID |
| employee_departments_db | department | 6 | Primary key: DeptID; references location |
| employee_departments_db | employee | 6 | Primary key: EmployeeID; references department |

## Results worth comparing

- The first-floor employee/role query returns four assignments. The Gates-led project query returns Smith, White, and Doyle.
- The consultant JOIN returns Jones twice and Doyle once. The IN query returns Jones and Doyle once each; P12 shows the corresponding DISTINCT join.
- Cartesian pairing produces 36 employee/department combinations; the keyed inner join returns six. Right and full-join examples retain the Department of Resources with a NULL employee, returning seven rows.
- The slide 22 nested query returns Smith, White, and Doyle because each has at least one assignment on a consultant-free project. The stricter “no consultant projects at all” interpretation returns only White. Both are retained.

The results describe only the supplied teaching records. The department script defines nullable foreign keys and the projects script permits NULL salary/start date; no extra business rules are imposed.

## Run in MySQL Workbench

Use a disposable exercise server compatible with the reference scripts. The recorded run used MySQL Community Server 9.7.1, strict SQL mode, and case-insensitive table lookup. CHECK constraints require MySQL 8.0.16 or later. The department script uses double-quoted string values, so its session must not enable `ANSI_QUOTES`.

On a fresh server without these two schemas, execute in order:

1. `sql/setup_projects.sql`
2. `sql/setup_departments.sql`
3. `sql/create_floor_view.sql`
4. `sql/projects_queries.sql`
5. `sql/departments_queries.sql`

The setup scripts use IF NOT EXISTS for tables but their INSERT statements are not repeatable on populated tables. Do not rerun setup or CREATE VIEW on existing objects. Query files only retrieve data and can be rerun. No existing application database needs to be changed.

## Reproduce validation

Clone the full repository so the shared validation helpers remain available. From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_class_exercises.py --user root --ask-password
```

For a local Unix socket, add `--socket /path/to/mysql.sock`. For TCP, `--host` and `--port` are available. A first run creates the two exercise schemas from the unchanged scripts. If they already exist, the runner stops unless `--reuse` is explicitly supplied. Reuse verifies every source row, field name, type, and relationship before proceeding; it does not repeat INSERT statements or replace a view.

All 45 query outputs are independently calculated from the original INSERT values in Python and compared as multisets, preserving duplicates. The 14 constraint tests run in separate transactions and roll back. Every original row and table definition is checked again afterward. Successful validation refreshes the complete evidence files.

## Sources

- [MySQL Exercises.pptx](<sources/MySQL Exercises.pptx>)
- [EMPLOYEE_PROJECTS SCRIPT - FULL.txt](<sources/EMPLOYEE_PROJECTS SCRIPT - FULL.txt>)
- [EMPLOYEE_DEPARTMENTS SCRIPT - FULL.txt](<sources/EMPLOYEE_DEPARTMENTS SCRIPT - FULL.txt>)
- [Original join diagrams](docs/join-diagrams.md) and [slide text extraction](docs/slide-text.md)

The [Creditcard home exercises](../week-10-mysql-creditcard-aggregation/) are a separate Week 10 section. The [first thirteen Creditcard Part 2 questions](../week-09-mysql-creditcard-queries/) include the checked answer key and all its alternatives.
