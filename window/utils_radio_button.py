

class RadioButtonUtils:
    @staticmethod
    def getMinor(values):
        returnThis = ''

        if values["Person"]:
            returnThis = "Person"
        elif values["Mask"]:
            returnThis = "Mask"
        elif values["Location"]:
            returnThis = "Location"
        elif values["Business"]:
            returnThis = "Business"
        elif values["Group"]:
            returnThis = "Group"
        elif values["City"]:
            returnThis = "City"

        return returnThis

