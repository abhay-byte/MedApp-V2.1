import sqlite3

conn = sqlite3.connect('MedApp_database.db')

conn.execute('''CREATE TABLE PATIENTS
         (ID TEXT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE_GENDER            TEXT     NOT NULL,
         MODEL_FEATURES        CHAR(50),
         GR         TEXT,
         MR         TEXT,
         BR         TEXT);''')






