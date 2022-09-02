import platform
import secrets
import os
import sshtunnel


class Config:
    SECRET_KEY = f'{secrets.token_hex(16)}' # Generate random secure token for flask_sessions and bcrypt
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
            # For dev environment
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
        print("no")
