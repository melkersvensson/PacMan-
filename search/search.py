# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# # Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""
"""
The `problem` parameter in the search methods (dfs, bfs, etc.) is an instance of the `SearchProblem` class.
This class outlines the structure of a search problem, but doesn't implement any of the methods.
You will need to use the methods of this class to interact with the search problem.
"""
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in obj-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()


def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# def addSuccessors(problem, addCost=True):

class SearchNode:
    def __init__(self, parent, node_info):
        """
            parent: parent SearchNode.

            node_info: tuple with three elements => (coord, action, cost)

            coord: (x,y) coordinates of the node position

            action: Direction of movement required to reach node from
            parent node. Possible values are defined by class Directions from
            game.py

            cost: cost of reaching this node from the starting node.
        """

        self.__state = node_info[0]
        self.action = node_info[1]
        self.cost = node_info[2] if parent is None else node_info[2] + parent.cost
        self.parent = parent

    # The coordinates of a node cannot be modified, se we just define a getter.
    # This allows the class to be hashable.
    @property
    def state(self):
        return self.__state

    def get_path(self):
        path = []
        current_node = self
        while current_node.parent is not None:
            path.append(current_node.action)
            current_node = current_node.parent
        path.reverse()
        return path
    
    # Consider 2 nodes to be equal if their coordinates are equal (regardless of everything else)
    # def __eq__(self, __o: obj) -> bool:
    #     if (type(__o) is SearchNode):
    #         return self.__state == __o.__state
    #     return False

    # # def __hash__(self) -> int:
    # #     return hash(self.__state)

def depth_first_search(problem):
    # Create stack to store nodes to be visited
    stack = util.Stack()
    visited = set()

    # Push start node onto stack
    start_node = SearchNode(None, (problem.get_start_state(), None, 0))
    stack.push(start_node)

    while not stack.is_empty():
        current_node = stack.pop()
        
        # Check if current node is goal state
        if problem.is_goal_state(current_node.state):
            return current_node.get_path()
        
        # Mark current node as visited
        if current_node.state not in visited:
            visited.add(current_node.state)

            # Push successors onto the stack if they haven't been visited
            for successor in problem.get_successors(current_node.state):
                successor_state = successor[0]  # Get the state portion of successor
                
                if successor_state not in visited:
                    stack.push(SearchNode(current_node, successor))
    return []





def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Create queue to store nodes to be visited
    queue = util.Queue()
    visited = set()
    
    # Push start node onto queue
    queue.push(SearchNode(None, (problem.get_start_state(), None, 0)))
    
    while not queue.is_empty():
        # Pop node from front of queue
        current_node = queue.pop()
        
        # Check if current node is goal state
        if problem.is_goal_state(current_node.state):
            return current_node.get_path()
        
        if current_node.state not in visited:
            # Mark current node as visited
            visited.add(current_node.state)
            
            # Push all successors of current node onto the queue
            for successor in problem.get_successors(current_node.state):
                queue.push(SearchNode(current_node, successor))
    return []

def uniform_cost_search(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # we implement dijkstra's algorithm as UCS
    # Create a priority queue to store nodes to be visited
    pq = util.PriorityQueue()
    visited = set()
    
    # Push start node onto priority queue with priority 0
    pq.push(SearchNode(None, (problem.get_start_state(), None, 0)), 0)
    
    while not pq.is_empty():
        # Pop node with lowest cost from priority queue
        current_node = pq.pop()
        
        # Check if current node is goal state
        if problem.is_goal_state(current_node.state):
            return current_node.get_path()
        
        if current_node.state not in visited:
            # Mark current node as visited
            visited.add(current_node.state)
            
            # Push all successors of current node onto priority queue
            for successor in problem.get_successors(current_node.state):
                pq.push(SearchNode(current_node, successor), current_node.cost + successor[2])
    
    return []


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def a_star_search(problem, heuristic=null_heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Create a priority queue to store nodes to be visited
    pq = util.PriorityQueue()
    visited = set()
    
    # Push start node onto priority queue with priority 0
    pq.push(SearchNode(None, (problem.get_start_state(), None, 0)), 0)
    
    while not pq.is_empty():
        # Pop node with lowest cost from priority queue
        current_node = pq.pop()
        
        # Check if current node is goal state
        if problem.is_goal_state(current_node.state):
            return current_node.get_path()
        
        if current_node.state not in visited:
            # Mark current node as visited
            visited.add(current_node.state)
            
            # Push all successors of current node onto priority queue with updated priority
            for successor in problem.get_successors(current_node.state):
                pq.push(SearchNode(current_node, successor), current_node.cost + successor[2] + heuristic(successor[0], problem))
    
    return []

# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
