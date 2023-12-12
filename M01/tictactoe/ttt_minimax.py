# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
# A simple Python3 program to find maximum score that maximizing player can get
import math

def minimax(curDepth,nodeIndex,maxTurn,scores,targetDepth):

	# base case: targetDepth reached
	if (curDepth == targetDepth): return scores[nodeIndex]
	
	# nodeIndex je samo zbog toga što je stablo prezentirano kao lista
	# želi se reći odi rekurzivno na djecu i nađi njihov min/max

	if (maxTurn):
		return max(
			    minimax(curDepth+1,nodeIndex*2,False,scores,targetDepth), 
				minimax(curDepth+1,nodeIndex*2+1,False,scores,targetDepth)
				)
	
	else:
		return min(
			    minimax(curDepth+1,nodeIndex*2,True,scores,targetDepth), 
				minimax(curDepth+1,nodeIndex*2+1,True,scores,targetDepth)
				)
	
def main():
	scores = [3, 5, 2, 9, 12, 5, 23, 23]	
	treeDepth = math.log(len(scores), 2)
	# pretpostavlja da će scores bit len 2^n pa je dubina n
	# što je normalno za obično binarno stablo, nebitno
	print("The optimal value is : ", end = "")
	print(minimax(0, 0, True, scores, treeDepth))
