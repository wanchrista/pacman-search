# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # store all the visited nodes in a list
    visited = list()
    nodes = util.Stack()
    path = []

    # store the parent, action and state for the start node
    current = dict()
    current["prev"] = None
    current["dir"] = None
    current["pos"] = problem.getStartState()

    # Check if we are already at the goal, if so, return path immediately
    if problem.isGoalState(current["pos"]):
        path.append(current["dir"])
        return path

    # If it is not at the goal, add it to the frontier
    nodes.push(current)

    # Keep popping off the stack
    while not nodes.isEmpty():
        current = nodes.pop()

        # If we have reached the goal state, then we break the loop
        if problem.isGoalState(current["pos"]):
            break

        # Add the node to the list of visited nodes
        visited.append(current["pos"])

        # Loop through all the successors
        for i in problem.getSuccessors(current["pos"]):
            # If it is not visited, add it to visited and onto the stack
            if not i[0] in visited:
                # store the parent, action and state for the next node
                next_node = dict()
                next_node["prev"] = current
                next_node["pos"] = i[0]
                next_node["dir"] = i[1]

                nodes.push(next_node)

    while current["dir"]:
        # Insert at the front of the list so that the actions happen in chronological order
        path.insert(0, current["dir"])
        # Check if the current node has a parent - If not, break
        if current["prev"]:
            current = current["prev"]
        else:
            break

    return path


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # store all the visited nodes in a list
    visited = list()
    nodes = util.Queue()
    path = []

    # store the parent, action and state for the start node
    current = dict()
    current["prev"] = None
    current["dir"] = None
    current["pos"] = problem.getStartState()

    # Check if we are already at the goal, if so, return path immediately
    if problem.isGoalState(current["pos"]):
        path.append(current["dir"])
        return path

    # If it is not at the goal, add it to the frontier
    nodes.push(current)

    while not nodes.isEmpty():
        current = nodes.pop()

        # Skip to the next node if you have already visited (cycle checking)
        if current["pos"] in visited:
            continue

        visited.append(current["pos"])

        if problem.isGoalState(current["pos"]):
            break

        # i[0] = pos, i[1] = dir, i[2] = cost
        for i in problem.getSuccessors(current["pos"]):
            if i[0] not in visited:
                next_node = dict()
                next_node["prev"] = current
                next_node["pos"] = i[0]
                next_node["dir"] = i[1]

                nodes.push(next_node)

    while current["dir"]:
        path.insert(0, current["dir"])
        if current["prev"]:
            current = current["prev"]
        else:
            break

    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = list()
    nodes = util.PriorityQueue()
    path = []

    current = dict()
    current["prev"] = None
    current["dir"] = None
    current["pos"] = problem.getStartState()
    current["cost"] = 0

    # Check if we are already at the goal, if so, return path immediately
    if problem.isGoalState(current["pos"]):
        path.append(current["dir"])
        return path

    # Give priority based on cost of the path
    nodes.push(current, current["cost"])

    while not nodes.isEmpty():
        current = nodes.pop()

        if current["pos"] in visited:
            continue

        visited.append(current["pos"])

        if problem.isGoalState(current["pos"]):
            break

        # i[0] = pos, i[1] = dir, i[2] = cost
        for i in problem.getSuccessors(current["pos"]):
            if not i[0] in visited:
                next_node = dict()
                next_node["prev"] = current
                next_node["pos"] = i[0]
                next_node["dir"] = i[1]
                next_node["cost"] = i[2] + current["cost"]

                nodes.push(next_node, next_node["cost"])

    while current["dir"]:
        path.insert(0, current["dir"])
        if current["prev"]:
            current = current["prev"]
        else:
            break

    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = list()
    nodes = util.PriorityQueue()
    path = []

    current = dict()
    current["prev"] = None
    current["dir"] = None
    current["pos"] = problem.getStartState()
    current["cost"] = 0
    # Get the estimated value of what the h(n) value is
    current["est"] = heuristic(problem.getStartState(), problem)

    # Check if we are already at the goal, if so, return path immediately
    if problem.isGoalState(current["pos"]):
        path.append(current["dir"])
        return path

    # The cost of the path is determined by cost to get there + cost of heuristic
    nodes.push(current, current["est"] + current["cost"])

    while not nodes.isEmpty():
        current = nodes.pop()

        if current["pos"] in visited:
            continue

        visited.append(current["pos"])
        if problem.isGoalState(current["pos"]):
            break

        for i in problem.getSuccessors(current["pos"]):
            if not i[0] in visited:
                next_node = dict()
                next_node["prev"] = current
                next_node["pos"] = i[0]
                next_node["dir"] = i[1]
                next_node["cost"] = i[2] + current["cost"]
                next_node["est"] = heuristic(next_node["pos"], problem)

                nodes.push(next_node, next_node["est"] + next_node["cost"])

    while current["dir"]:
        path.insert(0, current["dir"])
        if current["prev"]:
            current = current["prev"]
        else:
            break

    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
