card_values = {"A":14, "K":13, "Q":12, "T":10, "9":9, "8":8, "7":7, "6":6, "5":5, "4":4, "3":3, "2":2,"J":0}
hand_value_map = {"five of a kind":7,"four of a kind":6,"full house":5,"three of a kind":4,"two pair":3,"one pair":2,"high card":1}

from collections import Counter

class Hand:
    def __init__(self,hand,bid):
        self.hand = hand
        self.bid = bid
        self.type = self.__categorize_hand__()

    def __categorize_hand__(self):
        card_counts = Counter(self.hand)
        card_type_count = len(card_counts)

        #  LOGIC OF PART 2
        if "J" in card_counts:
            j_count = card_counts["J"]

            if card_type_count == 1:
                return hand_value_map["five of a kind"]
            elif card_type_count == 2:
                return hand_value_map["five of a kind"]
            elif card_type_count == 3:
                if j_count != 3 and 3 in card_counts.values(): # this would normally be three of a kind
                    return hand_value_map["four of a kind"]
                elif j_count == 2:
                    return hand_value_map["four of a kind"]
                elif j_count == 1:
                    return hand_value_map["full house"]
                elif j_count == 3:
                    return hand_value_map["four of a kind"]
                else:
                    raise NotImplementedError

            elif card_type_count == 4:
                return hand_value_map["three of a kind"]
            elif card_type_count == 5:
                return hand_value_map["one pair"]
            else:
                return NotImplementedError

        else:
            if card_type_count == 1:
                return hand_value_map["five of a kind"]
            elif card_type_count == 2:
                if 1 in card_counts.values():
                    return hand_value_map["four of a kind"] # four of a kind
                else:
                    return hand_value_map["full house"] # full house
            elif card_type_count == 3:
                if 3 in card_counts.values():
                    return hand_value_map["three of a kind"] # three of a kind
                else:
                    return hand_value_map["two pair"] # two pair
            elif card_type_count == 4:
                return hand_value_map["one pair"] # one pair
            elif card_type_count == 5:
                return hand_value_map["high card"] # high card
            else:
                raise NotImplementedError

    def __gt__(self, other):
        if self.type == other.type:
            for card1,card2 in zip(self.hand,other.hand):
                if card_values[card1] > card_values[card2]:
                    return True
                elif card_values[card1] > card_values[card2]:
                    return False
        elif self.type > other.type:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.type == other.type:
            for card1,card2 in zip(self.hand,other.hand):
                if card_values[card1] < card_values[card2]:
                    return True
                elif card_values[card1] > card_values[card2]:
                    return False
        elif self.type < other.type:
            return True
        else:
            return False

    def __str__(self):
        return f"{''.join(self.hand)} --- {self.type} ---- {'J' in self.hand}"

def main():
    hands = []
    with open("./inputs/day7.txt") as f:
        for line in f:
            hand,bid = line.strip().split(" ")
            hands.append(Hand(list(hand),int(bid)))

    hands = sorted(hands)

    part1 = 0
    for i,hand in enumerate(hands,start=1):
        part1 += i * hand.bid

    print("Part 2: ",part1)

if __name__ == "__main__":
    main()