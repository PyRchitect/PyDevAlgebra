from enum import Enum
from os import system
from time import sleep

class Constants(Enum):
	DISK_DOT = "X"
	DISK_NOT = "-"
	SPACING = 4
	SLEEP_TIME = 1

class tower_disk():
	def __init__(self,half_length,half_width):
		self.width = half_width*2
		self.image = Constants.DISK_DOT.value*(half_length*2)

	def __str__(self):
		return f"{self.image:{Constants.DISK_NOT.value}^{self.width}}"

class tower_stack():
	def __init__(self,name,h=0,th=0):
		self.name = name
		self.total_height = th
		self.height = h
		if h == 0:
			self.disks = []
		else:
			self.disks = [tower_disk(x,h) for x in range(1,h+1)]

	def pop(self):
		disk = self.disks.pop(0)
		return disk

	def push(self,new_disk):
		self.disks.insert(0,new_disk)

	def render(self):
		image = []
		image.append(f"{self.name}{'.'*(self.total_height*2-1)}")
		for x in range(self.total_height - len(self.disks)):
			# empty rows
			image.append(Constants.DISK_NOT.value*self.total_height*2)
		for x in self.disks:
			# rows with disks
			image.append(str(x))
		image
		return image

class board():
	def __init__(self,images):
		status = []
		col_break = [" "*Constants.SPACING.value for _ in range(len(images[0]))]
		for i in images:
			status.append(i)
			status.append(col_break)
		self.status = list(zip(*status))

	def show(self):
		for s in self.status:
			print(*s)

def hanoi(n,source:'tower_stack',aux:'tower_stack',dest:'tower_stack'):
	if n>0:
		hanoi(n-1,source,dest,aux)

		dest.push(source.pop())

		render_list = sorted((source,dest,aux),key=lambda x: x.name)
		sleep(Constants.SLEEP_TIME.value)
		system('cls')
		print("MOVE:\n")
		board([t.render() for t in render_list]).show()

		hanoi(n-1,aux,source,dest)

def game(n):
	towers = [tower_stack('A',n,n),tower_stack('B',0,n),tower_stack('C',0,n)]

	sleep(Constants.SLEEP_TIME.value)
	system('cls')
	print("START:\n")
	board([t.render() for t in towers]).show()

	hanoi(n,*towers)

def main():
	new_game = True
	while new_game == True:
		n = input("Unesi n ili [x] za izlaz: ")

		try:
			game(int(n))
		except:
			if n == 'x':
				new_game = False
			else:
				print("Pogresan unos!")

# BACKUP

# def hanoi(n,source,aux,dest):
# 	if n>0:
# 		hanoi(n-1,source,dest,aux)
# 		print(f"Move {n} from {source} to {dest}")
# 		hanoi(n-1,aux,source,dest)

# def main():
# 	towers = ('A','B','C')
# 	new_game = True
# 	while new_game == True:
# 		n = input("Unesi n ili [x] za izlaz: ")
# 		try:
# 			#hanoi(int(n),*towers)
# 			game(int(n))
# 		except:
# 			if n == 'x':
# 				new_game = False
# 			else:
# 				print("Pogresan unos!")

main()