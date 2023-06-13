import PySimpleGUI as pg

import window.node_select as ns
from n4j_db.n4j_db import N4J_DB
from n4j_db.n4j_cypher_builder import CypherBuilder

class RelationWindow:
    def __init__(self):
        pg.theme("LightGreen10")
        self.db = N4J_DB()

        minor_list = self.getPerson()
        relation_list = self.getAllRelations()
        minor_1 = ns.NodeSelectWindow.node_select_layout()
        second_1 = ns.NodeSelectWindow.node_select_layout("2")

        layout = ([pg.Column([[pg.Text("Relations Window Primary")],
            [pg.Radio("Existing", "NeoNode", default=True, key="node_exist")],
            minor_1,
            [pg.Listbox(values=minor_list, select_mode="single",
                        key="primary_name", enable_events=True,
                        size=(40, 5))],
            [pg.Radio("New Item", "NeoNode", key="new_node")],
            [pg.InputText(key="new_node_name", size=(40, 1))]]
            ),
             pg.Column([[pg.Text("Relationship")],
                [pg.Listbox(values=relation_list, select_mode="single",
                    key="relation_selected", size=(40,5))],
               [pg.InputText(key="var1_name", size=(10, 1)),
                pg.InputText(key="var1_value", size=(28, 1))],
               [pg.InputText(key="var2_name", size=(10,1)),
                pg.InputText(key="var2_value", size=(28,1))],
               [pg.InputText(key="var3_name", size=(10,1)),
                pg.InputText(key="var3_value", size=(28,1))]
               ]),
            pg.Column([[pg.Text("Relations Window Secondary")],
             second_1,
             [pg.Listbox(values=minor_list, select_mode="single",
                        enable_events=True, key="secondary_name",
                         size=(40, 5))]])],
             [pg.Button("Done", disabled=False), pg.Button("Event-test"),
                pg.Button("Create"), pg.Button("Refresh")]
        )
        self.window = pg.Window("Persona Relations", layout, modal=True)

    def close(self):
        self.window.close()
        self.db.close()

    def create_new_node(self, ntype, nname):
        if ntype not in (None, "") and not nname in (None, ""):
            response, summary, keys = self.db.driver.execute_query(
                CypherBuilder().merge_line("n", ntype, "neoName")
                    .return_line().text(),
                neoName=nname
            )
            for record in response:
                n1 = record.data().get("n").get("name")
                print("Node", n1, "added to database.")
        else:
            print("Missing critical values")

    def create_relationship(self, values, aname=""):
        atype = values["node_label"][0]
        btype = values["node_label2"][0]
        bname = ""
        rtype = ""
        if len(values["primary_name"]) > 0:
            aname = values["primary_name"][0]
        if len(values["relation_selected"]):
            rtype = values["relation_selected"][0]
        if len(values["secondary_name"]) > 0:
            bname = values["secondary_name"][0]

        rel_props = []
        if values["var1_name"] not in (None, ""):
            rel_props.append((values["var1_name"], values["var1_value"]))
        if values["var2_name"] not in (None, ""):
            rel_props.append((values["var2_name"], values["var2_value"]))
        if values["var3_name"] not in (None, ""):
            rel_props.append((values["var3_name"], values["var3_value"]))

        if not (aname in (None, "")) and not (bname in (None, "")) \
            and not (atype in (None, "")) and not (btype in (None, ""))\
            and not (rtype in (None, "")):
            response, summary, keys = self.db.driver.execute_query(
                CypherBuilder().merge_line("a", atype, "aname")
                    .merge_line("b", btype, "bname")
                    .relation_complex("a", "b", rtype, rel_props)
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

    def getAllNodes(self):
        returnThis =[]
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().custom_line("""MATCH (n) 
                RETURN DISTINCT TYPE(n) AS name;""").text()
        )
        for record in response:
            returnThis.append(record.data().get("name"))
        returnThis.sort()

        return returnThis

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
            if event in (None, "Done", pg.WIN_CLOSED):
                break
            elif event in ("node_label", "node_label2", "Refresh"):
                self.refresh(values)
            elif event in ("primary_name", "secondary_name"):
                pass
            elif event == "Create":
                if values["node_exist"]:
                    self.create_relationship(values)
                elif values["new_node"]:
                    if len(values["node_label"]) > 0:
                        node_type = values["node_label"][0]
                        node_name = values["new_node_name"]
                        self.create_new_node(node_type, node_name)
                    else:
                        print("Missing node type.")
                else:
                    print("Invalid value")
            elif event == "Event-test":
                print(event)
                print(values["node_label"][0])
                if len(values["primary_name"]) > 0:
                    print(values["primary_name"][0])
                if len(values["relation_selected"]):
                    print(values["relation_selected"][0])
                if values["var1_name"] != "":
                    print(values["var1_name"], ":", values["var1_value"])
                if values["var2_name"] != "":
                    print(values["var2_name"], ":", values["var2_value"])
                if len(values["secondary_name"]) > 0:
                    print(values["secondary_name"][0])
            else:
                print(event)
        self.close()

    def refresh(self, values):
        if values["node_label"] == []:
            values["node_label"].append("Person")
        if values["node_label2"] == []:
            values["node_label2"].append("Person")
        node_type = values["node_label"][0]
        node_type2 = values["node_label2"][0]

        neo_list = self.getList(node_type)
        neo_list2 = self.getList(node_type2)

        self.window["primary_name"].Update(neo_list)
        self.window["secondary_name"].Update(neo_list2)

        self.window["relation_selected"].Update(self.getAllRelations())

if __name__ == "__main__":
    window = RelationWindow()
    window.read()
    window.close()

