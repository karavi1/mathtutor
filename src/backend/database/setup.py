import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert

# Load environment variables from .env file
load_dotenv()
env = {
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'name': os.getenv('DB_NAME')
}

engine = create_engine(f"postgresql://{env['username']}:{env['password']}@localhost/{env['name']}")
meta = MetaData()


### Create Topics Table
resources = Table(
   'resources', meta,
   Column('topic_id', Integer, primary_key = True),
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

with engine.connect() as conn:
    conn.execute(first)
    conn.execute(second)
    conn.execute(third)
    conn.execute(fourth)
    conn.commit()