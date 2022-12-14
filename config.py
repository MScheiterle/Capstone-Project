import datetime
import os
import pathlib
import platform
import secrets
# Dev imports
from flask_bcrypt import Bcrypt
import requests
import sqlite3
from sqlite3 import Error

import sshtunnel


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_sql(conn, sql, *params):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql, params)
    except Error as e:
        print(e)


def populate_db(conn):
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    WORDS = [x.decode('utf-8') for x in response.content.splitlines()]
    options = ["Walk Dog", "Do 100 Pushups", "Commit Code"]
    
    now = datetime.datetime.now()
    one_day = datetime.timedelta(days=1)
    two_days = datetime.timedelta(days=2)

    in_progress_dates = [now-one_day, now+one_day]
    yet_to_start_dates = [now+one_day, now+two_days]
    past_due_dates = [now-two_days, now-one_day]

    dates = [in_progress_dates, yet_to_start_dates, past_due_dates]

    bcrypt = Bcrypt()

    execute_sql(
        conn, "INSERT INTO user(username, email, password) VALUES(?, ?, ?)", "test", "test@test.com", bcrypt.generate_password_hash("test").decode(
            "utf-8"
        ))

    for x in range(99):
        random_username = ''.join(secrets.choice(WORDS) for i in range(3))
        random_email = f'{random_username}@{random_username}.com'
        random_password = bcrypt.generate_password_hash(random_username).decode(
            "utf-8"
        )
        execute_sql(
            conn, "INSERT INTO user(username, email, password) VALUES(?, ?, ?)", random_username, random_email, random_password)
        for y in range(3):
            execute_sql(
                conn, "INSERT INTO tasks(name, min_value, max_value, value, repeat, start_date, end_date, public, status, user_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", options[y], 0, 100, 50, 'false', dates[y][0], dates[y][1], 'true', 'in_progress', x)

    conn.commit()


def create_dev_tables():
    database = str(pathlib.Path(
        __file__).parent.resolve()) + f"\\dev.db"
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL UNIQUE,
                                        image_file text NOT NULL DEFAULT 'default.png',
                                        email text UNIQUE,
                                        secondary_email text UNIQUE,
                                        password text NOT NULL,
                                        motto text,
                                        bio text,
                                        birthday DATE,
                                        rank text NOT NULL DEFAULT 'user',
                                        telephone_number text,
                                        tasks_completed integer DEFAULT 0,
                                        tasks_in_progress integer DEFAULT 0,
                                        tasks_failed integer DEFAULT 0
                                    ); """
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    min_value integer NOT NULL,
                                    max_value integer NOT NULL,
                                    value integer NOT NULL,
                                    repeat text NOT NULL,
                                    user_id integer NOT NULL,
                                    start_date text NOT NULL,
                                    end_date text NOT NULL,
                                    public text NOT NULL,
                                    status text NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users (id)
                                );"""

    # Create a database connection
    conn = create_connection(database)
    # Create users table
    execute_sql(conn, sql_create_users_table)
    # Create tasks table
    execute_sql(conn, sql_create_tasks_table)

    populate_db(conn)


class Config:
    # Generate random secure token for flask_sessions and bcrypt
    SECRET_KEY = f'{secrets.token_hex(16)}'
    system = platform.platform()

    try:
        # For production environment
        if 'windows' not in system.lower():
            SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
                username="Simpl1f1ed",
                password=os.environ.get("DB_PASSOWRD"),
                hostname="Simpl1f1ed.mysql.pythonanywhere-services.com",
                databasename="Simpl1f1ed$ToDoosDB",
            )
        else:
            # For dev environment to connect to production DB
            tunnel = sshtunnel.SSHTunnelForwarder(
                ('ssh.pythonanywhere.com'),
                ssh_username='Simpl1f1ed',
                ssh_password=os.environ.get("PA_ACCOUNT_PW"),
                remote_bind_address=(
                    'Simpl1f1ed.mysql.pythonanywhere-services.com', 3306))

            tunnel.start()

            SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://Simpl1f1ed:{password}@127.0.0.1:{bind_port}/Simpl1f1ed$ToDoosDB'.format(
                password=os.environ.get("DB_PASSOWRD"),
                bind_port=tunnel.local_bind_port)
    except ValueError:
        # Dev DB when there is no production DB or a faulty connection
        SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
