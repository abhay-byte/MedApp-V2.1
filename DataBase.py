
import sqlite3

conn = sqlite3.connect('MedApp_database.db')

conn.execute('''CREATE TABLE PATIENTS
         (ID TEXT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            VARCHAR(4)     NOT NULL,
         GENDER         VARCHAR(8),
         MODEL_FEATURES        CHAR(50),
         GR         TEXT,
         MR         TEXT,
         BR         TEXT);''')

