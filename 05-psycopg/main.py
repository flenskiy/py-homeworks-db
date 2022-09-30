import pprint
import psycopg2


def init_client_db(database_name, user_name, user_password):
    conn = psycopg2.connect(
        database=database_name, user=user_name, password=user_password
    )
    with conn.cursor() as cur:
        # cur.execute(
        #     """
        #             DROP TABLE phone;
        #             DROP TABLE client;
        #         """
        # )
        cur.execute(
            """
                    CREATE TABLE IF NOT EXISTS client(
                        client_id SERIAL NOT NULL PRIMARY KEY, 
                        name varchar(40) NOT NULL,
                        surname varchar(40) NOT NULL,
                        email varchar(40) UNIQUE NOT NULL
                    );
                """
        )
        cur.execute(
            """
                    CREATE TABLE IF NOT EXISTS phone(
                        phone_id SERIAL NOT NULL PRIMARY KEY,
                        phone varchar(40) UNIQUE,
                        client_id INT REFERENCES client(client_id) NOT NULL
                        );
                """
        )
    conn.commit()
    return conn


def add_client(conn, name, surname, email, *phones):
    with conn.cursor() as cur:
        cur.execute(
            """
                    INSERT INTO client(name, surname, email) VALUES(%s, %s, %s) RETURNING client_id
                    """,
            (name, surname, email),
        )
        client_id = cur.fetchone()[0]
        for phone in phones:
            cur.execute(
                """
                        INSERT INTO phone(phone, client_id) VALUES(%s, %s)
                        """,
                (phone, client_id),
            )
        return client_id


def check_client_email(conn, email):
    with conn.cursor() as cur:
        cur.execute(
            """
                    SELECT client_id, email FROM client;
                    """
        )
        for item in cur.fetchall():
            client_id, client_email = item
            if email == client_email:
                return [True, client_id]
    return [False, None]


def add_client_phone(conn, email, *phones):
    mail_check_result, client_id = check_client_email(conn, email)
    if mail_check_result:
        with conn.cursor() as cur:
            for phone in phones:
                cur.execute(
                    """
                            INSERT INTO phone(phone, client_id) VALUES(%s, %s)
                            """,
                    (phone, client_id),
                )
            return client_id


def change_client_data(conn, email, data):
    """
    data = {
                'name': [flag,name],
                'surname': [flag, surname],
                'email': [flag, email],
                'phone': [flag, [phone_1, ...,]
            }
    """
    mail_check_result, client_id = check_client_email(conn, email)
    if mail_check_result:
        with conn.cursor() as cur:
            if data["name"][0]:
                new_name = data["name"][1]
                cur.execute(
                    """
                        UPDATE client SET name=%s WHERE client_id=%s;
                        """,
                    (new_name, client_id),
                )
            if data["surname"][0]:
                new_surname = data["surname"][1]
                cur.execute(
                    """
                        UPDATE client SET surname=%s WHERE client_id=%s;
                        """,
                    (new_surname, client_id),
                )
            if data["email"][0]:
                new_email = data["email"][1]
                cur.execute(
                    """
                        UPDATE client SET email=%s WHERE client_id=%s;
                        """,
                    (new_email, client_id),
                )
            if data["phone"][0]:
                phones = data["phone"][1]
                cur.execute(
                    """
                       DELETE FROM phone WHERE client_id=%s;
                       """,
                    (client_id,),
                )
                for phone in phones:
                    cur.execute(
                        """
                                INSERT INTO phone(phone, client_id) VALUES(%s, %s)
                                """,
                        (phone, client_id),
                    )
            conn.commit()
            return client_id


def delete_client_phone(conn, email):
    mail_check_result, client_id = check_client_email(conn, email)
    if mail_check_result:
        with conn.cursor() as cur:
            cur.execute(
                """
                   DELETE FROM phone WHERE client_id=%s;
                   """,
                (client_id,),
            )
            conn.commit()
            return client_id


def delete_client(conn, email):
    mail_check_result, client_id = check_client_email(conn, email)
    if mail_check_result:
        with conn.cursor() as cur:
            cur.execute(
                """
                   DELETE FROM phone WHERE client_id=%s;
                   """,
                (client_id,),
            )
            cur.execute(
                """
                   DELETE FROM client WHERE client_id=%s;
                   """,
                (client_id,),
            )
            conn.commit()
            return client_id


def search_client(conn, search_params):
    """
    search_params = {
                        'name': [flag, name],
                        'surname': [flag, surname],
                        'email': [flag, email],
                        'phone': [flag, phone]
                    }
    """

    def _get_client_data():
        if not result:
            return None
        else:
            client_id = result[0][0]
        cur.execute(
            """
                SELECT name, surname, email, phone FROM client cl
                FULL JOIN phone ph ON cl.client_id = ph.client_id
                WHERE cl.client_id=%s;
                """,
            (client_id,),
        )
        return cur.fetchall()

    with conn.cursor() as cur:
        if search_params["name"][0]:
            searched_name = search_params["name"][1]
            cur.execute(
                """
                    SELECT cl.client_id FROM client cl
                    FULL JOIN phone ph ON cl.client_id = ph.client_id
                    WHERE name=%s;
                    """,
                (searched_name,),
            )
            result = cur.fetchall()
            return _get_client_data()
        if search_params["surname"][0]:
            searched_surname = search_params["surname"][1]
            cur.execute(
                """
                    SELECT cl.client_id FROM client cl
                    FULL JOIN phone ph ON cl.client_id = ph.client_id
                    WHERE surname=%s;
                    """,
                (searched_surname,),
            )
            result = cur.fetchall()
            return _get_client_data()
        if search_params["email"][0]:
            searched_email = search_params["email"][1]
            cur.execute(
                """
                    SELECT cl.client_id FROM client cl
                    FULL JOIN phone ph ON cl.client_id = ph.client_id
                    WHERE email=%s;
                    """,
                (searched_email,),
            )
            result = cur.fetchall()
            return _get_client_data()
        if search_params["phone"][0]:
            searched_phone = search_params["phone"][1]
            cur.execute(
                """
                    SELECT cl.client_id FROM client cl
                    FULL JOIN phone ph ON cl.client_id = ph.client_id
                    WHERE phone=%s;
                    """,
                (searched_phone,),
            )
            result = cur.fetchall()
            return _get_client_data()


def show_clients_info(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
                SELECT cl.client_id, name, surname, email, phone FROM client cl
                FULL JOIN phone ph ON cl.client_id = ph.client_id; 
                """
        )
        pprint.pprint(cur.fetchall())
        print()


if __name__ == "__main__":
    # 1. Функция, создающая структуру БД (таблицы)
    db_conn = init_client_db(
        database_name="netology_db", user_name="postgres", user_password="P@ssw0rd"
    )

    print("1. Функция, создающая структуру БД (таблицы)")
    show_clients_info(db_conn)

    # 2. Функция, позволяющая добавить нового клиента
    add_client(db_conn, "Ivan", "Ivanov", "ivanov@mail.ru", "89991773361")
    add_client(
        db_conn, "Petr", "Petrov", "petrov@mail.ru", "89991771362", "89996201042"
    )
    add_client(db_conn, "Vasily", "Vasiliev", "vasiliev@mail.ru")

    print("2. Функция, позволяющая добавить нового клиента")
    show_clients_info(db_conn)

    # 3. Функция, позволяющая добавить телефон для существующего клиента
    add_client_phone(db_conn, "ivanov@mail.ru", "89991773360")
    add_client_phone(db_conn, "vasiliev@mail.ru", "89991776369")
    print("3. Функция, позволяющая добавить телефон для существующего клиента")
    show_clients_info(db_conn)

    # 4. Функция, позволяющая изменить данные о клиенте
    change_client_data(
        db_conn,
        "vasiliev@mail.ru",
        {
            "name": [True, "Vladimir"],
            "surname": [False, None],
            "email": [True, "vladimir.vasiliev@mail.ru"],
            "phone": [True, ["89991776000", "25-17-00"]],
        },
    )
    print("4. Функция, позволяющая изменить данные о клиенте")
    show_clients_info(db_conn)

    # 5. Функция, позволяющая удалить телефон для существующего клиента
    delete_client_phone(db_conn, "ivanov@mail.ru")
    print("5. Функция, позволяющая удалить телефон для существующего клиента")
    show_clients_info(db_conn)

    # 6. Функция, позволяющая удалить существующего клиента
    delete_client(db_conn, "vladimir.vasiliev@mail.ru")
    print("6. Функция, позволяющая удалить существующего клиента")
    show_clients_info(db_conn)

    # 7. Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
    print(
        "7. Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)"
    )
    print("Поиск по телефону")
    search_result = search_client(
        db_conn,
        {
            "name": [False, None],
            "surname": [False, None],
            "email": [False, None],
            "phone": [True, "89991771362"],
        },
    )
    pprint.pprint(search_result)
    print("Поиск по имени")
    search_result = search_client(
        db_conn,
        {
            "name": [True, "Ivan"],
            "surname": [False, None],
            "email": [False, None],
            "phone": [False, None],
        },
    )
    pprint.pprint(search_result)
    print("Поиск по email")
    search_result = search_client(
        db_conn,
        {
            "name": [False, None],
            "surname": [False, None],
            "email": [True, "petrov@mail.ru"],
            "phone": [False, None],
        },
    )
    pprint.pprint(search_result)

    db_conn.close()
