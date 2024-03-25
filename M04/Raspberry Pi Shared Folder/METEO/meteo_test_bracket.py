# from sys import path as sys_path
# from requests import get as rget
# import xml.etree.ElementTree as ET

# url = 'https://vrijeme.hr/hrvatska_n.xml'

# root = ET.fromstring(rget(url).text)
# for grad in root.findall("Grad"):
# 	if grad.find("GradIme").text == "Zagreb-Maksimir":
# 		podaci = grad.find("Podatci")
# 		t = podaci.find("Temp").text
# 		h = podaci.find("Vlaga").text
# 		p = podaci.find("Tlak").text
# 		print(t,h,p)

# res = rget(url)
# with open(sys_path[0]+'\\'+'feed.xml','wb') as f:
# 	f.write(res.content)

# tree = ET.parse(sys_path[0]+'\\'+'feed.xml')
# root = tree.getroot()
# print(root)



unos_ugoda_bracket = [0,12,22]
temp = [-1,0,1,11,12,13,21,22,23]

for t in temp:
	unos_ugoda = 0
	for x in unos_ugoda_bracket:
		if t > x:
			unos_ugoda += 1
	print(f"> temp: {t}, ugoda: {unos_ugoda}")