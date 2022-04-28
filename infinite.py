from itertools import product
import matplotlib.pyplot as plt
from random import choices

# A node has a name, a node above, a node left, and a node right
class node:
    def __init__(
            self, 
            up    = None, # Don't make nodes until needed
            left  = None, 
            right = None, 
            name  = "0"): # The "origin" is node "0"
        self.name  = name
        self.up    = up
        self.left  = left
        self.right = right 
                
    # The node above has "U" added to name
    # Without loss of generality, assume this node is on the left
    def go_up(self):
        if(self.up == None):
            self.up = node(left = self, name = self.name + "U")
        return(self.up)
    
    # The node left has "L" added to name
    def go_left(self):
        if(self.left == None):
            self.left = node(up = self, name = self.name + "L")
        return(self.left)
    
    # The node above has "R" added to name
    def go_right(self):
        if(self.right == None):
            self.right = node(up = self, name = self.name + "R")
        return(self.right)
    
    def __str__(self):
        return(self.name)
    
# Find destinations of all paths of length k
def all_paths(k = 1, verbal = False):
    start = node()
    all_options = product(["up", "left", "right"], repeat = k)
    final_node_list = []
    if(verbal):
        print("\nAll paths of length {}:\n".format(k))
    for option in all_options:
        nodes = [start]
        for move in option:
            if move == "up":    nodes.append(nodes[-1].go_up())
            if move == "left":  nodes.append(nodes[-1].go_left())
            if move == "right": nodes.append(nodes[-1].go_right())
        final_node_list.append(nodes[-1].name)
        if(verbal):
            print(option)
            for i, n in enumerate(nodes):
                print(n, end = " -> " if i != k else " ")
            print("\n")
    if(verbal): 
        print("Final nodels:")
        print(final_node_list)
    return(final_node_list)

# Find proportion of paths of length k ending at node
def paths_like_this(my_node = "0", k = 1):
    final_node_list = all_paths(k=k)
    total_paths = len(final_node_list)
    given_paths = final_node_list.count(my_node)
    print("k = {}: \t{} \t\t/ \t\t{} \t\t= {}".format(
        k,
        given_paths, 
        total_paths, 
        given_paths/total_paths))
    return(given_paths/total_paths)
            

# Find destinations of random paths of length k
def random_paths(k = 1, count = 256):
    start = node()
    random_options = []
    while(len(random_options) < count):
        random_options.append(choices(["up", "left", "right"], k=k))
    final_node_list = []
    for option in random_options:
        nodes = [start]
        for move in option:
            if move == "up":    nodes.append(nodes[-1].go_up())
            if move == "left":  nodes.append(nodes[-1].go_left())
            if move == "right": nodes.append(nodes[-1].go_right())
        final_node_list.append(nodes[-1].name)
    return(final_node_list)

# Find proportion of random paths of length k ending at node
def random_paths_like_this(my_node = "0", k = 1, count = 256):
    final_node_list = random_paths(k=k, count=count)
    total_paths = len(final_node_list)
    given_paths = final_node_list.count(my_node)
    print("k = {}: \t{} \t\t/ \t\t{} \t\t= {}".format(
        k,
        given_paths, 
        total_paths, 
        given_paths/total_paths))
    return(given_paths/total_paths)
            


def plot_path_proportion(my_node, k_count, random = False, count = 256):
    if(random):
        print("\nProportion of random paths ending at {} after k steps:\n".format(my_node))
    else:
        print("\nProportion of paths ending at {} after k steps:\n".format(my_node))
    proportions = []
    for k in range(1,k_count):
        if(random):
            proportions.append(random_paths_like_this(my_node = my_node, k = k, count = count))
        else:
            proportions.append(paths_like_this(my_node = my_node, k = k))
    
    x = [i for i in range(1, k_count) if proportions[i-1] != 0]
    y = [p for p in proportions if p != 0]
    plt.plot(x,y)
    plt.ylim([0, 1])
    plt.show()
    
if __name__ == "__main__":
    all_paths(k=3, verbal = True)
    plot_path_proportion("0", 13)
    plot_path_proportion("0", 25, random = True, count = 2**16)