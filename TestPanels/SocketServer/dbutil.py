import sqlite3
import sys

connection = sqlite3.connect('..\\djangoweb\\db.sqlite3')


def select(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result


def execute(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close()