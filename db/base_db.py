import sqlite3

from db.queries import q_person, q_config, q_health


_dbpath = "./db/counter_strokes_viena.db"


def connection():
    return sqlite3.connect(_dbpath)


def init_db() -> True:
    with connection() as conn:
        from db.config_db import ConfigDb

        cursor = conn.cursor()

        cursor.execute(q_config.create_table)
        cursor.execute(q_person.create_table)
        cursor.execute(q_health.create_table)
        conn.commit()
        _ = ConfigDb(conn).get_config()
        cursor.close()
