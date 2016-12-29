#!/usr/bin/env python
#Question 5
#Find the element in a singly linked list that's m elements from the end.
# For example, if a linked list has 5 elements, the 3rd element from the end is the 3rd element.
# The function definition should look like question5(ll, m), where ll is the first node of a linked list
#  and m is the "mth number from the end".
# You should copy/paste the Node class below to use as a representation of a node in the linked list.
# Return the value of the node at that position.

class Node(object):

  def __init__(self, data):
    self.data = data
    self.next = None

  def addNode(self, newnode):
    self.next = newnode


def  findKthNodeFromLast(node,k) :

  p1 = node
  p2 = p1
  i=0
  while  (i < k) :

    try:
      p1 = p1.next
    except:
      print "Given k is more than available elements",(k)
      return None
    i += 1

  if p1.next != None :
    while (p1.next != None) :
      p1 = p1.next
      p2 = p2.next

    print "Reached the End. Kth position value is :", p2.data
    return p2.data

  else :
    print "Error..."
    return None



if __name__ == '__main__':

    startNode = Node(1)

    n = startNode
    for i in range(1, 11):
      print i
      newnode = Node(i)
      n.addNode(newnode)
      n = newnode

    print('The Linked List:')

    n = startNode
    while (n.next != None ) :
    #print n.data
        n = n.next

    #findKthNodeFromLast(startNode, 2)

    assert(findKthNodeFromLast(startNode, 2) == 8)
    assert(findKthNodeFromLast(startNode, 15) == None)