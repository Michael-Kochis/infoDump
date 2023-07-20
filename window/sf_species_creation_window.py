import PySimpleGUI as ps

import window.node_select as ns
from n4j_db.n4j_db import N4J_DB

from n4j_db.n4j_cypher_builder import CypherBuilder

class SFSpeciesCreationWindow():
    def __init__(self):
        ps.theme("LightGreen10")
        self.db = N4J_DB()
        srw_list = ["Energy Beam", "Laser", "Sprint Missile"]
        lrw_list = ["Force Beam", "Plasma Torpedo", "Regular Missile"]
        layout = (
          [ps.Text("Name"), ps.InputText(key="SpeciesName", default_text="Alien")],
          [ps.Text("Plural"), ps.InputText(key="SpeciesPlural", default_text="Aliens")],
          [ps.Text("Ownership"), ps.InputText(key="SpeciesOwnership", default_text="Alien", size=(41,1))],
          [ps.Text("Militancy"), ps.InputText(key="RM", default_text=60, size=(4,1)),
                ps.Text("Determination"), ps.InputText(key="RD", default_text=60, size=(4,1)),
                ps.Text("Chauvinism"), ps.InputText(key="RC", default_text=30, size=(4,1))
             ],
            [ps.Text("Outlook"), ps.Text(key="RO", text="50")],
            [ps.Text("Government")],
            [ps.Listbox(key="SFGovernment",size=(40,3), values=["Player"])],
            [ps.Text("Engine Select")],
            [ps.Listbox(key="SpeciesEngine", size=(40,2),
                values=["Inertialess Engine", "Tactical Engine"])],
            [ps.Text("SRW Select")],
            [ps.Listbox(key="SpeciesSRW", size=(40,3), values=srw_list)],
            [ps.Text("LRW Select")],
            [ps.Listbox(key="SpeciesLRW", size=(40,3), values=lrw_list)],
            [ps.Button("Done"), ps.Button("Create"), ps.Button("K3 Select"), ps.Button("Reset")]
        )

        self.window = ps.Window("Starfire Species Creation", layout, modal=True)

    def close(self):
        self.db.close()
        self.window.close()

    def read(self):
        while True:
            event, values = self.window.read()
            if event in (None, "Done", ps.WIN_CLOSED):
                break


if __name__ == "__main__":
    window = SFSpeciesCreationWindow()
    window.read()
    window.close()