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

    def count_rows(self) -> int:
        cursor = self.conn.cursor()
        count = cursor.execute("""SELECT COUNT(*) from person_data;""").fetchone()[0]
        cursor.close()
        return count

    def get_stoken(self) -> list[PersonData]:
        cursor = self.conn.cursor()
        db_data = cursor.execute("""
            SELECT *
            FROM person_data person
            JOIN person_health health on person.id = health.person_id;
            WHERE health.stroke = 1;
        """).fetchall()
        people_data = []
        for data in db_data:
            people_data.append(PersonData.create_from_db(data))
        cursor.close()
        return people_data

    def get_people_avg_glucose_level(self, name: str) -> float:
        cursor = self.conn.cursor()
        avg = cursor.execute("""
            SELECT AVG(health.avg_glucose_level)
            FROM person_data person
            JOIN person_health health on person.id = health.person_id;
            WHERE person.name like '%?%'
        """, name).fetchone()[0]
        cursor.close()
        return avg
