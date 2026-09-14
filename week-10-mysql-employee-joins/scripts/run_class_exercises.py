"""Load the supplied exercise databases and verify all slide-query variants in MySQL."""

import argparse
import ast
import csv
import getpass
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

import pymysql

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'week-09-mysql-creditcard-queries/scripts'))
from run_queries import plain, table

DATABASES = {
    'employee_projects_db': ('projects', 'EMPLOYEE_PROJECTS SCRIPT - FULL.txt'),
    'employee_departments_db': ('departments', 'EMPLOYEE_DEPARTMENTS SCRIPT - FULL.txt'),
}
FIELDS = {
    'projects': {'employee': ['enum', 'ename', 'startdate', 'salary', 'floor'],
                 'project': ['pnum', 'pname', 'leader'], 'works_on': ['enum', 'pnum', 'role']},
    'departments': {'location': ['LocationID', 'Address1', 'Address2', 'City', 'Postcode'],
                    'department': ['DeptID', 'DeptName', 'LocationID'],
                    'employee': ['EmployeeID', 'LastName', 'FirstName', 'Startdate', 'Salary', 'DeptID']},
}
TYPES = {
    'projects': {'employee': ['int', 'char(15)', 'date', 'decimal(7,2)', 'tinyint'],
                 'project': ['int', 'char(15)', 'char(15)'], 'works_on': ['int', 'int', 'char(15)']},
    'departments': {'location': ['char(4)', 'varchar(40)', 'varchar(40)', 'varchar(40)', 'varchar(7)'],
                    'department': ['char(4)', 'varchar(45)', 'char(4)'],
                    'employee': ['char(4)', 'char(40)', 'char(40)', 'date', 'decimal(9,2)', 'char(4)']},
}


def statements(text):
    text = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('--'))
    return [part.strip() for part in text.split(';') if part.strip()]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_rows(kind, path):
    tables = {}
    for name, body in re.findall(r'INSERT INTO (\w+) VALUES\s*(.*?);', path.read_text(), re.S):
        rows = ast.literal_eval('[' + body + ']')
        tables[name] = [dict(zip(FIELDS[kind][name], row)) for row in rows]
    assert set(tables) == set(FIELDS[kind])
    for name, rows in tables.items():
        for row in rows:
            for field in FIELDS[kind][name]:
                if field.lower() == 'salary':
                    row[field] = Decimal(str(row[field]))
    return tables


def reference_results(sources):
    p = sources['projects']
    employees = {row['enum']: row for row in p['employee']}
    projects = {row['pnum']: row for row in p['project']}
    assignments = p['works_on']
    floor = [(employees[row['enum']]['ename'], row['role']) for row in assignments if employees[row['enum']]['floor'] == 1]
    gates = [(employees[row['enum']]['ename'], employees[row['enum']]['salary']) for row in assignments if projects[row['pnum']]['leader'] == 'Gates']
    consultant = [(employees[row['enum']]['ename'],) for row in assignments if row['role'] == 'Consultant']
    consultant_ids = {row['enum'] for row in assignments if row['role'] == 'Consultant'}
    unique_consultants = [(row['ename'],) for row in p['employee'] if row['enum'] in consultant_ids]
    avg = sum(row['salary'] for row in p['employee']) / len(employees)
    staffing = Counter(row['pnum'] for row in assignments)
    consultant_projects = {row['pnum'] for row in assignments if row['role'] == 'Consultant'}
    clean_assignments = [row for row in assignments if row['pnum'] not in consultant_projects]
    clean_ids = {row['enum'] for row in clean_assignments}
    exposed_ids = {row['enum'] for row in assignments if row['pnum'] in consultant_projects}
    expected = {f'P{i:02d}': floor for i in range(1, 6)}
    expected.update({f'P{i:02d}': gates for i in range(6, 10)})
    expected.update(P10=consultant, P11=unique_consultants, P12=unique_consultants,
                    P13=[(row['ename'],) for row in p['employee'] if row['salary'] > avg],
                    P14=[(sum(count < 2 for count in staffing.values()),)],
                    P15=[(sum(staffing[row['pnum']] < 2 for row in p['project']),)],
                    P16=[(row['pnum'],) for row in assignments if row['role'] == 'Consultant'],
                    P17=[(row['enum'],) for row in clean_assignments],
                    P18=[(row['ename'],) for row in p['employee'] if row['enum'] in clean_ids],
                    P19=[(row['ename'],) for row in p['employee'] if row['enum'] not in exposed_ids],
                    P20=[(row['enum'], row['ename']) for row in p['employee'] if row['floor'] == 1])
    d = sources['departments']
    departments = {row['DeptID']: row for row in d['department']}
    locations = {row['LocationID']: row for row in d['location']}
    joined = [(row['LastName'], departments[row['DeptID']]['DeptName']) for row in d['employee']]
    with_city = [(row['LastName'], departments[row['DeptID']]['DeptName'], locations[departments[row['DeptID']]['LocationID']]['City']) for row in d['employee']]
    filtered = [joined_row for row, joined_row in zip(d['employee'], with_city) if row['Salary'] > 34000]
    assigned = {row['DeptID'] for row in d['employee']}
    right = joined + [(None, row['DeptName']) for row in d['department'] if row['DeptID'] not in assigned]
    expected['D01'] = [(e['LastName'], dep['DeptName']) for e in d['employee'] for dep in d['department']]
    for ids, result in [(range(2, 8), joined), (range(8, 14), with_city), (range(14, 18), filtered),
                        (range(18, 21), joined), (range(21, 26), right)]:
        for i in ids:
            expected[f'D{i:02d}'] = result
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=3306)
    parser.add_argument('--socket')
    parser.add_argument('--user', default='root')
    parser.add_argument('--ask-password', action='store_true')
    parser.add_argument('--reuse', action='store_true', help='Validate existing exercise schemas after verifying all source rows; no inserts are repeated')
    args = parser.parse_args()
    sources = {kind: source_rows(kind, ROOT / 'sources' / filename) for kind, filename in DATABASES.values()}
    expected = reference_results(sources)
    conn = pymysql.connect(host=args.host, port=args.port, unix_socket=args.socket, user=args.user,
                           password=getpass.getpass('MySQL password: ') if args.ask_password else '',
                           charset='utf8mb4', autocommit=True)
    results, snapshots, schemas, tests, source_warnings = [], {}, {}, [], []
    try:
        with conn.cursor() as c:
            c.execute('SELECT VERSION(), @@sql_mode, @@lower_case_table_names')
            version, sql_mode, case_mode = c.fetchone()
            assert 'ANSI_QUOTES' not in sql_mode, 'The unchanged department script uses double-quoted strings; use a compatible exercise session'
            assert any(mode in sql_mode for mode in ['STRICT_TRANS_TABLES', 'STRICT_ALL_TABLES'])
            c.execute('SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME IN (%s,%s)', tuple(DATABASES))
            existing = {row[0] for row in c.fetchall()}
            if existing and not args.reuse:
                raise RuntimeError('Exercise schema already exists. Nothing changed; use --reuse only for these verified exercise databases.')
            for db, (kind, filename) in DATABASES.items():
                setup = ROOT / f'sql/setup_{kind}.sql'
                assert setup.read_bytes() == (ROOT / 'sources' / filename).read_bytes()
                if db not in existing:
                    for sql in statements(setup.read_text()):
                        c.execute(sql)
                        c.execute('SHOW WARNINGS')
                        source_warnings += [list(row) for row in c.fetchall()]
                assert not source_warnings, source_warnings
                c.execute(f'USE {db}')
                snapshots[db], schemas[db] = {}, {}
                for name, fields in FIELDS[kind].items():
                    c.execute(f'DESCRIBE {name}')
                    description = c.fetchall()
                    assert [r[0] for r in description] == fields
                    assert [r[1] for r in description] == TYPES[kind][name]
                    c.execute(f'SHOW CREATE TABLE {name}')
                    schemas[db][name] = c.fetchone()[1]
                    order = 'enum, pnum' if name == 'works_on' else fields[0]
                    c.execute(f'SELECT * FROM {name} ORDER BY {order}')
                    actual = c.fetchall()
                    wanted = [tuple(row[field] for field in fields) for row in sources[kind][name]]
                    assert Counter(tuple(map(plain, row)) for row in actual) == Counter(tuple(map(plain, row)) for row in wanted), (db, name, 'Source mismatch')
                    snapshots[db][name] = {'columns': fields, 'rows': [tuple(map(plain, row)) for row in actual]}
            c.execute("SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA IN (%s,%s) AND REFERENCED_TABLE_NAME IS NOT NULL", tuple(DATABASES))
            foreign_keys = list(c.fetchall())
            assert set(foreign_keys) == {
                ('employee_projects_db', 'works_on', 'enum', 'employee', 'enum'),
                ('employee_projects_db', 'works_on', 'pnum', 'project', 'pnum'),
                ('employee_departments_db', 'department', 'LocationID', 'location', 'LocationID'),
                ('employee_departments_db', 'employee', 'DeptID', 'department', 'DeptID')}
            c.execute('USE employee_projects_db')
            c.execute("SHOW FULL TABLES LIKE 'floor_1_emp'")
            view = c.fetchone()
            if view:
                assert view[1] == 'VIEW', 'Existing floor_1_emp is not a view'
            else:
                for sql in statements((ROOT / 'sql/create_floor_view.sql').read_text()):
                    c.execute(sql)
            c.execute('SHOW CREATE VIEW floor_1_emp')
            view_definition = c.fetchone()[1]
            c.execute('SET SESSION TRANSACTION READ ONLY')
            conn.begin()
            for db, (kind, _) in DATABASES.items():
                c.execute(f'USE {db}')
                blocks = re.findall(r'-- ([PD]\d{2}): ([^\n]+)\n(.*?;)', (ROOT / f'sql/{kind}_queries.sql').read_text(), re.S)
                assert len(blocks) == (20 if kind == 'projects' else 25)
                for query_id, title, sql in blocks:
                    assert sql.startswith('SELECT ')
                    c.execute(sql)
                    columns = [col[0] for col in c.description]
                    rows = [tuple(map(plain, row)) for row in c.fetchall()]
                    c.execute('SHOW WARNINGS')
                    assert not c.fetchall(), query_id
                    assert Counter(rows) == Counter(tuple(map(plain, row)) for row in expected[query_id]), query_id
                    results.append(dict(id=query_id, title=title, sql=sql, columns=columns, rows=rows, row_count=len(rows), check='PASS'))
            conn.rollback()
            c.execute('SET SESSION TRANSACTION READ WRITE')

            def check(name, sql, error=None):
                conn.begin()
                observed = None
                try:
                    c.execute(sql)
                except pymysql.MySQLError as exc:
                    observed = exc.args[0]
                finally:
                    conn.rollback()
                assert observed == error, (name, observed, error)
                tests.append(dict(test=name, expected_error=error, observed_error=observed, result='PASS'))

            c.execute('USE employee_projects_db')
            check('Duplicate employee primary key', "INSERT INTO employee VALUES (852341, 'Test', '2020-01-01', 100, 1)", 1062)
            check('Duplicate assignment composite key', "INSERT INTO works_on VALUES (852341,121,'Test')", 1062)
            check('Unknown assignment employee', "INSERT INTO works_on VALUES (999999,121,'Test')", 1452)
            check('Unknown assignment project', "INSERT INTO works_on VALUES (852341,999999,'Test')", 1452)
            check('NULL assignment key', "INSERT INTO works_on VALUES (NULL,121,'Test')", 1048)
            check('Salary must be positive', "INSERT INTO employee VALUES (999999,'Test','2020-01-01',0,1)", 3819)
            check('Start date lower bound', "INSERT INTO employee VALUES (999999,'Test','1999-12-31',100,1)", 3819)
            check('Required employee name', "INSERT INTO employee VALUES (999999,NULL,'2020-01-01',100,1)", 1048)
            check('Salary decimal capacity', "INSERT INTO employee VALUES (999999,'Test','2020-01-01',100000,1)", 1264)
            check('Nullable start date and salary retained', "INSERT INTO employee VALUES (999999,'Test',NULL,NULL,1)")
            c.execute('USE employee_departments_db')
            check('Department requires a valid location when present', "INSERT INTO department VALUES ('D999','Test','L999')", 1452)
            check('Employee requires a valid department when present', "INSERT INTO employee VALUES ('9999','Test','Test','2020-01-01',100,'D999')", 1452)
            check('Duplicate department employee primary key', "INSERT INTO employee VALUES ('1001','Test','Test','2020-01-01',100,'D101')", 1062)
            check('Nullable employee department retained', "INSERT INTO employee VALUES ('9999','Test','Test','2020-01-01',100,NULL)")
            for db, (kind, _) in DATABASES.items():
                c.execute(f'USE {db}')
                for name, snapshot in snapshots[db].items():
                    c.execute(f'SELECT * FROM {name}')
                    assert Counter(tuple(map(plain, row)) for row in c.fetchall()) == Counter(snapshot['rows'])
                    c.execute(f'SHOW CREATE TABLE {name}')
                    assert c.fetchone()[1] == schemas[db][name]
    finally:
        conn.close()

    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    for kind, prefix in [('projects', 'P'), ('departments', 'D')]:
        lines = [f'# {kind.title()}: complete query results', '', f'MySQL {version}. Every result row is retained. Queries without ORDER BY have no guaranteed display order.', '']
        for result in [r for r in results if r['id'].startswith(prefix)]:
            lines += [f"## {result['id']}: {result['title']}", '', '```sql', result['sql'], '```', '', table(result['columns'], result['rows']), '', f"Rows returned: {result['row_count']}.", '']
            with (evidence / f"{result['id'].lower()}.csv").open('w', newline='') as stream:
                writer = csv.writer(stream, lineterminator='\n')
                writer.writerow(result['columns'])
                writer.writerows(result['rows'])
        (evidence / f'{kind}-results.md').write_text('\n'.join(lines))
    schema_lines = ['# Executed schemas and complete source records', '']
    for db, tables in snapshots.items():
        for name, snapshot in tables.items():
            schema_lines += [f'## {db}.{name}', '', '```sql', schemas[db][name] + ';', '```', '', table(snapshot['columns'], snapshot['rows']), '']
    schema_lines += ['## floor_1_emp view', '', '```sql', view_definition + ';', '```', '']
    (evidence / 'schemas-and-records.md').write_text('\n'.join(schema_lines))
    (evidence / 'constraint-tests.md').write_text('# Constraint behaviour tests\n\nEvery test ran in a transaction and was rolled back. The original records remained unchanged.\n\n' + table(['Test', 'Expected', 'Observed', 'Result'], [(r['test'], r['expected_error'] or 'Accept', r['observed_error'] or 'Accept', r['result']) for r in tests]) + '\n')
    with ZipFile(ROOT / 'sources/MySQL Exercises.pptx') as archive:
        slide_names = sorted([n for n in archive.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml', n)], key=lambda n:int(re.search(r'slide(\d+)', n).group(1)))
        text = ['# Slide text extraction', '', 'Text and native table cells in source XML order. Original formatting, images, diagrams, and layout remain in the unchanged PowerPoint file.', '']
        for i, name in enumerate(slide_names, 1):
            text += [f'## Slide {i}', '']
            root = ET.fromstring(archive.read(name))
            for paragraph in root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}p'):
                value = ''.join(t.text or '' for t in paragraph.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t'))
                if value.strip():
                    text.append(value.rstrip())
            text.append('')
    docs = ROOT / 'docs'
    docs.mkdir(exist_ok=True)
    (docs / 'slide-text.md').write_text('\n'.join(text).rstrip() + '\n')
    manifest = dict(verified_at_utc=datetime.now(timezone.utc).isoformat(), mysql_version=version,
                    sql_mode=sql_mode, lower_case_table_names=case_mode, slide_count=len(slide_names),
                    query_variants_checked=len(results), constraint_cases_checked=len(tests),
                    all_cells_match_independent_source_calculations=True, original_records_unchanged=True,
                    source_warnings=source_warnings, table_counts={db:{name:len(value['rows']) for name,value in tables.items()} for db,tables in snapshots.items()},
                    foreign_keys=foreign_keys, results=results, constraints=tests,
                    input_sha256={str(path.relative_to(ROOT)):digest(path) for folder in ['sources','sql'] for path in sorted((ROOT/folder).iterdir()) if path.is_file()})
    (evidence / 'validation.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f'MySQL {version}: {len(results)} query variants, {len(tests)} constraint tests, six source tables and the view verified. All original rows unchanged.')


if __name__ == '__main__':
    main()
