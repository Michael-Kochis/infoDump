

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

    def limit(self, limit):
        self.string += "LIMIT " + str(limit) +"\n"
        return self

    def match_line(self, letter, type, xname):
        self.letters.append(letter)
        self.string += "MATCH (" + letter + " :" \
            + type + " {name: $" + xname + "})\n"
        return self

    def match_all_line(self, letter, type):
        self.letters.append(letter)
        self.string += "MATCH (" + letter + " :" \
            + type + ")\n"
        return self

    def merge_line(self, letter, type, xname):
        self.letters.append(letter)
        self.string += "MERGE (" + letter + " :" \
            + type + " {name: $" + xname + "})\n"
        return self

    def relation_basic(self, start, end, rel_name):
        self.string += "MERGE (" + start + ")-[:" \
            + rel_name + "]->(" + end + ")\n"
        return self

    def relation_complex(self, start, end, rel_name, prop_list):
        self.string += "MERGE (" + start + ")-[r:" + rel_name
        if len(prop_list) > 0:
            self.string += " { "
            iterations = 0
            loops = len(prop_list)
            for entry in prop_list:
                iterations += 1
                if not(entry[0] in (None, "")) and not(entry[1] in (None, "")):
                    self.string += entry[0] + " : \"" + entry[1] + "\""
                    if iterations < loops:
                        self.string += ", "
            self.string += "} "

        self.string += "]->(" + end + ")\n"
        return self

    def where(self, text):
        self.string += "WHERE " + text + "\n"
        return self

    def return_line(self):
        self.string += "RETURN "
        self.string += ", ".join(self.get_letters()) + ";"
        return self

    def text(self):
        return self.string

