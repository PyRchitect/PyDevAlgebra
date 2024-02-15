import sqlite3
import sys

update_table_query = '''UPDATE Employees
						SET name=?,email=?
						WHERE id=?'''

dbname = 'TvrtkaDB.db'
filepath = sys.path[0] + '\\' + dbname

try:
	sc = sqlite3.connect(filepath)
	cursor = sc.cursor()

	cursor.execute(update_table_query,('Ana Anic Matic','aanic@hotmail.com',2,))
	
	sc.commit()

	cursor.close()
	print("Cursor otpusten.")

except sqlite3.Error as e:
	print(f"Dogodila se greska {e}")

finally:
	if sc:
		sc.close()
		print("Zatvorena konekcija na bazu")