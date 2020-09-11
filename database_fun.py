import os
import psycopg2


def create_database():
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')  # Connect the Heroku database

    cursor = conn.cursor()

            SQL_order = '''CREATE TABLE account(
                            subject, class, url, path, name, finish, solution
                    );'''
        
            cursor.execute(SQL_order)
            conn.commit()

            cursor.close()
            conn.close()