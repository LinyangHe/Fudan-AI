# class Test(object):
# 	"""docstring for Test"""
# 	def __init__(self, arg):
# 		self.arg = arg
# 		self.__fuck = arg

# 	def getarg(self):
# 		return (self.arg)

# 	def getfuck(self):
# 		return (self.__fuck)

# 	def __func__(self):
# 		return

# # a = Test(5)
# a = Test()
# print(a.arg)
# print(a.getarg())
# print(a.getfuck())

# print(a.__fuck)
b = 0
while not b == 10:
	b += 1
	print(b)
test = [1,2,3,3,4]
print(test)


# def depthFirstSearch(problem):
#     """
#     Search the deepest nodes in the search tree first.

#     Your search algorithm needs to return a list of actions that reaches the
#     goal. Make sure to implement a graph search algorithm.

#     To get started, you might want to try some of these simple commands to
#     understand the search problem that is being passed in:

#     print "Start:", problem.getStartState()
#     print "Is the start a goal?", problem.isGoalState(problem.getStartState())
#     print "Start's successors:", problem.getSuccessors(problem.getStartState())
#     """
#     "*** YOUR CODE HERE ***"
#     from game import Directions
#     s = Directions.SOUTH
#     w = Directions.WEST
#     e = Directions.EAST
#     n = Directions.NORTH

#     search_stack = util.Stack()

#     initial_state = problem.getStartState()
#     current_node = (initial_state, Directions.STOP, 0)
#     search_stack.push(current_node)
#     while not problem.isGoalState(current_node[0]):
#         print "***************", search_stack.list
#         print "Current:", current_node
#         successors = problem.getSuccessors(current_node[0])
#         print "Successors:", successors

#         for successor in successors:
#             if successor[0] not in problem._visited:
#                 # print (search_stack.list)
#                 search_stack.push(successor)
#                 current_node = successor
#                 break
#         else:
#             current_node = search_stack.pop()
#             # successors = problem.getSuccessors(current_node[0])

#         if problem.isGoalState(current_node[0]):
#             while not search_stack.isEmpty():
#                 action_list = []
#                 action_list.append(search_stack.pop()[1])
#             break
#         #Test if the node is the leaf node. If so, pop the node
#     print(action_list[::-1][1:])

#     return action_list[::-1][1:]