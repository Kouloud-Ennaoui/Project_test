import dataprocesser as dp
import sqlquery as sqlcmd
from config import config
import psycopg2
import re


database_name = 'Spark_test_db'


def create_database_connection():
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        # create a cursor
        cursor = conn.cursor()

        # cursor.execute('Drop Database python_db_test')
        cursor.execute('CREATE DATABASE python_test_db')
        print('done')
        conn.commit()
        cursor.close()
        return database_name

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params, database="python_test_db")
        conn.autocommit = True
        # create a cursor
        cursor = conn.cursor()

        # create tables
        for command in sqlcmd.sql_table_creation_commands:
            cursor.execute(command)
        conn.commit()
        print("Tables are created with success")

        # get the data
        df_user, df_sub = dp.user_data_parser()
        df_msg = dp.message_data_parser()

        # insert into table
        # insert into user table
        items_user = [tuple(row.values) for index, row in df_user.iterrows()]
        result = cursor.executemany(sqlcmd.sql_insert_user, items_user)
        
        # insert into subscription table
        items_subs = [tuple(row.values) for index, row in df_sub.iterrows()]
        result = cursor.executemany(sqlcmd.sql_insert_subscription, items_subs)

        # insert into message
        items_message = [tuple(row.values) for index, row in df_msg.iterrows()]
        result = cursor.executemany(sqlcmd.sql_insert_message, items_message)

        conn.commit()

        # select query
        # total_messages_per_day
        cursor.execute(sqlcmd.total_messages_per_day)
        results = cursor.fetchall()
        print("Total messages per day:", results)

        # user_did_not_receive_any_message
        cursor.execute(sqlcmd.user_did_not_receive_any_message)
        results = cursor.fetchall()
        user_list = [(item[:3], re.findall(r'@.*', item[3]), item[4:]) for item in results]
        print('Users that did not receive any message are:', user_list)

        # total_subs_today
        cursor.execute(sqlcmd.total_subs_today)
        results = cursor.fetchall()
        print('Number of active subscription today is:', results)

        # sender_without_active_sub
        cursor.execute(sqlcmd.sender_without_active_sub)
        results = cursor.fetchall()
        sender_list = [(item[:3], re.findall(r'@.*', item[3]), item[4:]) for item in results]
        print('Users sending messages without an active subscription:', sender_list)

        # average_subscription_per_year_month
        cursor.execute(sqlcmd.average_subscription_per_year_month)
        results = cursor.fetchall()
        print('The average subscription amount per year/month:', results)

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_database_connection()
    connect()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
