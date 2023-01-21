# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

from copy import copy


def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "ucs": ucs,
        "astar": astar,
        "astar_multi": astar_multi,
    }.get(searchMethod)(maze)


class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position



def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    paths = [[  maze.getStart() ]]
    objectives = maze.getObjectives()
    total_path = []
    visited = {maze.getStart()}
        
    while(objectives):
        if paths[0][-1] not in objectives:
            found = False
            while not found:
                current_path = paths.pop(0)
                possible_moves = maze.getNeighbors(current_path[-1][0], current_path[-1][1])
                for move in possible_moves:
                    if move not in visited:
                        copy_path = current_path.copy()
                        copy_path.append(move)
                        paths.append(copy_path)
                        visited.add(move)
                        if move in objectives:
                            total_path += copy_path
                            paths = [[move]]
                            found = True
                            objectives.remove(move)
                            visited = {move}
                            break

    return total_path



def dfs(maze):
    """
    Runs DFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    paths = [[  maze.getStart() ]]
    objectives = maze.getObjectives()
    total_path = []
    visited = {maze.getStart()}
        
    while(objectives):
        if paths[0][-1] not in objectives:
            found = False
            while not found:
                current_path = paths.pop()
                possible_moves = maze.getNeighbors(current_path[-1][0], current_path[-1][1])
                for move in possible_moves:
                    if move not in visited:
                        copy_path = current_path.copy()
                        copy_path.append(move)
                        paths.append(copy_path)
                        visited.add(move)
                        if move in objectives:
                            total_path += copy_path
                            paths = [[move]]
                            found = True
                            objectives.remove(move)
                            visited = {move}
                            break

    return total_path
        
        
        

  


def ucs(maze):
    """
    Runs ucs for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """

    # TODO: Write your code here
    import heapq
    paths = [[1, maze.getStart()]]
    objectives = maze.getObjectives()
    total_path = []
    visited = {maze.getStart()}


    while(objectives):
        if paths[0][-1] not in objectives:
            found = False
            while not found:
                current_path = heapq.heappop(paths)
                possible_moves = maze.getNeighbors(current_path[-1][0], current_path[-1][1])
                for move in possible_moves:
                    if move not in visited:
                        copy_path = current_path.copy()
                        copy_path.append(move)
                        copy_path[0] += 1
                        heapq.heappush(paths, copy_path)
                        visited.add(move)
                        if move in objectives:
                            total_path += copy_path[1:]
                            paths = [[1, move]]
                            found = True
                            objectives.remove(move)
                            visited = {move}
                            break

    return total_path

    


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    import heapq

    objective = maze.getObjectives()[0]
    paths = [[1 + abs(objective[0] - maze.getStart()[0]) + abs(objective[1]-maze.getStart()[1]) , maze.getStart() ]]
    visited = {maze.getStart()}
    
        
    while(True):
        current_path = heapq.heappop(paths)  
        possible_moves = maze.getNeighbors(current_path[-1][0], current_path[-1][1])
        for move in possible_moves:
            if move not in visited:
                copy_path = current_path.copy()
                copy_path.append(move)
                copy_path[0] = len(copy_path) +  abs(objective[0] - copy_path[-1][0]) + abs(objective[1] - copy_path[-1][1])
                heapq.heappush(paths, copy_path)
                visited.add(move)
                if move == objective:
                    return copy_path[1:]


    



def astar_multi(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    import heapq
    objectives = maze.getObjectives()

    min_value = float("inf")
    for obj in objectives:
        curr_value = 1 + abs(maze.getStart()[0] - obj[0]) + abs(maze.getStart()[1] - obj[1])
        if curr_value < min_value:
            min_value = curr_value
    paths = [[ min_value ,  maze.getStart() ]]

    total_path = []
    visited = {maze.getStart()}
    


    while(objectives):
        if paths[0][-1] not in objectives:
            found = False
            while not found:
                current_path = heapq.heappop(paths)
                possible_moves = maze.getNeighbors(current_path[-1][0], current_path[-1][1])
                for move in possible_moves:
                    if move not in visited:
                        copy_path = current_path.copy()
                        copy_path.append(move)
                        copy_path[0] = float("inf")
                        for obj in objectives:
                            curr_value = len(current_path)+ abs(current_path[-1][0] - obj[0]) + abs(current_path[-1][1] - obj[1])
                            if curr_value < copy_path[0]:
                                copy_path[0] = curr_value  
                        heapq.heappush(paths, copy_path)
                        visited.add(move)
                        if move in objectives:
                            total_path += copy_path[1:]
                            min_value = float("inf")
                            for obj in objectives:
                                curr_value = 1 + abs(maze.getStart()[0] - obj[0]) + abs(maze.getStart()[1] - obj[1])
                                if curr_value < min_value:
                                    min_value = curr_value
                            paths = [[min_value, move]]
                            found = True
                            objectives.remove(move)
                            visited = {move}
                            break

    return total_path
