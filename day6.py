import math
def main():
    with open("./inputs/day6.txt") as f:
        times = [int(num) for num in f.readline().strip().split(':')[1].strip().split(" ") if num != ""]
        dists = [int(num) for num in f.readline().strip().split(':')[1].strip().split(" ") if num != ""]

    wins = []
    for time,dist in zip(times,dists):
        hold = 1
        win_count = 0
        while hold < time:
            if (time - hold) * hold > dist:
                win_count += 1
            hold += 1
        wins.append(win_count)

    part1 = 1
    for win in wins:
        part1 *= win

    print("Part 1: ",part1)

    # Part 2
    part2time = int("".join([str(time) for time in times]))
    part2dist = int("".join([str(dist) for dist in dists]))

    # just going to solve using equations of motions and quadratic equation
    hold_time_1 = (part2time + math.sqrt((part2time ** 2) - 4 * part2dist)) / 2
    hold_time_2 = (part2time - math.sqrt((part2time ** 2) - 4 * part2dist)) / 2

    # now need to check if i need to round up or down
    floor_time_1 = math.floor(hold_time_1)
    if (part2time - floor_time_1) * floor_time_1 > part2dist:
        hold_time_1 = floor_time_1
    else:
        hold_time_1 = math.ceil(hold_time_1)

    floor_time_2 = math.floor(hold_time_2)
    if (part2time - floor_time_2) * floor_time_2 > part2dist:
        hold_time_2 = floor_time_2
    else:
        hold_time_2 = math.ceil(hold_time_2)

    print("Part 2: ",abs(hold_time_2 - hold_time_1) + 1)

if __name__ == "__main__":
    main()