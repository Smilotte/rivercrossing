import numpy as np


class Node:
    def __init__(self, m_wrong_side, c_wrong_side, boat_wrong_side, parent_node):
        self.m_wrong_side = m_wrong_side
        self.c_wrong_side = c_wrong_side
        self.boat_wrong_side = boat_wrong_side
        self.parent_node = parent_node

        # store the positions in a array
        self.state = np.array([m_wrong_side, c_wrong_side, boat_wrong_side])

        # def the goal state
    def is_goal_state(self):
        return np.all(self.state == 0)

    def get_child_node(self, action):
        if self.boat_wrong_side == 1:
            new_state = self.state - action
        elif self.boat_wrong_side == 0:
            new_state = self.state + action
        else:
            raise ValueError ("boat_wrong_side has to be either 0 or 1.")
        child_node = Node(new_state[0], new_state[1], new_state[2], parent_node=self)
        return child_node

    def is_valid(self):
        if 0 <= self.m_wrong_side <= 3 \
                and 0 <= self.c_wrong_side <= 3 \
                and (self.m_wrong_side == 0 or self.c_wrong_side <= self.m_wrong_side) \
                and (self.m_wrong_side == 3 or self.c_wrong_side >= self.m_wrong_side):
            return True
        else:
            return False

    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

    def __hash__(self):
        return hash(tuple(self.state))

    def __str__(self):
        return ("Node <" + str(self.m_wrong_side) + "," +
                str(self.c_wrong_side) + "," +
                str(self.boat_wrong_side) + ">")


class Game:
    def __init__(self):
        self.initial_node = Node(m_wrong_side=3, c_wrong_side=3, boat_wrong_side=1,
                                 parent_node="initial")
        self.actions = [np.array([1, 0, 1]),
                        np.array([2, 0, 1]),
                        np.array([0, 1, 1]),
                        np.array([0, 2, 1]),
                        np.array([1, 1, 1])]

    def breadth_first_search(self):
        if self.initial_node.is_goal_state():
            return self.initial_node

        frontier = []
        frontier.append(self.initial_node)
        explored = set()

        while True:
            if len(frontier) == 0:
                return "Failure"
            # FIFO: get first element
            node = frontier.pop(0)
            explored.add(node)
            print("Exploring", node, "...")
            for action in self.actions:
                child = node.get_child_node(action)
                if child.is_valid() and (child not in explored) and (child not in frontier):
                    if child.is_goal_state():
                        return child
                    frontier.append(child)


def find_path_to_start(goal_node):
    def get_parent_node(node):
        parent_node = node.parent_node
        print("-->", parent_node)
        if isinstance(parent_node.parent_node, str) and parent_node.parent_node == "initial":
            return parent_node
        else:
            get_parent_node(parent_node)

    print("Goal node:", goal_node)
    start_node = get_parent_node(goal_node)
    return start_node


if __name__ == "__main__":
    g = Game()
    goal_state = g.breadth_first_search()
    print("Found goal state", goal_state)

    print()

    find_path_to_start(goal_state)
