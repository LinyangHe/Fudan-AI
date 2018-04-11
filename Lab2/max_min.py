def constructTree(n, tree, rule):
    '''
    construct a tree using given information, and return the root node
    :param n:  the height of tree
    :param tree: the input tree described with list nested structure
    :param rule: root node's type, 1 for max, 0 for min
    :return: root node
    '''
    node = Node(rule=rule)
    successors = []
    if n == 1:
        for t in tree:
            successors.append(Node(rule=1 - rule, isLeaf=True, value=t))
    else:
        for t in tree:
            successors.append(constructTree(n - 1, t, 1 - rule))
    node.successor = successors
    return node


def run():
	first_line = [int(i) for i in input().strip().split(' ')]
	print(first_line)
	tree = eval(input().strip())
	n = first_line[1]
	root_node = constructTree(n-1, tree, rule)
	# second_line = input().strip('[[').strip(']').split('')
	# second_line = input().strip()
	# for 
	print(second_line)

if __name__ == '__main__':
	run()
