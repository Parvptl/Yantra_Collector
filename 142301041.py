class YantraCollector:
    """
    YantraCollector class to solve the yantra collection puzzle.
    The player must collect all yantras sequentially and reach the exit.
    """
    
    def __init__(self, grid):
        self.grid = grid
        self.n = len(grid)
        self.start = self.find_position('P')
        self.exit = None
        self.yantras = self.find_all_yantras()
        self.revealed_yantra = self.find_position('Y1')
        self.collected_yantras = 0
        self.total_frontier_nodes = 0
        self.total_explored_nodes = 0
    
    def find_position(self, symbol):
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == symbol:
                    return (i, j)
        return None

    def find_all_yantras(self):
        positions = {}
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j].startswith('Y'):
                    positions[int(self.grid[i][j][1:])] = (i, j)
                elif self.grid[i][j] == 'E':
                    self.exit = (i, j)
        return positions

    def reveal_next_yantra_or_exit(self):
        self.collected_yantras += 1
        if self.collected_yantras + 1 in self.yantras:
            self.revealed_yantra = self.yantras[self.collected_yantras + 1]
        elif self.collected_yantras == len(self.yantras):
            self.revealed_yantra = self.exit
        else:
            self.revealed_yantra = None

    def goal_test(self, position):
        if self.collected_yantras<len(self.yantras):
            return position == self.revealed_yantra
            
        return position == self.exit

    def get_neighbors(self, position):
        i, j = position
        neighbors = []
        directions = [(-1,0), (0, 1), (1,0), (0, -1)]
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.n and 0 <= nj < self.n and (self.grid[ni][nj] !='#' and self.grid[ni][nj]!='T'):
                neighbors.append((ni, nj))
        
        return neighbors
    
    def bfs(self):
        if self.collected_yantras==0 :
            queue = [(self.start, [])]
        else:
            queue = [(self.yantras[self.collected_yantras],[])]
        explored = []        
        
        while queue:
            (current, path) = queue.pop(0)           
            explored.append(current)
            new_path = path + [current]
            
            if self.goal_test(current):
                return new_path, len(queue), len(explored)
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in explored and neighbor not in [i[0] for i in queue]:
                    queue.append((neighbor, new_path))
                    
        
        return None, len(queue), len(explored)
    
    def dfs(self):
        if self.collected_yantras==0 :
            stack = [(self.start, [])]
        else:
            stack = [(self.yantras[self.collected_yantras],[])]
    
        explored = []
    
        
        while stack:
            (current, path) = stack.pop(0)
            if current in explored:
                continue
            explored.append(current)
            new_path = path + [current]
            
            if self.goal_test(current):
                return new_path, len(stack), len(explored)
            
            for neighbor in reversed(self.get_neighbors(current)):
                if neighbor not in explored and neighbor not in [i[0] for i in stack]:
                    stack.insert(0,(neighbor, new_path))
                
        
        return None, len(stack), len(explored)
    
    def solve(self, strategy):
        path = []
        while self.collected_yantras != len(self.yantras)+1:
            if strategy == "BFS":
                p1, fn, en = self.bfs()
            else:
                p1, fn, en = self.dfs()
            if p1:
                path.extend(p1[0:len(p1)-1])
            else:
                return None, self.total_frontier_nodes, self.total_explored_nodes

            self.total_frontier_nodes += fn
            self.total_explored_nodes += en

            self.start = self.revealed_yantra
            self.reveal_next_yantra_or_exit()

        path.append(self.find_position('E'))
        
        return path, self.total_frontier_nodes, self.total_explored_nodes

if __name__ == "__main__":
    grid = [
        ['P', '.', '.', '#', 'Y2'],
        ['#', 'T', '.', '#', '.'],
        ['.', '.', 'Y1', '.', '.'],
        ['#', '.', '.', 'T', '.'],
        ['.', '.', '.', '.', 'E']
    ]

    game = YantraCollector(grid)
    strategy =   "DFS"
    solution, total_frontier, total_explored = game.solve(strategy)

    if solution:
        print("Solution Path:", solution)
        print("Total Frontier Nodes:", total_frontier)
        print("Total Explored Nodes:", total_explored)
    else:
        print("No solution found.")
