import sqlite3
import sys

create_table_query = '''CREATE TABLE IF NOT EXISTS Employees (
						id INTEGER PRIMARY KEY,
						name TEXT NOT NULL,
						email TEXT NOT NULL UNIQUE);'''

dbname = 'TvrtkaDB.db'
filepath = sys.path[0] + '\\' + dbname

try:
	sc = sqlite3.connect(filepath)

	cursor = sc.cursor()
	print("Spojeni smo na bazu.")

	cursor.execute(create_table_query)

	sc.commit()

	cursor.close()
	print("Cursor otpusten.")

except sqlite3.Error as e:
	print(f"Dogodila se greska {e}")

finally:
	if sc:
		sc.close()
		print("Zatvorena konekcija na bazu!")