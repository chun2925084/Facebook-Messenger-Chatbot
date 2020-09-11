import os
import psycopg2


def create_database():
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')  # Connect the Heroku database

    cursor = conn.cursor()

    # SQL_order = '''CREATE TABLE account(
    #             subject, class, url, path, name, finish, solution
    #             );'''

    create_table_query = '''CREATE TABLE alpaca_training(
        record_no serial PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        training VARCHAR (50) NOT NULL,
        duration INTERVAL NOT NULL,
        date DATE NOT NULL
    );'''

    cursor.execute(create_table_query)
    conn.commit()

    cursor.close()
    conn.close()

def check_database():

    DATABASE_URL = os.environ['DATABASE_URL']

    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a chatbot-dev-dev-usovp1wjj977n9').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'alpaca_training'")
