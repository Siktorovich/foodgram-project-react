import csv
import os
import psycopg2
import sys
from dotenv import load_dotenv
from psycopg2 import Error

from django.core.management.base import BaseCommand

DATA_PATH = './data/'
FILENAME = 'ingredients.csv'


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
        try:
            load_dotenv()
            conn = psycopg2.connect(
                user=os.getenv('POSTGRES_USER', 'empty'),
                password=os.getenv('POSTGRES_PASSWORD', 'empty'),
                port=os.getenv('DB_PORT', 5432),
                host=os.getenv('DB_HOST', 'empty'),
                database=os.getenv('POSTGRES_DB', 'empty')
            )
            cur = conn.cursor()
            with open(DATA_PATH + FILENAME, 'r', newline='') as f:
                reader = csv.reader(f, delimiter=',')
                try:
                    for row in reader:
                        if reader.line_num == 1:
                            continue
                        else:
                            cur.execute(
                                'INSERT INTO recipes_ingredient '
                                'VALUES (?,?)',
                                row
                            )
                            self.imported_counter += 1
                except csv.Error as err:
                    sys.exit(f'{FILENAME}, line {reader.line_num}: {err}')
                conn.commit()
                conn.close()
        except (Exception, Error) as error:

            sys.exit(f'Ошибка при создании соединения, {error}')

    def handle(self, *args, **kwargs):
        self.starting_import()
        self.import_ingredients()
        self.finalise()
