#!/usr/bin/env python

from random import randint

class Node:
    def __init__(self, value):
        self.next_elem = None
        self.value = value


class LinkedList:
    def __init__(self):
        self.root = None


    def add(self, value):
        if self.root == None:
            self.root = Node(value)
        else:
            self.add_node(value, self.root) 

    def add_node(self, value, node):
        if node.next_elem != None:
            self.add_node(value, node.next_elem)
        else:
            node.next_elem = Node(value)

    def print_him(self):
        if self.root != None:
            self.print_list(self.root)

    def print_list(self, node):
        if node != None:
            if node.value == None:
                print "for some reason it's None o_O"
            print str(node.value) + ' ', 
            self.print_list(node.next_elem)
    
    def remove(self, value):
        if self.root != None:
            self.remove_node(value, None,  self.root)
        else:
            return None

    def remove_node(self, value, parent_node, node):
        if node.value == value:
            if parent_node == None:
                self.root = node.next_elem
            else:
                parent_node.next_elem = node.next_elem

        else:
            self.remove_node(value, node, node.next_elem)

if __name__ == '__main__':
    list2 = LinkedList() 
    for val in range(100):
        list2.add(randint(1, 50))

    list2.print_him()


