import random as rn
from abc import abstractmethod

class TreeNode():
    max_children = 0

    def __init__(self,data=None):
        self.data = data
        self.parent = None
        self.children = []

    def isRoot(self):
        return True if self.parent == None else False
    
    def fetchRoot(self):
        fetch_root = self

        if not fetch_root.isRoot():
            fetch_root = fetch_root.parent 

        return fetch_root
    
    def makeRoot(self):
        self.parent = None
    
    def isLeaf(self):
        return True if self.children == [] else False

    # TO DO: loopLeaves > nakon iter

    def parents(self):
        if self.isRoot(): return None

        parents_list = []
        current = self.parent

        while not current.isRoot(current):
            parents_list.append(current)
        
        return parents_list
    
    def hasParents(self):
        return True if not self.parents() else False

    def node_level(self):
        p = self.parents()
        return 0 if not p else len(p)
    
    def hasChildren(self):
        return True if any(self.children) else False

    def loopChildren(self):
        for child in self.children:
            yield child
    
    def firstChild(self):
        if self.isLeaf():
            return None
        else:
            return self.children[0]
    
    def isFirstChild(self):
        if self.isRoot():
            return True
        else:            
            fc = self.parent.firstChild(self.parent)
            return True if self == fc else False
    
    def lastChild(self):
        if self.isLeaf():
            return None
        else:
            return self.children[-1]
    
    def isLastChild(self):
        if self.isRoot():
            return True
        else:            
            lc = self.parent.lastChild(self.parent)
            return True if self == lc else False

    def whichChild(self):
        if self.isRoot():
            return 0
        else:            
            return self.parent.children.index(self)

    def isOnlyChild(self):
        if self.isRoot():
            return True
        else:            
            return True if len(self.parent.children) == 1 else False

    # TO DO: loopSiblings > nakon iter

    def addChild(self,child):
        if len(self.children) == TreeNode.max_children:
            raise IndexError(f"broj djece je maksimalan ({TreeNode.max_children})")
        else:
            child.parent = self
            self.children.append(child)
    
    def removeChild(self,child):
        child.parent = None
        self.children.remove(child)
    
    def removeFromParent(self):
        self.parent.removeChild(self.parent,self)
    
    def removeChildren(self):
        self.children = []
    
    # TO DO: OPERATIONS

    # TO DO: move

    # TO DO: copy

    # TO DO: find

    # TO DO: TRAVERSALS
    
    # TO DO: iter

    # TO DO: DFS

    # TO DO: BFS

    # TO DO: LFS

class BinaryTree(TreeNode):
    max_children = 2

    def left(self):
        return self.firstChild()
    
    def right(self):
        return self.lastChild()

    def sequential_traversal(self,guide,start,end,step=1):

        if start==end: return None

        mid = int((start+end)/2)

        if guide>=start and guide<=mid:
            yield (self,0)
            nextNode = self.left()            
        else:
            yield (self,1)
            nextNode = self.right()

        yield from nextNode.sequential_traversal(nextNode,guide,start,mid,step+1)

    def populate_tree(self):
        raise NotImplementedError('svaka podklasa mora definirati vlastiti način')

class ProbabilityBinaryTree(BinaryTree):

    def populate_tree(self,input_method,tree_depth,traversal_method):

        input_random = lambda : rn.random()

        input_user = lambda : input(f" unesi vrijednost: ")       

        def input_file():
            import sys
            filepath=sys.path[0]+'\\'+'data.txt'            
            with open(filepath) as myfile:
                for line in myfile:
                    yield float(line)

        input_method_options = {0:input_random,1:input_user,2:input_file}

        current = self

        max = pow(2,tree_depth)
        
        for x in range(max):
            for (current,next_move) in traversal_method(current,x,1,max):
                # check next move (0 = left, 1 = right):
                # if no children:
                # # if next move 0 > add child
                # if one child:
                # # if next move 0 > move on
                # # if next move 1 > add child
                # if two children:
                # # if next move 0 > move on
                # # if next move 1 > move on
                if len(current.children) <= (next_move):
                    current.addChild(TreeNode())
                    # add child with empty data

                    if len(current.children)==1:                        
                        node_data = input_method_options[input_method]
                        # if first child added, populate with random probability
                    else:
                        node_data = 1 - current.firstChild.data
                        # if second child, take 1 minus first child probability
                    current.lastChild.data = node_data




def main():

    pbt = ProbabilityBinaryTree(1)
    # inicijaliziraj root s data = 1 (vjerojatnost = 1)

    pbt.populate_tree('random_input',3,pbt.sequential_traversal)
    # napuni stablo s random vjerojatnostima




def pogodi_broj(broj,start, end,korak=1,sirina=0):

    if start==end: return start

    print(f"{korak:0>{2}}. korak",end=" ")
    poloviste = int((start+end)/2)
    
    if broj in list(range(start,poloviste+1)):             
        print(f"> broj je u 1. bucketu :: start: {start:0>{sirina}}, end: {poloviste:0>{sirina}}")
        return pogodi_broj(broj,start,poloviste,korak+1,sirina)
    else:        
        print(f"> broj je u 2. bucketu :: start: {poloviste:0>{sirina}}, end: {end:0>{sirina}}")
        return pogodi_broj(broj,poloviste+1,end,korak+1,sirina)
            
def main():
    
    test_start = 1
    test_end = 1024
    broj = rn.randint(test_start,test_end)

    result = pogodi_broj(broj,test_start,test_end,sirina=len(str(test_end)))

    print(f"\nodgovor: {result}, zadano: {broj}")

main()