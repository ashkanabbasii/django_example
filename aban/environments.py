from os import getenv

from dotenv import load_dotenv

load_dotenv()

POSTGRES_NAME = getenv('POSTGRES_NAME', "db")
POSTGRES_DB = getenv('POSTGRES_DB', "order")
POSTGRES_USER = getenv('POSTGRES_USER', "user")
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', "P@ssw9rd")
POSTGRES_HOST = getenv('POSTGRES_HOST', "db")
POSTGRES_PORT = getenv('POSTGRES_PORT', "5432")


# REDIS
REDIS_HOST = getenv('REDIS_HOST', 'redis')
REDIS_PORT = getenv('REDIS_PORT', '6379')
REDIS_PASSWORD = getenv('REDIS_PASSWORD', 'P@ssw0rd')

REDIS_CACHE = 0
REDIS_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE}'
