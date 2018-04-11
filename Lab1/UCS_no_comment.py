import heapq
class PriorityQueue(object): 
    def __init__(self):
        self.heap = []
        self.count = 0
    def push(self, item, priority):
        entry = (priority, self.count, item) 
        heapq.heappush(self.heap, entry)
        self.count += 1
    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item
    def isEmpty(self):
        return len(self.heap) == 0
    def update(self, item, priority): 
        for index, (p, c, i) in enumerate(self.heap):
            if i.state == item.state:
                if p <= priority:
                    return
                del self.heap[index] 
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                return
        else:
            self.push(item, priority)

class node:
    def __init__(self, state, parent, path_cost, action):
        self.state = state
        self.parent = parent 
        self.path_cost = path_cost 
        self.action = action
class problem:
    def __init__(self, initial_state, actions):
        self.initial_state = initial_state
        self.actions = actions
    def search_actions(self, state):
        acts = []
        for item in self.actions:
            if item[0] == state:
                acts.append(item)
        return acts
    def solution(self, node):
        position = node
        path = []
        while position.state != self.initial_state:
            path.append(position.state)
            position = position.parent
        path.append("Start")
        path.reverse()
        return path
    def transition(self, state, action):
        if(state != action[0]):
            raise Exception("transition error")
        return action[1]
    def goal_test(self, state):
        return state == "Goal"
    def step_cost(self, state1, action, state2):
        return action[2]
    def child_node(self, node_begin, action):
        father = node_begin
        state = action[1]
        path_cost = action[2] + node_begin.path_cost 
        son = node(state, father, path_cost, action)
        return son

def UCS(problem):
    node_test = node(problem.initial_state, '', 0, '')
    frontier = PriorityQueue()
    frontier.push(node_test, node_test.path_cost)
    explored = []
    while not frontier.isEmpty():
        node_test = frontier.pop() 
        if problem.goal_test(node_test.state):
            return problem.solution(node_test)
        explored.append(node_test.state)
        actions = problem.search_actions(node_test.state)
        for act in actions:
            if not act[1] in explored:
                son = problem.child_node(node_test,act)
                frontier.update(son,son.path_cost)
    return 'Unreachable'

actions = []
while True:
    a = input().strip()
    if a != 'END':
        a = a.split()
        a[2] = int(a[2])
        actions.append(a)
    else:
        break
graph_problem = problem('Start', actions)
answer = UCS(graph_problem)
s = "->"
if answer == 'Unreachable':
    print(answer)
else:
    path = s.join(answer)
    print(path)