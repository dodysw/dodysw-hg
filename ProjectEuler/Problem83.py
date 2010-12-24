from time import time
st = time()

def djikstra3():
    nodes = dict([[(y,x), int(cell)] for y,row in enumerate(file("matrix.txt").read().split("\n")) for x,cell in enumerate(row.split(","))])
    max_x = max_y = 79
    dist = dict.fromkeys(nodes, float("inf"))
    dist[0,0] = nodes[0,0]
    
    while nodes:
        y,x = min(nodes, key=dist.get)
        del nodes[(y,x)]
        if x == max_x and y == max_y:
            break
        right, down, up, left = (y, x+1), (y+1, x), (y-1, x), (y, x-1)
        if x == 0:
            neighbors = [right, down, up]
        elif y == 0:
            neighbors = [right, down, left]
        elif y == max_y:
            neighbors = [right, up, left]
        else:
            neighbors = [right, up, down, left]

        for i,j in neighbors:
            if (i,j) in nodes:
                next_dist = dist[y,x] + nodes[i,j]
                if next_dist < dist[i,j]:
                    dist[i,j] = next_dist

    return dist[y,x]
print "ans:", djikstra3()
print time()-st