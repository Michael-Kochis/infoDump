import PySimpleGUI as front
import bcrypt

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

    def read(self):

        pcrypt = b""
        while True:
            event, values = self.window.read()

            if event in (None, "Cancel"):
                break
            if event in ("Register"):
                pcrypt = bcrypt.hashpw(bytes(values["password"], encoding='utf8'), bcrypt.gensalt(16))
            if event in ("Login"):
                if bcrypt.checkpw(bytes(values["password"], encoding='utf8'), pcrypt):
                    self.window["loginStatus"].Update("MATCH!")
                else:
                    self.window["loginStatus"].Update("Something went wrong.")

    def close(self):
        self.window.close()

if __name__ == "__main__":
    window = MainInfodumpWindow()
    window.read()
    window.close()