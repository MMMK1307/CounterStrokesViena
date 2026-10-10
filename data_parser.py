import time
from sqlite3 import Connection

import pandas as pd
from models import PersonData

_RAW_DATA_PATH = "./data/s_data.csv"


def get_raw_person_data():
    data: pd.DataFrame = pd.read_csv(_RAW_DATA_PATH)
    data = data.dropna()
    return data


def parse_person_data(raw_data: pd.DataFrame):
    people_data = []

    print("\n[ LOADING CSV DATA ]\n")
    raw_data.info()
    print("\n[", end="")

    for i, row in raw_data.iterrows():
        if i % (raw_data.shape[0] // 60) == 0:
            print("|", end="")
            time.sleep(0.02)
        people_data.append(PersonData.create_from_series(row))
    print(f"] \n[ Parsed Rows: {len(people_data)} | Total Data: {raw_data.size} ]")

    return people_data


def parse_people_into_db(conn: Connection, people_data: list[PersonData]):
    cursor = conn.cursor()
    batch_size = 255
    batch_count = 1
    batch_data = ()

    print("\n[ FEEDING THE DB ] ")
    print("[ Inserting Person Data ]\n[", end="")

    for person_data in people_data:
        batch_data += person_data.to_db_tuple()

        if batch_count % batch_size == 0 or len(people_data) - batch_count <= 0:
            values_templates = "(?, ?, ?, ?, ?, ?, ?)," * ((len(batch_data)//7) - 1)
            insert_query = f"""
                INSERT INTO person_data 
                VALUES
                {values_templates}
                (?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, batch_data)
            conn.commit()
            batch_data = ()

        batch_count += 1

        if batch_count % (len(people_data) // 60) == 0:
            print("|", end="")

    print("]\n[ Inserting Health Data ]\n[", end="")
    batch_count = 1
    batch_data = ()
    for person_data in people_data:
        person_health = person_data.health
        batch_data += person_health.to_db_tuple()

        if batch_count % batch_size == 0 or len(people_data) - batch_count <= 0:
            values_templates = "(?, ?, ?, ?, ?, ?, ?, ?)," * ((len(batch_data)//8) - 1)
            insert_query = f"""
                INSERT INTO person_health
                VALUES
                {values_templates}
                (?, ?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, batch_data)
            conn.commit()
            batch_data = ()

        batch_count += 1
        if batch_count % (len(people_data) // 60) == 0:
            print("|", end="")

    print("]\n[ Database was fed ]\n")

