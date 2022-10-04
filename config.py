import os
import pathlib
import platform
import secrets
# Dev imports
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


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_dev_tables():
    database = str(pathlib.Path(
        __file__).parent.resolve()) + f"\\dev.db"
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL UNIQUE,
                                        image_file text NOT NULL DEFAULT 'default.png',
                                        email text UNIQUE,
                                        password text NOT NULL,
                                        motto text,
                                        bio text,
                                        birthday DATE,
                                        rank text NOT NULL DEFAULT 'user'
                                    ); """
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    min_value integer NOT NULL,
                                    max_value integer NOT NULL,
                                    value integer NOT NULL,
                                    user_id integer NOT NULL,
                                    start_date text NOT NULL,
                                    end_date text NOT NULL,
                                    status text NOT NULL,
                                    public text NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users (id)
                                );"""
    # Create a database connection
    conn = create_connection(database)
    # Create users table
    create_table(conn, sql_create_users_table)
    # Create tasks table
    create_table(conn, sql_create_tasks_table)


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
                databasename="Simpl1f1ed$ToDosDB",
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

            SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://Simpl1f1ed:{password}@127.0.0.1:{bind_port}/Simpl1f1ed$ToDosDB'.format(
                password=os.environ.get("DB_PASSOWRD"),
                bind_port=tunnel.local_bind_port)
    except ValueError:
        # Dev DB when there is no production DB or a faulty connection
        SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
