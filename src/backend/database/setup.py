from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
engine = create_engine('postgresql://localhost/mathtutordb')
meta = MetaData()


### Create Topics Table
topic = Table(
   'topic', meta,
   Column('topic_id', Integer, primary_key = True),
   Column('name', String),
   Column('resources', String),
)
meta.create_all(engine)

first = (
    insert(topic).
    values(name='Algebra', resources='https://www.wolframalpha.com/examples/mathematics/algebra')
)

with engine.connect() as conn:
    result = conn.execute(first)
    conn.commit()