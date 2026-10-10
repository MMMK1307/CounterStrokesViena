from sqlite3 import Connection

from models import PersonData


class PersonDb:
    conn: Connection

    def __init__(self, conn: Connection | None):
        from db import base_db
        if conn:
            self.conn = conn
        self.conn = base_db.connection()

    def load_all(self):
        cursor = self.conn.cursor()
        db_data = cursor.execute("""
        SELECT *
        FROM person_data person
        JOIN person_health health on person.id = health.person_id;
        """).fetchall()
        people_data = []
        for data in db_data:
            people_data.append(PersonData.create_from_db(data))
        cursor.close()
        return people_data
