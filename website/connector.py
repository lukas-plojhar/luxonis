import psycopg2

from psycopg2.extensions import connection


def connect_to_database() -> connection:
    return psycopg2.connect(
        host="database",
        port="5432",
        database="postgres",
        user="postgres",
        password="password",
    )
