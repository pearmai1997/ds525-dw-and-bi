from typing import NewType

import psycopg2


PostgresCursor = NewType("PostgresCursor", psycopg2.extensions.cursor)
PostgresConn = NewType("PostgresConn", psycopg2.extensions.connection)

table_drop_events = "DROP TABLE IF EXISTS events"
table_drop_actors = "DROP TABLE IF EXISTS actors"
table_drop_repo = "DROP TABLE IF EXISTS repo"
table_drop_payload_push = "DROP TABLE IF EXISTS payload_push"
table_drop_commits = "DROP TABLE IF EXISTS commits"
table_drop_org = "DROP TABLE IF EXISTS org"


table_create_actors = """
    CREATE TABLE IF NOT EXISTS actors (
        id int,
        login text,
        display_login text,
        gravatar_id text,
        url text,
        avatar_url text,
        PRIMARY KEY(id)
    )
"""

table_create_repo = """
    CREATE TABLE IF NOT EXISTS repo (
        id int,
        name text,
        url text,
        PRIMARY KEY(id)
    )
"""

table_create_org = """
    CREATE TABLE IF NOT EXISTS org (
        id int,
        login text,
        gravatar_id text,
        url text,
        avatar_url text,
        PRIMARY KEY(id)
    )
"""

table_create_payload_push = """
    CREATE TABLE IF NOT EXISTS payload_push (
        id bigint,
        size int,
        ref text,
        head text,
        before text,
        PRIMARY KEY(id)
    )
"""

table_create_events = """
    CREATE TABLE IF NOT EXISTS events (
        id bigint,
        type text,
        actor_id int,
        repo_id int,
        org_id int,
        payload_action text,
        payload_push_id bigint,
        public boolean,
        create_at timestamp,
        PRIMARY KEY(id),
        CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id),
        CONSTRAINT fk_repo FOREIGN KEY(repo_id) REFERENCES repo(id),
        CONSTRAINT fk_org FOREIGN KEY(org_id) REFERENCES org(id),
        CONSTRAINT fk_payload_push FOREIGN KEY(payload_push_id) REFERENCES payload_push(id)
    )
"""

table_create_commits = """
    CREATE TABLE IF NOT EXISTS commits (
        commits_sha text,
        author_email text,
        author_name text,
        message text,
        url text,
        payload_push_id bigint,
        PRIMARY KEY(commits_sha),
        CONSTRAINT fk_payload_push FOREIGN KEY(payload_push_id) REFERENCES payload_push(id)

    )
"""

create_table_queries = [
    table_create_actors,
    table_create_repo,
    table_create_payload_push,
    table_create_org,
    table_create_events,
    table_create_commits
]
drop_table_queries = [
    table_drop_events,
    table_drop_actors,
    table_drop_repo,
    table_drop_commits,
    table_drop_payload_push,
    table_drop_org
]


def drop_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database.
    - Establishes connection with the sparkify database and gets
    cursor to it.
    - Drops all the tables.
    - Creates all tables needed.
    - Finally, closes the connection.
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
