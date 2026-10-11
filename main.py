
from data_parser import get_raw_person_data, parse_person_data, parse_people_into_db
from db.base_db import init_db, connection
from db.config_db import ConfigDb
from db.person_db import PersonDb
from models import PersonData, SmokingStatus, WorkType
import pandas as pd
import matplotlib.pyplot as plt


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


def age_tenths(age: int):
    if age < 10:
        return 10
    tenth = age // 10
    return int(tenth * 10)


def work_type_renaming(s):
    return WorkType.get_label(s)


def plotting(data: pd.DataFrame):
    plot_op = int(input("[1] Age Distribution [2] Hypertension Comparison [3] Work Comparison\n> "))

    match plot_op:
        case 1:
            have_stroked = data.loc[data["health_stroke"] == 1]
            d = have_stroked["age"].apply(age_tenths)
            d.groupby(d).count().plot(kind="pie")
            plt.title("Distribuição por Idade \nIdades comprimidas ao digito mais relevante. 73 -> 70 ou 59 -> 50")
        case 2:
            d = data.loc[(data["health_hypertension"] == 1) | (data["health_stroke"] == 1)].groupby(["health_stroke", "health_hypertension"])["id"].count()
            d = d.rename({0: "N", 1: "S"})
            d.plot(kind="bar", xlabel="AVC, Hipertensão \n S = Sim | N = Não", ylabel="Quantidade Pessoas")
            plt.title("Comparação Hipertensão")
        case 3:
            have_stroked = data.loc[data["health_stroke"] == 1]
            have_stroked['work_type'] = have_stroked['work_type'].apply(work_type_renaming)
            have_stroked.groupby("work_type")["id"].count().plot(kind="bar", ylabel="Tipo Trabalho", xlabel="Quantidade Pessoas")
            plt.title("Comparação Tipo de Trabalho")

    plt.show()


def menu(people_data: list[PersonData]):
    option = 1
    people_frame = pd.DataFrame(person_data.to_dict() for person_data in people_data)
    while option != 0:
        print("\n[MENU]")
        print("[1] Stroke Studies [2] Plotting [0] exit")

        try:
            option = int(input("> "))
        except ValueError:
            option = 5

        print()
        match option:
            case 1:
                stroke_studies(people_frame)
            case 2:
                plotting(people_frame)

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
