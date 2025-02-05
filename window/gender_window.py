import PySimpleGUI as front

import window.node_select as ns
from n4j_db.n4j_db import N4J_DB

from n4j_db.n4j_cypher_builder import CypherBuilder

class GenderWindow:
    def __init__(self):
        front.theme("LightGreen10")
        self.db = N4J_DB()
        ns_layout = ns.NodeSelectWindow.node_select_layout()
        gender_list = self.getGenderList()
        layout = (
            [front.Text("Missing Gender")],
            [front.Listbox(values=gender_list, select_mode="single",
                           key="gender_list", size=(40, 20))],
            [front.Button("Done", disabled=False),
                front.Button("Male"), front.Button("Female"),
                front.Button("Variable"), front.Button("Neuter")]
        )
        self.window = front.Window("Gender Finder", layout, modal=True)

    def getGenderList(self):
        returnThis = []
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_all_line("p", "Person")
            .where("p.gender IS NULL").limit(20)
            .return_line().text()
        )
        for record in response:
            returnThis.append(record.data().get("p").get("name"))
            returnThis.sort()

        return returnThis

    def close(self):
        self.db.close()
        self.window.close()

    def read(self):
        while True:
            event, values = self.window.read()
            neo_name = ""
            if (values["gender_list"]):
                neo_name = values["gender_list"]
            if event in (None, "Done", front.WIN_CLOSED):
                break
            elif event in ("Male"):
                self.setNodeGender(neo_name, "male")
            elif event in ("Female"):
                self.setNodeGender(neo_name, "female")
            elif event in ("Neuter"):
                self.setNodeGender(neo_name, "neuter")
            elif event in ("Variable"):
                self.setNodeGender(neo_name, "variable")
        self.close()

    def setNodeGender(self, neo_name, neoGender):
        if (neo_name[0]):
            new_name = ""
            new_name += neo_name[0]
            n = len(neo_name)
            for val in range(1, n):
                new_name += ' ' + val;
            response, summary, keys = self.db.driver.execute_query(
                CypherBuilder().match_all_line("p", "Person")
                .where("p.name = \"" + new_name + "\"")
                .node_property("p", "gender", neoGender)
                .return_line().text()
            )
            print("Person " + new_name + "is now gender: " + neoGender)
            neolist = self.getGenderList()
            self.window["gender_list"].Update(neolist)
        else:
            print("Select an individual to engender.")


if __name__ == "__main__":
    window = GenderWindow()
    window.read()
    window.close()