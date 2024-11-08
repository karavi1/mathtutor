from sqlalchemy import create_engine, text


def get_resources(topic: str):
    engine = create_engine('postgresql://localhost/mathtutordb', echo = True)
    with engine.connect() as conn:
        output = conn.execute(text('SELECT * FROM public.resources'))

    ## There is definitely a better way to write this with sql lol
    return [row[2] for row in output.fetchall() if row[1] == topic]

print(get_resources('algebra'))