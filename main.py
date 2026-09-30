from data_parser import get_raw_person_data, parse_person_data


def main():
    parse_person_data(get_raw_person_data())


if __name__ == '__main__':
    main()
