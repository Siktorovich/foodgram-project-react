import csv
import sqlite3
import sys

from django.core.management.base import BaseCommand

DATA_PATH = '../data/'
FILENAME = 'ingredients.csv'
DATABASE_NAME = 'db.sqlite3'


class Command(BaseCommand):
    help = ('Import data from data directory ONLY in Ingredient model.'
            'Can be extend.'
            'For executing use python3 manage.py import_data')

    def starting_import(self):
        self.imported_counter = 0
        self.stdout.write(
            f'Import {FILENAME} starts\n'
        )

    def finalise(self):
        self.stdout.write(
            f'Import {FILENAME} ends\n'
            f'Instances imported: {self.imported_counter}\n'
        )

    def import_ingredients(self):
        conn = sqlite3.connect(DATABASE_NAME)
        cur = conn.cursor()
        with open(DATA_PATH + FILENAME, 'r', newline='') as f:
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
                        self.imported_counter += 1
            except csv.Error as err:
                sys.exit(f'{FILENAME}, line {reader.line_num}: {err}')
            conn.commit()
            conn.close()

    def handle(self, *args, **kwargs):
        self.starting_import()
        self.import_ingredients()
        self.finalise()
