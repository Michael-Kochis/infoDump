

class RadioButtonUtils:
    @staticmethod
    def getMinor(values, section=""):
        returnThis = ''

        if values["Person" + section]:
            returnThis = "Person"
        elif values["Mask" + section]:
            returnThis = "Mask"
        elif values["Location" + section]:
            returnThis = "Location"
        elif values["Business" + section]:
            returnThis = "Business"
        elif values["Group" + section]:
            returnThis = "Group"
        elif values["City" + section]:
            returnThis = "City"

        return returnThis

