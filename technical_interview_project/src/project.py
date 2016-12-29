from question1 import *
from question2 import *
from question3 import *
from question4 import *
from question5 import *

def question1(str, substr) :
    return is_anagram(str, substr)


def question2(str) :
    (maxSize, res) = palindromic(str)
    return maxSize

def question3(gdict):

    gdict = {
        'A': [('B', 2), ('C', 1)],
        'B': [('A', 2), ('C', 5)],
        'C': [('B', 5)]
    }

    g = Graph()

    for vertex, edges in gdict.items():
        g.add_node(vertex)
        for edge in edges:
            g.add_edge(vertex, edge[0], edge[1])

    mst = g.spanning_tree(False)
    return mst



def question4(list, root, node1, node2):
    bst = BST()
    for i in l:
        bst.add(i)

    nodes = bst.preorder_array()
    return find_ancestor(nodes, node1, node2)


def question5(node,k):
    return findKthNodeFromLast(node,k)



if __name__ == '__main__':

    #1
    print "---------------------- Executing question 1 with param udacity,ud -----------------"
    assert (question1("udacity", "ud") == True)

    #2
    print "---------------------- Executing question 2   -----------------------"
    assert (palindromic("zzaabbc")[0] == 7)

    #3
    print "---------------------- Executing question 3  ------------------------"
    gdict = {
        'A': [('B', 2), ('C', 1)],
        'B': [('A', 2), ('C', 5)],
        'C': [('B', 5)]
    }
    mst = question3(gdict)
    print mst
    print "Minimum Spanning Tree Graph is "
    printGraph(mst)


    #4
    print "------------------------- Executing question 4 ------------------------"
    m = [[0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [1, 0, 0, 0, 1],
         [0, 0, 0, 0, 0]],

    ### I was not sure about parent/child relationship for a Tree in matrix form. The instructions not very clear
    ### Hence I followed array arepresentation of a Tree
    l = [10, 5, 6, 3, 8, 2, 1, 11, 9, 4]
    print 'Ancestor for 3, 11:', question4(l, 10, 3, 11)
    assert (question4(l, 10, 3, 11) == 10)


    #5
    print "-------------------------- Executing question 5 -------------------------"

    startNode = Node(1)
    n = startNode
    for i in range(1, 11):
        newnode = Node(i)
        n.addNode(newnode)
        n = newnode

    assert (question5(startNode, 2) == 8)
    assert (question5(startNode, 15) == None)
