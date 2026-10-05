
create_table = """
CREATE TABLE IF NOT EXISTS person_data (
    id TEXT PRIMARY KEY,
    v_id INTEGER,
    gender char(10),
    age float,
    ever_married bool,
    work_type char(15),
    residence_type char(8)
);
"""