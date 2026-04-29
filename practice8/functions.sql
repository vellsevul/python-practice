-- ==============================
-- PRACTICE 8 FUNCTIONS & PROCEDURES
-- PhoneBook database
-- ==============================


-- 1. SEARCH BY PATTERN FUNCTION
-- ищет по части имени или телефона

CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(
    id INT,
    username VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.username, c.phone
    FROM contacts c
    WHERE c.username ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%';
END;
$$;



-- 2. UPSERT CONTACT PROCEDURE
-- если контакт есть → update
-- если нет → insert

CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contacts WHERE username = p_name
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE username = p_name;
    ELSE
        INSERT INTO contacts(username, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;



-- 3. PAGINATION FUNCTION
-- вывод по страницам (limit + offset)

CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(
    id INT,
    username VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM contacts
    ORDER BY id
    LIMIT p_limit OFFSET p_offset;
END;
$$;



-- 4. DELETE CONTACT PROCEDURE
-- удаляет по имени ИЛИ телефону

CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE username = p_value
       OR phone = p_value;
END;
$$;

-- 5. BULK INSERT PROCEDURE
-- вставка многих записей
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names VARCHAR[], 
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        -- Простая валидация: телефон должен быть длиннее 5 символов
        IF length(p_phones[i]) >= 5 THEN
            INSERT INTO contacts (username, phone) 
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (username) DO UPDATE SET phone = p_phones[i];
        ELSE
            RAISE NOTICE 'Invalid phone for user %: %', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;