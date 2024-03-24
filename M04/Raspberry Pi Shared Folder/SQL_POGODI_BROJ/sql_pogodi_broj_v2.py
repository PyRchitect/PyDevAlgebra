import sqlite3
 
table_score='''CREATE TABLE IF NOT EXISTS Score (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            points INTEGER,
            date TEXT);'''
 
enter_score='''INSERT INTO Score (name, points, date)
            VALUES (?, ?, ?)'''
 
show_score='SELECT * FROM Score'
 
show_score_above_10_points='SELECT name, points FROM Score WHERE points>10'
 
database_name='GameX.db'
 
def create_db():
    try:
        sc=sqlite3.connect(database_name)
        cursor=sc.cursor()
        cursor.execute(table_score)
        sc.commit()
        cursor.close()
    except sqlite3.Error as e:
        print("Dogodila se greska. ",e)
    finally:
        if sc:
            sc.close()
 
 
def enter_result(user, score, sdate):
    try:
        sc=sqlite3.connect(database_name)
        cursor=sc.cursor()
        cursor.execute(enter_score,(user,score,sdate))
        sc.commit()
        cursor.close()
    except sqlite3.Error as e:
        print("Dogodila se greska. ",e)
    finally:
        if sc:
            sc.close()
 
def read_scoreboard():
    try:
        sc=sqlite3.connect(database_name)
        cursor=sc.cursor()
        cursor.execute(show_score)
        records=cursor.fetchall()
        for record in records:
            #print(record)
            print(f'{record[1]}: {record[2]} bodova - dana {record[3][-2:]}.{record[3][4:6]}.{record[3][0:4]}.')
        cursor.close()
    except sqlite3.Error as e:
        print("Dogodila se greska. ",e)
    finally:
        if sc:
            sc.close()
 
enter_result('Jure', 40, '20240323')
read_scoreboard()