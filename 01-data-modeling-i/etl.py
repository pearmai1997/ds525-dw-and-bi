import glob
import json
import os
from typing import List

import psycopg2

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

def get_files(filepath: str) -> List[str]:
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


def process(cur, conn, filepath):
    # Get list of files from filepath
    all_files = get_files(filepath)

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

                
def main():
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    process(cur, conn, filepath="../data")

    conn.close()


if __name__ == "__main__":
    main()