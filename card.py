

class Card():
    """
    Class Card
    """

    def __init__(self, value=0, suit=""):
        self.value = value
        self.suit = suit
        self.name = self.get_symbol() # Using symbol for suit
        # self.name = self.get_name() # Using character for suit

    def get_name(self):
        if self.value < 11 and self.value != 1:
            return str(self.value) + self.suit

        alt = {1: "A", 11: "J", 12: "Q", 13: "K"}
        return alt[self.value] + self.suit

    def get_symbol(self):
        symbols = {"S": "\u2660", "C": "\u2663",
                   "H": "\u2665", "D": "\u2666", "": ""}

        if self.value < 11 and self.value != 1:
            return str(self.value) + symbols[self.suit]

        alt = {1: "A", 11: "J", 12: "Q", 13: "K"}
        return alt[self.value] + symbols[self.suit]


if __name__ == "__main__":
    card = Card(13, "C")
    print(card.name)
    print(card.value)
    print(card.suit)
