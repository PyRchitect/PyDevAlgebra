def report(L):
	if not L:
		raise ValueError("nijedna ocjena nije upisana!")
	else:
		return (min(L),max(L),sum(L)/len(L))

def main():
	ocjene = [5,3,2,5,3,3,1,2,4,2,5]
	print(f"ocjene: {ocjene}")
	labels = ["> min: ","> max: ","> avg: "]

	try:
		result = report(ocjene)		
		[print(l,f"{r:.2f}") for (l,r) in zip(labels,result)]
	except ValueError as VE:
		print(VE)

main()