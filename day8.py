import math


def main():
    with open("./inputs/day8.txt") as f:
        move_seq = f.readline().strip()
        f.readline()
        mappings = {}
        for line in f:
            key,val = line.strip().split(" = ")
            left = val.split(", ")[0][1:]
            right = val.split(", ")[1][:-1]

            mappings[key] = (left,right)

    # current = "AAA"
    # goal = "ZZZ"
    # i = 0
    n = len(move_seq)
    # while True:
    #     move_dir = move_seq[i % n]
    #
    #     if move_dir == "L":
    #         current = mappings[current][0]
    #     else:
    #         current = mappings[current][1]
    #
    #     if current == goal:
    #         break
    #
    #     i += 1
    #
    # print("Part 1: ",i + 1)


    # Part 2
    # Basically the same thing with some extra work
    current = [key for key in mappings.keys() if key.endswith("A")]
    loop_detection = []
    loops = []
    loop_bounds = [[]]*len(current)
    for i,key in enumerate(current):
        loop_detection.append(set())
        loop_detection[i].add(key)
        loops.append([key])

    valid_loops = [False]*len(current)
    i = 0
    while True:
        move_dir = move_seq[i % n]
        if move_dir == "L":
            current = [mappings[key][0] for i,key in enumerate(current)]
        else:
            current = [mappings[key][1] for i,key in enumerate(current)]


        for j,loop_set in enumerate(loop_detection):
            if current[j] in loop_set and valid_loops[j] and loop_bounds[j] == []:
                bounds = [0,0,0]
                for k,key in enumerate(loops[j]):
                    if key == current[j]:
                        #print("Beginning of loop: ",k)
                        #print("End of loop: ",len(loops[j]) - 1)
                        bounds = [k,len(loops[j]) -1 ,0]
                    elif key.endswith("Z"):
                        #print("Z Location: ",k)
                        bounds[-1] = k
                loop_bounds[j] = bounds
            else:
                if current[j].endswith("Z"):
                    valid_loops[j] = True
                loop_detection[j].add(current[j])
                loops[j].append(current[j])

        if all([len(bounds) for bounds in loop_bounds]):
            lcms = []
            for bound in loop_bounds:
                lcms.append(bound[1])
            print("Part 2: ",math.lcm(*lcms))
            break
        i += 1



if __name__ == "__main__":
    main()