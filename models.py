import uuid
from uuid import UUID

import pandas as pd
import enum
from dataclasses import dataclass


class Gender(enum.StrEnum):
    Male = 'male'
    Female = 'female'
    Other = 'other'


class WorkType(enum.StrEnum):
    Private = 'private'
    SelfEmployed = 'self_employed'
    Gov = 'govt_job'
    Children = 'children'
    NeverWorked = 'never_worked'

    @staticmethod
    def create_from_str(value: str):
        value = value.lower()
        if value == "self-employed":
            return WorkType.SelfEmployed
        return WorkType(value)


class ResidenceType(enum.StrEnum):
    Rural = 'rural'
    Urban = 'urban'


class SmokingStatus(enum.StrEnum):
    Smoked = 'smoked'
    NeverSmoked = 'never_smoked'
    FormerlySmoked = 'formerly_smoked'
    Smokes = 'smokes'
    Unknown = 'unknown'

    @staticmethod
    def create_from_str(value: str):
        value = value.lower()
        match value:
            case "never smoked":
                return SmokingStatus.NeverSmoked
            case "formerly smoked":
                return SmokingStatus.FormerlySmoked
            case _:
                return SmokingStatus(value)


@dataclass
class PersonHealth:
    hypertension: bool
    heart_disease: bool
    avg_glucose_level: float
    bmi: float
    smoking_status: SmokingStatus
    stroke: bool
    person_id: UUID

    @staticmethod
    def create_from_series(data: pd.Series, person_id: UUID):
        return PersonHealth(
            hypertension=bool(data['hypertension']),
            heart_disease=data['heart_disease'] == 1,
            avg_glucose_level=float(data["avg_glucose_level"]),
            bmi=float(data["bmi"]),
            smoking_status=SmokingStatus.create_from_str(data["smoking_status"]),
            stroke=bool(data["stroke"]),
            person_id=person_id,
        )


@dataclass
class PersonData:
    id: UUID
    v_id: int
    gender: Gender
    age: float
    ever_married: bool
    work_type: WorkType
    residence_type: ResidenceType
    health: PersonHealth

    @staticmethod
    def create_from_series(data: pd.Series):
        person_id = uuid.uuid4()
        return PersonData(
            id=person_id ,
            v_id=data["id"],
            gender=Gender(data["gender"].lower()),
            age=data["age"],
            ever_married=data['ever_married'] == "Yes",
            work_type=WorkType.create_from_str(data['work_type']),
            residence_type=ResidenceType(data['Residence_type'].lower()),
            health=PersonHealth.create_from_series(data, person_id)
        )

    def to_db_tuple(self):
        return (
            str(self.id), self.v_id, self.gender.value,
            self.age, self.ever_married,
            self.work_type.value, self.residence_type.value
        )


@dataclass
class DbConfigModel:
    id: int
    data_was_imported: bool = False

    @staticmethod
    def create_from_db(data: tuple):
        return DbConfigModel(data[0], data[1])
