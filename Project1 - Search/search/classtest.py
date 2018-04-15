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

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost