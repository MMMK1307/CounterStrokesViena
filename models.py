import uuid
from uuid import UUID

import math
import pandas as pd
import enum
from dataclasses import dataclass, asdict


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
    id: UUID
    hypertension: bool
    heart_disease: bool
    avg_glucose_level: float
    bmi: float | None
    smoking_status: SmokingStatus
    stroke: bool
    person_id: UUID

    @staticmethod
    def create_from_db(data: tuple):
        return PersonHealth(
            uuid.UUID(data[0]),
            data[1],
            data[2],
            data[3],
            data[4],
            SmokingStatus(data[5]),
            data[6],
            uuid.UUID(data[7])
        )

    @staticmethod
    def create_from_series(data: pd.Series, person_id: UUID):
        bmi = float(data["bmi"])
        return PersonHealth(
            id=uuid.uuid4(),
            hypertension=bool(data['hypertension']),
            heart_disease=data['heart_disease'] == 1,
            avg_glucose_level=float(data["avg_glucose_level"]),
            bmi=bmi if not math.isnan(bmi) else None,
            smoking_status=SmokingStatus.create_from_str(data["smoking_status"]),
            stroke=bool(data["stroke"]),
            person_id=person_id,
        )

    def to_db_tuple(self):
        return (
            str(self.id),
            self.hypertension,
            self.heart_disease,
            self.avg_glucose_level,
            self.bmi,
            self.smoking_status.value,
            self.stroke,
            str(self.person_id),
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
    def create_from_db(data: tuple):
        return PersonData(
            uuid.UUID(data[0]),
            data[1],
            Gender(data[2]),
            data[3],
            data[4],
            WorkType(data[5]),
            ResidenceType(data[6]),
            PersonHealth.create_from_db(data[7:])
        )

    @staticmethod
    def create_from_series(data: pd.Series):
        person_id = uuid.uuid4()
        return PersonData(
            id=person_id,
            v_id=data["id"],
            gender=Gender(data["gender"].lower()),
            age=float(data["age"]),
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

    def to_dict(self) -> dict:
        base_data = asdict(self)
        del base_data["health"]
        d = {f"health_{name}": value for name, value in asdict(self.health).items()}
        return { **base_data, **d }


@dataclass
class DbConfigModel:
    id: int
    data_was_imported: bool = False

    @staticmethod
    def create_from_db(data: tuple):
        return DbConfigModel(data[0], data[1])
