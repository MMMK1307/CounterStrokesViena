from data_parser import get_raw_person_data, parse_person_data, parse_people_into_db
from db.base_db import init_db, connection
from db.config_db import ConfigDb
from db.person_db import PersonDb


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

if __name__ == '__main__':
    main()
