def get_connections(point,type,rows,cols):
    i,j = point
    connections = []

    if type == "|":
        connections.extend([(i-1,j),(i+1,j)])
    elif type == "-":
        connections.extend([(i,j-1),(i,j+1)])
    elif type == "L":
        connections.extend([(i-1,j),(i,j+1)])
    elif type == "J":
        connections.extend([(i-1,j),(i,j-1)])
    elif type == "7":
        connections.extend([(i+1,j),(i,j-1)])
    elif type == "F":
        connections.extend([(i+1,j),(i,j+1)])

    for i in range(len(connections)):
        x,y = connections[i]

        if x < 0 or x >= rows:
            connections.pop(i)

        if y < 0 or y >= cols:
            connections.pop(i)

    return connections

def get_valid_connections(type):
    if type == "|":
        return {"|","L","J","7","F"}
    elif type == "-":
        return {"-","L","J","7","F"}
    elif type == "L":
        return {"-","|","J","7","F"}
    elif type == "J":
        return {"-","|","L","7","F"}
    elif type == "7":
        return {"-","|","L","J","F"}
    elif type == "F":
        return {"-","|","L","J","7"}
    else:
        return None

def get_neighbors(pt,rows,cols):
    x, y = pt
    deltas = [(1,0),(-1,0),(0,1),(0,-1)]

    neighbors = []
    for dx,dy in deltas:
        new_x,new_y = x+dx,y+dy

        if 0 <= new_x < rows and 0 <= new_y < cols:
            neighbors.append((new_x,new_y))

    return neighbors

def get_tile(pt,grid):
    return grid[pt[0]][pt[1]]

def get_cw_cardinal_neighbors(pt):
    neighbors = []
    i,j = pt


    # left,up,right,down
    neighbors.append((i, j - 1))
    neighbors.append((i - 1, j))
    neighbors.append((i, j + 1))
    neighbors.append((i + 1, j))

    return neighbors

def walk_point(pt,grid,walls,rows,cols,delta):
    i,j = pt
    dx,dy = delta

    while 0 <= i < rows and 0 <= j < cols:
        if (i,j) in walls:
            return True

        i += dx
        j += dy

    return False



def part1(grid,start):
    # Part 1

    # starting from "S", each pipe in the loop must be connected to EXACTLY 2 other pipes

    # First put the valid neighboring locations into the queue
    rows = len(grid)
    cols = len(grid[0])



    search_directions = [(x,y) for x,y in get_neighbors(start,rows,cols) if grid[x][y] != "."]

    prev = start
    solution_found = False
    loop = set()
    for search_dir in search_directions:
        q = [search_dir]
        path_count = 2
        loop = set()
        loop.add(start)

        while q:
            current = q.pop()
            i,j = current
            loop.add(current)

            connections = get_connections(current,grid[i][j],rows,cols)
            if len(connections) == 2 and prev in connections:
                connections.remove(prev)
                connection_type = grid[connections[0][0]][connections[0][1]]

                if connection_type == "S": # Found the loop
                    solution_found = True
                    break

                if grid[i][j] in get_valid_connections(connection_type):
                    q.append(connections[0])
                    prev = current

            path_count += 1

        if solution_found:
            print("Part 1: ",path_count//2)
            return loop




def part2(grid,start,main_loop):
    rows,cols = len(grid),len(grid[0])
    total_area = rows*cols

    remaining_area = total_area - len(main_loop)

    # First, identify zones that are not part of the main loop



    zones = []
    visited = set()
    visited.update(main_loop)
    while remaining_area:
        zone = set()

        # Need to add one node to the q to expand upon
        q_ready = False
        q = []
        for node in main_loop:
            for neighbor in get_neighbors(node,rows,cols):
                if neighbor not in visited:
                    q.append(neighbor)
                    q_ready = True
                    break
            if q_ready:
                break


        # Now expand upon the identified node
        while q:
            current = q.pop()
            visited.add(current)
            zone.add(current)

            for neighbor in get_neighbors(current,rows,cols):
                if neighbor not in visited:
                    if get_tile(neighbor,grid) == ".":
                        q.append(neighbor)
                    remaining_area -= 1
        zones.append(zone)

    # Second, identify if those zones are contained by the main loop

    #   a zone is contained when an infinitesimal horizontal and vertical line collides
    #   with walls a both ends
    valid_zones = []
    for i,zone in enumerate(zones):
        pt = list(zone)[0]


        left,top,right,down = get_cw_cardinal_neighbors(pt)

        # Walk each point until hitting a wall
        if not walk_point(left,grid,main_loop,rows,cols,(0,-1)):
            continue
        if not walk_point(top, grid, main_loop, rows, cols, (-1, 0)):
            continue
        if not walk_point(right, grid, main_loop, rows, cols, (0, 1)):
            continue
        if not walk_point(down, grid, main_loop, rows, cols, (1, 0)):
            continue

        valid_zones.append(i)

    print(valid_zones)





    # Lastly, check that zones satisfy the squeak through property

def main():
    with open("./inputs/day10.txt") as f:
        grid = [list(line.strip()) for line in f]

    # Get the starting position
    start = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                start = (i,j)
                break

    assert start is not None

    main_loop = part1(grid,start)

    part2(grid,start,main_loop)



if __name__ == "__main__":
    main()