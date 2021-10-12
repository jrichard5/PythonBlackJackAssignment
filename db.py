#/usr/bin/env python3

import sqlite3
from contextlib import closing

SQ_FILE = "datamanager.db"

def readLastStopMoney():
    conn = sqlite3.connect(SQ_FILE)
    with closing(conn.cursor()) as cur:
        query = '''SELECT stopMoney FROM Session
                WHERE sessionID = (SELECT MAX(sessionID) from Session)'''
        cur.execute(query)
        data = cur.fetchone()
        if (data != None):
            conn.row_factory = sqlite3.Row
            money = data[0]
        else:
            money = 0

        return money

def writeSession(startTime, startMoney, addedMoney, stopTime, stopMoney):
    conn = sqlite3.connect(SQ_FILE)
    with closing(conn.cursor()) as cur:
        query = ''' INSERT INTO Session
                    (startTime, startMoney, addedMoney, stopTime, stopMoney)
                    VALUES
                    (?, ?, ?, ?, ?)'''
        cur.execute(query, (startTime, startMoney, addedMoney, stopTime, stopMoney))
        conn.commit()



