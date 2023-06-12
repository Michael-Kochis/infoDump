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
            minor_1,
            [pg.Listbox(values=minor_list, select_mode="single",
                           key="primary_name", size=(40, 5))]]),
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
                            key="secondary_name", size=(40, 5))]])],
             [pg.Button("Done", disabled=False), pg.Button("Event-test"),
                pg.Button("Create"), pg.Button("Refresh")]
        )
        self.window = pg.Window("Persona Relations", layout, modal=True)

    def close(self):
        self.window.close()
        self.db.close()

    def create_relationship(self, values):
        atype = values["node_label"][0]
        aname = ""
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
            elif event == "Create":
                self.create_relationship(values)
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

            elif event == "Refresh":
                self.refresh(values)
            else:
                print(event)
        self.close()

    def refresh(self, values):
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

