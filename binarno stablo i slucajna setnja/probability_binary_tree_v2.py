import random as rn
import sys

rounding = 4
test_trial_probability = 0.4

# Tree Class

class TreeNode():
    max_children = 0

    def __init__(self,data=None):
        self.data = data
        self.parent = None
        self.children = []
        self.trajectory = []
    
        self.walk_methods = {}
        # FROM HERE: expand to DFS, BFS, LS, ...

    def isRoot(self):
        return True if self.parent == None else False
    
    def makeRoot(self):
        self.parent = None
    
    def fetchRoot(self):
        fetch_root = self
        while not fetch_root.isRoot(): fetch_root = fetch_root.parent
        return fetch_root
    
    def isLeaf(self):
        return True if self.children == [] else False

    # TO DO: loopLeaves > nakon iter
    
    def hasParents(self):
        return True if not self.parents() else False

    def parents(self):
        if self.isRoot(): return None

        parents_list = []
        current = self.parent
        while True:
            parents_list.append(current)
            if current.isRoot(): break
            current = self.parent
        
        return parents_list

    def node_level(self):
        return 0 if not self.parents() else len(self.parents())
    
    def hasChildren(self):
        return True if any(self.children) else False

    def loopChildren(self):
        for child in self.children: yield child
    
    def firstChild(self):
        return None if self.isLeaf() else self.children[0]
    
    def isFirstChild(self):
        return True if (self.isRoot() or self == self.parent.firstChild()) else False

    def lastChild(self):
        return None if self.isLeaf() else self.children[-1]
    
    def isLastChild(self):
        return True if (self.isRoot() or self == self.parent.lastChild()) else False

    def whichChild(self):
        return 0 if self.isRoot() else self.parent.children.index(self)

    def isOnlyChild(self):
        return True if (self.isRoot() or len(self.parent.children) == 1) else False

    # TO DO: loopSiblings > nakon iter

    def addChild(self,child):
        if len(self.children) == self.max_children:
            raise IndexError(f"greska: broj djece je vec maksimalan ({self.max_children})")
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

    # TO DO: SEARCHES 
    # TO DO: iter
    # TO DO: DFS
    # TO DO: BFS
    # TO DO: LS

    def input_methods(self,assign_type):
        # (0, zadana vrijednost)
        # (1, random funkcija)
        # (2, type funkcija)
        # (3, source filepath)

        # INPUT METHODS (random, input, file):

        # 0. fixed assignment, receive parameter
        if assign_type[0] == 0: return lambda : assign_type[1]

        # 1. simple random assignment, float with n decimal places
        if assign_type[0] == 1: return lambda : round(assign_type[1](),rounding)

        # 2. expects user input
        if assign_type[0] == 2: return lambda : assign_type[1](input(f"unesi vrijednost: "))

        # 3. expects input from file
        if assign_type[0] == 3: return lambda : [line.rstrip() for line in open(assign_type[1])]
        
        return (NotImplementedError, "ne postoji tip unošenja")
        # FROM HERE: expand to download from service, from SQL DB, from XL, ...

    def assign_action(self):
        return (NotImplementedError, "svaka potklasa definira svoj assignment")

    def assign_to_node(self, assign_type, assign_mode, node_data):
        self.addChild(self.__class__())

        if assign_mode != 0:
            # if fixed, already set beforehand / if dynamic, set for this node
            node_data = self.assign_action(self,assign_type,node_data)
        
        return node_data


    def populate_tree(self,assign_input,assign_mode,tree_depth,search_method):        

        # ASSIGNMENT MODE (0 = fixed, 1 = dynamic):
        if assign_mode == 0:
            # 0. fixed > set value for all beforehand
            node_data = self.input_methods(assign_input)()
        else:
            # 1. dynamic > require input for each node
            node_data = None

        # SEARCH METHODS (custom for each type)
        if len(self.walk_methods) == 0:
            raise (NotImplementedError, "metode pretraživanja nisu definirane")
        
        start_node = self
        # just in case:
        start_node.makeRoot()
        start_node.children = []

        self.walk_methods[search_method](
            start_node, tree_depth, 'assign', assign_input, (assign_mode,node_data))



# Binary Tree Class

class BinaryTreeNode(TreeNode):
    max_children = 2

    def __init__(self,data=None):
        TreeNode.__init__(self,data)

        self.walk_methods =   {
                                    0:BinaryTreeNode.sequential_walk
                                }

    def left(self): return self.firstChild()

    def right(self): return self.lastChild()

    @staticmethod
    def sequential_search(node,guide,start,end,step=1):

        if start==end: return StopIteration # test - zadnji krug?
        #if start==end: return 0

        mid = int((start+end)/2)

        if guide>=start and guide<=mid:
            yield (node,0)
            yield from BinaryTreeNode.sequential_search(node.left(),guide,start,mid,step+1)
        else:
            yield (node,1)
            yield from BinaryTreeNode.sequential_search(node.right(),guide,mid+1,end,step+1)

    def sequential_walk(start_node,tree_depth,op,op_type,op_mode):
        # operation = type of operation (assign, read, delete, ...)
        # operation_type = input handling (fixed, rnd, input, file, ...)
        # operation_mode = (mode, value)
        # > mode = fixed (set beforehand) / dynamic (per node)
        # > value = node_value if fixed, else None

        for x in list(range(1,pow(2,tree_depth)+1)):
            for (current,next_move) in BinaryTreeNode.sequential_search(start_node,x,1,pow(2,tree_depth)):
                if len(current.children) <= (next_move):
                    
                    # DALJE OVISI O TIPU OP:

                    if op == 'assign':
                        node_data = start_node.assign_to_node(op_type,*op_mode)
                        current.lastChild().data = node_data
                        current.lastChild().trajectory = current.trajectory+[next_move]

    @staticmethod
    def printBinaryTree(node,level=0):
        if node != None:
            BinaryTreeNode.printBinaryTree(node.left(),level+1)
            print(f"{' '*8 * level} -> {node.data:.{rounding}f}, {node.trajectory}")
            BinaryTreeNode.printBinaryTree(node.right(),level+1)

# Probability Binary Tree Class        

class PBinaryTreeNode(BinaryTreeNode):

    def assign_action(self,assign_type,node_data):
        if self.children[0].isOnlyChild():
            # if first child added, populate with chosen method
            node_data = self.input_methods(assign_type)[1]()
        else:
            # if second child added, take 1 minus first child
            node_data = 1 - self.firstChild().data

        return node_data

    def calculate_trajectories(root_node,tree_depth,chosen_trajectories=None):

        search_args = (1,pow(2,tree_depth))     # true range for guide
        range_args = (1,pow(2,tree_depth)+1)    # ! range needs +1 (last)

        checklist = chosen_trajectories or list(range(*range_args))

        calculated_trajectories=[[],[]]

        for x in checklist:
            product = 1
            sum = 0

            for (current,next_move) in BinaryTreeNode.sequential_search(root_node,x,*search_args):
                if next_move == 0:
                    product *= current.left().data
                else:
                    product *= current.right().data
                sum+=next_move

            calculated_trajectories[0].append(product)
            calculated_trajectories[1].append(sum)
        
        return calculated_trajectories



# MAIN

def print_trajectories(chosen,calculated):    
            
    for t in zip(chosen,*calculated):    
        print(f"Trajectory {t[0]}: P = {t[1]:.{rounding}f}, sum = {t[2]}")    

def main():

    def test_random():

        print("\n TEST: RANDOM")

        pbt = PBinaryTreeNode(1)
        depth = 3

        pbt.populate_tree((0,0.5),0,depth,0)

        print("\n> tree:")
        PBinaryTreeNode.printBinaryTree(pbt.fetchRoot())

        # CALCULATE TRAJECTORIES

        # print("\n> example: all")
        # custom_trajectories = list(range(1,pow(2,depth)+1))
        # result = PBinaryTreeNode.calculate_trajectories(pbt.fetchRoot(),depth)
        # print_trajectories(custom_trajectories,result)

        # print("\n> example: hardcode 1,4")
        # custom_trajectories = [1,4]
        # result = PBinaryTreeNode.calculate_trajectories(pbt.fetchRoot(),depth,custom_trajectories)
        # print_trajectories(custom_trajectories,result)

        # print("\n> example: comprehension - evens")
        # custom_trajectories = [x for x in range(1,pow(2,depth)+1) if x%2==0]
        # result = PBinaryTreeNode.calculate_trajectories(pbt.fetchRoot(),depth,custom_trajectories)
        # print_trajectories(custom_trajectories,result)
    
    def test_binomial():        

        print("\n TEST: BINOMIAL")

        pbt = PBinaryTreeNode(1)
        depth = 5

        pbt.populate_tree(0,0,depth,0)

        print("\n> STABLO (VJEROJATNOSTI):")
        PBinaryTreeNode.printBinaryTree(pbt.fetchRoot())

        # CALCULATE TRAJECTORIES

        print("\n> REZULTAT (TRAJEKTORIJE):")
        custom_trajectories = list(range(1,pow(2,depth)+1))
        result = PBinaryTreeNode.calculate_trajectories(pbt.fetchRoot(),depth)
        print_trajectories(custom_trajectories,result)

        # SUM OVER TRAJECTORIES WITH SAME SUM (same number of L and D)

        print("\n> REZULTAT (KUMULATIV):")
        cumulative = [0]*(depth+1)

        for x in zip(result[0],result[1]): cumulative[x[1]]+=x[0]
        for i,c in enumerate(cumulative): print(f"[{depth-i}xL,{i}xD] P = {c:.{rounding}f}")

        # from numpy import random as np_rd
        # x = np_rd.binomial(n=depth,p=0.5,size=depth)
        # print(x)

        print("\n> TEST (BINOMIAL):")
        from scipy.stats import binom
        for i,x in enumerate(range(depth+1)): 
            p = binom.pmf(k=x,n=depth,p=test_trial_probability)
            print(f"[{i}xL,{depth-i}xD] P = {p:.{rounding}f}")

    test_random()

    # test_binomial()

main()
# pogodi_broj_main()