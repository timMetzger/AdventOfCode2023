# Mappings in text file go
# destination range start , source range start, range length
# if see number is not mapped then the number remains the same
from threading import Thread, Lock


def seed_to_location(seed,mappings):
    # Map seed to location
    current_num = seed
    for mapping in mappings:
        for source_range,dest_range in mapping:
            if current_num in range(source_range[0],source_range[1]):
                to_add = current_num - source_range[0]
                current_num = dest_range[0] + to_add
                break
    return current_num

def in_bounds(source_range,mapping_range):
    left,right = source_range
    map_left,map_right = mapping_range

    if left >= map_left and left < map_right:
        if right < map_right:
            return "BOTH"
        if right >= map_right:
            return "LEFT"
    elif left < map_left:
        if right < map_right and right > map_left:
            return "RIGHT"


    return None


def main():
    with open("./inputs/day5.txt") as f:
        seeds = list(map(int,f.readline()[7:].strip().split(" ")))
        mappings = []
        f.readline()
        f.readline()
        mapping_entry = []
        for line in f:
            if line.endswith(":\n"):
                mappings.append(mapping_entry[:])
                mapping_entry = []
            elif line == "\n":
                continue
            else:
                dest_start,source_start,length = map(int,line.strip().split(" "))

                dest_range = (dest_start, dest_start + length)
                source_range = (source_start, source_start + length)

                mapping_entry.append((source_range,dest_range))
        mappings.append(mapping_entry[:])

    locations = []
    for seed in seeds:
        locations.append(seed_to_location(seed,mappings))

    print("Part 1: ",min(locations))


    # Part 2
    seed_ranges = []
    i = 0
    while i < len(seeds):
        seed_ranges.append((seeds[i],seeds[i] + seeds[i+1]))
        i += 2

    # Cases:
    #   left inside mapping range
    #   right inside mapping range
    #   left and right inside mapping range
    #   left and right envelop mapping range
    #   no overlap
    location_ranges = []
    for seed_range in seed_ranges:
        current_ranges = [seed_range]
        for mapping in mappings:
            next_ranges = []
            while len(current_ranges) > 0:
                left,right = current_ranges.pop()
                overlap = False
                for source_range,dest_range in mapping:
                    overlap_type = in_bounds((left,right),source_range)
                    if overlap_type == "BOTH":
                        next_ranges.append((dest_range[0] + (left - source_range[0]),dest_range[0] + (right - source_range[0])))
                        overlap = True
                        break
                    elif overlap_type == "LEFT":
                        next_ranges.append((dest_range[0] + (left - source_range[0]),dest_range[1]))
                        if source_range[1] != right:
                            current_ranges.append((source_range[1],right))
                        overlap = True
                        break
                    elif overlap_type == "RIGHT":
                        next_ranges.append((dest_range[0],dest_range[0] + (right - source_range[0])))
                        if left != source_range[0]:
                            current_ranges.append((left,source_range[0]))
                        overlap = True
                        break
                    elif left < source_range[0] and right > source_range[1]:
                        next_ranges.append((dest_range[0],dest_range[1]))
                        current_ranges.append((left,source_range[0]))
                        current_ranges.append((source_range[1],right))
                        overlap = True
                        break

                if not overlap:
                    next_ranges.append((left,right))

            current_ranges = next_ranges[:]
        location_ranges.extend(current_ranges[:])



    print("Part 2:",min(location_ranges))





if __name__ == "__main__":
    main()