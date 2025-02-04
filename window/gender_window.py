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
            [front.Listbox(values=gender_list, select_mode="single",
                           key="gender_list", size=(40, 10))],
        )
        self.window = front.Window("Infodump Main", layout, modal=True)

    def getGenderList(self):
        returnThis = []
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_all_line("p", "Person")
            .where("p.gender IS NULL").limit(10)
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
            if event in (None, "Done", front.WIN_CLOSED):
                break
        self.close()

if __name__ == "__main__":
    window = GenderWindow()
    window.read()
    window.close()