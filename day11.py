import queue

def get_neighbors(node,rows,cols):
    x, y = node
    deltas = [(1,0),(-1,0),(0,1),(0,-1)]

    neighbors = []
    for dx,dy in deltas:
        new_x,new_y = x+dx,y+dy

        if 0 <= new_x < rows and 0 <= new_y < cols:
            neighbors.append((new_x,new_y))

    return neighbors

def get_empty_rows_cols(grid,rows,cols):
    # Check for empty rows
    empty_rows = []
    for i in range(rows):
        empty_row = True
        for j in range(cols):
            if grid[i][j] == "#":
                empty_row = False
                break

        if empty_row:
            empty_rows.append(i)

    # Check for empty cols
    empty_cols = []
    for j in range(cols):
        empty_col = True
        for i in range(rows):
            if grid[i][j] == "#":
                empty_col = False
                break
        if empty_col:
            empty_cols.append(j)


    return set(empty_rows),set(empty_cols)

def get_galaxies(grid,rows,cols):
    galaxies = set()
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "#":
                galaxies.add((i,j))

    return galaxies

def dijkstras(grid,start,goals,empty_rows,empty_cols,rows,cols,expansion_constant):
    # Since all weights are 1 we can simply use bfs
    #   as the first encounter of a galaxy will be the shortest path

    dist = {}
    prev = {}
    dist[start] = 0
    q = queue.PriorityQueue()
    for i in range(rows):
        for j in range(cols):
            if (i,j) != start:
                dist[(i,j)] = float('inf')
                prev[(i,j)] = None

            q.put((dist[(i,j)], (i,j)))


    dist[start] = 0


    total_cost = 0
    while not q.empty():
        cost,current = q.get()

        if current in goals:
            goals.remove(current)
            total_cost += cost

        for neighbor in get_neighbors(current,rows,cols):
            i,j = neighbor
            next_cost = dist[current]
            if i in empty_rows or j in empty_cols:
                next_cost += expansion_constant
            else:
                next_cost += 1

            if next_cost < dist[neighbor]:
                dist[neighbor] = next_cost
                prev[neighbor] = current
                q.put((next_cost,neighbor))


    return total_cost


def part1(grid):
    # First identify empty rows/cols
    rows = len(grid)
    cols = len(grid[0])

    empty_rows,empty_cols = get_empty_rows_cols(grid,rows,cols)
    galaxies = get_galaxies(grid,rows,cols)

    total_cost = 0
    for galaxy in galaxies:
        goals = galaxies - set(galaxy)
        total_cost += dijkstras(grid,galaxy,goals,empty_rows,empty_cols,rows,cols,1)


    print("Part 1: ",total_cost//2)


def part2(grid):
    # First identify empty rows/cols
    rows = len(grid)
    cols = len(grid[0])

    empty_rows, empty_cols = get_empty_rows_cols(grid, rows, cols)
    galaxies = get_galaxies(grid, rows, cols)

    total_cost = 0
    for galaxy in galaxies:
        goals = galaxies - set(galaxy)
        total_cost += dijkstras(grid, galaxy, goals, empty_rows, empty_cols, rows, cols, 1000000)

    print("Part 2: ", total_cost // 2)

def main():
    with open("./inputs/day11.txt") as f:
        grid = []
        for line in f:
            grid.append(list(line.strip()))

    #part1(grid)
    part2(grid)





if __name__ == "__main__":
    main()