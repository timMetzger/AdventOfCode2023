def main():
    cards = []
    with open("./inputs/day4.txt") as f:
        for line in f:
            colon_index = line.index(":")
            winning_line,my_line = line[colon_index+1:].strip().split("|")
            cards.append((
                {int(num) for num in winning_line.strip().split(" ") if num != ""},
                {int(num) for num in my_line.strip().split(" ") if num != ""}))

    total_score = 0
    winning_map = {}
    card_totals = [0] * len(cards)
    for i,card in enumerate(cards):
        shared = card[0].intersection(card[1])
        if shared:
            score = 1
            score *= 2 ** (len(shared) - 1)

            total_score += score
            card_totals[i] = 1

        winning_map[i] = len(shared)


    print("Part 1: ",total_score)

    no_win_count = 0
    for k,v in winning_map.items():
        if v:
            for i in range(k+1,k+v+1):
                if i == len(cards):
                    break
                card_totals[i] += card_totals[k]
        else:
            no_win_count += 1



    print("Part 2: ",sum(card_totals) + no_win_count)



if __name__ == "__main__":
    main()