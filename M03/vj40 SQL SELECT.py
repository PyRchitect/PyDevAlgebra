import sqlite3
import sys

select_table_query = '''SELECT * FROM Employees WHERE id=?'''

dbname = 'TvrtkaDB.db'
filepath = sys.path[0] + '\\' + dbname

try:
	sc = sqlite3.connect(filepath)
	cursor = sc.cursor()
	cursor.execute(select_table_query,(2,))
	records = cursor.fetchall()

	for record in records:
		print(record)

	cursor.close()
except sqlite3.Error as e:
	print(f"Dogodila se greska {e}")

finally:
	if sc:
		sc.close()