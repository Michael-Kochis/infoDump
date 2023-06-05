import PySimpleGUI as front
import bcrypt

class MainInfodumpWindow:
    def __init__(self):
        front.theme("LightGreen10")
        layout = (
            [front.Text("Infodump")],
            [front.Text("   Login   "),front.InputText(key='login')],
            [front.Text("Password"), front.InputText(key='password')],
            [front.Submit(), front.Cancel()]
        )
        self.window = front.Window("Infodump Main", layout)

    def read(self):
        event, values = self.window.read()
        pcrypt = bcrypt.hashpw(bytes(values["password"], encoding='utf8'), bcrypt.gensalt(16))
        print("Value entered", values['login'], ":", pcrypt)
        if bcrypt.checkpw(bytes(values["password"], encoding='utf8'), pcrypt):
            print("MATCH!")
        else:
            print("Something went wrong.")

    def close(self):
        self.window.close()

if __name__ == "__main__":
    window = MainInfodumpWindow()
    window.read()
    window.close()