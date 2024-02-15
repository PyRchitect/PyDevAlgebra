import sqlite3
import sys

select_query = "SELECT sqlite_version();"

dbname = 'SQLite_Python.db'
filepath = sys.path[0] + '\\' + dbname

try:
	sqliteConnection = sqlite3.connect(filepath)

	cursor = sqliteConnection.cursor()
	print("Spojeni smo na bazu")

	cursor.execute(select_query)

	records = cursor.fetchall()

	print('SQLite verzija',records)

	cursor.close()
	print("Cursor otpusten.")

except sqlite3.Error as e:
	print(f"Dogodila se greska {e}")

finally:
	if sqliteConnection:
		sqliteConnection.close()
		print("Zatvorena konekcija na bazu!")