def main():
    with open("./inputs/day2.txt") as f:
        game_data = []
        for i,line in enumerate(f,start=1):
            colon_index = line.index(":")
            line_data = line[colon_index + 1:].strip().split(";")
            blue,red,green = 0,0,0

            for bag in line_data:
                cubes = bag.strip().split(",")
                colors = {"blue": 0, "red": 0, "green": 0}
                for cube in cubes:
                    cube = cube.strip().split(" ")
                    colors[cube[1]] += int(cube[0])

                blue = max(blue,colors["blue"])
                red = max(red,colors["red"])
                green = max(green,colors["green"])



            game_data.append((i,red,green,blue))

        possible_games = []
        cube_set_power = []
        for game in game_data:
            if game[1] <= 12 and game[2] <= 13 and game[3] <= 14:
                possible_games.append(game[0])

            cube_set_power.append(game[1] * game[2] * game[3])

        print("Part 1:",sum(possible_games))
        print("Part 2: ",sum(cube_set_power))


if __name__ == "__main__":
    main()