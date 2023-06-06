import PySimpleGUI as front

from n4j_db.n4j_db import N4J_DB
from n4j_db.n4j_cypher_builder import CypherBuilder

class SeriesTVWindow:
    def __init__(self):
        front.theme("LightGreen10")
        self.db = N4J_DB()
        series_list = self.getSeries()
        layout = (
            [front.Text("TV Series Window")],
            [front.Listbox(values=series_list, select_mode="single",
                           key="series_name", size=(40, 5))],
            [front.Button("Done", disabled=False), front.Button("Event-test")]
        )
        self.window = front.Window("Infodump Main", layout, modal=True)

    def getSeries(self):
        returnThis =[]
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_all_line("s", "Series_TV")
                .return_line().text()
        )
        for record in response:
            returnThis.append(record.data().get("s").get("name"))
        return returnThis


    def read(self):
        while True:
            event, values = self.window.read()
            if event in (None, "Done", front.WIN_CLOSED):
                break
            elif event == "Done":
                break
            elif event == "Event-test":
                print(event)
                print(values["series_name"])
            elif event == "series_name":
                print(event)
            else:
                print(event)
        self.close()

    def close(self):
        self.window.close()


if __name__ == "__main__":
    window = MainInfodumpWindow()
    window.read()
    window.close()