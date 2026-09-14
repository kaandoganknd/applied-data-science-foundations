# Source choices and corrections

The full setup scripts control the schema and stored values. The slide deck controls example coverage. Original sources are never edited; the following changes apply only to runnable query examples.

| Source location | Difference or issue | Treatment |
|---|---|---|
| Slides 3–6 | The slides call the employee date `sdate` and show SMALLINT project keys. The full script uses `startdate` and INT keys. | Keep the full script's names and types. Both sides of each foreign key match. |
| Slide 5 | One CREATE TABLE example has a trailing comma. The ALTER examples demonstrate alternatives to constraints already in the full script. | Execute the complete supplied setup rather than duplicate constraints. The original alternatives remain in the deck and text extraction; metadata and behaviour tests verify the resulting keys. |
| Slide 7, Mark 4 | The first-floor example omits `WHERE floor = 1`. Slide 10's repeated version includes it. | Restore the filter in P04. P01–P05 each return four assignments. |
| Slides 8–9 and 11 | Typographic quotation marks appear around SQL string values. | Use ASCII single quotes in runnable SQL. |
| Slide 11 | The JOIN lists consultant assignments, repeating Jones. The IN query lists employees once. | Keep both outputs in P10–P11. Add P12 with DISTINCT to show the equivalent employee-level join. |
| Slide 12 | The grouped WORKS_ON subquery cannot include a project with no assignments. | Keep the source query as P14. P15 uses a LEFT JOIN and counts the non-null assignment key. Both return two for this dataset, which has no unassigned projects. |
| Slide 14 | Some postal/address spellings differ from the full script, including BA04/B04, McDonald/Mcdonald, and Rose Hill/RoseHill. | Keep the script's exact values; no silent cleaning. |
| Slide 15, Mark 2 | SELECT/WHERE use `e` and `d` but FROM does not define them. | Declare both aliases in D03. |
| Slide 16, Marks 4–6 | The requested City is absent from some SELECT lists. Mark 5 uses a dash instead of equality in its join predicate. | Include City in D11–D13 and correct the predicate to `d.LocationID = l.LocationID`. |
| Slides 18–20 | Outer joins must preserve unmatched rows. | D21–D25 include the Department of Resources with a NULL employee; the original diagrams are retained. |
| Slide 20 | UNION removes duplicate projected rows. That is not general SQL bag-preserving full-outer-join behaviour. | Preserve the source UNION in D24. D25 adds UNION ALL with unmatched-right filtering. Both produce seven rows on this dataset. |
| Slide 22 | The nested query means “at least one consultant-free project”, not “no projects with consultants”. | Preserve the three nested steps as P16–P18. P19 separately implements the strict reading. Source result: Smith, White, Doyle. Strict result: White. |
| Slide 23 | The view renames the two selected columns. | Create `floor_1_emp (employee_no, name)` and retain both returned records in P20. |

Examples with no ORDER BY are compared as multisets, so duplicate rows remain meaningful without assuming a particular output order. No claim is made that alternative forms remain equivalent after arbitrary schema or data changes.

Four supporting query variants go beyond literal slide code to make the differences inspectable: P12 (DISTINCT consultant join), P15 (zero-assignment coverage), P19 (strict consultant exclusion), and D25 (bag-preserving full-join emulation). They supplement rather than replace the source examples.
