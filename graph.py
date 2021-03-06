import tkinter as tk
import random
from typing import Mapping

# ans=1
case1 = ['   /', '/   ']
# ans=2
case2 = ['/']
# ans=2
case3 = ['  /' ' /''/  ']
# ans=1
case4 = [' ']
# ans=8
case5 = ['//\\\\\\', '\\\\/\\/', '\\/\\ \\', '/ \\//', ' / \\  ']
# ans=15
case6 = ['///\\/\\/\\', '////////', '\\\\\\//\\/\\', '/\\/\\\\/\\/']
# ans=23
case7 = ['///\\/\\/\\', '////////', '\\\\\\//\\/\\', '/\\/\\\\/\\/', '///\\/\\/\\', '////////', '\\\\\\//\\/\\', '/\\/\\\\/\\/']


def randomCase(w=0, h=0):
    W = random.randint(5, 15) if w == 0 else w
    H = random.randint(5, 10) if h == 0 else h
    case = []
    for i in range(H):
        case.append(''.join(random.choices(['/', '\\', ' '], weights=[0.45, 0.45, 0.1], k=W)))
    return case

def check_graph_empty(graph):
    if isinstance(graph, list):
        return all(map(check_graph_empty, graph))
    else:
        return False

def connect(p1x, p1y, p2x, p2y):
    global graph
    graph[p1y][p1x].append((p2x, p2y))
    graph[p2y][p2x].append((p1x, p1y))

def check_dreege1_point():
    global graph
    for line in graph:
        for point in line:
            if len(point) == 1:
                return True
    return False

def delete_dreege1_points(px=-1, py=-1):
    global graph
    global w
    global h
    if px == -1 and py == -1:
        for i in range(w+1):
            for j in range(h+1):
                if len(graph[j][i]) == 1:
                    dx, dy = graph[j][i][0]
                    graph[dy][dx].remove((i, j))
                    delete_dreege1_points(dx, dy)
                    graph[j][i] = []
    else:
        if len(graph[py][px]) == 1:
            dx, dy = graph[py][px][0]
            graph[dy][dx].remove((px, py))
            delete_dreege1_points(dx, dy)
            graph[py][px] = []

def delete_dreege2_point():
    global graph
    global w
    global h
    for j in range(max((w+1), (h+1))):
        for i in range(min(j, w+1)):
            if len(graph[j][i]) == 2:
                if len(graph[j][i]) == 2:
                    dx, dy = graph[j][i][0]
                    graph[dy][dx].remove((i, j))
                    dx, dy = graph[j][i][1]
                    graph[dy][dx].remove((i, j))
                    graph[j][i] = []
                    return None
        for i in range(min(j, h+1), -1, -1):
            if len(graph[i][j]) == 2:
                dx, dy = graph[i][j][0]
                graph[dy][dx].remove((j, i))
                dx, dy = graph[i][j][1]
                graph[dy][dx].remove((j, i))
                graph[i][j] = []
                return None

def delete_dreege2_point_old():
    global graph
    global w
    global h
    for i in range(w+1):
        for j in range(h+1):
            if len(graph[j][i]) == 2:
                dx, dy = graph[j][i][0]
                graph[dy][dx].remove((i, j))
                dx, dy = graph[j][i][1]
                graph[dy][dx].remove((i, j))
                graph[j][i] = []
                return None

def draw_graph_dreege():
    global graph
    for line in graph:
        for point in line:
            print(len(point), end=' ')
        print()
    print()

def check_graph_number():
    global graph
    global w
    global h
    count = 0
    mapgraph = [[0 for _ in range(w+1)] for _ in range(h+1)]
    def visitV(px, py):
        for dx, dy in graph[py][px]:
            if mapgraph[dy][dx] == 0:
                mapgraph[dy][dx] = count
                visitV(dx, dy)
    for i in range(w+1):
        for j in range(h+1):
            if len(graph[j][i]) > 0:
                if count == 0:
                    count = count+1
                    mapgraph[j][i] = count
                    visitV(i, j)
                elif mapgraph[j][i] == 0:
                    count = count+1
                    mapgraph[j][i] = count
                    visitV(i, j)
    return count

def tkinterDraw(graph, s=1000):
    c = tk.Canvas(root, height=len(graph)*50-30, width=len(graph[0])*50-30)
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            c.create_oval(j*50+9, i*50+9, j*50+11, i*50+11, fill='#000000')
            if len(graph[i][j]) != 0:
                for x, y in graph[i][j]:
                    c.create_line(j*50+10, i*50+10, x*50+10, y*50+10)
    c.pack()
    def quitAndClean():
        c.destroy()
        root.quit()
    root.after(s, quitAndClean)
    root.mainloop()

if __name__ == '__main__':
    #case=[line.strip().strip('\"').strip('\'').replace("\\\\", "\\") for line in str(input().strip('[]')).split(',')]
    #case = case5
    case = [" /", "/ "]
    #case = randomCase()
    for line in case:
        print(line)
    # generate and initialize graph
    w = len(case[0])
    h = len(case)
    # graph[y][x]=point(x,y)
    graph = [[[] for _ in range(w+1)] for _ in range(h+1)]
    for i in range(w):
        connect(i, 0, i+1, 0)
        connect(i, h, i+1, h)
    for i in range(h):
        connect(0, i, 0, i+1)
        connect(w, i, w, i+1)
    x, y = 0, 0
    for line in case:
        for key in line:
            if key == "/":
                connect(x+1, y, x, y+1)
            if key == "\\":
                connect(x, y, x+1, y+1)
            x = x+1
        x = 0
        y = y+1
    draw_graph_dreege()
    root = tk.Tk()
    tkinterDraw(graph)
    # reuduce edge
    count = 0
    graphCount = check_graph_number()
    while check_dreege1_point():
        delete_dreege1_points()
    while not check_graph_empty(graph):
        print(count, graphCount)
        draw_graph_dreege()
        tkinterDraw(graph)
        count = count+1
        delete_dreege2_point()
        while check_dreege1_point():
            delete_dreege1_points()
        newgraphCount = check_graph_number()
        if newgraphCount > graphCount:
            graphCount = newgraphCount
            count = count-1
        elif newgraphCount < graphCount:
            graphCount = newgraphCount
    print(count)
