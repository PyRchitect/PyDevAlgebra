import sqlite3
import sys

insert_table_query = '''INSERT INTO Employees (name,email)
						VALUES (?,?)'''

dbname = 'TvrtkaDB.db'
filepath = sys.path[0] + '\\' + dbname

lista_radnika = [
	('Mate Matic','mmatic@mail.com'),
	('Ana Anic','aanic@hotmail.com'),
	('Jure Juric','jjuric@brzi.hr')
]

try:
	sc = sqlite3.connect(filepath)
	cursor = sc.cursor()

	for radnik in lista_radnika:
		cursor.execute(insert_table_query,radnik)
	
	sc.commit()

	cursor.close()
	print("Cursor otpusten.")

except sqlite3.Error as e:
	print(f"Dogodila se greska {e}")

finally:
	if sc:
		sc.close()
		print("Zatvorena konekcija na bazu")