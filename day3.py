def check_neighbors(data,x,y):
    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    for dx,dy in neighbors:
        new_x = x + dx
        new_y = y + dy

        if 0 <= new_x < len(data) and 0 <= new_y < len(data[0]):
            neighbor_value = data[new_x][new_y]
            if not neighbor_value.isnumeric() and neighbor_value != ".":
                return True

    return False

def capture_numbers(data,x,y):
    # Going to make windows around numbers by walking two pointers left and right
    nums = set()

    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    q = set()
    # Construct neighboring points first this time so we don't duplicate numbers
    for dx,dy in neighbors:
        new_x = x + dx
        new_y = y + dy
        if 0 <= new_x < len(data) and 0 <= new_y < len(data[0]):
            if data[new_x][new_y].isnumeric():
                q.add((new_x,new_y))

    while q:
        new_x,new_y = q.pop()

        start = new_y
        left = start
        right = start

        # First walk new_y to left
        while left >= 0 and data[new_x][left].isnumeric():
            left -= 1

        # Fix left pointer so splicing works correctly
        if not data[new_x][left].isnumeric():
            left += 1

        # Next walk new_y to the right
        while right < len(data[0]) and data[new_x][right].isnumeric():
            right += 1

        # Finally add the number found
        nums.add(int(data[new_x][left:right]))

    return list(nums)



def main():
    with open("./inputs/day3.txt") as f:
        schematic = [line.strip() for line in f]

    # Going to create a window around the number and then check the neighbors around it

    part_numbers = []
    for row,line in enumerate(schematic):
        # Walk across entry line, expanding window when a number is encountered
        i = 0
        while i < len(line):
            if line[i].isnumeric():
                j = i + 1
                while j < len(line) and line[j].isnumeric():
                    j += 1

                left = i
                right = j

                # Walk i forward checking neighbors
                while i <= j - 1:
                    if check_neighbors(schematic,row,i):
                        part_numbers.append(int(line[left:right]))
                        i = j + 1
                        break

                    i += 1
            else:
                i += 1

    print("Part 1:",sum(part_numbers))

    # Part 2
    # going to do something similar but going to parse through looking for gears and then create
    # windows around the neighboring numbers (can only have two)

    count = 0
    for row,line in enumerate(schematic):
        # Check for cogs
        for col,c in enumerate(line):
            if c == "*":
                # Now find neighboring numbers
                nums = capture_numbers(schematic,row,col)
                if len(nums) == 2:
                    count += nums[0] * nums[1]

    print("Part 2:",count)



if __name__ == "__main__":
    main()