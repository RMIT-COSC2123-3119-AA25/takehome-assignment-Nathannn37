# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Greedy maze solver for all entrance, exit pairs
#
# __author__ = <student name here>
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze

from knapsack.knapsack import Knapsack
from itertools import permutations

from typing import List, Dict, Optional


class TaskDSolver:
    def __init__(self, knapsack:Knapsack):
        self.m_solverPath: List[Coordinates] = []
        self.m_cellsExplored = 0 # count of UNIQUE cells visited. i.e. final count should equal len(set(self.m_solverPath))
        self.m_entranceUsed = None
        self.m_exitUsed = None
        self.m_knapsack = knapsack
        self.m_value = 0
        self.m_reward = float('-inf') # initial reward should be terrible

        # you may which to add more parameters here, such as probabilities, etc
        # you may update these parameters using the Maze object in SolveMaze

    def reward(self):
        return self.m_knapsack.optimalValue - self.m_cellsExplored
    
    def bfs(self, maze: Maze, start: Coordinates, goal: Coordinates) -> List[Coordinates]:
        """
        Finds the shortest path between start and goal coordinate using breadth first search

        @param maze: the maze we are working on.
        @param start: the starting coordinate.
        @param goal: the goal coordinate.

        @return A list containing coordinates to go from the start to the goal.
        """

        if start == goal:
            return [start]

        visited = set()
        queue = [start]
        predecessors: Dict[Coordinates, Optional[Coordinates]] = {start: None}

        while queue:
            curr = queue.pop(0)

            if curr == goal:
                # Reconstruct path from goal to start
                path = []
                while curr is not None:
                    path.append(curr)
                    curr = predecessors[curr]
                return list(reversed(path))

            visited.add(curr)

            for neighbor in maze.neighbours(curr):
                if neighbor not in visited and neighbor not in predecessors:
                    if not maze.hasWall(curr, neighbor):
                        queue.append(neighbor)
                        predecessors[neighbor] = curr

        # If goal is unreachable (shouldn’t happen in a fully connected maze)
        return []

    def solveMaze(self, maze: Maze, entrance: Coordinates, exit: Coordinates):
        """
        Solution for Task D goes here.

        Be sure to increase self.m_cellsExplored whenever you visit a NEW cell
        Be sure to increase the knapsack_value whenever you find an item and put it in your knapsack.
        You may use the maze object to check if a cell you visit has an item
        maze.m_itemParams can be used to calculate things like predicted reward, etc. But you can only use
        maze.m_items to check if your current cell contains an item (and if so, what is its weight and value)

        Code in this function will be rigorously tested. An honest but bad solution will still gain quite a few marks.
        A cheated solution will gain 0 marks for all of Task D.
        Args:
            maze: maze object
            entrance: initial entrance coord
            exit: exit coord

        Returns: Nothing, but updates variables
        """
         # set up initial condition for knapsack
        self.m_knapsack.optimalCells = []
        self.m_knapsack.optimalValue = 0
        self.m_knapsack.optimalWeight = 0

        # get the number of items in the maze from the paramaters
        items_in_maze = maze.m_itemParams[0]
        # calculate total weight in maze form item list
        maze_item_weight = sum(weight_value[0] for weight_value in maze.m_items.values())
        # calculate total value in maze from item list
        maze_item_value = sum(weight_value[1] for weight_value in maze.m_items.values())
        
        midmaze = [maze.colNum // 2][maze.rowNum // 2]
        # Find the path from entrance to exit
        path = self.bfs(maze, entrance, exit)

        points = [entrance] + midmaze + [exit]

        for i in range(len(points)):
            for j in range(len(points)):
                if j != i:
                    path = self.bfs(maze, points[i], points[j])

        for cell in path:
            # Convert `cell` to a tuple to match the format in `maze.m_items`
            cell_tuple = (cell.getRow(), cell.getCol())
            if cell_tuple in maze.m_items:
                weight, value = maze.m_items[cell_tuple]
                # Check if adding the item exceeds the knapsack capacity
                if self.m_knapsack.optimalWeight + weight <= self.m_knapsack.capacity:
                    self.m_knapsack.optimalCells.append(cell_tuple)
                    self.m_knapsack.optimalWeight += weight
                    self.m_knapsack.optimalValue += value

        self.m_solverPath = path
        self.m_entranceUsed = entrance
        self.m_exitUsed = exit
        self.m_cellsExplored = len(set(self.m_solverPath))
        self.m_reward = self.reward()