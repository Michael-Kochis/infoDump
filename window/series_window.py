import PySimpleGUI as front

import window.node_select as ns
from n4j_db.n4j_db import N4J_DB

from n4j_db.n4j_cypher_builder import CypherBuilder

class SeriesWindow:
    def __init__(self):
        front.theme("LightGreen10")
        self.db = N4J_DB()
        ns_layout = ns.NodeSelectWindow.node_select_layout()

        series_list = self.getSeriesTV()
        layout = (
            [front.Text("Series Window")],
            [front.Radio("TV", "Series", default=True, enable_events=True, key="TV"),
             front.Radio("Movie", "Series", enable_events=True, key="Movie"),
             front.Radio("Comic", "Series", enable_events=True, key="Comic"),
             front.Radio("Book", "Series", enable_events=True, key="Book")],
            [front.Radio("Universe", "Series", enable_events=True, key="Universe"),
             front.Radio("Game", "Series", enable_events=True, key="Game")],
            [front.Listbox(values=series_list, select_mode="single",
                           key="series_name", size=(40, 5))],
            [front.Text("Add:")],
            ns_layout,
            [front.InputText(key="MinorName")],
            [front.Button("Done", disabled=False),
                 front.Button("Create"), front.Button("Refresh")]
        )
        self.window = front.Window("Infodump Main", layout, modal=True)

    def create_record(self, values):
        name = values["MinorName"]

        series = ""
        if len(values["series_name"]) > 0:
            series = values["series_name"][0]
        minor_type = values["node_label"][0]
        if series in (None, ""):
            print("No series selected.")
        elif values["TV"]:
            self.db.common.within(minor_type, name, "Series_TV", series)
        elif values["Movie"]:
            self.db.common.within(minor_type, name, "Series_TMovie", series)
        elif values["Comic"]:
            self.db.common.within(minor_type, name, "Series_Comic", series)
        elif values["Book"]:
            self.db.common.within(minor_type, name, "Series_Book", series)
        elif values["Universe"]:
            self.db.common.within(minor_type, name, "Universe", series)
        elif values["Game"]:
            self.db.common.within(minor_type, name, "Series_Game", series)
        else:
            print("Something went wrong.")

    def getSeries(self, type):
        returnThis =[]
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_all_line("s", type)
                .return_line().text()
        )
        for record in response:
            returnThis.append(record.data().get("s").get("name"))
            returnThis.sort()

        return returnThis

    def getSeriesBook(self):
        return self.getSeries("Series_Book")

    def getSeriesComic(self):
        return self.getSeries("Series_Comic")

    def getSeriesGame(self):
        return self.getSeries("Series_Game")

    def getSeriesMovie(self):
        return self.getSeries("Series_Movie")

    def getSeriesTV(self):
        return self.getSeries("Series_TV")

    def read(self):
        while True:
            event, values = self.window.read()
            if event in (None, "Done", front.WIN_CLOSED):
                break
            elif event in ("node_label"):
                pass
            elif event in ("Book", "Comic", "Movie",
                "Refresh", "TV", "Universe", "Game"):
                self.refresh(values)
            elif event == "Create":
                self.create_record(values)
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
        elif values["Universe"]:
            neo_list = self.getSeries("Universe")
        elif values["Game"]:
            neo_list = self.getSeriesGame()

        self.window["series_name"].Update(neo_list)

    def close(self):
        self.db.close()
        self.window.close()


if __name__ == "__main__":
    window = SeriesWindow()
    window.read()
    window.close()