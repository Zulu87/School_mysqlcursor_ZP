import mysql.connector
import click

from helper import read_csv, form_insert_from_dict_tuple


@click.command()
@click.option('--host', default="localhost", help='MySQL to connect to')
@click.option('--port', default=3306, help='MySQL to connect to')
@click.option('--username', help='Database username')
@click.option('--password', help='Database password')
@click.option('--database', help='Database to user')
def insert_data(host, port, username, password, database):
    db_connector = mysql.connector.connect(user=username, password=password, host=host, port=port, database=database)
    cursor = db_connector.cursor()

    school_workers = read_csv("school_workers.csv")

    school_classes = read_csv("school_classes.csv")

    school_students = read_csv("school_students.csv")


    # Insert school workers
    cursor.execute(form_insert_from_dict_tuple('school_workers', school_workers))
    db_connector.commit()


    # Insert school classes
    cursor.execute(form_insert_from_dict_tuple('school_classes', school_classes))
    db_connector.commit()

    # Insert school students
    cursor.execute(form_insert_from_dict_tuple('school_students', school_students))
    db_connector.commit()

    db_connector.close()


if __name__ == "__main__":
    insert_data()