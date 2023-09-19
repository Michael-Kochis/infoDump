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
                        key="section_name", enable_events=True,
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
                        enable_events=True, key="section_name2",
                         size=(40, 5))]])],
             [pg.Button("Done", disabled=False), pg.Button("Delete"),
                pg.Button("Rename"),
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
        if len(values["section_name"]) > 0:
            aname = values["section_name"][0]
        if len(values["relation_selected"]):
            rtype = values["relation_selected"][0]
        if len(values["section_name2"]) > 0:
            bname = values["section_name2"][0]

        rel_props = []
        if values["var1_name"] not in (None, ""):
            rel_props.append((values["var1_name"], values["var1_value"]))
        if values["var2_name"] not in (None, ""):
            rel_props.append((values["var2_name"], values["var2_value"]))
        if values["var3_name"] not in (None, ""):
            rel_props.append((values["var3_name"], values["var3_value"]))

        if rtype in (None, ""):
            print("Relation not selected.")
        else:
            if not (aname in (None, "")) and not (bname in (None, "")) \
                and not (atype in (None, "")) and not (btype in (None, "")):
                response, summary, keys = self.db.driver.execute_query(
                    CypherBuilder().merge_line("a", atype, "aname")
                        .merge_line("b", btype, "bname")
                        .relation_complex("a", "b", rtype, rel_props)
                        .return_line().text(),
                    aname=aname,
                    bname=bname
                )
                for record in response:
                    a1 = record.data().get("a").get("name")
                    b1 = record.data().get("b").get("name")
                print(a1, "has a", rtype, "relation with", b1)
            else:
                print("Some critical value was missing")

    def delete_node(self, values):
        atype, aname = self.get_atype_aname(values)
        respons, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_line("n", atype, "dname")
                .custom_line("DETACH DELETE n;").text(),
            dname=aname
        )
        print(atype, aname, "has been deleted.")

    def get_atype_aname(self, values):
        atype = values["node_label"][0]
        if len(values["section_name"]) > 0:
            aname = values["section_name"][0]
        return atype, aname

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
            elif event in ("node_label"):
                self.refresh(values, "")
            elif event in ("node_label2"):
                self.refresh(values, "2")
            elif event in ("Refresh"):
                self.refresh(values, "")
                self.refresh(values, "2")
            elif event in ("section_name", "section_name2"):
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
            elif event == "Rename":
                self.rename_node(values)
            elif event == "Delete":
                self.delete_node(values);
            else:
                print(event)
        self.close()

    def refresh(self, values, section=""):
        if values["node_label" + section] == []:
            values["node_label" + section].append("Person")
        node_type = values["node_label" + section][0]

        neo_list = self.getList(node_type)

        self.window["section_name" + section].Update(neo_list)
        self.window["relation_selected"].Update(self.getAllRelations())
        self.refresh_relationship_values()
        self.refresh_new_node_name()

    def refresh_new_node_name(self):
        self.window["new_node_name"].Update("")

    def refresh_relationship_values(self):

        for i in range(1, 4):
            precursor = "var" + str(i)
            vname = precursor + "_name"
            vvalue = precursor + "_value"
            self.window[vname].Update("")
            self.window[vvalue].Update("")

    def rename_node(self, values):
        atype, aname = self.get_atype_aname(values)
        neo_name = values["new_node_name"]
        results, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_line("n", atype, "nname")
                .custom_line("SET n.name = \"" + neo_name + "\"")
                .return_line().text(),
            nname=aname
        )
        for record in results:
            n1 = record.data().get("n").get("name")
        print("Record", n1, "has been updated.")

if __name__ == "__main__":
    window = RelationWindow()
    window.read()
    window.close()

