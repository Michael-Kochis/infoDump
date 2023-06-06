import PySimpleGUI as front

from n4j_db.n4j_db import N4J_DB
from window.series_tv_window import SeriesTVWindow

class MainInfodumpWindow:
    def __init__(self):
        front.theme("LightGreen10")
        layout = (
            [front.Text("Infodump")],
            [front.Text("   Login   "),front.InputText(key='login')],
            [front.Text("Password"), front.InputText(key='password')],
            [front.Text("Login Not Attempted", key='loginStatus')],
            [front.Button("Login"), front.Button("Register"), front.Button("Cancel")]
        )
        self.window = front.Window("Infodump Main", layout)
        self.db = N4J_DB()

    def read(self):

        while True:
            event, values = self.window.read()

            if event in (None, "Cancel", front.WIN_CLOSED):
                break
            if event in ("Register"):
                if self.db.login.login_exists(values["login"]):
                    self.window["loginStatus"].Update("Login already exists.")
                else:
                    self.db.login.register_login(values["login"], values["password"], "Player")
                    self.window["loginStatus"].Update("Login created:", values["login"])
            if event in ("Login"):
                if self.db.login.login_exists(values["login"]):
                    if self.db.login.login(values["login"], values["password"]):
                        self.window["loginStatus"].Update("MATCH!")
                        SeriesTVWindow().read()
                    else:
                        self.window["loginStatus"].Update("Something went wrong.")
                else:
                    self.window["loginStatus"].Update("Login does not exist")

    def close(self):
        self.window.close()

if __name__ == "__main__":
    window = MainInfodumpWindow()
    window.read()
    window.close()