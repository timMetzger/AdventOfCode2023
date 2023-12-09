def main():
    with open("./inputs/day9.txt") as f:
        readings = [list(map(int,line.strip().split(" "))) for line in f]

    # Part 1

    # First construct the differences until a row of zeros
    differences = []
    for history in readings:
        current = history
        history_diffs = [history[:]]
        while sum([val != 0 for val in current]):
            diff = []
            for i in range(len(current) - 1):
                diff.append(current[i+1] - current[i])

            history_diffs.append(diff)
            current = diff[:]
        differences.append(history_diffs[:])

    # Now work back up the differences to extrapolate the values
    extrapolated_values = []
    for diffs in differences:
        current = 0
        for i in range(len(diffs)-2,-1,-1):
            current += diffs[i][-1]

        extrapolated_values.append(current)

    print("Part 1: ",sum(extrapolated_values))

    # Part 2

    # same thing but extrapolate backwards
    extrapolated_values = []
    for diffs in differences:
        current = 0
        for i in range(len(diffs)-2,-1,-1):
            current = diffs[i][0] - current

        extrapolated_values.append(current)

    print("Part 2: ",sum(extrapolated_values))

if __name__ == "__main__":
    main()