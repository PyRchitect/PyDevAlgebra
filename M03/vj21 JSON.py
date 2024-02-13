import sys
import json

filename = 'user_p01.json'
filepath = sys.path[0]+'\\'+filename

def read_json_01():
	try:
		with open(filepath,'r') as fr:
			tekst_json = fr.read()
	except Exception as e:
		print(f"Dogodila se greska {e}")
	
	print(f"data type: {type(tekst_json)}")
	print("\nUSER:")
	print(tekst_json)

def read_json_02():
	try:
		with open(filepath,'r') as fr:
			dict_json = json.loads(fr.read())
	except Exception as e:
		print(f"Dogodila se greska {e}")
	
	print(f"data type: {type(dict_json)}")
	print("\nUSER:")
	print(dict_json)
	# print("\nUSER > COMPANY:")
	# print(dict_json['company'])
	# print("\nUSER > COMPANY > NAME:")
	# print(dict_json['company']['name'])

def read_json_03():
	try:
		with open(filepath,'r') as fr:
			dict_json = json.load(fr)
	except Exception as e:
		print(f"Dogodila se greska {e}")
	
	print("\nUSER:")
	for k,v in dict_json.items():
		print(f"{k} => {v}")
		try:
			#print("\nUSER > SUB:")
			for k2,v2 in v.items():
				print(f"> {k2} => {v2}")
		except Exception as e:
			pass

# read_json_01()
# read_json_02()
read_json_03()