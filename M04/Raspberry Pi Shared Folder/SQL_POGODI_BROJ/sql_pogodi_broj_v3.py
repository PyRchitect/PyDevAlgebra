import sqlite3
import random
import datetime as dt
 
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
            print(f'{record[1]}: {record[2]} pokušaj(a) - dana {record[3][-2:]}.{record[3][5:7]}.{record[3][0:4]}.')
        cursor.close()
    except sqlite3.Error as e:
        print("Dogodila se greska. ",e)
    finally:
        if sc:
            sc.close()
 
def read_top_player():
    try:
        sc=sqlite3.connect(database_name)
        cursor=sc.cursor()
        cursor.execute(show_score)
        records=cursor.fetchall()
        attempts=100
        for record in records:
            #print(record)
            if record[2]<attempts:
                attempts=record[2]
                user=record[1]
        print(f'Najbolji igrač je {user}')
            #print(f'{record[1]}: {record[2]} pokušaj(a) - dana {record[3][-2:]}.{record[3][5:7]}.{record[3][0:4]}.')
        cursor.close()
    except sqlite3.Error as e:
        print("Dogodila se greska. ",e)
    finally:
        if sc:
            sc.close()
 
def generate_number(numberFrom=1,numberTo=20):
    return random.randint(numberFrom,numberTo)
 
 
def check_number(generated, entered):
    if generated==entered:
        return True
    return False
 
def input_number(numberFrom=1,numberTo=20):
    while(True):
        print(f'Unesite broj od {numberFrom} do {numberTo}')
        broj=input()
        try:
            broj=int(broj)
            if broj<numberFrom or broj>numberTo:
                continue
            break
        except:
            continue
    return broj
 
def return_date_string():
    current_date=dt.date.today()
    return current_date
 
print(return_date_string())
 
nf=1 #pocetni broj
nt=5#krajnji broj
 
entered_number=input_number(nf,nt)
generated_number=generate_number(nf,nt)
attempt=1
while True:
    if check_number(generated_number, entered_number):
        print(f'Pogodili ste broj {entered_number} iz {attempt}. pokušaja')
        user_name=input("Unesite svoje ime: ")
        score_date=return_date_string()
        enter_result(user_name, attempt, score_date)
        break
    else:
        entered_number=input_number(nf,nt)
        attempt+=1
        continue
 
#if check_number(generated_number, entered_number):
#    print(f'Pogodili ste broj {entered_number}')
#else:
#    print(f'Niste pogodili broj {generated_number}')
 
 
#enter_result('Jure', 40, '20240323')
read_scoreboard()
print()
read_top_player()