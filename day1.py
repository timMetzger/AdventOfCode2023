

def main():
    number_mapping = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
    with open("./inputs/day1.txt") as f:

        # Part 1 solution
        # nums = []
        # for line in f:
        #     num = []
        #     for c in line:
        #         if c.isnumeric():
        #             num.append(c)
        #
        #     if len(num) == 1:
        #         nums.append(int(num[0] + num[0]))
        #     else:
        #         nums.append(int(num[0] + num[-1]))
        #
        # print("Part 1: ",sum(nums))

        # Part 2 solution
        # i think a sliding window would work here where the window starts at a length of the longest word as a number
        # if char at i is numeric then advance i and j
        # if char at i is not numeric then check the window
        nums = []
        for line in f:
            num = []
            i = 0
            while i < len(line):
                j = i + 5
                if line[i].isnumeric():
                    num.append(line[i])
                else:
                    # step back j if out of bounds
                    while j >= len(line):
                        j -= 1

                    # Check if the window contains a number in word form
                    while j - i >= 3:
                        window = line[i:j]
                        if window in number_mapping:
                            num.append(number_mapping[window])
                            break
                        j -= 1

                i += 1

            if len(num) == 1:
                nums.append(int(num[0] + num[0]))
            else:
                nums.append(int(num[0] + num[-1]))

        print("Part 2: ",sum(nums))



if __name__ == "__main__":
    main()