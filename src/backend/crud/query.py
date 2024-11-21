import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

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
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def get_resources(topics: list) -> list:
    with engine.connect() as conn:
        output = conn.execute(text('SELECT * FROM resources'))

    ## There is definitely a better way to write this with sql lol
    return [row[2] for row in output.fetchall() if row[1] in topics]


if __name__ == "__main__":
    # Example usage
    print(get_resources('algebra'))
