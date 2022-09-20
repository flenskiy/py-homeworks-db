import psycopg2


def init_client_db(database_name, user_name, user_password):
    conn = psycopg2.connect(
        database=database_name, user=user_name, password=user_password
    )
    with conn.cursor() as cur:
        cur.execute(
            """
                    DROP TABLE phone;
                    DROP TABLE client;
                """
        )
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
                JOIN phone ph ON cl.client_id = ph.client_id
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
                    JOIN phone ph ON cl.client_id = ph.client_id
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
                    JOIN phone ph ON cl.client_id = ph.client_id
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
                    JOIN phone ph ON cl.client_id = ph.client_id
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
                    JOIN phone ph ON cl.client_id = ph.client_id
                    WHERE phone=%s;
                    """,
                (searched_phone,),
            )
            result = cur.fetchall()
            return _get_client_data()


db_conn = init_client_db(
    database_name="netology_db", user_name="postgres", user_password="P@ssw0rd"
)
add_client(db_conn, "Ivan", "Ivanov", "ivanov@mail.ru", "89991776361")
add_client(db_conn, "Fedor", "Fedorov", "fedorov@mail.ru", "89991776364")
add_client(db_conn, "Petr", "Petrov", "petrov@mail.ru", "89991776362", "89996203042")
add_client(db_conn, "Vasiliy", "Vasiliev", "vasiliev@mail.ru")

# with db_conn.cursor() as db_cur:
#     db_cur.execute(
#         """
#                 SELECT * FROM client;
#                 """
#     )
#     print(db_cur.fetchall())
#
#     db_cur.execute(
#         """
#                 SELECT * FROM phone;
#                 """
#     )
#     print(db_cur.fetchall())

add_client_phone(db_conn, "fedorov@mail.ru", "89991776365")
add_client_phone(db_conn, "vasiliev@mail.ru", "89991776369")
# change_client_data(
#     db_conn,
#     "petrov@mail.ru",
#     {
#         "name": [True, "Vladimir"],
#         "surname": [True, "Vladimirov"],
#         "email": [True, "vladimirov@mail.ru"],
#         "phone": [True, ["776415"]],
#     },
# )
# delete_client_phone(db_conn, "vasiliev@mail.ru")
# delete_client(db_conn, "vasiliev@mail.ru")

# with db_conn.cursor() as db_cur:
#     db_cur.execute(
#         """
#                 SELECT * FROM client;
#                 """
#     )
#     print(db_cur.fetchall())
#
#     db_cur.execute(
#         """
#                 SELECT * FROM phone;
#                 """
#     )
#     print(db_cur.fetchall())


result1 = search_client(
    db_conn,
    {
        "name": [False, None],
        "surname": [False, None],
        "email": [True, "fedorov@mail.ru"],
        "phone": [False, None],
    },
)
print(result1)

db_conn.close()
