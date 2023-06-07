import PySimpleGUI as front

from window.utils_radio_button import RadioButtonUtils as rb
from n4j_db.n4j_db import N4J_DB
from n4j_db.n4j_cypher_builder import CypherBuilder

class RelationWindow:
    def __init__(self):
        front.theme("LightGreen10")
        self.db = N4J_DB()

        minor_list = self.getPerson()
        relation_list = self.getAllRelations()
        layout = (
            [front.Column([[front.Text("Relations Window Primary")],
            [front.Radio("Person", "Minor", key="Person"),
             front.Radio("Mask", "Minor", key="Mask"),
             front.Radio("Business", "Minor", key="Business")],
            [front.Radio("Location", "Minor", key="Location"),
             front.Radio("Group", "Minor", key="Group"),
             front.Radio("City", "Minor", key="City"),
             ],
            [front.Listbox(values=minor_list, select_mode="single",
                           key="primary_name", size=(40, 5))]]),
             front.Column([[front.Text("Relationship")],
                [front.Listbox(values=relation_list, select_mode="single",
                    key="relation_selected", size=(40,5))],
                           [front.InputText(key="var1_name", size=(10, 1)),
                            front.InputText(key="var1_value", size=(28, 1))],
                           [front.InputText(key="var2_name", size=(10,1)),
                            front.InputText(key="var2_value", size=(28,1))],
                           ]),
            front.Column([[front.Text("Relations Window Secondary")],
             [front.Radio("Person", "Minor2", key="Person2"),
              front.Radio("Mask", "Minor2", key="Mask2"),
              front.Radio("Business", "Minor2", key="Business2")],
             [front.Radio("Location", "Minor2", key="Location2"),
              front.Radio("Group", "Minor2", key="Group2"),
              front.Radio("City", "Minor2", key="City2"),
              ],
             [front.Listbox(values=minor_list, select_mode="single",
                            key="secondary_name", size=(40, 5))]])],
             [front.Button("Done", disabled=False), front.Button("Event-test"),
                front.Button("Create"), front.Button("Refresh")]
        )
        self.window = front.Window("Persona Relations", layout, modal=True)

    def close(self):
        self.window.close()
        self.db.close()

    def create_relationship(self, values):
        atype = rb.getMinor(values)
        aname = ""
        btype = rb.getMinor(values, "2")
        bname = ""
        rtype = ""
        if len(values["primary_name"]) > 0:
            aname = values["primary_name"][0]
        if len(values["relation_selected"]):
            rtype = values["relation_selected"][0]
        if len(values["secondary_name"]) > 0:
            bname = values["secondary_name"][0]

        if not (aname in (None, "")) and not (bname in (None, "")) \
            and not (atype in (None, "")) and not (btype in (None, "")):
            response, summary, keys = self.db.driver.execute_query(
                CypherBuilder().merge_line("a", atype, "aname")
                    .merge_line("b", btype, "bname")
                    .relation_complex("a", "b", rtype,
                        [(values["var1_name"], values["var1_value"]),
                         (values["var2_name"], values["var2_value"])])
                    .return_line().text(),
                aname=aname,
                bname=bname
            )
        else:
            print("Some critical value was missing")


    def getList(self, item_type):
        returnThis =[]
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_all_line("n", item_type)
                .return_line().text()
        )
        for record in response:
            returnThis.append(record.data().get("n").get("name"))
        returnThis.sort()

        return returnThis


    def getPerson(self):
        return self.getList("Person")

    def getAllRelations(self):
        returnThis =[]
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().custom_line("""MATCH (n)-[r]-() 
                RETURN DISTINCT TYPE(r) AS name;""").text()
        )
        for record in response:
            returnThis.append(record.data().get("name"))
        returnThis.sort()

        return returnThis

    def read(self):
        while True:
            event, values = self.window.read()
            if event in (None, "Done", front.WIN_CLOSED):
                break
            elif event == "Create":
                self.create_relationship(values)
            elif event == "Event-test":
                print(event)
                print(rb.getMinor(values))
                if len(values["primary_name"]) > 0:
                    print(values["primary_name"][0])
                if len(values["relation_selected"]):
                    print(values["relation_selected"][0])
                if values["var1_name"] != "":
                    print(values["var1_name"], ":", values["var1_value"])
                if values["var2_name"] != "":
                    print(values["var2_name"], ":", values["var2_value"])
                print (rb.getMinor(values, "2"))
                if len(values["secondary_name"]) > 0:
                    print(values["secondary_name"][0])

            elif event == "Refresh":
                self.refresh(values)
            else:
                print(event)
        self.close()

    def refresh(self, values):
        node_type = rb.getMinor(values)
        neo_list = self.getList(node_type)
        self.window["primary_name"].Update(neo_list)

        node_type2 = rb.getMinor(values, "2")
        neo_list2 = self.getList(node_type2)
        self.window["secondary_name"].Update(neo_list2)

        self.window["relation_selected"].Update(self.getAllRelations())

if __name__ == "__main__":
    window = RelationWindow()
    window.read()
    window.close()

