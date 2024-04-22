import logging

import json
import glob
import os
from typing import List

from airflow import DAG
from airflow.utils import timezone
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


def _get_files(filepath: str):
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files

def _create_tables():
    hook = PostgresHook(postgres_conn_id="my_postgres_conn")
    conn = hook.get_conn()
    cur = conn.cursor()

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

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def _process(**context):
    hook = PostgresHook(postgres_conn_id="my_postgres_conn")
    conn = hook.get_conn()
    cur = conn.cursor()

    actors_table_insert = ("""
        INSERT INTO actors
        (id, login, display_login, gravatar_id, url, avatar_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """)

    repo_table_insert = ("""
        INSERT INTO repo
        (id, name, url)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """)

    payload_push_table_insert = ("""
        INSERT INTO payload_push 
        (id, size, ref, head, before)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """)

    commits_table_insert = ("""
        INSERT INTO commits
        (commits_sha, author_email, author_name, message, url, payload_push_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (commits_sha) DO NOTHING;
    """)

    org_table_insert = ("""
        INSERT INTO org 
        (id, login, gravatar_id, url, avatar_url)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """)

    ti = context["ti"]

    # Get list of files from filepath
    all_files = ti.xcom_pull(task_ids="get_files", key="return_value")
    # all_files = get_files(filepath)

    for datafile in all_files:
        with open(datafile, "r") as f:
            data = json.loads(f.read())
            for each in data:

                insert_actors_val = (
                    each["actor"]["id"], 
                    each["actor"]["login"],
                    each["actor"]["display_login"],
                    each["actor"]["gravatar_id"],
                    each["actor"]["url"],
                    each["actor"]["avatar_url"]
                    )

                insert_repo_val = (
                    each["repo"]["id"], 
                    each["repo"]["name"],
                    each["repo"]["url"]
                    )

                cur.execute(actors_table_insert, insert_actors_val)
                cur.execute(repo_table_insert, insert_repo_val)

                insert_event_val = (
                    each["id"],
                    each["type"],
                    each["actor"]["id"],
                    each["repo"]["id"],
                    each.get("payload").get("action"),
                    each["public"],
                    each["created_at"]
                )

                insert_events = f"""
                    INSERT INTO events (
                        id,
                        type,
                        actor_id,
                        repo_id,
                        payload_action,
                        public,
                        create_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)

                    ON CONFLICT (id) DO NOTHING
                """   
                cur.execute(insert_events, insert_event_val)
                conn.commit() 

                if each.get("payload").get("push_id") != None:                
                    insert_payload_push_val = ( 
                        each["payload"].get("push_id"),                    
                        each["payload"].get("size", None),
                        each["payload"].get("ref", None),
                        each["payload"].get("head", None),
                        each["payload"].get("before", None),
                    )
                    cur.execute(payload_push_table_insert, insert_payload_push_val)

                    update_events1 = f"""
                        UPDATE events
                        SET payload_action = 'pushed',
                            payload_push_id = {each["payload"]["push_id"]}
                        WHERE id = {each["id"]}
                    """   
                    cur.execute(update_events1)
                    conn.commit() 

                    for val in each["payload"]["commits"]:
                        insert_commits_val = (
                            val["sha"],
                            val["author"]["email"],
                            val["author"]["name"],
                            val["message"],
                            val["url"],
                            each["payload"]["push_id"]
                        )
                        cur.execute(commits_table_insert, insert_commits_val)
                        conn.commit() 

                if each.get("org") != None:                                                                           
                    insert_org_val = (
                        each.get("org").get("id"),                        
                        each.get("org").get("login"),
                        each.get("org").get("gravatar_id"),
                        each.get("org").get("url"),
                        each.get("org").get("avatar_url")
                        )    
                    
                    cur.execute(org_table_insert, insert_org_val)

                    update_events2 = f"""
                        UPDATE events
                        SET org_id = {each["org"]["id"]}
                        WHERE id = {each["id"]}
                    """   

                    cur.execute(update_events2)
                    conn.commit()   



with DAG(
    dag_id="etl",
    start_date=timezone.datetime(2024, 4, 22),
    schedule="@daily",
    tags=["DS525"],
) as dags:
    
    start = EmptyOperator(task_id="start")

    get_files = PythonOperator(
        task_id="get_files",
        python_callable=_get_files,
        op_kwargs={
            "filepath": "/opt/airflow/dags/data",
        }
    )
    
    create_tables = PythonOperator(
        task_id="create_table",
        python_callable=_create_tables,
    )

    process = PythonOperator(
        task_id="process",
        python_callable=_process,
    )

    end = EmptyOperator(task_id="end")
    
    start >> [get_files, create_tables] >> process >> end
