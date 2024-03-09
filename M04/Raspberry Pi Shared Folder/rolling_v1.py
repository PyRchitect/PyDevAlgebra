from os import system
from time import sleep
from random import randint,sample
from collections import deque
from enum import Enum

class PulseStream():

	class Constants(Enum):
		BASE_MARK = "M"
		BASE_CLEAR = "X"

		ACTIVE_MARK = "O"
		ACTIVE_CLEAR = "."

		DEF_H_DENSITY = 3
		DEF_V_DENSITY = 1

		SLEEP_TIME = 0.5

	def __init__(self,
			  bandwidth,
			  view_height,
			  h_density = None,
			  v_density = None):

		self.width = bandwidth
		self.h_density = PulseStream.Constants.DEF_H_DENSITY.value or h_density
		self.v_density = PulseStream.Constants.DEF_V_DENSITY.value or v_density

		self.view = deque()
		self.height = view_height
		self.init_view()

	@staticmethod
	def clear_perimeter(vector:'list',p):
		rel = [[0,1],[-1,0,1],[-1,0]]

		if p > 0 and p < len(vector)-1:				
			d = rel[1]
		elif p == 0:
			d = rel[0]
		elif p == len(vector)-1:
			d = rel[2]

		for x in d:
			vector[p+x] = PulseStream.Constants.BASE_MARK.value
		return vector

	def generate_pulse(self,
		object_generator=lambda :PulseStream.Constants.ACTIVE_MARK.value):

		band_base = [PulseStream.Constants.BASE_CLEAR.value]*self.width
		band_active = [PulseStream.Constants.ACTIVE_CLEAR.value]*self.width

		for _ in range(randint(1,self.h_density)):

			band_available=[]
			for i,x in enumerate(band_base):
				if x == PulseStream.Constants.BASE_CLEAR.value:
					band_available.append(i)
			if not band_available: break
			position = sample(band_available,k=1)[0]

			band_active[position] = object_generator()

			band_base = PulseStream.clear_perimeter(band_base,position)
		
		return band_active

	def generate_empty(self):
		return [PulseStream.Constants.ACTIVE_CLEAR.value]*self.width

	def generate_signal(self):
		signal = []
		signal.append(self.generate_pulse())
		for _ in range(randint(1,self.v_density)):
			signal.append(self.generate_empty())
		return signal

	def init_view(self):
		for _ in range(self.height):
			self.view.append(self.generate_empty())
	
	def render_view(self):
		system('cls')
		for row in self.view:
			print(row)
	
	def update_view(self,test_height):
		self.render_view()
		for _ in range(test_height):
			for band in self.generate_signal():
				self.view.pop()
				self.view.appendleft(band)
				sleep(PulseStream.Constants.SLEEP_TIME.value)
				self.render_view()

def main():
	stream = PulseStream(8,8)
	stream.update_view(8)

main()