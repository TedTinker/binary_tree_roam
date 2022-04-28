class node:
    def __init__(
            self, 
            up    = None, 
            left  = None, 
            right = None, 
            name  = "0"): # The "origin" is node "0"
        assert name[0] == "0"
        for i in range(1, len(name)):
            if name[i] == "U": assert name[i-1] != "L"
            if name[i] == "L": assert name[i-1] != "U"
        self.name  = name
        self.up    = up
        self.left  = left
        self.right = right 
                
    def go_up(self):
        return(self.up)
    
    def go_left(self):
        return(self.left)
    
    def go_right(self):
        return(self.right)
    
    def __str__(self):
        return("{} \t: {} up, {} left, {} right".format(
            self.name, 
            "None" if self.up    == None else self.up.name, 
            "None" if self.left  == None else self.left.name,
            "None" if self.right == None else self.right.name))

class binary_tree:
    def __init__(self, node_list):
        self.node_dict = {name : node(name = name) for name in node_list}
        for n in self.node_dict.values():
            possible_nodes = {
                "U" : n.name + "U" if not n.name[-1] in ["L","R"] else n.name[:-1],
                "L" : n.name + "L" if n.name[-1] != "U" else n.name[:-1],
                "R" : n.name + "R"
                }
            for p, n_ in possible_nodes.items():
                if(n_ in self.node_dict):
                    if(p == "U"): n.up = self.node_dict[n_];    self.node_dict[n_].left == n
                    if(p == "L"): n.left = self.node_dict[n_];  self.node_dict[n_].up == n
                    if(p == "R"): n.right = self.node_dict[n_]; self.node_dict[n_].up == n
                    
    def __str__(self):
        n_list = []
        for n in self.node_dict.values():
            n_list.append(str(n))
        return("\n" + "\n".join(n_list))

bt = binary_tree(["0", "0U", "0UU", "0UUU", "0L", "0LL", "0LLL", "0LLLL", "0LLLLL", "0LR", "0R", "0RL", "0RR"])

def all_paths(start = bt.node_dict["0"], k=1, path = [], option = []):
    paths = []; options = []
    if(k==0): return(path + [start], option)
    if(start.up != None):
        p, o = all_paths(
            start = start.up, k=k-1, 
            path = path + [start], 
            option = option + ["U"])
        paths.append(p)
        options.append(o)
    if(start.left != None):
        p, o = all_paths(
            start = start.left, k=k-1, 
            path = path + [start],
            option = option + ["L"])
        paths.append(p)
        options.append(o)
    if(start.right != None):
        p, o = all_paths(
            start = start.right, k=k-1, 
            path = path + [start],
            option = option + ["R"])
        paths.append(p)
        options.append(o)
    while(type(paths[0][0]) == list):
        paths = sum(paths, [])
    while(type(options[0][0]) == list):
        options = sum(options, [])
    return(paths, options)
    
paths, options = all_paths(k=3)
    
for p, o in zip(paths, options):
    print()
    print(o)
    for i, n in enumerate(p): 
        print(n.name, end = " -> " if i+1 != len(p) else "")
    print()
    
# Find proportion of paths of length k ending at node
def paths_like_this(my_node = "0", k = 1):
    paths, _ = all_paths(k=k)
    final_node_list = [p[-1].name for p in paths]
    total_paths = len(final_node_list)
    given_paths = final_node_list.count(my_node)
    print("k = {}: \t{} \t\t/ \t\t{} \t\t= {}".format(
        k,
        given_paths, 
        total_paths, 
        given_paths/total_paths))
    return(given_paths/total_paths)
            
my_node = "0"
k_count = 15
print("\nProportion of paths ending at {} after k steps:\n".format(my_node))
proportions = []
for k in range(1,k_count):
    proportions.append(paths_like_this(my_node = my_node, k = k))




import matplotlib.pyplot as plt

plt.plot(
    [i for i in range(1,k_count)],
    proportions
    )
plt.ylim([0, 1])
plt.show()