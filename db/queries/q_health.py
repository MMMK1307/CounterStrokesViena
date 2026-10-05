
create_table = """
CREATE TABLE IF NOT EXISTS person_health (
    id text PRIMARY KEY,
    hypertension integer,
    heart_disease integer,
    avg_glucose_level real,
    bmi real,
    smoking_status text,
    stroke integer,
    person_id text,
    FOREIGN KEY(person_id) references person(id)
);
"""