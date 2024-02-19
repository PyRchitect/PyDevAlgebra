import sys
import json

user = {
	"id"			: 1,
	"firstName"		: "Petar",
	"lastName"		: "Peric",
	"username"		: "pperic",
	"email"			: "pperic@nekafirma.hr",
	"address"		: {
		"street"	: "Ilica 256",
		"city"		: "Zagreb",
		"zipcode"	: "10000"
	},
	"phone"			: "+38512345678",
	"website"		: "www.nekafirma.hr",
	"company"		: {
		"name"		: "Neka Firma",
		"catchPhrase"	: "Prava firma za prave pitone",
		"bs"		: "Najbolja poslovna rjesenja"
	}
}

def write_json_01():
	filename = 'user_p01.json'
	filepath = sys.path[0]+'\\'+filename

	try:
		with open(filepath,'w') as fw:
			json.dump(user,fw)
	except Exception as e:
		print(f"Dogodila se greska {e}")

def write_json_02():
	filename = 'user_p02.json'
	filepath = sys.path[0]+'\\'+filename

	try:
		with open(filepath,'w') as fw:
			json.dump(user,fw,indent=4)
	except Exception as e:
		print(f"Dogodila se greska {e}")

# write_json_01()
# write_json_02()

