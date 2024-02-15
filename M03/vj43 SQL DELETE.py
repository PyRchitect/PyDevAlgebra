import sqlite3
import sys

delete_everything_query = '''DELETE FROM Employees'''

dbname = 'TvrtkaDB.db'
filepath = sys.path[0] + '\\' + dbname

try:
	sc = sqlite3.connect(filepath)
	cursor = sc.cursor()

	cursor.execute(delete_everything_query)
	
	sc.commit()

	cursor.close()
	print("Cursor otpusten.")

except sqlite3.Error as e:
	print(f"Dogodila se greska {e}")

finally:
	if sc:
		sc.close()
		print("Zatvorena konekcija na bazu")