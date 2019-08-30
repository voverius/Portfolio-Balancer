import sqlite3
from Constants.constants import *


def InitializeDB():
    with sqlite3.connect(DATABASE_DIR) as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS History (date INTEGER,'
                       ' coin varchar(20), high FLOAT, low FLOAT,'
                       ' open FLOAT, close FLOAT, volume FLOAT, '
                       ' quoteVolume FLOAT, weightedAverage FLOAT,'
                       'PRIMARY KEY (date, coin));')
        connection.commit()


if __name__ == "__main__":
    InitializeDB()
