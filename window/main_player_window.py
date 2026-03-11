import tkinter as tk
from tkinter import ttk

from n4j_db.n4j_db import N4J_DB
from n4j_db.n4j_cypher_builder import CypherBuilder


class MainPlayerWindow:
    def __init__(self, login="Sir_Mike_K"):
        self.login = login
        self.db = N4J_DB()

        self.root = tk.Tk()
        self.root.title("Game Selection")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.minor_name_var = tk.StringVar()

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)

        ttk.Label(main, text="Game Selefction Window").grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.active_game_listbox = tk.Listbox(main, exportselection=False, height=5, width=40)
        self.active_game_listbox.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self.active_game_listbox.bind("<<ListboxSelect>>", self._on_active_game_select)

        ttk.Label(main, text="Add:").grid(row=2, column=0, sticky="w", pady=(0, 4))

        self.potential_game_listbox = tk.Listbox(main, exportselection=False, height=5, width=40)
        self.potential_game_listbox.grid(row=3, column=0, sticky="ew", pady=(0, 8))
        self.potential_game_listbox.bind("<<ListboxSelect>>", self._on_potential_game_select)

        ttk.Label(main, text="Use Alias").grid(row=4, column=0, sticky="w", pady=(0, 4))

        self.minor_name_entry = ttk.Entry(main, textvariable=self.minor_name_var, width=40)
        self.minor_name_entry.grid(row=5, column=0, sticky="ew", pady=(0, 8))

        button_frame = ttk.Frame(main)
        button_frame.grid(row=6, column=0, sticky="w")

        ttk.Button(button_frame, text="Done", command=self.close).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Create", command=self._handle_create).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Refresh", command=self.refresh).pack(side=tk.LEFT)

    def _get_selected_listbox_value(self, listbox):
        selection = listbox.curselection()
        if not selection:
            return ""
        return listbox.get(selection[0])

    def _clear_selection(self, listbox):
        listbox.selection_clear(0, tk.END)

    def _populate_listbox(self, listbox, values):
        listbox.delete(0, tk.END)
        for value in values:
            listbox.insert(tk.END, value)

    def _on_active_game_select(self, event):
        if self.active_game_listbox.curselection():
            self._clear_selection(self.potential_game_listbox)

    def _on_potential_game_select(self, event):
        if self.potential_game_listbox.curselection():
            self._clear_selection(self.active_game_listbox)

    def _handle_create(self):
        self.create_record()
        self.refresh()

    def close(self):
        if getattr(self, "db", None) is not None:
            self.db.close()
            self.db = None
        if getattr(self, "root", None) is not None:
            self.root.destroy()
            self.root = None

    def create_record(self):
        game_target = self._get_selected_listbox_value(self.potential_game_listbox)
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
        return_this = []
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_all_line("g", "PlayerGameInfo")
            .match_line("l", "Login", "lname")
            .custom_line("WHERE (g)-[:PLAYER]->(l)")
            .return_line().text(),
            lname=login
        )
        for record in response:
            return_this.append(record.data().get("g").get("name"))
            return_this.sort()

        return return_this

    def getPotentialGames(self, login):
        return_this = []
        agames = self.filterActiveGames()

        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder()
            .match_line("l", "Login", "lname")
            .match_all_line("gi", "PlayerGameInfo")
            .match_all_line("g", "GameInstance")
            .custom_line("WHERE NOT (l)<-[:PLAYER]-(gi)-[:GAME]->(g)")
            .return_line().text(),
            lname=login
        )
        for record in response:
            rname = record.data().get("g").get("name")
            if rname in agames:
                print("Discard " + rname)
            elif rname not in return_this:
                return_this.append(rname)
                return_this.sort()

        return_this = [i for i in return_this if i not in agames]
        return return_this

    def filterActiveGames(self):
            return_this = []
            temp_games = self.getActiveGames(self.login)
            for record in temp_games:
                string = record.split(": ")[1]
                return_this.append(string)

            return return_this

    def read(self):
            self.root.mainloop()

    def refresh(self):
            self._clear_selection(self.active_game_listbox)
            self._clear_selection(self.potential_game_listbox)
            self.minor_name_var.set("")

            self._populate_listbox(self.active_game_listbox, self.getActiveGames(self.login))
            self._populate_listbox(self.potential_game_listbox, self.getPotentialGames(self.login))

if __name__ == "__main__":
        window = MainPlayerWindow()
        window.read()