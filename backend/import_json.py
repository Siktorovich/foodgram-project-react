import csv
import sqlite3
import sys
import os


DATA_PATH = '../data/'

def import_ingredients():
        IMPORTED_COUNTER = 0
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        with open(DATA_PATH + 'ingredients.csv', 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            try:
                for i, row in enumerate(reader):
                    if reader.line_num == 1:
                        continue
                    else:
                        cur.execute(
                            f'INSERT INTO recipes_ingredient VALUES ({i},?,?)',
                            row
                        )
                        IMPORTED_COUNTER += 1
            except csv.Error as err:
                sys.exit(f'ingredients.csv, line {reader.line_num}: {err}')
        conn.commit()
        conn.close()
        print(
        f'Import ingredients.csv ends\n'
        f'Instances imported: {IMPORTED_COUNTER}\n'
        )

def starting_import():
    print('Starting import ingredients.csv')


if __name__ == '__main__':
    starting_import()
    import_ingredients()