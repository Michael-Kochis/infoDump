

class CypherBuilder:
    def __init__(self):
        self.string = ""
        self.letters = []

    def get_letters(self):
        self.letters.sort()
        return self.letters

    def merge_line(self, letter, type, xname):
        self.letters.append(letter)
        self.string += "MERGE (" + letter + " :" \
            + type + " {name: $" + xname + "})\n"
        return self

    def return_line(self):
        self.string += "RETURN "
        self.string += self.string.join(self.get_letters()) + ";"
        return self

    def text(self):
        return self.string

