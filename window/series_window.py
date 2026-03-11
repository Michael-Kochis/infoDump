import tkinter as tk
from tkinter import ttk

from n4j_db.n4j_db import N4J_DB
from n4j_db.n4j_cypher_builder import CypherBuilder


class SeriesWindow:
    def __init__(self):
        self.db = N4J_DB()

        self.root = tk.Tk()
        self.root.title("Infodump Main")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.series_type = tk.StringVar(value="TV")
        self.minor_name_var = tk.StringVar()

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)

        ttk.Label(main, text="Series Window").grid(row=0, column=0, sticky="w", pady=(0, 8))

        series_type_frame_1 = ttk.Frame(main)
        series_type_frame_1.grid(row=1, column=0, sticky="w", pady=(0, 4))

        ttk.Radiobutton(
            series_type_frame_1, text="TV", variable=self.series_type,
            value="TV", command=self.refresh
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Radiobutton(
            series_type_frame_1, text="Movie", variable=self.series_type,
            value="Movie", command=self.refresh
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Radiobutton(
            series_type_frame_1, text="Comic", variable=self.series_type,
            value="Comic", command=self.refresh
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Radiobutton(
            series_type_frame_1, text="Book", variable=self.series_type,
            value="Book", command=self.refresh
        ).pack(side=tk.LEFT)

        series_type_frame_2 = ttk.Frame(main)
        series_type_frame_2.grid(row=2, column=0, sticky="w", pady=(0, 8))

        ttk.Radiobutton(
            series_type_frame_2, text="Universe", variable=self.series_type,
            value="Universe", command=self.refresh
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Radiobutton(
            series_type_frame_2, text="GameVerse", variable=self.series_type,
            value="GameVerse", command=self.refresh
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Radiobutton(
            series_type_frame_2, text="Game", variable=self.series_type,
            value="Game", command=self.refresh
        ).pack(side=tk.LEFT)

        self.series_listbox = tk.Listbox(main, exportselection=False, height=5, width=40)
        self.series_listbox.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(main, text="Add:").grid(row=4, column=0, sticky="w", pady=(0, 4))

        ttk.Label(main, text="Node Type").grid(row=5, column=0, sticky="w")
        self.node_listbox = tk.Listbox(main, exportselection=False, height=5, width=40)
        self.node_listbox.grid(row=6, column=0, sticky="ew", pady=(0, 8))
        self._populate_node_types()

        self.minor_name_entry = ttk.Entry(main, textvariable=self.minor_name_var, width=40)
        self.minor_name_entry.grid(row=7, column=0, sticky="ew", pady=(0, 8))

        button_frame = ttk.Frame(main)
        button_frame.grid(row=8, column=0, sticky="w")

        ttk.Button(button_frame, text="Done", command=self.close).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Create", command=self._handle_create).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Refresh", command=self.refresh).pack(side=tk.LEFT)

    def _populate_node_types(self):
        self.node_listbox.delete(0, tk.END)
        for node_name in self.get_nodes():
            self.node_listbox.insert(tk.END, node_name)

    def _get_selected_listbox_value(self, listbox):
        selection = listbox.curselection()
        if not selection:
            return ""
        return listbox.get(selection[0])

    def _handle_create(self):
        self.create_record()
        self.refresh()

    def create_record(self):
        name = self.minor_name_var.get().strip()
        series = self._get_selected_listbox_value(self.series_listbox)
        minor_type = self._get_selected_listbox_value(self.node_listbox)

        if series in (None, ""):
            print("No series selected.")
            return
        if minor_type in (None, ""):
            print("Node type not selected")
            return
        if name in (None, ""):
            print("No name entered.")
            return

        series_type = self.series_type.get()

        if series_type == "TV":
            self.db.common.within(minor_type, name, "Series_TV", series)
        elif series_type == "Movie":
            self.db.common.within(minor_type, name, "Series_Movie", series)
        elif series_type == "Comic":
            self.db.common.within(minor_type, name, "Series_Comic", series)
        elif series_type == "Book":
            self.db.common.within(minor_type, name, "Series_Book", series)
        elif series_type == "Universe":
            self.db.common.within(minor_type, name, "Universe", series)
        elif series_type == "GameVerse":
            self.db.common.within(minor_type, name, "Game", series)
        elif series_type == "Game":
            self.db.common.within(minor_type, name, "Game", series)
        else:
            print("Something went wrong.")

    @staticmethod
    def get_nodes():
        return_this = []
        response, summary, keys = N4J_DB().driver.execute_query(
            CypherBuilder().custom_line(
                """MATCH (n) 
                RETURN DISTINCT labels(n) AS name;"""
            ).text()
        )
        for record in response:
            labels = record.data().get("name")
            if labels not in (None, ""):
                for label in labels:
                    if label not in return_this:
                        return_this.append(label)

        return_this.sort()
        return return_this

    def getBook(self):
        return self.getSeries("Book")

    def getGames(self):
        return self.getSeries("Game")

    def getSeries(self, node_type):
        return_this = []
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_all_line("s", node_type)
            .return_line().text()
        )
        for record in response:
            return_this.append(record.data().get("s").get("name"))
            return_this.sort()

        return return_this

    def getLoneBook(self):
        return self.getSeries("Book")

    def getSeriesBook(self):
        return self.getSeries("Series_Book")

    def getSeriesComic(self):
        return self.getSeries("Series_Comic")

    def getGameVerse(self):
        return self.getSeries("GameVerse")

    def getMovie(self):
        return self.getSeries("Movie")

    def getSeriesMovie(self):
        return self.getSeries("Series_Movie")

    def getSeriesTV(self):
        return self.getSeries("Series_TV")

    def refresh(self):
        series_type = self.series_type.get()

        if series_type == "TV":
            neo_list = self.getSeriesTV()
        elif series_type == "Movie":
            neo_list = self.getMovie()
        elif series_type == "Comic":
            neo_list = self.getSeriesComic()
        elif series_type == "Book":
            neo_list = self.getBook()
        elif series_type == "Universe":
            neo_list = self.getSeries("Universe")
        elif series_type == "GameVerse":
            neo_list = self.getGameVerse()
        elif series_type == "Game":
            neo_list = self.getGames()
        else:
            neo_list = []

        self.series_listbox.delete(0, tk.END)
        for item in neo_list:
            self.series_listbox.insert(tk.END, item)

    def read(self):
        self.root.mainloop()

    def close(self):
        if getattr(self, "db", None) is not None:
            self.db.close()
            self.db = None
        if getattr(self, "root", None) is not None:
            self.root.destroy()
            self.root = None


if __name__ == "__main__":
    window = SeriesWindow()
    window.read()