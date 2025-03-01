from collections import deque
import sys

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

    def coordinates(self):
        return self.x, self.y        

class PacManTest:
    def __init__(self, grid, start, end, steps, path_and_moves):
        # print("Initializing PacManTest" ,start,end)
        self.grid = self._read_map_from_file(grid)
        # print(self.grid)
        self.start, self.end = self._find_start_end(self.grid)
        self.steps = self._shortest_path_bfs(self.grid, self.start, self.end)
        self.expected_start = (self.start.x, self.start.y)
        self.expected_end = (self.end.x, self.end.y)
        self.expected_steps = self.steps
        self.input_start = start
        self.input_end = end
        self.input_steps = steps
        self.path_and_moves = path_and_moves
        
    def _read_map_from_file(self, filename):
        grid = []
        with open(filename, 'r') as file:
            for line in file:
                row = line.strip()
                grid.append(list(row))
        return grid

    def _find_start_end(self, grid):
        start, end = None, None
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 'a':
                    start = Node(i, j)
                elif grid[i][j] == 'f':
                    end = Node(i, j)
                if start and end:
                    return start, end

    def _shortest_path_bfs(self, grid, start, end):
        queue = deque()
        visited = set()
        queue.append(start)
        visited.add((start.x, start.y))

        while queue:
            current = queue.popleft()

            if current.x == end.x and current.y == end.y:
                path_length = 0
                while current.parent:
                    path_length += 1
                    current = current.parent
                return path_length

            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                new_x, new_y = current.x + dx, current.y + dy

                if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] != "*" and (new_x, new_y) not in visited:
                    neighbor = Node(new_x, new_y)
                    neighbor.parent = current
                    queue.append(neighbor)
                    visited.add((new_x, new_y))

        return None

    def _is_path_possible(self, path, moves, food_position, board):
        agent_position = path[0]

        for move in moves:
            if move == 1:  # Up
                agent_position = (agent_position[0] - 1, agent_position[1])
            elif move == 2:  # Right
                agent_position = (agent_position[0], agent_position[1] + 1)
            elif move == 3:  # Down
                agent_position = (agent_position[0] + 1, agent_position[1])
            elif move == 4:  # Left
                agent_position = (agent_position[0], agent_position[1] - 1)

            if agent_position[0] >= 0 and agent_position[0] < len(board) and agent_position[1] >= 0 and agent_position[1] < len(board[0]):
                if board[agent_position[0]][agent_position[1]] == '*':
                    return False

            if agent_position == food_position:
                return True

        return False

    def compare_results(self):
        if self.input_start == self.expected_start and self.input_end == self.expected_end and self.input_steps == self.expected_steps:
            print("Results match the expected values.")
            print(self.expected_start)
        else:
            if self.input_start != self.expected_start:
                print("start do not match the expected values:")
                print("expected_start:", self.expected_start)
                print("your start:", self.input_start)
            if self.input_end != self.expected_end:
                print("end do not match the expected values.")
                print("expected_end:", self.expected_end)
                print("your end:", self.input_end)
            if self.input_steps != self.expected_steps:
                print("steps do not match the expected values.")
                print("expected_steps:", self.expected_steps)
                print("your steps:", self.input_steps)

    def _read_input_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            start = tuple(map(int, filter(None, lines[0].strip().replace('(', '').replace(')', '').split(','))))
            end = tuple(map(int, filter(None, lines[1].strip().replace('(', '').replace(')', '').split(','))))
            steps = int(lines[2].strip())
            path_and_moves = eval(lines[-1].strip())
        return start, end, steps, path_and_moves

    def path(self):
        if self.steps:
            print("path found :)")
        else:
            print("No path found!")
            sys.exit(1)
        print("-------------------------------")

        result = self._is_path_possible(self.path_and_moves, self.path_and_moves[1:], self.expected_end, self.grid)

        if result:
            print("It is possible to reach the food from this path.")
        else:
            print("It is not possible to reach the food from this path.")
        print("-------------------------------")

