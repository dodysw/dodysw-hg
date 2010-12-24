from time import time
st = time()


#http://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
def djikstra(starting_pos=[0,0]):
    y,x = starting_pos
    nodes = nodes_orig.copy()
    print "Djikstra", starting_pos
    #Let the node at which we are starting be called the initial node. 
    #Let the distance of node Y be the distance from the initial node to Y. 
    #Dijkstra's algorithm will assign some initial distance values and will try to improve them step by step.

    #"Assign to every node a distance value. Set it to zero for our initial node and to 
    #infinity for all other nodes."
    # my note: assume None is infinity, avoiding which number to choose as maximum
    dist = dict.fromkeys(nodes, float("inf"))
    
    # for this problem, the starting has initial distance
    dist[y,x] = nodes[y,x]
    
    #"Mark all nodes as unvisited. Set initial node as current."
    while nodes:
        #If all nodes have been visited, finish. Otherwise, set the unvisited node with the smallest 
        #distance (from the initial node) as the next "current node" and continue from step 3.
        current_node_key = min(nodes, key=dist.get)
        current_node_val = nodes.pop(current_node_key)

        y,x = current_node_key
        #print "Curr:%s(%s) Distance:%s" % ( current_node_key, current_node_val, dist[current_node_key])
                
        #for this problem, we stop at right side
        if x == max_x:
            break
                                
        #For current node, consider all its unvisited neighbors and calculate their tentative 
        # distance (from the initial node). For example, if current node (A) has distance of 6, 
        # and an edge connecting it with another node (B) is 2, the distance to B through A will be 6+2=8. 
        # If this distance is less than the previously recorded distance (infinity in the beginning, 
        # zero for the initial node), overwrite the distance.
        
        #-neighbor can be at up, right, down, except on first column, neighbor is only right (since going up/down will always make the distance longer)
        right, down, up = (y, x+1), (y+1, x), (y-1, x)
        if x == 0:
            neighbors = [right]
        elif y == 0:
            neighbors = [right, down]
        elif y == max_y:
            neighbors = [right, up]
        else:
            neighbors = [right, up, down]

        for i,j in neighbors:
            if (i,j) in nodes:
                dist[i,j] = min(dist[i,j], dist[y,x] + nodes[i,j])
    
        #When we are done considering all neighbors of the current node, mark it as visited. 
        #A visited node will not be checked ever again; its distance recorded now is final and minimal.

    return dist[y,x]

def djikstra_left2right():
    nodes = dict([[(y,x), int(cell)] for y,row in enumerate(file("matrix.txt").read().split("\n")) for x,cell in enumerate(row.split(","))])
    max_x = max_y = 79
    dist = dict.fromkeys(nodes, float("inf"))
    for y in xrange(max_y+1):
        dist[y,0] = nodes[y,0]
    
    while nodes:
        y,x = min(nodes, key=dist.get)
        del nodes[(y,x)]
        if x == max_x:
            break
        right, down, up = (y, x+1), (y+1, x), (y-1, x)
        if x == 0:
            neighbors = [right]
        elif y == 0:
            neighbors = [right, down]
        elif y == max_y:
            neighbors = [right, up]
        else:
            neighbors = [right, up, down]

        for i,j in neighbors:
            if (i,j) in nodes:
                next_dist = dist[y,x] + nodes[i,j]
                if next_dist < dist[i,j]:
                    dist[i,j] = next_dist

    return dist[y,x]

def djikstra_left2right_array():
    nodes = [map(int, row.split(",")) for row in file("matrix.txt").read().split("\n")]
    max_y = max_x = 79
    dist = [[float("inf")] * max_x]*max_y
    for y in xrange(max_y+1):
        dist[y][0] = nodes[y][0]
    
    while nodes:
        y,x = min(nodes, key=dist.get)
        current_node_val = nodes.pop((y,x))
        if x == max_x:
            break
        right, down, up = (y, x+1), (y+1, x), (y-1, x)
        if x == 0:
            neighbors = [right]
        elif y == 0:
            neighbors = [right, down]
        elif y == max_y:
            neighbors = [right, up]
        else:
            neighbors = [right, up, down]

        for i,j in neighbors:
            if (i,j) in nodes:
                next_dist = dist[y,x] + nodes[i,j]
                if next_dist < dist[i,j]:
                    dist[i,j] = next_dist

    return dist[y,x]

#try1 (SLOW)
#nodes_orig = dict([[(y,x), int(cell)] for y,row in enumerate(file("matrix.txt").read().split("\n")) for x,cell in enumerate(row.split(","))])
#max_x = max_y = 79       
#print "ans:", min([djikstra([y,0]) for y in xrange(max_y+1)])
#260324

print "ans:", djikstra_left2right()
print time()-st