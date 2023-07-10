# http://www.projectrho.com/public_html/starmaps/catalogues.php

import csv
import time

# HVG refers to database in which objects are stored
# In this case we are renaming name to hvg_db for code readability
"""  made minor changes to code prior to start of coding, such as naming conventions that the IDE suggested """


# The class star has a built-in constructor used to hold the information of a class
class Star:

    def __init__(self, hvg_db, name, mag, spectral, habit, dist):
        self.hvg_db = hvg_db  # reference number  in file (find record in file)
        self.display_name = name  # star name
        self.magnitude = mag  # measure of brightness of an object based on magnitude scale
        self.spectral_class = spectral  # refers to stellar classification based on Morgan-Keenan System
        self.habitable = habit  # refers to "habitable zone" in which "life" could exist human/-non-human
        self.distance_parsecs = dist  # unit of measurement, for reference, 1 parsec = 3.26 light-years

    # print function to test code
    def print_me(self):
        print("display_name=" + self.display_name + ", magnitude =" +
              self.magnitude)
        print("hvg_db=" + self.hvg_db + ", spectral=" + self.spectral_class +
              ", habitable=" + self.habitable)


# Wrap info for one star in a node suitable for placing in the tree
# contains star object, adds left and right references to enable insertion to a tree
# helps build tree and contains a star (ref to line 35)
# adds left and right reference
class TreeNode:

    def __init__(self, star):
        self.left = None
        self.right = None
        self.star_info = star
        self.name = "N" + str(self.star_info.hvg_db)
        self.key = star.display_name

    def print_key(self):
        print(self.key)

        # print for debugging purposes

    def print_me(self):
        print("node name =" + self.name)

        if self.left is None:
            print("left is None")
        else:
            print("left child:", end="")
            self.left.print_me()

        if self.right is None:
            print("right is None")
        else:
            print("right child:", end="")
            self.right.print_me()

        if self.star_info is None:
            print("value is None", end="")
        else:
            self.star_info.print_me()


class Tree:

    def __init__(self, name):
        self.name = name
        self.node_num = 0
        self.node_list = []
        self.root = None

    def insert(self, star):  # method insert uses stars Tree Node Value not name

        star = TreeNode(star)  # node object must be created

        if self.root is None:
            self.root = star  # sol is assigned as first value
            print("Root Assigned to Value: " +
                  str(self.root.key + "\n"))  # prints value of root
        else:
            current = self.root
            while current is not None:
                if star.key < current.key:  # node to insert compared against parent
                    if current.left is None:
                        current.left = star  # if null left results in left becoming current object if less than
                        current = None  # sets current to none
                    else:
                        current = current.left  # sets current to left
                else:
                    if current.right is None:  # if greater than object is none
                        current.right = star  # sets current node to right
                        current = None
                    else:
                        current = current.right
    """
    Zybook section 5.10
    BSTInsertRecursive(parent, nodeToInsert) {
       if (nodeToInsert⇢key < parent⇢key) {
          if (parent⇢left is null)
             parent⇢left = nodeToInsert
          else
             BSTInsertRecursive(parent⇢left, nodeToInsert)
       }
       else {
          if (parent⇢right is null)
             parent⇢right = nodeToInsert
          else
             BSTInsertRecursive(parent⇢right, nodeToInsert)
       }
    }
    """

    # Non-recursive method here. Handle empty root here, otherwise recurse
    def recursive_insert_wrapper(self, parent, star):
        # empty tree, create root node
        new_node = TreeNode(star) 
        if parent is None :   
            self.root = TreeNode(star) 
            print("Root is " + self.root.key)
        else:
            # Now recursively traverse existingtree and insert new_node
            self.insert_rec( parent, new_node)

    # Call method recursively for all but initial root
    # pretty much like the pseudo-code starting at line 100
    def insert_rec(self, parent, new_node):
        if new_node.key < parent.key:
            if parent.left is None:
                parent.left = new_node
            else:
                self.insert_rec(parent.left, new_node)
        else: 
            if parent.right is None:
                parent.right = new_node
            else:
                self.insert_rec(parent.right, new_node)
            

    def preorder_print(self, root):

        if root is not None:
            self.preorder_print(root.left)
            print(root.key)
            self.preorder_print(root.right)

    def search(self, opt_key):

        star = self.root  # value of node

        while star is not None:
            if star.key == opt_key:
                # automatic return of the key if there is a match
                return star
                # search will commence from the left side
            elif opt_key < star.key:
                star = star.left
                # search will commence from the right side
            else:
                star = star.right

                # value of none is returned if there is no key
        return None

    # Utility functions


# from: https://www.techiedelight.com/c-program-print-binary-tree/
# provided by instructor


# trunk draws the diagram to show pretty output
class Trunk:

    def __init__(self, prev=None, str=None):
        self.prev = prev
        self.str = str


def show_trunks(p):
    if p is None:
        return
    show_trunks(p.prev)
    print(p.str, end='')


def print_tree(root, prev, is_left):
    if root is None:
        return

    prev_str = '	'
    trunk = Trunk(prev, prev_str)
    print_tree(root.right, trunk, True)

    if prev is None:
        trunk.str = '———'
    elif is_left:
        trunk.str = '.———'
        prev_str = '   |'
    else:
        trunk.str = '`———'
        prev.str = prev_str

    show_trunks(trunk)
    print(' ' + root.star_info.display_name)
    if prev:
        prev.str = prev_str
    trunk.str = '   |'
    print_tree(root.left, trunk, False)


#
# main starts here
#
def main():
    # Instantiate Binary Tree to hold the stars
    star_tree = Tree("Star Catalog")

    with open('HabHYG_short.csv', 'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')

        # skip header row
        next(csvfile)

        # get time in nanoseconds -- maybe OS-specific?
        # See https://docs.python.org/3/library/time.html

        t0 = time.perf_counter_ns()

        obs_processed = 0
        
        for row in lines:
            # hvg_db, name, mag, spectral, habit, dist)
            this_star = Star(row[0], row[3], row[16], row[11], row[2], row[12])
            star_tree.recursive_insert_wrapper(star_tree.root, this_star)
            obs_processed = obs_processed + 1

    t1 = time.perf_counter_ns() - t0
    print("elapsed ms = " + str(t1 / 1000))
    print("obs_processed = " + str(obs_processed))

    # Your test and debug code here...
    star_tree.preorder_print(star_tree.root)

    # print the tree in quasi-graphic form
    print_tree(star_tree.root, None, False)
    print("***")

    #
    # Add three or more tests here, including not found case
    #

    # test search Procyon

    node_found = star_tree.search("Rigel Kentaurus A")
    if node_found is None:
        print("Not found")
    else:
        node_found.star_info.print_me()

    # test search Kapteyn's Star
    node_found = star_tree.search("Epsilon Indi")
    if node_found is None:
        print("Not found")
    else:
        node_found.star_info.print_me()


if __name__ == "__main__":
    main()
