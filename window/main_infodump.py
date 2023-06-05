import PySimpleGUI as front

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
        print("Value entered", values['login'], ":", values['password'])

    def close(self):
        self.window.close()

if __name__ == "__main__":
    window = MainInfodumpWindow()
    window.read()
    window.close()