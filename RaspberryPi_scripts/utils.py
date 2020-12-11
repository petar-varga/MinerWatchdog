# utils.py
from flask_mysqldb import MySQLdb
from datetime import datetime, timedelta
from dbconnection import db

import os

def db_write(query, params):
    cursor = db.connection.cursor()
    try:
        cursor.execute(query, params)
        db.connection.commit()
        cursor.close()

        return True

    except:
        cursor.close()
        return False

def db_write_executemany(query, params):
    cursor = db.connection.cursor()
    try:
        cursor.executemany(query, params)
        db.connection.commit()
        cursor.close()

        return True

    except:
        cursor.close()
        return False

def db_insert_id(query, params):
    cursor = db.connection.cursor()
    try:
        cursor.execute(query, params)
        db.connection.commit()
        cursor.close()

        id = cursor.lastrowid
        return id

    except:
        cursor.close()
        return None

def db_read(query, params=None):
    cursor = db.connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    entries = cursor.fetchall()
    cursor.close()

    content = []

    for entry in entries:
        content.append(entry)

    return content
