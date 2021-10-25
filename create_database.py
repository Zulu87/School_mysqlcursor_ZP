import mysql.connector
import click


@click.command()
@click.option('--host', default="localhost", help='MySQL to connect to')
@click.option('--port', default=3306, help='MySQL to connect to')
@click.option('--username', help='Database username')
@click.option('--password', help='Database password')
@click.option('--database', help='Database to create')
def create_database(host, port, username, password, database):
    db_connector = mysql.connector.connect(user=username, password=password, host=host, port=port)
    cursor = db_connector.cursor()
    create_query = f"CREATE DATABASE {database}"
    cursor.execute(create_query)
    db_connector.close()

if __name__ == "__main__":
    create_database()
