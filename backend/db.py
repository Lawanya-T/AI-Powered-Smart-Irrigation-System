import os
import psycopg2

def get_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing")

return psycopg2.connect(DATABASE_URL)
