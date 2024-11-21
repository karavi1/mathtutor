import os
from dotenv import load_dotenv

def get_sqlalchemy_database_url():
        
    # Load environment variables from .env file
    load_dotenv()
    env = {
        'username': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'name': os.getenv('DB_NAME'),
        'endpoint': os.getenv('DB_HOSTNAME'),
        'port': os.getenv('DB_PORT')
    }

    return f"postgresql://{env['username']}:{env['password']}@{env['endpoint']}:{env['port']}/{env['name']}"

