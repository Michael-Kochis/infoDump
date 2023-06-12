import PySimpleGUI as pg

from n4j_db.n4j_db import N4J_DB
from n4j_db.n4j_cypher_builder import CypherBuilder

class NodeSelectWindow:
    def __init__(self):
        self.db = N4J_DB()

    @staticmethod
    def get_nodes():
        returnThis =[]
        response, summary, keys = N4J_DB().driver.execute_query(
            CypherBuilder().custom_line("""MATCH (n) 
                RETURN DISTINCT labels(n) AS name;""").text()
        )
        for record in response:
            returnThis.append(record.data().get("name"))
        returnThis.sort()

        return returnThis

    @staticmethod
    def node_select_layout(add_string=""):
        node_list = NodeSelectWindow.get_nodes()
        layout = [pg.Listbox(values=node_list, select_mode="single",
                           key="node_label" + add_string, size=(40, 5))]
        return layout

if __name__ == "__main__":
    print("Unit testing goes here")