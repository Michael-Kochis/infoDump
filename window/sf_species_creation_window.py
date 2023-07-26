import math

import PySimpleGUI as ps

import window.node_select as ns
from n4j_db.n4j_db import N4J_DB

from n4j_db.n4j_cypher_builder import CypherBuilder

class SFSpeciesCreationWindow():
    eng_types = ["Inertialess Engines", "Tactical Drive"]
    gov_types = ["Player"]
    srw_list = ["Energy Beam", "Force Beam", "Laser", "X-Ray Laser"]
    lrw_list = ["Kinetic Weapon", "Plasma Torpedo", "Regular Missile"]

    def __init__(self):
        ps.theme("LightGreen10")
        self.db = N4J_DB()
        layout = (
          [ps.Text("Name"), ps.InputText(key="SpeciesName", default_text="Alien")],
          [ps.Text("Plural"), ps.InputText(key="SpeciesPlural", default_text="Aliens")],
          [ps.Text("Ownership"), ps.InputText(key="SpeciesOwnership", default_text="Alien", size=(41,1))],
          [ps.Text("Militancy"),
           ps.InputText(key="RM", default_text=60, size=(4,1), enable_events=True),
                ps.Text("Determination"),
                ps.InputText(key="RD", default_text=60, size=(4,1), enable_events=True),
                ps.Text("Chauvinism"),
                ps.InputText(key="RC", default_text=30, size=(4,1), enable_events=True)
             ],
            [ps.Text("Outlook"), ps.Text(key="RO", text="50")],
            [ps.Text("Government")],
            [ps.Listbox(key="SFGovernment",size=(40,3), select_mode="single",
                values=self.gov_types)],
            [ps.Text("Engine Select")],
            [ps.Listbox(key="SpeciesEngine", size=(40,2),select_mode="single",
                values=self.eng_types)],
            [ps.Text("SRW Select")],
            [ps.Listbox(key="SpeciesSRW", size=(40,3), select_mode="single",
                values=self.srw_list)],
            [ps.Text("LRW Select")],
            [ps.Listbox(key="SpeciesLRW", size=(40,3), values=self.lrw_list)],
            [ps.Button("Done"), ps.Button("Create"), ps.Button("K3 Select"), ps.Button("Reset")]
        )

        self.window = ps.Window("Starfire Species Creation", layout, modal=True)

    def close(self):
        self.db.close()
        self.window.close()

    def reset_gov(self):
        self.window["SFGovernment"].Update(self.gov_types)

    def reset_engine(self):
        self.window["SpeciesEngine"].Update(self.eng_types)

    def reset_long(self):
        self.window["SpeciesLRW"].Update(self.lrw_list)

    def reset_short(self):
        self.window["SpeciesSRW"].Update(self.srw_list)

    def read(self):
        while True:
            event, values = self.window.read()
            if event in (None, "Done", ps.WIN_CLOSED):
                break
            elif event in ("RM", "RD", "RC"):
                if self.window["RM"].get() in (""):
                  self.window["RM"].Update("0")
                elif self.window["RD"].get() in (""):
                  self.window["RD"].Update("0")
                elif self.window["RC"].get() in (""):
                  self.window["RC"].Update("0")
                self.set_racial_outlook()
            elif event in ("K3 Select"):
                print("K3 Select Pressed")
            elif event in ("Reset"):
                self.set_defaults()
            elif event in ("Create"):
                print("Create Pressed")
            else:
                print(event)

    def set_defaults(self):
        self.window["SpeciesName"].Update("Alien")
        self.window["SpeciesPlural"].Update("Aliens")
        self.window["SpeciesOwnership"].Update("Alien")
        self.window["RM"].Update("60")
        self.window["RD"].Update("60")
        self.window["RC"].Update("30")
        self.set_racial_outlook()
        self.reset_gov()
        self.reset_engine()
        self.reset_long()
        self.reset_short()

    def set_racial_outlook(self):
        self.window["RO"].Update(math.floor(
            (int(self.window["RM"].get()) + int(self.window["RD"].get()) +
             int(self.window["RC"].get()))/3
        ))


if __name__ == "__main__":
    window = SFSpeciesCreationWindow()
    window.read()
    window.close()