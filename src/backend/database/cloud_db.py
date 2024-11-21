import os
from dotenv import load_dotenv
from sqlalchemy import inspect, create_engine, MetaData, Table, Column, Integer, String, insert
from sqlalchemy.exc import OperationalError
from connect import get_sqlalchemy_database_url

# Load environment variables from .env file
load_dotenv()
env = {
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'name': os.getenv('DB_NAME'),
    'endpoint': os.getenv('DB_HOSTNAME'),
    'port': os.getenv('DB_PORT')
}

SQLALCHEMY_DATABASE_URL = f"postgresql://{env['username']}:{env['password']}@{env['endpoint']}:{env['port']}/{env['name']}"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    meta = MetaData()
    with engine.connect() as conn:
        print("Connection successful!")
        ### Create Topics Table
        resources = Table(
            'resources', meta,
            Column('topic_id', Integer, primary_key=True),
            Column('topic', String),
            Column('resource', String),
        )
        meta.create_all(engine)

        ### Add sample topics for Algebra and Geometry
        first = (
            insert(resources).
            values(topic='algebra', resource='https://www.wolframalpha.com/examples/mathematics/algebra')
        )

        second = (
            insert(resources).
            values(topic='algebra', resource='https://byjus.com/maths/algebra-problems/')
        )

        third = (
            insert(resources).
            values(topic='geometry', resource='https://www.wolframalpha.com/examples/mathematics/geometry')
        )

        fourth = (
            insert(resources).
            values(topic='geometry', resource='https://www.studyguidezone.com/geometry-help.htm')
        )
        conn.execute(first)
        conn.execute(second)
        conn.execute(third)
        conn.execute(fourth)


        # Inspect the database
        inspector = inspect(engine)

        # List all tables in the database
        tables = inspector.get_table_names()
        print(tables)
        print("records added!")
        conn.commit()
except OperationalError as e:
    # Handle the specific operational error (database connection issue)
    print("Connection failed:", str(e))
except Exception as e:
    # Catch any other unexpected errors
    print("An unexpected error occurred:", str(e))

