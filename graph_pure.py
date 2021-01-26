class graph:
    def __init__(self, grid):
        self.w = len(grid[0])
        self.h = len(grid)
        self.grid = [[[] for _ in range(self.w+1)] for _ in range(self.h+1)]
        for i in range(self.w):
            self.connect(i, 0, i+1, 0)
            self.connect(i, self.h, i+1, self.h)
        for i in range(self.h):
            self.connect(0, i, 0, i+1)
            self.connect(self.w, i, self.w, i+1)
        x, y = 0, 0
        for line in grid:
            for key in line:
                if key == "/":
                    self.connect(x+1, y, x, y+1)
                if key == "\\":
                    self.connect(x, y, x+1, y+1)
                x = x+1
            x, y = 0, y+1
        self.count = 0
        graphCount = self.check_graph_number()
        while self.check_dreege1_point():
            self.delete_dreege1_points()
        while not self.check_graph_empty(self.grid):
            self.count = self.count+1
            self.delete_dreege2_point()
            while self.check_dreege1_point():
                self.delete_dreege1_points()
            newgraphCount = self.check_graph_number()
            if newgraphCount > graphCount:
                graphCount = newgraphCount
                self.count = self.count-1
            elif newgraphCount < graphCount:
                graphCount = newgraphCount

    def check_graph_empty(self, grid):
        return all(map(self.check_graph_empty, grid)) if isinstance(grid, list) else False

    def connect(self, p1x, p1y, p2x, p2y):
        self.grid[p1y][p1x].append((p2x, p2y))
        self.grid[p2y][p2x].append((p1x, p1y))

    def check_dreege1_point(self):
        for line in self.grid:
            for point in line:
                if len(point) == 1:
                    return True
        return False

    def delete_dreege1_points(self, px=-1, py=-1):
        if px == -1 and py == -1:
            for i in range(self.w+1):
                for j in range(self.h+1):
                    if len(self.grid[j][i]) == 1:
                        dx, dy = self.grid[j][i][0]
                        self.grid[dy][dx].remove((i, j))
                        self.grid[j][i] = []
                        self.delete_dreege1_points(dx, dy)
        else:
            if len(self.grid[py][px]) == 1:
                dx, dy = self.grid[py][px][0]
                self.grid[dy][dx].remove((px, py))
                self.delete_dreege1_points(dx, dy)
                self.grid[py][px] = []

    def delete_dreege2_point(self):
        for i in range(self.w+1):
            for j in range(self.h+1):
                if len(self.grid[j][i]) == 2:
                    for dx, dy in self.grid[j][i]:
                        self.grid[dy][dx].remove((i, j))
                    self.grid[j][i] = []
                    return None

    def check_graph_number(self):
        count = 0
        mapgraph = [[0 for _ in range(self.w+1)] for _ in range(self.h+1)]
        def visitV(px, py):
            for dx, dy in self.grid[py][px]:
                if mapgraph[dy][dx] == 0:
                    mapgraph[dy][dx] = count
                    visitV(dx, dy)
        for i in range(self.w+1):
            for j in range(self.h+1):
                if len(self.grid[j][i]) > 0:
                    if count == 0 or mapgraph[j][i] == 0:
                        count = count+1
                        mapgraph[j][i] = count
                        visitV(i, j)
        return count

class Solution(object):
    def regionsBySlashes(self, grid):
        g = graph(grid)
        return(g.count)

if __name__ == '__main__':
    case = [" /", "/ "]
    s = Solution()
    print(s.regionsBySlashes(case))