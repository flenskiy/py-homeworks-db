import psycopg2


def init_client_db(database_name, user_name, user_password):
    conn = psycopg2.connect(database=database_name, user=user_name, password=user_password)
    with conn.cursor() as cur:
        cur.execute("""
                    DROP TABLE phone;
                    DROP TABLE client;
                """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS client(
                        client_id SERIAL NOT NULL PRIMARY KEY, 
                        name varchar(40) NOT NULL,
                        surname varchar(40) NOT NULL,
                        email varchar(40) NOT NULL
                    );
                """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS phone(
                        phone_id SERIAL NOT NULL PRIMARY KEY,
                        phone varchar(40) UNIQUE,
                        client_id INT REFERENCES client(client_id) NOT NULL
                        );
                """)
    conn.commit()
    return conn


def add_client(conn, name, surname, email, *phones):
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO client(name, surname, email) VALUES(%s, %s, %s) RETURNING client_id
                    """,
                    (name, surname, email))
        client_id = cur.fetchone()[0]
        for phone in phones:
            cur.execute("""
                        INSERT INTO phone(phone, client_id) VALUES(%s, %s)
                        """,
                        (phone, client_id))
        return client_id


db_conn = init_client_db(database_name="netology_db", user_name="postgres", user_password="P@ssw0rd")
add_client(db_conn, 'Ivan', 'Ivanov', 'ivanov@mail.ru', '89991776361')
add_client(db_conn, 'Petr', 'Petrov', 'petrov@mail.ru', '89991776362', '89996203042')

with db_conn.cursor() as cur:
    cur.execute("""
    SELECT * FROM client;
    """)
    print(cur.fetchall())

    cur.execute("""
        SELECT * FROM phone;
        """)
    print(cur.fetchall())

db_conn.close()
