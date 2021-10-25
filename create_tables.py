import mysql.connector
import click


@click.command()
@click.option('--host', default="localhost", help='MySQL to connect to')
@click.option('--port', default=3306, help='MySQL to connect to')
@click.option('--username', help='Database username')
@click.option('--password', help='Database password')
@click.option('--database', help='Database to user')
def create_table(host, port, username, password, database):
    db_connector = mysql.connector.connect(user=username, password=password, host=host, port=port, database=database)
    cursor = db_connector.cursor()

    # Create school workers table
    cursor.execute("""
    CREATE TABLE school_workers (
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    NAME VARCHAR(50) NOT NULL,
    SURNAME VARCHAR(50) NOT NULL,
    POSITION VARCHAR(50) NOT NULL,
    SALARY INT NOT NULL
    );
    """)

    # Create school classes table
    cursor.execute("""
    CREATE TABLE school_classes (
    ID INT  NOT NULL AUTO_INCREMENT,
    CLASS_NAME VARCHAR(50) NOT NULL,
    CLASS_CAPACITY INT NOT NULL,
    PRIMARY KEY(ID, CLASS_NAME)
    );
    """)

    # Create school students table
    cursor.execute("""
    CREATE TABLE school_students (
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    NAME VARCHAR(50) NOT NULL,
    SURNAME VARCHAR(50) NOT NULL,
    CLASS_ID INT,
    CLASS_NAME VARCHAR(50),
    FOREIGN KEY (CLASS_ID, CLASS_NAME) REFERENCES school_classes (ID,CLASS_NAME) ON DELETE CASCADE
    );
    """)

    db_connector.close()

if __name__ == "__main__":
    create_table()