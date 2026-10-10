
from data_parser import get_raw_person_data, parse_person_data, parse_people_into_db
from db.base_db import init_db, connection
from db.config_db import ConfigDb
from db.person_db import PersonDb
from models import PersonData, SmokingStatus
import pandas as pd


def stroke_studies(data: pd.DataFrame):
    have_stroked = data.loc[data["health_stroke"] == 1]
    stroked_count = have_stroked["id"].count()
    total = data['id'].count()
    t_percent = round(100/stroked_count, 2)

    print("[ STROKE STUDIES ]")
    print(f"Total: {total} | Total Strokes: ", stroked_count)
    print(f"\nOf Age: \n > Mean: {round(have_stroked['age'].mean(), 1)} | Median: {have_stroked['age'].median()} | Min: {have_stroked['age'].min()}")

    hypertension_count = have_stroked.loc[data['health_hypertension'] == 1]["id"].count()
    print(f"Of Hypertension ({round(t_percent*hypertension_count, 2)}%): \n > {hypertension_count}")

    heart_disease_count = have_stroked.loc[data["health_heart_disease"] == 1]["id"].count()
    print(f"Of Heart Disease ({round(t_percent*heart_disease_count, 2)}%): \n > {heart_disease_count} ")

    glucose_count = have_stroked.loc[data["health_avg_glucose_level"] > 100]["id"].count()
    print(f"Of High Glucose [>100 mg/dl] ({round(t_percent*glucose_count, 2)}%): \n > {glucose_count}")

    high_bmi_count = have_stroked.loc[data["health_bmi"] > 25]["id"].count()
    print(f"Of High BMI [>25] ({round(t_percent*high_bmi_count, 2)}%): \n > {high_bmi_count}")

    smoking_status = have_stroked.groupby("health_smoking_status")["health_smoking_status"].count()
    print(f"Of Smoking Status: ")
    for index, value in smoking_status.items():
        print(f" > {SmokingStatus(index).name}: {value}")


def plotting(data: pd.DataFrame):
    print("")


def menu(people_data: list[PersonData]):
    option = 1
    people_frame = pd.DataFrame(person_data.to_dict() for person_data in people_data)
    while option != 0:
        print("\n[MENU]")
        print("[1] Stroke Studies [2] PLOTS [0] exit")

        try:
            option = int(input("> "))
        except ValueError:
            option = 5

        print()
        match option:
            case 1:
                stroke_studies(people_frame)







def main():
    init_db()
    people_data = []

    with connection() as conn:
        config = ConfigDb(conn).get_config()
        if not config.data_was_imported:
            people_data = parse_person_data(get_raw_person_data())
            parse_people_into_db(conn, people_data)
            config.data_was_imported = True
            ConfigDb(conn).save(config)

    if len(people_data) <= 0:
        people_data = PersonDb(conn).load_all()

    menu(people_data)

if __name__ == '__main__':
    main()
