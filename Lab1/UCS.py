import heapq

class PriorityQueue(object): # 待探索节点队列
    def __init__(self):
        self.heap = []
        self.count = 0 # 总节点数

    def push(self, item, priority):
        entry = (priority, self.count, item) # 距离,标号, node
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority): # 判断node是否应该放到队列中/替换队列中的原有元素
        for index, (p, c, i) in enumerate(self.heap):
            if i.state == item.state:
                if p <= priority: # 现有到达方案更优
                    # break
                    return
                del self.heap[index] # 替换原有到达方案
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                # break
                return
        else: # 还没有到达方案，添加
            self.push(item, priority)


class node:
    """define node"""

    def __init__(self, state, parent, path_cost, action):
        self.state = state # B
        self.parent = parent # A的节点
        self.path_cost = path_cost # 到start的距离
        self.action = action # 上一步的操作["A","B","2"]


class problem:
    """searching problem"""

    def __init__(self, initial_state, actions):
        self.initial_state = initial_state
        self.actions = actions
        # 可以在这里随意添加代码或者不加

    def search_actions(self, state):
        acts = []
        for item in self.actions:
            if item[0] == state:
                acts += [item]
        return acts
        # raise Exception('获取state的所有可行的动作')

    def solution(self, node):
        position = node
        path = []
        while position.state != self.initial_state:
            path += [position.state]
            position = position.parent
        path += ["Start"]
        path.reverse()
        return path
        # raise Exception('获取从初始节点到node的路径')

    def transition(self, state, action):
        if(state != action[0]):
            raise Exception("transition error")
        return action[1]
        # raise Exception('节点的状态（名字）经过action转移之后的状态（名字）')

    def goal_test(self, state):
        return state == "Goal"
        # raise Exception('判断state是不是终止节点')

    def step_cost(self, state1, action, state2):
        return action[2]
        # raise Exception('获得从state1到通过action到达state2的cost')

    def child_node(self, node_begin, action):
        father = node_begin
        state = action[1]
        path_cost = node_begin.path_cost + action[2]
        child = node(state, father, path_cost, action)
        return child
        # raise Exception('获取从起始节点node_begin经过action到达的node')


def UCS(problem):
    node_test = node(problem.initial_state, '', 0, '')
    frontier = PriorityQueue()
    frontier.push(node_test, node_test.path_cost)
    explored = []
    while not frontier.isEmpty():
        node_test = frontier.pop() # 探索下一个最近节点
        if problem.goal_test(node_test.state):
            return problem.solution(node_test)
        explored += [node_test.state]
        actions = problem.search_actions(node_test.state)
        for act in actions:
            if not act[1] in explored:
                son = problem.child_node(node_test,act)
                frontier.update(son,son.path_cost)
    return 'Unreachable'


def main():
    actions = []
    while True:
        a = input().strip()
        if a != 'END':
            a = a.split()
            a[2] = int(a[2])
            actions += [a]
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


if __name__ == '__main__':
    main()