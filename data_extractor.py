import sys
import json
import sqlite3
import contextlib


def connect(url):
    return sqlite3.connect(url)


create_db_sql_templ = """
CREATE TABLE build (id integer primary key,
                    build text,
                    type text,
                    md5 text);

CREATE TABLE params_combination (id integer primary key, {params});

CREATE TABLE result (build_id integer,
                     params_combination integer,
                     bandwith float,
                     deviation float);
"""


PARAM_COUNT = 20


def get_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cursor.fetchall()


def drop_database(conn):
    cursor = conn.cursor()
    cursor.execute("drop table result")
    cursor.execute("drop table params_combination")
    cursor.execute("drop table build")


def init_database(conn):
    cursor = conn.cursor()

    params = ["param_{0} text".format(i) for i in range(PARAM_COUNT)]
    create_db_sql = create_db_sql_templ.format(params=",".join(params))

    for sql in create_db_sql.split(";"):
        cursor.execute(sql)


def insert_build(cursor, build_id, build_type, iso_md5):
    cursor.execute("insert into build (build, type, md5) values (?, ?, ?)",
                   (build_id, build_type, iso_md5))
    return cursor.lastrowid


def insert_params(cursor, *param_vals):
    param_vals = param_vals + ("",) * (PARAM_COUNT - len(param_vals))

    params = ",".join(['?'] * PARAM_COUNT)
    select_templ = "select id from params_combination where {params_where}"

    params_where = ["param_{0}=?".format(i) for i in range(PARAM_COUNT)]
    req = select_templ.format(params_where=" AND ".join(params_where))
    cursor.execute(req, param_vals)
    res = cursor.fetchall()
    if [] != res:
        return res[0][0]

    params = ",".join(['?'] * PARAM_COUNT)
    param_insert_templ = "insert into params_combination ({0}) values ({1})"
    param_names = ",".join("param_{0}".format(i) for i in range(PARAM_COUNT))
    req = param_insert_templ.format(param_names, params)
    cursor.execute(req, param_vals)
    return cursor.lastrowid


def insert_results(cursor, build_id, params_id, bw, dev):
    req = "insert into result values (?, ?, ?, ?)"
    cursor.execute(req, (build_id, params_id, bw, dev))


@contextlib.contextmanager
def transaction(conn):
    try:
        cursor = conn.cursor()
        yield cursor
    except:
        conn.rollback()
        raise
    else:
        conn.commit()


def json_to_db(json_data, conn):
    data = json.loads(json_data)
    with transaction(conn) as cursor:
        for build_data in data:
            build_id = insert_build(cursor,
                                    build_data.pop("build_id"),
                                    build_data.pop("type"),
                                    build_data.pop("iso_md5"))

            for params, (bw, dev) in build_data.items():
                param_id = insert_params(cursor, *params.split(" "))
                insert_results(cursor, build_id, param_id, bw, dev)


conn = sqlite3.connect(sys.argv[1])
json_data = open(sys.argv[2]).read()

if len(get_all_tables(conn)) == 0:
    init_database(conn)

json_to_db(json_data, conn)