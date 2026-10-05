
create_table = """
CREATE TABLE IF NOT EXISTS db_config (
    id integer PRIMARY KEY,
    data_was_imported bool
);
"""

select_first = """
SELECT *
FROM db_config
LIMIT 1;
"""

init_config = """
INSERT INTO db_config
    (data_was_imported) 
VALUES
    (false);
"""