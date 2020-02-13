import os
from tabulate import tabulate
from random import choice

from card import Card


class FreeCell():
    """
    The Free Cell Game
    """

    def __init__(self):
        self.table = []
        self.cells = [Card() for _ in range(4)]
        self.foundations = [Card() for _ in range(4)]
        self.create_table()

    def game_loop(self):
        option = ""

        while True:
            self.clear()
            print(self.do_option(option))
            print(self.is_done())
            self.draw_table()
            print("")
            option = input("Option: ")

    def create_table(self):
        """
        Table store tableau in 2d list column by column
        Ex: 
        table = [['5S', 'AD', 'KS', '6C', '10H', 'QS', '3S'],
                ['JD', 'KH', 'AH', 'JH', '7D', '8H', '10D'],
                ['8D', '2H', '10S', '7S', '2S', 'QD', '9H'],
                ['4D', '10C', '8C', '3C', '6H', '9C', '4H'],
                ['5D', 'QC', 'JS', '7H', '2D', 'AS'],
                ['4C', 'KC', '7C', 'AC', 'QH', 'KD'],
                ['4S', '9S', '3D', '2C', '5H', '5C'],
                ['6S', '6D', '9D', '8S', 'JC', '3H']]

        """
        deck = self.create_deck()

        for i in range(8):
            column = []
            flag = 0

            if i > 3:
                flag = 1

            for _ in range(7 - flag):
                card = choice(deck)
                column.append(card)
                deck.remove(card)

            self.table.append(column)

    def create_deck(self):
        """
        Create 52 cards deck
        """
        suits = ["H", "D", "C", "S"]
        deck = []

        for suit in suits:
            for value in range(1, 14):
                deck.append(Card(value, suit))

        return deck

    def do_option(self, option):
        """
        Mapping command to function
        """
        if option == "":
            return ""

        option = option.split(" ")
        command = option[0]

        if command == "h":
            return self.print_menu()
        elif command == "q":
            quit()
        elif len(option) == 3:
            try:
                position = int(option[1])
                destination = int(option[2])
            except:
                return "Invalid command"

            if min(position, destination) < 1 or max(position, destination) > 8:
                return "Invalid move"

            if command == "t2t":
                return self.move_t2t(position - 1, destination - 1)
            elif command == "t2c":
                return self.move_t2c(position - 1, destination - 1)
            elif command == "c2t":
                return self.move_c2t(position - 1, destination - 1)
            elif command == "t2f":
                return self.move_t2f(position - 1, destination - 1)
            elif command == "c2f":
                return self.move_c2f(position - 1, destination - 1)

        return "Invalid command"

    def move_t2t(self, position, destination):
        """
        Move from tableau to tableau
        """
        if self.table[position]:
            card = self.table[position][-1]

            if self.table[destination]:
                destination_card = self.table[destination][-1]
            else:
                destination_card = Card()

            if self.validate_build(card, destination_card):
                self.table[destination].append(card)
                del self.table[position][-1]

                return f"Move {card.name} from Tableau {position + 1} to Tableau {destination + 1}"

        return "Invalid move"

    def move_t2c(self, position, destination):
        """
        Move from tableau to cell
        """
        if -1 < destination < 4:
            if self.cells[destination].value == 0:
                self.cells[destination] = self.table[position].pop()

                return f"Moving {self.cells[destination].name} from Tableau {position + 1} to Cell {destination + 1}"

        return "Invalid move"

    def move_c2t(self, position, destination):
        """
        Move from cell to tableau
        """
        if -1 < position < 4:
            card = self.cells[position]

            if self.table[destination]:
                destination_card = self.table[destination][-1]
            else:
                destination_card = Card()

            if card.value != 0 and self.validate_build(card, destination_card):
                self.table[destination].append(self.cells[position])
                self.cells[position] = Card()

                return f"Moving {self.table[destination][-1].name} from Cell {position + 1} to Tableau {destination + 1}"

        return "Invalid move"

    def move_t2f(self, position, destination):
        """
        Move from tableau to foundation
        """
        if -1 < destination < 4 and self.table[position]:
            card = self.table[position][-1]
            destination_card = self.foundations[destination]

            if self.validate_foundation_build(card, destination_card):
                self.foundations[destination] = self.table[position].pop()

                return f"Moving {self.foundations[destination].name} from Tableau {position + 1} \
                                                                    to Foundation {destination + 1}"

        return "Invalid move"

    def move_c2f(self, position, destination):
        """
        Move from cell to foundation
        """
        if -1 < position < 4 and -1 < destination < 4:
            card = self.cells[position]
            destination_card = self.foundations[destination]

            if card.value != 0 and self.validate_foundation_build(card, destination_card):
                self.foundations[destination] = self.cells[position]
                self.cells[position] = Card()

                return f"Moving {self.foundations[destination].name} from Cell {position + 1}\
                                                                 to Foundation {destination + 1}"

        return "Invalid move"

    def validate_build(self, card, destination_card):
        red = ["H", "D"]

        if destination_card.value == 0:
            return True

        if card.value == destination_card.value - 1:
            if card.suit in red and destination_card.suit not in red:
                return True
            if card.suit not in red and destination_card.suit in red:
                return True

        return False

    def validate_foundation_build(self, card, destination_card):
        if destination_card.value == 0 and card.value == 1:
            return True
        else:
            if card.value == destination_card.value + 1 and card.suit == destination_card.suit:
                return True

        return False

    def is_done(self):
        if all([card.value == 13 for card in self.foundations]):
            return "You win! <q to exit>"

        return ""

    def print_menu(self):
        menu = ["t2f T F -- move from Tableau T to Foundation F",
                "t2c T C -- move from Tableau T to Cell C",
                "t2t T1 T2 -- move from Tableau T1 to Tableau T2",
                "c2t C T -- move from Cell C to Tableau T",
                "c2f C F -- move from Cell C to Foundation F",
                "h -- help (displays the menu of options)",
                "q -- quit"]

        return "\n".join(menu)

    def draw_table(self):
        table_ = self.reshape_table()
        cell_ = [card.name for card in self.cells]
        foundation_ = [card.name for card in self.foundations]

        print(*cell_, sep=" " * 3, end=" " * 9)
        print(*foundation_, sep=" " * 3)
        print("")

        table_ = tabulate(table_,
                          headers=[i for i in range(1, 9)], stralign="right")

        print(table_)

    def reshape_table(self):
        """
        Flip table diagonal for printing

        Ex:
        table = [['5S', 'AD', 'KS', '6C', '10H', 'QS', '3S'],
                ['JD', 'KH', 'AH', 'JH', '7D', '8H', '10D'],
                ['8D', '2H', '10S', '7S', '2S', 'QD', '9H'],
                ['4D', '10C', '8C', '3C', '6H', '9C', '4H'],
                ['5D', 'QC', 'JS', '7H', '2D', 'AS'],
                ['4C', 'KC', '7C', 'AC', 'QH', 'KD'],
                ['4S', '9S', '3D', '2C', '5H', '5C'],
                ['6S', '6D', '9D', '8S', 'JC', '3H']]

        table_ =    [['5S','JD','8D','4D','5D','4C','4S','6S'],
                    ['AD','KH','2H','10C','QC','KC','9S','6D'],
                    ['KS','AH','10S','8C','JS','7C','3D','9D'],
                    ['6C','JH','7S','3C','7H','AC','2C','8S'],
                    ['10H','7D','2S','6H','2D','QH','5H','JC'],
                    ['QS','8H','QD','9C','AS','KD','5C','3H'],
                    ['3S','10D','9H','4H','','','','']]
        """
        table_ = []
        num_of_row = max([len(row) for row in self.table])

        for i in range(num_of_row):
            row = []

            for j in range(8):
                try:
                    name = self.table[j][i].name
                except IndexError:
                    name = ""

                row.append(name)

            table_.append(row)

        return table_

    def clear(self):
        """
        Clear screen
        """
        command = "clear"

        if os.name == "nt":
            command = "cls"

        os.system(command)


if __name__ == "__main__":
    game = FreeCell()
    game.game_loop()
