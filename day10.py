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

def can_squeak_through(pt1,pt2,grid,rows,cols,direction,invalid_coords):
    i1,j1 = pt1
    i2,j2 = pt2

    delta = None
    if direction == "L":
        delta = (0,-1)
    elif direction == "U":
        delta = (-1,0)
    elif direction == "R":
        delta = (0,1)
    elif direction == "D":
        delta = (1,0)
    else:
        raise NotImplementedError

    dx, dy = delta

    while 0 <= i1 < rows and 0 <= j1 < cols:
        if (i1,j1) in invalid_coords or (i2,j2) in invalid_coords:
            break

        if not is_squeak_through((i1,j1),(i2,j2),grid,direction):
            return False



        i1 += dx
        j1 += dy

        i2 += dx
        j2 += dy

    return True


def is_squeak_through(pt1,pt2,grid,direction):
    # Check for vertical and horizontal squeak through

    tile1 = grid[pt1[0]][pt1[1]]
    tile2 = grid[pt2[0]][pt2[1]]

    valid_vertical = set()
    valid_vertical.update([("|","|"),("|","F"),("|","L"),("J","L"),("J","F"),("7","F"),("J","|"),("7","|"),("7","L")])

    valid_horizontal = set()
    valid_horizontal.update([("-","-"),("-","7"),("-","F"),("L","-"),("J","-"),("L","7"),("L","F"),("J","7"),("J","F")])

    # Vertical Squeak Through
    if direction == "U" or direction == "D":
        if (tile1,tile2) in valid_vertical:
            return True
    # Horizontal Squeak Through
    elif direction == "L" or direction == "R":
        if (tile1, tile2) in valid_horizontal:
            return True


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
        loop = []
        loop.append(start)

        while q:
            current = q.pop()
            i,j = current
            loop.append(current)

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
                    q.append(neighbor)
                    visited.add(neighbor)
                    remaining_area -= 1
        if not zone:
            break
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

    # Lastly, check that zones satisfy the squeak through property
    #   a zone will become invalid if it comes into contact with previously
    #   marked invalid zone or the edge of the grid

    # Create set of coords that have already been marked invalid
    invalid_zones = list(set(list(range(len(zones)))).difference(valid_zones))
    invalid_coords = set()
    for i in invalid_zones:
        invalid_coords.update(zones[i])


    for i in valid_zones:
        visited = set()
        q = [list(zones[i])[0]]
        complete = False
        while q and not complete:
            current = q.pop()
            x,y = current
            visited.add(current)

            # Check walls for squeak through
            for neighbor in get_neighbors(current,rows,cols):
                if neighbor in main_loop:
                    visited.add(neighbor)
                    # determine which direction to check squeak through
                    direction = None
                    neighbor1 = None
                    neighbor2 = None
                    if neighbor == (x,y-1): # left
                        direction = "L"
                        neighbor1 = (x-1,y - 1)
                        neighbor2 = (x+1,y - 1)
                    elif neighbor == (x - 1,y): # up
                        direction = "U"
                        neighbor1 = (x - 1,y - 1)
                        neighbor2 = (x - 1,y + 1)
                    elif neighbor == (x,y+1): # right
                        direction = "R"
                        neighbor1 = (x - 1,y + 1)
                        neighbor2 = (x + 1,y + 1)
                    elif neighbor == (x+1,y): # down
                        direction = "D"
                        neighbor1 = (x + 1,y - 1)
                        neighbor2 = (x + 1,y + 1)
                    else:
                        raise NotImplementedError

                    if can_squeak_through(neighbor1,neighbor,grid,rows,cols,direction,invalid_coords):
                        invalid_zones.append(i)
                        invalid_coords.update(list(zones[i]))
                        complete = True
                        break
                    if can_squeak_through(neighbor,neighbor2,grid,rows,cols,direction,invalid_coords):
                        invalid_zones.append(i)
                        invalid_coords.update(list(zones[i]))
                        complete = True
                        break
                elif neighbor not in visited:
                    q.append(neighbor)

    final_zones = set(valid_zones).difference(invalid_zones)

    area = 0
    for i in final_zones:
        area += len(zones[i])

    print("Part 2: ",area)


def part2_with_shoelace_and_pick(loop):

    # Shoelace formula gives area of any ccw oriented set of points that form a polygon
    x, y = zip(*loop)
    area =  0.5 * abs(
        sum(x[i] * y[i - 1] - x[i - 1] * y[i] for i in range(len(loop)))
    )

    # Pick's theorem will give all the integer points inside the polygons area
    print("Part 2: ",int(area - 0.5 * len(loop) + 1))


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

    #part2(grid,start,main_loop)
    part2_with_shoelace_and_pick(main_loop)



if __name__ == "__main__":
    main()