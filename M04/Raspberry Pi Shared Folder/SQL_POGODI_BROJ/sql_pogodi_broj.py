import sqlite3
import random
import datetime as dt

table_score = '''
CREATE TABLE IF NOT EXISTS Score (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
points INTEGER,
date TEXT);
'''

enter_score = '''
INSERT INTO Score (
name, points, date
) VALUES (
?,?,?)
'''

show_score = '''
SELECT * FROM Score
'''

show_score_above_10_points = '''
SELECT name, points FROM Score WHERE points>10
'''

database_name="GameY.db"

def create_db():
	try:
		sc=sqlite3.connect(database_name)
		cursor = sc.cursor()
		cursor.execute(table_score)
		sc.commit()
		cursor.close()
	except sqlite3.Error as e:
		print("Dogodila se greska. ",e)
	finally:
		if sc:
			sc.close()

def enter_result(user,score,sdate):
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

def read_top_player():
	try:
		sc=sqlite3.connect(database_name)
		cursor = sc.cursor()
		cursor.execute(show_score)
		records = cursor.fetchall()
		attempts = 100
		for record in records:
			if record[2]<attempts:
				attempts=record[2]
				best_user=record[1]
		print(f"Najbolji igrac je {best_user}")
	except sqlite3.Error as e:
		print("Dogodila se greska. ",e)
	finally:
		if sc:
			sc.close()

def read_top_3_players():
	try:
		sc=sqlite3.connect(database_name)
		cursor = sc.cursor()
		cursor.execute(''' SELECT TOP 3 * FROM Score ORDER BY points''')
		records = cursor.fetchall()
		print("Najbolja 3 igrača:")
		for record in records:
			print(f"{record[1]}: {record[2]} bodova")
	except sqlite3.Error as e:
		print("Dogodila se greska. ",e)
	finally:
		if sc:
			sc.close()

def read_top_3_players_db():
	try:
		sc=sqlite3.connect(database_name)
		cursor = sc.cursor()
		cursor.execute(show_score)
		records = cursor.fetchall()
		print("Najbolja 3 igrača:")
		for record in sorted(records,key=lambda x: x[2])[:3]:			
			print(f"{record[1]}: {record[2]} bodova")
	except sqlite3.Error as e:
		print("Dogodila se greska. ",e)
	finally:
		if sc:
			sc.close()

def read_scoreboard():
	try:
		sc=sqlite3.connect(database_name)
		cursor = sc.cursor()
		cursor.execute(show_score)
		records = cursor.fetchall()
		for record in records:
			print(f'{record[1]}: {record[2]} bodova - dana {record[3][-2:]}.{record[3][5:7]}.{record[3][:4]}')
		cursor.close()
	except sqlite3.Error as e:
		print("Dogodila se greska. ",e)
	finally:
		if sc:
			sc.close()

create_db()
# enter_result('Jure',40,'20240323')
# read_scoreboard()

nf=1
nt=5

def return_date_string():
	return dt.date.today()

def generate_number(nf,nt):
	return random.randint(nf,nt)

def check_number(gn,en):
	return gn==en

def input_number(nf,nt):
	return int(input(f"Unesite broj od {nf} do {nt}: "))

print(return_date_string())
entered_number=input_number(nf,nt)
generated_number=generate_number(nf,nt)
attempt=1

while True:
	if check_number(generated_number,entered_number):
		print(f"Pogodili ste broj {entered_number} iz {attempt}. pokusaja")
		user_name=input("Unesite svoje ime: ")
		score_date = return_date_string()
		enter_result(user_name,attempt,score_date)
		break
	else:
		entered_number=input_number(nf,nt)
		attempt+=1
		continue

read_scoreboard()
print()
read_top_player()
read_top_3_players()
read_top_3_players_db()