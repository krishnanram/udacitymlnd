
#Question 4
#Find the least common ancestor between two nodes on a binary search tree.
# The least common ancestor is the farthest node from the root that is an ancestor of both nodes.
# For example, the root is a common ancestor of all nodes on the tree,
#  but if both nodes are descendents of the root's left child, then that left child might be the
#  lowest common ancestor. You can assume that both nodes are in the tree,
# and the tree itself adheres to all BST properties.
# The function definition should look like question4(T, r, n1, n2),
# where T is the tree represented as a matrix,
# where the index of the list is equal to the integer stored
# in that node and a 1 represents a child node,
# r is a non-negative integer representing the root,
# and n1 and n2 are non-negative integers representing the two nodes in no particular order.
#  For example, one test case might be

class Node(object):

    def __init__(self, item=None,):
        self.item = item
        self.left = None
        self.right = None

    def __repr__(self):
        return '{}'.format(self.item)

    def _add(self, value):
        new_node = Node(value)

        if not self.item:
            self.item = new_node

        else:
            if value > self.item:
                self.right = self.right and self.right._add(value) or new_node
            elif value < self.item:
                self.left = self.left and self.left._add(value) or new_node
            else:
                print("BSTs do not support repeated items.")

        return self # this is necessary!!!


    def _search(self, value):
        if self.item == value:
            return True # or self

        elif self.left and value < self.item:
                return self.left._search(value)

        elif self.right and value > self.item:
                return self.right._search(value)

        else:
            return False


    def _isLeaf(self):
        return not self.right and not self.left


    def _printPreorder(self):
        print self.item

        if self.left:
            self.left._printPreorder()

        if self.right:
            self.right._printPreorder()

    def _preorder_array(self):
        nodes = []
        if self.item:
            nodes.append(self.item)
        if self.left:
            nodes.extend(self.left._preorder_array())
        if self.right:
            nodes.extend(self.right._preorder_array())
        return nodes




class BST(object):

    def __init__(self):
        self.root = None

    def add(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self.root._add(value)

    def printPreorder(self):
        if self.root:
            self.root._printPreorder()

    def search(self, value):
        if self.root:
            return self.root._search(value)

    def preorder_array(self):
        if self.root:
            return self.root._preorder_array()
        else:
            return 'Tree is empty.'

def find_ancestor(path, low_item, high_item):

    while path:
        current_item = path[0]
        if current_item < low_item:
            try:
                path = path[2:]
            except:
                return current_item
        elif current_item > high_item:
            try:
                path = path[1:]
            except:
                return current_item
        elif low_item <= current_item <= high_item:
            return current_item

import numpy as np
from collections import Counter

def findCommonParent(array1,array2):
    aCounter = Counter(array1)
    for s in array2 :
        if aCounter[s] == 1 :
            return s


def findMatchPath(parent, node, search_item):
    result = []
    status = False

    if node.item == search_item :
        result.append(node.item)
        return (True, result)

    if node.left != None :
        (status, result) = findMatchPath(node, node.left, search_item)
        if status == True :
            result.append(node.item)
            return (True, result)

    if node.right != None :
        (status, result) = findMatchPath(node, node.right, search_item)
        if status == True:
            result.append(node.item)
            return (True, result)

    return (status, result)


def question4(l, root, node1, node2):
    bst = BST()
    for i in l:
        bst.add(i)

    root = bst.root
    (status, res1) =  findMatchPath(None, root, node1)
    if status == False :
        print "Given node not found..."

    (status, res2) =  findMatchPath(None, root, node2)
    if status == False :
        print "Given node not found..."

    return findCommonParent(res1,res2)

    #nodes = bst.preorder_array()
    #return find_ancestor(nodes, node1, node2)


if __name__ == '__main__':

    m = [[0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [1, 0, 0, 0, 1],
     [0, 0, 0, 0, 0]],

    l = [10, 5, 6, 3, 8, 2, 1, 11, 9, 4]
    print 'Ancestor for 3, 11:', question4(l, 10, 3, 11)
    print 'Ancestor for 3, 11:', question4(l, 10, 1, 9)
    print 'Ancestor for 3, 11:', question4(l, 10, 1, 4)





#and the answer would be 3.