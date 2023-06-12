import PySimpleGUI as pg


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
        elif values["Bloodline" + section]:
            returnThis = "Bloodline"
        elif values["Template" + section]:
            returnThis = "Template"
        elif values["Nation" + section]:
            returnThis = "Nation"
        elif values["Address" + section]:
            returnThis = "Address"
        elif values["Position" + section]:
            returnThis = "Position"
        elif values["Title" + section]:
            returnThis = "Title"

        return returnThis
    
    @staticmethod
    def set_minor_buttons(add_string = ""):
        minor_string = "Minor" + add_string
        line1 = [pg.Radio("Person", minor_string, key="Person" + add_string),
             pg.Radio("Mask", minor_string, key="Mask" + add_string),
             pg.Radio("Business", minor_string, key="Business" + add_string)]
        line2 = [pg.Radio("Location", minor_string, key="Location" + add_string),
             pg.Radio("Group", minor_string, key="Group" + add_string),
             pg.Radio("City", minor_string, key="City" + add_string),
             ]
        line3 = [pg.Radio("Bloodline", minor_string, key="Bloodline" + add_string),
            pg.Radio("Template", minor_string, key="Template" + add_string),
            pg.Radio("Nation", minor_string, key="Nation" + add_string),
            ]
        line4 = [pg.Radio("Address", minor_string, key="Address" + add_string),
                 pg.Radio("Position", minor_string, key="Position" + add_string),
                 pg.Radio("Title", minor_string, key="Title" + add_string)
            ]
        return line1, line2, line3, line4

