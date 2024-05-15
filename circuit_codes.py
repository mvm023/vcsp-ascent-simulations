import numpy as np
from anytree import Node, RenderTree
from scipy.spatial import distance



def max_code(n,k):
    if (n < 2):
        print("Please have n be at least 2")
        return
    starting_circuit = "0" * n
    root = Node(starting_circuit)
    child = Node("1" + starting_circuit[1:], parent=root)
    grandchild = Node("11" + starting_circuit[2:], parent=child)
    expand_tree(child.ancestors, child, grandchild, n, k)
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))
    print(f"The maximum length of a circuit code of length {n} with spread {k} is {max_depth(root)}")

def expand_tree(ancestors, parent, node, n, k):
    current_circuit = node.name
    for i in range (n):
        new_circuit= current_circuit[:i] + alternate_bit(current_circuit[i]) + current_circuit[i+1:]
        if not new_circuit == parent.name:
            if not any([distance.hamming(list(new_circuit),list(parent.name))*n < k for parent in ancestors]):
                new_node = Node(new_circuit, parent=node)
                expand_tree(new_node.parent.ancestors, new_node.parent, new_node, n, k)      
  

def alternate_bit(bit):
    if bit == "0":
        return "1"
    elif bit == "1":
        return "0"
    else:
        print(f"Unexpected bit {bit} encountered")

def max_depth(root): ##Very lazy implementation
    all_elems = root.descendants
    all_depths = [item.depth for item in all_elems]
    max_depth_elem_index = np.argmax(all_depths)
    max_depth_elem = all_elems[max_depth_elem_index]
    k = 0
    for ancestor in max_depth_elem.ancestors:
        print(f"{k}     {ancestor.name}")
        k += 1
    print(f"{k}     {max_depth_elem.name}")
    return max_depth_elem.depth

max_code(4,2)
