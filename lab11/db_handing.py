import psycopg2
import csv

conn = psycopg2.connect( # creating a connection
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2007"
)

# -- коменты в PgAdmin

search_on_pattern = '''
CREATE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE (
    id       INT,
    username VARCHAR(100),
    phone    VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT ph.id, ph.username, ph.phone
      FROM phonebook AS ph
     WHERE ph.username ILIKE '%' || pattern || '%'
        OR ph.phone    ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
'''

insert_user = '''
CREATE PROCEDURE upsert_user(
    user_name  TEXT,
    user_phone TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE username = user_name) THEN
        UPDATE phonebook
           SET phone = user_phone
         WHERE username = user_name;
    ELSE
        INSERT INTO phonebook(username, phone)
             VALUES (user_name, user_phone);
    END IF;
END;
$$;
'''

inser_list_of_users = '''
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_input') THEN
        CREATE TYPE user_input AS (username TEXT, phone TEXT);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_users(users user_input[])
LANGUAGE plpgsql AS $$
DECLARE
    u         user_input;
    bad_users user_input[] := '{}';
BEGIN
    FOREACH u IN ARRAY users LOOP
        IF u.phone ~ '^\d{10,}$' THEN --изспользуем RegEx должно быть 10 цифр
            CALL upsert_user(u.username, u.phone);
        ELSE
            bad_users := array_append(bad_users, u);
        END IF;
    END LOOP;
    RAISE NOTICE 'Invalid entries: %', bad_users;
END;
$$;
'''

querying_data = '''
CREATE OR REPLACE FUNCTION get_phonebook_page(
    page_limit  INT,
    page_offset INT
)
RETURNS TABLE (
    id       INT,
    username VARCHAR(100),
    phone    VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT ph.id,  --воспринимал id неправильно
           ph.username,
           ph.phone
      FROM phonebook AS ph
     ORDER BY ph.id         
     LIMIT  page_limit
    OFFSET page_offset;     
END;
$$ LANGUAGE plpgsql;

'''

delete_user = '''
CREATE OR REPLACE PROCEDURE delete_by_user_or_phone(target TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
     WHERE username = target
        OR phone    = target;
END;
$$;
'''

'''
-- Single upsert
CALL upsert_user('Alice', '87001234567');

-- Bulk insert
CALL insert_many_users(ARRAY[
    ROW('Bob',     '12345'),        -- invalid
    ROW('Charlie', '87775556666'),  -- valid
    ROW('Dana',    'abcdefghij')    -- invalid
]::user_input[]);

-- Search
SELECT * FROM search_phonebook('ali');

-- Pagination (e.g., get 5 rows starting from the 10th)
SELECT * FROM get_phonebook_page(5, 10);

-- Delete
CALL delete_by_user_or_phone('Charlie');

'''