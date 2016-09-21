#!/usr/bin/env python



class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value


class Tree:
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def add_node(self, value):
        if self.root == None:
            self.root = Node(value)
            print 'root node created, Node value: %s' % str(value)
        else:
            print 'appending will be started soon'
            self.append_tree(value, self.root)

    def append_tree(self, value, node):
        print 'appending'
        if value < node.value:
            if node.left != None:
                print 'Not null, going left'
                self.append_tree(value,node.left)
            else:
                print 'to the left, Node value: %s' % str(value)
                node.left = Node(value)
        else:
            if node.right != None:
                self.append_tree(value, node.right)
            else:
                print ' to the righti, Node value: %s' % str(value)
                node.right = Node(value)
    def find_node(self, value):
        if self.root != None:
            return tree_search(value, self.root)
        else:
            return None

    def tree_search(self, value, node):
        if value == node.value:
            return node
        elif value < node.value:
            tree_search(value, node.left)
        elif value > node.value:
            tree_search(value, node.right)

    def delete_tree(self):
        self.root = None

    def print_tree(self):
        if self.root != None:
            self.print_subtree(self.root)

    def print_subtree(self, node):
        if node != None:
            self.print_subtree(node.left)
            print str(node.value) + ' '
            self.print_subtree(node.right)

if __name__ == '__main__':
    new_tree = Tree()
    new_tree.add_node(3)
    print "Here is the second value"
    new_tree.add_node(2)
    print "should be added"
    new_tree.add_node(5)
    new_tree.add_node(8)
    new_tree.add_node(12)
    new_tree.add_node(0)
    new_tree.add_node(77)

    new_tree.print_tree()
