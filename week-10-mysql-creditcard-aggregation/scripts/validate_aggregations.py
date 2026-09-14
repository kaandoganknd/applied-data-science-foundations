"""Validate Creditcard aggregation and date queries without modifying the source table."""

import argparse
import calendar
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import pymysql
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT.parent / 'week-09-mysql-creditcard-queries'
SETUP = ROOT.parent / 'week-08-mysql-creditcard'
sys.path.insert(0, str(PREVIOUS / 'scripts'))
from run_queries import FIELDS, digest, plain, table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=3306)
    parser.add_argument('--socket')
    parser.add_argument('--user', default='root')
    parser.add_argument('--ask-password', action='store_true')
    parser.add_argument('--as-of', type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    source = SETUP / 'data/creditcard_insert.csv'
    with source.open(newline='') as stream:
        records = list(csv.DictReader(stream))
    for row in records:
        row['CreditcardNum'] = int(row['CreditcardNum'])
        row['Issue_Date'] = date.fromisoformat(row['Issue_Date'])
        for field in ['Credit_Limit', 'Totalspent']:
            row[field] = Decimal(row[field])
    records.sort(key=lambda row: row['CreditcardNum'])
    assert len(records) == 15
    by_city, by_holder, by_year = defaultdict(list), defaultdict(list), defaultdict(list)
    for row in records:
        by_city[row['City']].append(row)
        by_holder[row['CardHolder']].append(row)
        by_year[row['Issue_Date'].year].append(row)
    months = Counter(row['Issue_Date'].month for row in records)
    year_months = Counter(row['Issue_Date'].strftime('%Y-%m') for row in records)
    remainder = lambda row: row['Credit_Limit'] - row['Totalspent']
    amounts = lambda rows, field: [row[field] for row in rows]
    expected = {
        '18': [(city, max(amounts(rows, 'Credit_Limit')), min(amounts(rows, 'Credit_Limit')),
                sum(amounts(rows, 'Credit_Limit'))) for city, rows in sorted(by_city.items())],
        '19': [(holder, min(amounts(rows, 'Totalspent')), max(amounts(rows, 'Totalspent')))
               for holder, rows in sorted(by_holder.items())],
        '20': [(holder, sum(amounts(rows, 'Totalspent'))) for holder, rows in sorted(by_holder.items())],
        '21': [(row['CreditcardNum'], row['CardHolder'], row['Credit_Limit'], row['Totalspent'], remainder(row)) for row in records],
        '22': [(year, len(rows)) for year, rows in sorted(by_year.items())],
        '23': [(month, calendar.month_name[month], count) for month, count in sorted(months.items())],
        '23B': sorted(year_months.items()),
        '24': [tuple(row[field] for field in FIELDS) for row in sorted(records, key=lambda row: (row['Issue_Date'], row['CreditcardNum'])) if row['Issue_Date'] > args.as_of],
        '25': [(holder, sum(map(remainder, rows))) for holder, rows in sorted(by_holder.items())],
        '26': [(year, sum(map(remainder, rows))) for year, rows in sorted(by_year.items())],
    }
    source_w6 = ROOT / 'sources/CREDITCARD SCRIPT W6 - FULL SOLUTION.txt'
    assert source_w6.read_bytes() == (SETUP / 'sql/full_solution.sql').read_bytes()
    sql_file = ROOT / 'sql/questions_18_to_26.sql'
    blocks = re.findall(r'-- Q(\d{2}[A-Z]?): ([^\n]+)\n(.*?;)', sql_file.read_text(), re.S)
    assert [n for n, _, _ in blocks] == list(expected)
    assert all(sql.startswith('SELECT ') for _, _, sql in blocks)
    import getpass
    conn = pymysql.connect(host=args.host, port=args.port, unix_socket=args.socket,
                           user=args.user, database='financial_db', charset='utf8mb4', autocommit=True,
                           password=getpass.getpass('MySQL password: ') if args.ask_password else '')
    results = []
    try:
        with conn.cursor() as cursor:
            cursor.execute('SET SESSION TRANSACTION READ ONLY')
            cursor.execute("SET SESSION lc_time_names = 'en_US'")
            cursor.execute('SET @as_of_date = %s', (args.as_of,))
            conn.begin()
            cursor.execute('SELECT VERSION(), @@sql_mode, @@lower_case_table_names')
            version, mode, case_mode = cursor.fetchone()
            cursor.execute('SHOW CREATE TABLE creditcard')
            ddl = cursor.fetchone()[1]
            assert ddl + ';\n' == (SETUP / 'evidence/show-create-table.sql').read_text()
            cursor.execute('SELECT * FROM creditcard ORDER BY CreditcardNum')
            before = cursor.fetchall()
            assert [x[0] for x in cursor.description] == FIELDS
            assert [tuple(map(plain, row)) for row in before] == [tuple(plain(row[field]) for field in FIELDS) for row in records]
            for number, title, sql in blocks:
                cursor.execute(sql)
                columns = [x[0] for x in cursor.description]
                rows = [tuple(map(plain, row)) for row in cursor.fetchall()]
                cursor.execute('SHOW WARNINGS')
                assert not cursor.fetchall(), (number, 'Unexpected warning')
                assert rows == [tuple(map(plain, row)) for row in expected[number]], (number, 'Result differs')
                results.append(dict(question=number, title=title, sql=sql, columns=columns, rows=rows, row_count=len(rows), check='PASS'))
            cursor.execute('SELECT * FROM creditcard ORDER BY CreditcardNum')
            assert cursor.fetchall() == before
            cursor.execute('SHOW CREATE TABLE creditcard')
            assert cursor.fetchone()[1] == ddl
    finally:
        conn.rollback()
        conn.close()
    total_limit = sum(row['Credit_Limit'] for row in records)
    total_spent = sum(row['Totalspent'] for row in records)
    total_remaining = total_limit - total_spent
    assert sum(row[3] for row in expected['18']) == total_limit
    assert sum(row[1] for row in expected['20']) == total_spent
    assert sum(row[4] for row in expected['21']) == total_remaining
    assert sum(row[1] for row in expected['25']) == total_remaining
    assert sum(row[1] for row in expected['26']) == total_remaining
    assert sum(row[1] for row in expected['22']) == sum(months.values()) == sum(year_months.values()) == 15

    out = ROOT / 'evidence'
    out.mkdir(exist_ok=True)
    report = ['# Executed aggregation and date queries', '',
              f'MySQL {version}; unchanged 15-record reference table. Q24 as-of date: **{args.as_of.isoformat()}**.', '',
              'Currency: GBP as stated in the exercises. Complete result tables are retained below.', '']
    for result in results:
        report += [f"## Q{result['question']}. {result['title']}", '', '```sql', result['sql'], '```', '', table(result['columns'], result['rows']), '']
        if not result['rows']:
            report += ['No matching rows.', '']
        if result['question'] == '24':
            report += ['This identifies future-dated records only. There is no issue-status field, so it cannot independently establish actual issuance. Issue_Date is NOT NULL; all supplied dates are in 2018–2020.', '']
        with (out / f"q{result['question'].lower()}.csv").open('w', newline='') as stream:
            writer = csv.writer(stream, lineterminator='\n')
            writer.writerow(result['columns'])
            writer.writerows(result['rows'])
    report += ['## Reconciliation', '', table(['Measure', 'Value'], [('Total credit limit', total_limit), ('Total spent', total_spent), ('Total remaining credit', total_remaining)]), '',
               'Per-card, per-holder, and per-year remaining-credit totals reconcile. The year, month-of-year, and year-month counts each reconcile to 15 cards.', '']
    (out / 'query-results.md').write_text('\n'.join(report))
    numbered = []
    for p in Document(PREVIOUS / 'sources/MySQL Activities W8-W9.docx').paragraphs:
        prop = p._p.pPr
        num = prop.numPr if prop is not None else None
        if num is not None and int(num.ilvl.val) == 0:
            numbered.append(' '.join(p.text.split()))
    assert len(numbered) == 26
    lines = ['# Original questions 18–26', '', 'These continue after the thirteen Part 2 questions covered in the preceding project.', '']
    for number in range(18, 27):
        lines += [f'## Original Q{number} / Part 2 Q{number - 4}', '', numbered[number - 1], '']
    (ROOT / 'questions.md').write_text('\n'.join(lines).rstrip() + '\n')
    manifest = dict(verified_at_utc=datetime.now(timezone.utc).isoformat(), mysql_version=version,
                    sql_mode=mode, lower_case_table_names=case_mode, as_of_date=args.as_of.isoformat(),
                    source_rows=15, original_questions=list(range(18, 27)),
                    main_queries_checked=9, month_grouping_alternatives_checked=1,
                    all_result_cells_match_independent_calculations=True,
                    schema_and_records_unchanged=True, transaction_read_only=True,
                    w6_reference_byte_identical_to_w7=True,
                    totals={key:plain(value) for key,value in dict(credit_limit=total_limit, spent=total_spent, remaining=total_remaining).items()},
                    input_sha256={str(p.relative_to(ROOT.parent)):digest(p) for p in [source_w6, source, sql_file,
                        PREVIOUS / 'sources/MySQL Activities W8-W9.docx', SETUP / 'sql/full_solution.sql']},
                    results=results)
    (out / 'validation.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f'MySQL {version}: 9 main queries + 1 month alternative passed; totals reconciled; source unchanged; as-of {args.as_of}.')


if __name__ == '__main__':
    main()
