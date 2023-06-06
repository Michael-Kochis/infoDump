import PySimpleGUI as front

from n4j_db.n4j_db import N4J_DB
from n4j_db.n4j_cypher_builder import CypherBuilder

class SeriesWindow:
    def __init__(self):
        front.theme("LightGreen10")
        self.db = N4J_DB()
        series_list = self.getSeriesTV()
        layout = (
            [front.Text("TV Series Window")],
            [front.Radio("TV", "Series", default=True, key="TV"),
             front.Radio("Movie", "Series", key="Movie"),
             front.Radio("Comic", "Series", key="Comic"),
             front.Radio("Book", "Series", key="Book")],
            [front.Listbox(values=series_list, select_mode="single",
                           key="series_name", size=(40, 5))],
            [front.Text("Add:")],
            [front.Radio("Person", "Minor", key="Person"),
             front.Radio("Mask", "Minor", key="Mask"),
             front.Radio("Business", "Minor", key="Business")],
             [front.Radio("Location", "Minor", key="Location"),
             front.Radio("Group", "Minor", key="Group"),
             front.Radio("City", "Minor", key="City"),
             ],
            [front.InputText(key="MinorName")],
            [front.Button("Done", disabled=False), front.Button("Event-test"),
                front.Button("Refresh")]
        )
        self.window = front.Window("Infodump Main", layout, modal=True)

    def getSeries(self, type):
        returnThis =[]
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_all_line("s", type)
                .return_line().text()
        )
        for record in response:
            returnThis.append(record.data().get("s").get("name"))
        return returnThis

    def getSeriesBook(self):
        return self.getSeries("Series_Book")

    def getSeriesComic(self):
        return self.getSeries("Series_Comic")

    def getSeriesMovie(self):
        return self.getSeries("Series_Movie")

    def getSeriesTV(self):
        return self.getSeries("Series_TV")

    def read(self):
        while True:
            event, values = self.window.read()
            if event in (None, "Done", front.WIN_CLOSED):
                break
            elif event == "Event-test":
                print(event)
                print(values["series_name"])
                print(values["MinorName"])
            elif event == "Refresh":
                self.refresh(values)
            else:
                print(event)
        self.close()

    def refresh(self, values):
        neo_list = self.window["series_name"].GetListValues()
        if values["TV"]:
            neo_list = self.getSeriesTV()
        elif values["Movie"]:
            neo_list = self.getSeriesMovie()
        elif values["Comic"]:
            neo_list = self.getSeriesComic()
        elif values["Book"]:
            neo_list = self.getSeriesBook()

        self.window["series_name"].Update(neo_list)

    def close(self):
        self.window.close()


if __name__ == "__main__":
    window = SeriesWindow()
    window.read()
    window.close()