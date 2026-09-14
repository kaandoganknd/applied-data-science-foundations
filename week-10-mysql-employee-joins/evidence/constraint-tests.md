# Constraint behaviour tests

Every test ran in a transaction and was rolled back. The original records remained unchanged.

| Test | Expected | Observed | Result |
| --- | --- | --- | --- |
| Duplicate employee primary key | 1062 | 1062 | PASS |
| Duplicate assignment composite key | 1062 | 1062 | PASS |
| Unknown assignment employee | 1452 | 1452 | PASS |
| Unknown assignment project | 1452 | 1452 | PASS |
| NULL assignment key | 1048 | 1048 | PASS |
| Salary must be positive | 3819 | 3819 | PASS |
| Start date lower bound | 3819 | 3819 | PASS |
| Required employee name | 1048 | 1048 | PASS |
| Salary decimal capacity | 1264 | 1264 | PASS |
| Nullable start date and salary retained | Accept | Accept | PASS |
| Department requires a valid location when present | 1452 | 1452 | PASS |
| Employee requires a valid department when present | 1452 | 1452 | PASS |
| Duplicate department employee primary key | 1062 | 1062 | PASS |
| Nullable employee department retained | Accept | Accept | PASS |
