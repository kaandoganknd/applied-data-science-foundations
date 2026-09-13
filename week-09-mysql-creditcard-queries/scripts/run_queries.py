"""Run the nine continuation queries against the unchanged Creditcard exercise table."""

import argparse
import csv
import getpass
import hashlib
import json
import re
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import pymysql
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT.parent / 'week-08-mysql-creditcard'
FIELDS = ['CreditcardNum', 'Creditcard_company', 'Creditcard_type', 'Credit_Limit',
          'Totalspent', 'City', 'CardHolder', 'Issue_Date']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plain(value):
    if isinstance(value, Decimal):
        return format(value, '.2f')
    if isinstance(value, date):
        return value.isoformat()
    return value


def table(columns, rows):
    def cell(value):
        return str(plain(value) if value is not None else 'NULL').replace('|', '\\|')
    return '\n'.join(['| ' + ' | '.join(columns) + ' |',
                      '| ' + ' | '.join(['---'] * len(columns)) + ' |'] +
                     ['| ' + ' | '.join(map(cell, row)) + ' |' for row in rows])


def load_questions():
    doc = Document(ROOT / 'sources/MySQL Activities W8-W9.docx')
    questions = []
    for paragraph in doc.paragraphs:
        text = ' '.join(paragraph.text.split())
        if not text:
            continue
        prop = paragraph._p.pPr
        numbering = prop.numPr if prop is not None else None
        if numbering is not None and int(numbering.ilvl.val) == 0:
            questions.append({'number': len(questions) + 1, 'text': text, 'subtasks': []})
        elif numbering is not None:
            questions[-1]['subtasks'].append(text)
        elif questions:
            questions[-1]['text'] += ' ' + text
    assert len(questions) == 26 and len(questions[2]['subtasks']) == 6
    assert questions[12]['text'] == 'List all credit cards that were not issued in London?'
    return questions[:13]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=3306)
    parser.add_argument('--socket')
    parser.add_argument('--user', default='root')
    parser.add_argument('--ask-password', action='store_true')
    args = parser.parse_args()
    source = SETUP / 'data/creditcard_insert.csv'
    with source.open(newline='') as stream:
        expected = list(csv.DictReader(stream))
    for row in expected:
        row['CreditcardNum'] = int(row['CreditcardNum'])
        for field in ['Credit_Limit', 'Totalspent']:
            row[field] = Decimal(row[field])
    expected.sort(key=lambda row: row['CreditcardNum'])
    assert len(expected) == 15
    sql_file = ROOT / 'sql/questions_05_to_13.sql'
    blocks = re.findall(r'-- Q(\d{2}): ([^\n]+)\n(.*?;)', sql_file.read_text(), re.S)
    assert [int(n) for n, _, _ in blocks] == list(range(5, 14))
    assert all(query.lstrip().startswith('SELECT ') for _, _, query in blocks)
    questions = load_questions()
    companies = sorted({row['Creditcard_company'] for row in expected})
    highest = max(row['Credit_Limit'] for row in expected)
    to_rows = lambda records: [tuple(plain(row[field]) for field in FIELDS) for row in records]
    expected_results = {
        5: [(len(expected),)],
        6: [(len(companies),)],
        7: [(name,) for name in companies],
        8: to_rows(sorted(expected, key=lambda row: (-row['Credit_Limit'], row['CreditcardNum']))),
        9: to_rows([row for row in expected if row['Credit_Limit'] == highest]),
        10: to_rows([row for row in expected if row['City'] == 'London']),
        11: to_rows([row for row in expected if row['City'] == 'Aberdeen' and row['Credit_Limit'] > 5000]),
        12: to_rows([row for row in expected if row['Credit_Limit'] in [1200, 3000, 4500]]),
        13: to_rows([row for row in expected if row['City'] != 'London']),
    }
    conn = pymysql.connect(host=args.host, port=args.port, unix_socket=args.socket,
                           user=args.user, database='financial_db', charset='utf8mb4',
                           password=getpass.getpass('MySQL password: ') if args.ask_password else '',
                           autocommit=True)
    results = []
    try:
        with conn.cursor() as cursor:
            cursor.execute('SET SESSION TRANSACTION READ ONLY')
            conn.begin()
            cursor.execute('SELECT VERSION(), @@lower_case_table_names, @@sql_mode')
            version, case_mode, sql_mode = cursor.fetchone()
            cursor.execute('SHOW CREATE TABLE creditcard')
            ddl_before = cursor.fetchone()[1]
            assert ddl_before + ';\n' == (SETUP / 'evidence/show-create-table.sql').read_text(), 'Schema differs from the verified setup'
            cursor.execute('DESCRIBE creditcard')
            schema_columns = [column[0] for column in cursor.description]
            schema_rows = cursor.fetchall()
            cursor.execute('SELECT * FROM creditcard ORDER BY CreditcardNum')
            before = cursor.fetchall()
            assert [column[0] for column in cursor.description] == FIELDS
            assert [tuple(map(plain, row)) for row in before] == to_rows(expected), 'Table differs from the 15 source records; no data was changed'
            for number, title, query in blocks:
                cursor.execute(query)
                columns = [column[0] for column in cursor.description]
                rows = [tuple(map(plain, row)) for row in cursor.fetchall()]
                cursor.execute('SHOW WARNINGS')
                assert not cursor.fetchall(), f'Q{number}: unexpected warning'
                assert rows == expected_results[int(number)], f'Q{number}: result mismatch'
                results.append(dict(question=int(number), title=title, sql=query,
                                    columns=columns, rows=rows, row_count=len(rows), check='PASS'))
            cursor.execute('SELECT * FROM creditcard ORDER BY CreditcardNum')
            assert cursor.fetchall() == before, 'Records changed'
            cursor.execute('SHOW CREATE TABLE creditcard')
            assert cursor.fetchone()[1] == ddl_before, 'Schema changed'
    finally:
        conn.rollback()
        conn.close()

    out = ROOT / 'evidence'
    out.mkdir(exist_ok=True)
    docs = ROOT / 'docs'
    docs.mkdir(exist_ok=True)
    question_text = ['# Source questions 1–13', '',
                     'Numbering follows the original Word list, including the six subparts of question 3. Questions 14–26 are outside this activity.', '']
    for item in questions:
        question_text += [f"## {item['number']}. {item['text']}", '']
        question_text += [f'- {part}' for part in item['subtasks']]
        if item['subtasks']:
            question_text.append('')
    (docs / 'questions.md').write_text('\n'.join(question_text).rstrip() + '\n')
    report = ['# Executed Creditcard queries', '',
              f'MySQL {version}. Read-only queries on the 15 unchanged reference records in `financial_db.creditcard`.', '',
              'Questions 1–4 use the existing setup; the structure below was read again in this run. Questions 5–13 are listed in source order with complete outputs.', '',
              '## Table structure (Q2–Q3)', '', '```sql', 'DESCRIBE creditcard;', '```', '',
              table(schema_columns, schema_rows), '']
    for result in results:
        report += [f"## Q{result['question']:02d}. {result['title']}", '',
                   '```sql', result['sql'], '```', '',
                   table(result['columns'], result['rows']), '',
                   f"Rows returned: {result['row_count']}.", '']
        if result['question'] == 8:
            report += ['Q8 is interpreted as ordering all cards by descending limit; Q9 selects only the maximum-limit card(s).', '']
        with (out / f"q{result['question']:02d}.csv").open('w', newline='') as stream:
            writer = csv.writer(stream, lineterminator='\n')
            writer.writerow(result['columns'])
            writer.writerows(result['rows'])
    (out / 'query-results.md').write_text('\n'.join(report))
    (out / 'table-structure.sql').write_text(ddl_before + ';\n')
    manifest = dict(verified_at_utc=datetime.now(timezone.utc).isoformat(),
                    mysql_version=version, lower_case_table_names=case_mode, sql_mode=sql_mode,
                    schema='financial_db', table='creditcard', reference_rows=15,
                    source_question_numbers=list(range(1, 14)), newly_executed_questions=list(range(5, 14)),
                    passed_query_checks=len(results), failed_query_checks=0,
                    comparison='Every result cell compared with independent Python calculations on the reference INSERT CSV',
                    schema_matches_reference=True, records_match_reference=True,
                    schema_and_records_unchanged=True, transaction_read_only=True,
                    input_sha256={str(path.relative_to(ROOT.parent)): digest(path) for path in [
                        ROOT / 'sources/MySQL Activities W8-W9.docx', sql_file, source,
                        SETUP / 'sql/full_solution.sql', SETUP / 'evidence/show-create-table.sql']},
                    results=results)
    (out / 'validation.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f'MySQL {version}: 9/9 query checks passed; schema and 15 source records unchanged.')
    for result in results:
        print(f"Q{result['question']:02d}: {result['row_count']} output rows")


if __name__ == '__main__':
    main()
