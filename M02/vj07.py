def ispisi_brojeve(start,end,step):
	[print(x,end=' ') for x in range(start,end,step)]

def assign_value(msg,default):
	try:
		value = int(input(msg))
	except ValueError:
		value = default
	return value

def main_brojevi():
	inputs = {
		'start':["> pocetna vrijednost: ",0],
		'end':["> zavrsna vrijednost: ",1],
		'step':["> korak: ",1],
		}
	outputs = []

	try:
		for key in inputs:
			outputs.append(assign_value(*inputs[key]))
	except:
		print("Greška!")
	else:
		ispisi_brojeve(*outputs)

main_brojevi()