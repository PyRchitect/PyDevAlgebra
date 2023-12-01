import random as rn

class Tree():
    max_children = 0

    def __init__(self,data):
        self.data = data
        self.parent = None
        self.children = []

    def isRoot(self):
        return True if self.parent == None else False
    
    def fetchRoot(self):
        fetch_root = self

        if not fetch_root.isRoot(self):
            fetch_root = fetch_root.parent 

        return fetch_root
    
    def makeRoot(self):
        self.parent = None
    
    def isLeaf(self):
        return True if self.children == [] else False

    # TO DO: loopLeaves > nakon iter

    def parents(self):
        if self.isRoot(self): return None

        parents_list = []
        current = self.parent

        while not current.isRoot(current):
            parents_list.append(current)
        
        return parents_list
    
    def hasParents(self):
        return True if not self.parents(self) else False

    def node_level(self):
        p = self.parents(self)
        return 0 if not p else len(p)
    
    def hasChildren(self):
        return True if any(self.children) else False

    def loopChildren(self):
        for child in self.children:
            yield child
    
    def firstChild(self):
        if self.isLeaf(self):
            return None
        else:
            return self.children[0]
    
    def isFirstChild(self):
        if self.isRoot(self):
            return True
        else:            
            fc = self.parent.firstChild(self.parent)
            return True if self == fc else False
    
    def lastChild(self):
        if self.isLeaf(self):
            return None
        else:
            return self.children[-1]
    
    def isLastChild(self):
        if self.isRoot(self):
            return True
        else:            
            lc = self.parent.lastChild(self.parent)
            return True if self == lc else False

    def whichChild(self):
        if self.isRoot(self):
            return 0
        else:            
            return self.parent.children.index(self)

    def isOnlyChild(self):
        if self.isRoot(self):
            return True
        else:            
            return True if len(self.parent.children) == 1 else False

    # TO DO: loopSiblings > nakon iter

    def addChild(self,child):
        if len(self.children) == Tree.max_children:
            return None
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





class BinaryTree(Tree):
    max_children = 2




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