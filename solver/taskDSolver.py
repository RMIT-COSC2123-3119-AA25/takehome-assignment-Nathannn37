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
import random


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

    def dynamicKnapsack(self, items: list, capacity: int, num_items: int, filename: str):
        """
        Dynamic 0/1 Knapsack that saves the dynamic programming table as a csv.

        @param items: list of (name, weight, value)
        @param capacity: current remaining knapsack capacity
        @param num_items: number of items still being considered
        @param filename: save name for csv of table (used for testing)
        """
        # Initialize DP table with None
        dp = [[None] * (capacity + 1) for _ in range(num_items + 1)]
        # first row is all 0s
        dp[0] = [0] * (capacity + 1)

        selected_items, selected_weight, max_value = [], 0, 0

        """
        IMPLEMENT ME FOR TASK B
        """
        # list to store the weights of the items
        w = []
        # list to store the values of the items
        v = []

        def MFKnapsack(num_items, capacity): 
            # Base case
            if (num_items == 0 or capacity == 0):
                dp[num_items][capacity]
            # Storing the weights into the weight list
            for i in range(num_items):
                w.append(items[i][1])
            # Storing the values into the value list
            for i in range(num_items):
                v.append(items[i][2])

            # If this position in the dp table is none then
            if dp[num_items][capacity] is None:
                # Checks if the capacity is less than the weight at num_items-1
                if capacity < w[num_items-1]:
                    # Moves up in the table (Doesn't take that item)
                    x = MFKnapsack(num_items-1, capacity)
                else:
                    # (Takes the item)
                    x = max( MFKnapsack(num_items-1, capacity), v[num_items-1] + MFKnapsack(num_items - 1, capacity - w[num_items-1]))
                dp[num_items][capacity] = x
            return dp[num_items][capacity]
        
        max_value = MFKnapsack(num_items, capacity)

        c = capacity

        for i in range(num_items, 0, -1):
            # Checks if the current postion in the dp table is the same value as the value one above it
            # if its not the same than it picked up the item
            if dp[i][c] != dp[i - 1][c]:
                loc, wt, val = items[i - 1]
                selected_items.append(loc)
                selected_weight += wt
                c -= wt

        return selected_items, selected_weight, max_value

    def solveMaze(self, maze: Maze, entrance: Coordinates, exit: Coordinates):
        """
        Moves through the maze cell by cell using neighbours and bfs.
        Tracks every cell entered, including backtracking steps.
        """
        # Initialize knapsack and solver state
        self.m_knapsack.optimalCells = []
        self.m_knapsack.optimalValue = 0
        self.m_knapsack.optimalWeight = 0

        # get the number of items in the maze from the paramaters
        items_in_maze = maze.m_itemParams[0]
        # calculate total weight in maze form item list
        maze_item_weight = sum(weight_value[0] for weight_value in maze.m_items.values())
        # calculate total value in maze from item list
        maze_item_value = sum(weight_value[1] for weight_value in maze.m_items.values())
        
        mazesize = maze.rowNum() * maze.colNum()
        currItems = items_in_maze
        treasureprob = (currItems*maze_item_value)/mazesize
        currValue = maze_item_value

        # Start
        current_cell = entrance
        self.m_solverPath = [current_cell]
        visited = {current_cell}
        self.m_cellsExplored = 1
        mazesize -= 1

        while current_cell != exit:
            # Check for treasure
            cell_tuple = (current_cell.getRow(), current_cell.getCol())
            if cell_tuple in maze.m_items:
                weight, value = maze.m_items[cell_tuple]
                density = (currItems * currValue) / mazesize
                if cell_tuple not in self.m_knapsack.optimalCells:
                    self.m_knapsack.optimalCells.append(cell_tuple)
                    currItems -= 1
                    currValue -= value
                    self.m_knapsack.optimalWeight += weight
                    self.m_knapsack.optimalValue += value

                if density < treasureprob:
                    print("Density below threshold. Moving to exit.")
                    path_to_exit = self.bfs(maze, current_cell, exit)
                    for step in path_to_exit[1:]:
                        self.m_solverPath.append(step)
                        if step not in visited:
                            visited.add(step)
                            self.m_cellsExplored += 1
                    break

            # Explore neighbors
            neighbors = maze.neighbours(current_cell)
            next_cell = None
            list_of_neighbors = []
            for neighbor in neighbors:
                if neighbor not in visited and not maze.hasWall(current_cell, neighbor):
                    list_of_neighbors.append(neighbor)
            # Randomly select an unvisited neighbor if there is a valid one
            if list_of_neighbors:
                next_cell = random.choice(list_of_neighbors)
        
            if not next_cell:
                # Backtrack visted cells till an unvisited cell is found
                found_new_path = False
                for backtrack_index in range(len(self.m_solverPath) - 2, -1, -1):
                    backtrack_cell = self.m_solverPath[backtrack_index]
                    if not maze.hasWall(current_cell, backtrack_cell):
                        current_cell = backtrack_cell
                        self.m_solverPath.append(current_cell)
                        if current_cell not in visited:
                            visited.add(current_cell)
                            self.m_cellsExplored += 1

                        # Look for new direction
                        for neighbor in maze.neighbours(current_cell):
                            if neighbor not in visited and not maze.hasWall(current_cell, neighbor):
                                current_cell = neighbor
                                self.m_solverPath.append(current_cell)
                                visited.add(current_cell)
                                self.m_cellsExplored += 1
                                found_new_path = True
                                break
                        if found_new_path:
                            break
                if not found_new_path:
                    print("Dead end during backtracking.")
                    break
                continue

            # Move forward
            current_cell = next_cell
            self.m_solverPath.append(current_cell)
            if current_cell not in visited:
                visited.add(current_cell)
                self.m_cellsExplored += 1
            mazesize -= 1

        # Final state update
        self.m_entranceUsed = entrance
        self.m_exitUsed = exit
        self.m_reward = self.reward()

        print("Solver path length:", len(self.m_solverPath))
        print("Unique cells visited:", self.m_cellsExplored)
        print("Optimal value:", self.m_knapsack.optimalValue)
