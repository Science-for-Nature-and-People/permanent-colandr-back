import cipy

CONN_CREDS = cipy.db.get_conn_creds('DATABASE_URL')
PGDB = cipy.db.PostgresDB(CONN_CREDS)