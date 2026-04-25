import psycopg2
from config import config

def connect():
    conn = psycopg2.connect(**config)
    return conn