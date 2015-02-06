__author__ = 'ZH'

import sqlite3

def main():
    conntion = sqlite3.connect('../../db.sqlite3')
    cursor = conntion.cursor()


if __name__ == '__main__':
    main()