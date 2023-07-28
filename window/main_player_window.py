import PySimpleGUI as front

import window.node_select as ns
from n4j_db.n4j_db import N4J_DB

from n4j_db.n4j_cypher_builder import CypherBuilder

class MainPlayerWindow:
    def __init__(self, login="Sir_Mike_K"):
        self.login = login
        front.theme("LightGreen10")
        self.db = N4J_DB()
        ns_layout = ns.NodeSelectWindow.node_select_layout()

        games_list = self.getActiveGames(login)
        potential_games_list = self.getPotentialGames(login)
        layout = (
            [front.Text("Game Selefction Window")],
            [front.Listbox(values=games_list, select_mode="single",
                          enable_events=True, key="active_game", size=(40, 5))],
            [front.Text("Add:")],
            [front.Listbox(values=potential_games_list, select_mode="single",
                          enable_events=True, key="potential_game", size=(40,5))],
            [front.Text("Use Alias")],
            [front.InputText(key="MinorName")],
            [front.Button("Done", disabled=False),
                 front.Button("Create"), front.Button("Refresh")]
        )
        self.window = front.Window("Game Selection", layout, modal=True)

    def close(self):
        self.db.close()
        self.window.close()

    def create_record(self, values):
        game_target = ""
        if len(values["potential_game"]) > 0:
            game_target = values["potential_game"][0]
        if game_target in (None, ""):
            print("Missing game selection")
        else:
            gi_name = self.login + " : " + game_target
            response, summary, keys = self.db.driver.execute_query(
                CypherBuilder().match_line("g", "GameInstance", "gname")
                .match_line("l", "Login", "lname")
                .merge_line("gi", "PlayerGameInfo", "giname")
                .relation_basic("gi", "l", "PLAYER")
                .relation_basic("gi", "g", "GAME")
                 .return_line().text(),
                gname=game_target,
                giname=gi_name,
                lname=self.login
            )
            l = ""
            g1 = ""
            for record in response:
                g1 = record.data().get("g").get("name")
                l = record.data().get("l").get("name")
            print("Login " + l + " has joined game " + g1)

    def getActiveGames(self, login):
        returnThis = []
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_all_line("g", "PlayerGameInfo")
              .match_line("l", "Login", "lname")
              .custom_line("WHERE (g)-[:PLAYER]->(l)")
              .return_line().text(),
            lname=login
        )
        for record in response:
            returnThis.append(record.data().get("g").get("name"))
            returnThis.sort()

        return returnThis

    def getPotentialGames(self, login):
        returnThis = []
        agames = self.filterActiveGames()

        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder()
              .match_line("l", "Login", "lname")
              .match_all_line("gi", "PlayerGameInfo")
              #.custom_line("WHERE NOT (l)<-[:PLAYER]-(gi)")
              .match_all_line("g", "GameInstance")
              .custom_line("WHERE NOT (l)<-[:PLAYER]-(gi)-[:GAME]->(g)")
              .return_line().text(),
            lname=login
        )
        for record in response:
            rname = record.data().get("g").get("name")
            if rname in agames:
                print("Discard " + rname)
            elif rname not in returnThis:
                returnThis.append(rname)
                returnThis.sort()

        returnThis = [i for i in returnThis if i not in agames]
        return returnThis

    def filterActiveGames(self):
        returnThis = []
        temp_games = self.getActiveGames(self.login)
        for record in temp_games:
            string = record.split(": ")[1]
            returnThis.append(string)

        return returnThis

    def read(self):
        while True:
            event, values = self.window.read()
            if event in (None, "Done", front.WIN_CLOSED):
                break
            elif event in ("potential_game"):
                self.window["active_game"].update(set_to_index=[])
            elif event in ("active_game"):
                self.window["potential_game"].update(set_to_index=[])
            elif event == "Refresh":
                self.refresh()
            elif event == "Create":
                self.create_record(values)
                self.refresh()
            else:
                print(event)
        self.close()

    def refresh(self):
        self.window["active_game"].update(set_to_index=[])
        self.window["potential_game"].update(set_to_index=[])
        self.window["MinorName"].update("")


if __name__ == "__main__":
    window = MainPlayerWindow()
    window.read()
    window.close()