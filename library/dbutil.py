#!/usr/bin/python3

# Author: Nilesh Ghule <nilesh@sunbeaminfo.com>
# library -> dbutil.py
# Date: 8/11/19

from config import dbcfg
import mysql.connector

def exec_dql_query(sql, params=tuple()):
    con = None
    cursor = None
    result = []
    try:
        con = mysql.connector.connect(user=dbcfg['user'], password=dbcfg['passwd'], host=dbcfg['host'], database=dbcfg['db'])
        cursor = con.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
    except Exception as e:
        print("sql query execution failed.")
        print(e)
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()
    return result


def exec_dml_query(sql, params=tuple()):
    con = None
    cursor = None
    result = 0
    try:
        con = mysql.connector.connect(user=dbcfg['user'], password=dbcfg['passwd'], host=dbcfg['host'], database=dbcfg['db'])
        cursor = con.cursor()
        cursor.execute(sql, params)
        con.commit()
        result = cursor.rowcount
    except Exception as e:
        print("sql query execution failed.")
        print(e)
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()
    return result
