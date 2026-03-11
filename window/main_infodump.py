import tkinter as tk
from tkinter import ttk

from n4j_db.n4j_db import N4J_DB
from window.main_player_window import MainPlayerWindow
from window.series_window import SeriesWindow
from window.relation_window import RelationWindow


class MainInfodumpWindow:
    login_role = []

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Infodump Main")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.login_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.login_status_var = tk.StringVar(value="Login Not Attempted")

        self._build_ui()
        self.db = N4J_DB()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(main, text="Infodump").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(main, text="   Login   ").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        ttk.Entry(main, textvariable=self.login_var, width=30).grid(row=1, column=1, sticky="ew", pady=(0, 4))

        ttk.Label(main, text="Password").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        ttk.Entry(main, textvariable=self.password_var, width=30, show="*").grid(row=2, column=1, sticky="ew", pady=(0, 4))

        ttk.Label(main, textvariable=self.login_status_var).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(4, 8)
        )

        button_frame = ttk.Frame(main)
        button_frame.grid(row=4, column=0, columnspan=2, sticky="w")

        ttk.Button(button_frame, text="Login", command=self._on_login).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Register", command=self._on_register).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Cancel", command=self.close).pack(side=tk.LEFT)

        main.columnconfigure(1, weight=1)

    def _current_values(self):
        return {
            "login": self.login_var.get(),
            "password": self.password_var.get(),
        }

    def _on_login(self):
        self.do_login(self._current_values())

    def _on_register(self):
        values = self._current_values()
        if self.db.login.login_exists(values["login"]):
            self.login_status_var.set("Login already exists.")
        else:
            self.db.login.register_login(values["login"], values["password"], "Player")
            self.login_status_var.set("Login created: " + values["login"])

    def get_login_roles(self, values):
        if self.db.login.login_exists(values["login"]):
            return self.db.login.get_login_roles(values["login"])
        else:
            return []

    def read(self):
        self.root.mainloop()

    def do_login(self, values):
        if self.db.login.login_exists(values["login"]):
            if self.db.login.login(values["login"], values["password"]):
                self.login_status_var.set("MATCH!")
                self.login_role = self.get_login_roles(values)
                if "DB_Admin" in self.login_role:
                    SeriesWindow().read()
                    RelationWindow().read()
                    MainPlayerWindow(values["login"]).read()
                elif "Player" in self.login_role:
                    MainPlayerWindow(values["login"]).read()
                else:
                    print("No recognized role.")
                    print(self.login_role)
            else:
                self.login_status_var.set("Something went wrong.")
        else:
            self.login_status_var.set("Login does not exist")

    def close(self):
        if getattr(self, "db", None) is not None:
            self.db.close()
            self.db = None
        if getattr(self, "root", None) is not None:
            self.root.destroy()
            self.root = None


if __name__ == "__main__":
    window = MainInfodumpWindow()
    window.read()