import time

import pandas as pd
from models import PersonData

_RAW_DATA_PATH = "./data/s_data.csv"


def get_raw_person_data():
    return pd.read_csv(_RAW_DATA_PATH)


def parse_person_data(raw_data: pd.DataFrame):
    people_data = []

    print("\n[ LOADING CSV DATA ]")
    print("[ ", end="")

    for i, row in raw_data.iterrows():
        if i % (raw_data.shape[0] // 60) == 0:
            print("|", end="")
            time.sleep(0.02)
        people_data.append(PersonData.create_from_series(row))
    print(" ]")
    print(f"[ Parsed Rows: {len(people_data)} | Total Data: {raw_data.size} ]")

    return people_data
