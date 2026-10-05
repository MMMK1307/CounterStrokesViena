from sqlite3 import Connection
from db.queries import q_config
from models import DbConfigModel


class ConfigDb:
    conn: Connection

    def __init__(self, conn: Connection | None):
        from db import base_db
        if conn:
            self.conn = conn
        self.conn = base_db.connection()

    def _create_config(self):
        cursor = self.conn.cursor()
        cursor.execute(q_config.init_config)
        self.conn.commit()

    def get_config(self) -> DbConfigModel:
        cursor = self.conn.cursor()
        config_data = cursor.execute(q_config.select_first).fetchone()

        if not config_data:
            self._create_config()
            config_data = cursor.execute(q_config.select_first).fetchone()

            if not config_data:
                raise Exception("Failed to Load Config")

        cursor.close()
        return DbConfigModel.create_from_db(config_data)

    def save(self, model: DbConfigModel):
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE db_config
        SET
            data_was_imported = ?
        WHERE id = ?;
        """, (model.data_was_imported, model.id))
        self.conn.commit()
        cursor.close()
