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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    start_state = problem.getStartState() #Start of the search
    front = util.Stack()                  #DAta Structure
    explored = []                          #Explored nodes
    node = (start_state, [])
    front.push(node)
    
    while not front.isEmpty():      #Begin by Exploring the last node in the stack
        current_state, actions = front.pop()    
        if current_state not in explored:    # Check if the current node is explored or not
            explored.append(current_state)       #If the current node is not explored add it to the explored nodes
            if problem.isGoalState(current_state):   #if the current state is the goal, return the path to it
                return actions
            else:
                successors = problem.getSuccessors(current_state) # get a list of possible successors#
                for successor_state, successor_action, successor_cost in successors:
                    new_action = actions + [successor_action]         
                    new_node = (successor_state, new_action)
                    front.push(new_node)  # push the successors to the stack#

    return actions  
      
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    start_state =problem.getStartState() #Start of the search
    explored =[]                         
    front = util.Queue()                   #DAta Structure
    cost =0
    node = (start_state, [] , cost)
    front.push(node)
      #I used the same methodology as in dfs the only difference is that i used a queue as 
      # Data Structure instead of a stack 
    while not front.isEmpty():
         current_state, actions, current_cost = front.pop()
         if current_state not in explored:
             explored.append(current_state)
             if problem.isGoalState(current_state):
                 return actions
             else:
                 successor = problem.getSuccessors(current_state)
                 for successor_state, successor_action, successor_cost in successor:
                     new_action = actions + [successor_action]
                     new_cost = current_cost + successor_cost
                     new_node = (successor_state, new_action, new_cost) 
                     front.push(new_node)
    return actions    

    util.raiseNotDefined()         

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    front = util.PriorityQueue()
    cost =0
    explored = {}
    node = (start_state, [], cost)
    #The initialization of the variable here is almost the same as i did in the two previous functions but the only difference
    # is again the data strucure which is a priority queue
    front.push(node, cost)
    while not front.isEmpty():
        current_state, actions, current_cost = front.pop()
        if (current_state not in explored) :
            explored[current_state] =current_cost
            if problem.isGoalState(current_state):
                return actions
            else:
                successor = problem.getSuccessors(current_state)
                for successor_state, successor_action, successor_cost in successor:
                    new_action = actions + [successor_action]
                    new_cost = current_cost + successor_cost
                    new_node =(successor_state, new_action, new_cost)
                    front.update(new_node,new_cost)
    return actions
         
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***" 
    start_state = problem.getStartState() 
    front = util.PriorityQueue()
    explored = [] 
    cost =0
    
    node = (start_state, [], cost) 

    front.push(node, cost)

    while not front.isEmpty():

        current_state, actions, current_cost = front.pop()
        explored.append((current_state, current_cost))

        if problem.isGoalState(current_state):
            return actions

        else:
            successor = problem.getSuccessors(current_state)
            
            for successor_state, successor_action, successor_cost in successor:
                new_action = actions + [successor_action]
                new_cost = problem.getCostOfActions(new_action)
                new_node = (successor_state, new_action, new_cost)
                
                already_explored = False
                for ex in explored:
                    #Examine each node in the explored nodes
                    explored_state, explored_cost = ex
                    if (successor_state == explored_state) and (new_cost >= explored_cost):
                        already_explored = True
                if not already_explored:
                    #if the successor is not already explored  put it in the queue and in the explored nodes
                    front.push(new_node, new_cost + heuristic(successor_state, problem))
                    explored.append((successor_state, new_cost))

    return actions              
                
    
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
