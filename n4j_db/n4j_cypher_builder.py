

class CypherBuilder:
    def __init__(self):
        self.string = ""
        self.letters = []

    def clear(self):
        self.string = ""
        self.letters = []
        return self

    def custom_line(self, newline, new_letters=()):
        self.string += newline + "\n"
        for neoletter in new_letters:
            self.letters.append(neoletter)
        return self

    def get_letters(self):
        self.letters.sort()
        return self.letters

    def merge_line(self, letter, type, xname):
        self.letters.append(letter)
        self.string += "MERGE (" + letter + " :" \
            + type + " {name: $" + xname + "})\n"
        return self

    def relation_basic(self, start, end, rel_name):
        self.string += "MERGE (" + start + ")-[:" \
            + rel_name + "]->(" + end + ")\n"
        return self

    def return_line(self):
        self.string += "RETURN "
        self.string += ", ".join(self.get_letters()) + ";"
        return self

    def text(self):
        return self.string

