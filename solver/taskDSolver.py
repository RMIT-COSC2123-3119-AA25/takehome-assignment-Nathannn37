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

    # def solveMaze(self, maze: Maze, entrance: Coordinates, exit: Coordinates):
    #     """
    #     Moves through the maze cell by cell using neighbours and bfs.
    #     Tracks every cell entered, including backtracking steps.
    #     """
    #     # Initialize knapsack and solver state
    #     self.m_knapsack.optimalCells = []
    #     self.m_knapsack.optimalValue = 0
    #     self.m_knapsack.optimalWeight = 0

    #     # get the number of items in the maze from the paramaters
    #     items_in_maze = maze.m_itemParams[0]
    #     # calculate total weight in maze form item list
    #     maze_item_weight = sum(weight_value[0] for weight_value in maze.m_items.values())
    #     # calculate total value in maze from item list
    #     maze_item_value = sum(weight_value[1] for weight_value in maze.m_items.values())
        
    #     mazesize = maze.rowNum() * maze.colNum()
    #     currItems = items_in_maze
    #     treasureprob = (currItems*maze_item_value)/mazesize
    #     currValue = maze_item_value

    #     # Start at the entrance
    #     current_cell = entrance
    #     self.m_solverPath = [current_cell]  # Track the full path
    #     visited = set()  # Track visited cells
    #     visited.add(current_cell)
    #     mazesize -= 1 # Decrement for the entrance cell
    #     self.m_cellsExplored += 1

    #     while current_cell != exit:
    #         # Check if the current cell contains an item
    #         cell_tuple = (current_cell.getRow(), current_cell.getCol())
    #         print("MazeSize: ",  mazesize, " Items: ", currItems)
    #         if cell_tuple in maze.m_items:
    #             weight, value = maze.m_items[cell_tuple]
    #             density = (currItems*currValue)/mazesize
    #             print(density)
    #             if density >= treasureprob:
    #                 # if self.m_knapsack.optimalWeight + weight <= self.m_knapsack.capacity:
    #                 if cell_tuple not in self.m_knapsack.optimalCells:
    #                     self.m_knapsack.optimalCells.append(cell_tuple)
    #                     print("Adding item to knapsack: ", cell_tuple)
    #                     currItems -= 1
    #                     currValue -= value
    #                     self.m_knapsack.optimalWeight += weight
    #                     self.m_knapsack.optimalValue += value
    #                 # else:
    #                 #     print("Knapsack is full. Moving to exit.")
    #                 #     path_to_exit = self.bfs(maze, current_cell, exit)
    #                 #     self.m_solverPath.extend(path_to_exit[1:])
    #                 #     break
    #             else:
    #                 if cell_tuple not in self.m_knapsack.optimalCells:
    #                     self.m_knapsack.optimalCells.append(cell_tuple)
    #                     print("Adding item to knapsack: ", cell_tuple)
    #                     currItems -= 1
    #                     self.m_knapsack.optimalWeight += weight
    #                     self.m_knapsack.optimalValue += value
    #                 print("Moving to exit treasureprobabilty.")
    #                 path_to_exit = self.bfs(maze, current_cell, exit)
    #                 self.m_solverPath.extend(path_to_exit[1:])
    #                 break

    #         # Find unvisited neighbors
    #         neighbors = maze.neighbours(current_cell)
    #         next_cell = None
    #         for neighbor in neighbors:
    #             if neighbor not in visited and not maze.hasWall(current_cell, neighbor):
    #                 next_cell = neighbor
    #                 break

    #         # If no unvisited neighbors are found, backtrack
    #         if not next_cell:
    #             found_new_path = False
    #             path_len = len(self.m_solverPath)
                
    #             # Step-by-step backtracking
    #             for backtrack_index in range(path_len - 2, -1, -1):  # Skip the current cell
    #                 backtrack_cell = self.m_solverPath[backtrack_index]

    #                 # Check that there’s no wall between current and backtrack_cell
    #                 if not maze.hasWall(current_cell, backtrack_cell):
    #                     # Move to that cell
    #                     current_cell = backtrack_cell
    #                     self.m_solverPath.append(current_cell)
    #                     # self.m_cellsExplored += 1

    #                     # Look for unvisited neighbor from here
    #                     neighbors = maze.neighbours(current_cell)
    #                     for neighbor in neighbors:
    #                         if neighbor not in visited and not maze.hasWall(current_cell, neighbor):
    #                             # Move to the valid neighbor
    #                             self.m_solverPath.append(neighbor)
    #                             visited.add(neighbor)
    #                             current_cell = neighbor
    #                             # self.m_cellsExplored += 1
    #                             found_new_path = True
    #                             break

    #                     if found_new_path:
    #                         break

    #             if not found_new_path:
    #                 print("Dead end: no valid unvisited neighbor after backtracking.")
    #                 break
    #             continue
    #         # Move to the next cell
    #         print("Moving to next cell: ", next_cell)
    #         current_cell = next_cell
    #         self.m_solverPath.append(current_cell)
    #         visited.add(current_cell)
    #         mazesize -= 1
    #         self.m_cellsExplored += 1

    #     # Update solver state
    #     self.m_entranceUsed = entrance
    #     self.m_exitUsed = exit
    #     self.m_reward = self.reward()

    #     print("solver path: ", len(self.m_solverPath))
    #     print("Visted cells: ", len(visited))
    #     print("Optimal value: ", self.m_knapsack.optimalValue)
    #     print("Total cells explored: ", self.m_cellsExplored)
    def solveMaze(self, maze: Maze, entrance: Coordinates, exit: Coordinates):
        """
        Moves through the maze cell by cell using neighbours and bfs.
        Tracks every cell entered, including backtracking steps.
        """
        # Initialize knapsack and solver state
        self.m_knapsack.optimalCells = []
        self.m_knapsack.optimalValue = 0
        self.m_knapsack.optimalWeight = 0

        # Get maze item stats
        items_in_maze = maze.m_itemParams[0]
        maze_item_value = sum(v for _, v in maze.m_items.values())
        currItems = items_in_maze
        currValue = maze_item_value
        mazesize = maze.rowNum() * maze.colNum()
        treasureprob = (currItems * maze_item_value) / mazesize

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
            for neighbor in neighbors:
                if neighbor not in visited and not maze.hasWall(current_cell, neighbor):
                    next_cell = neighbor
                    break

            if not next_cell:
                # Backtrack
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
