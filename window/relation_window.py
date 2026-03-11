import tkinter as tk
from tkinter import ttk

from n4j_db.n4j_db import N4J_DB
from n4j_db.n4j_cypher_builder import CypherBuilder


class RelationWindow:
    def __init__(self):
        self.db = N4J_DB()

        self.root = tk.Tk()
        self.root.title("Persona Relations")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.node_mode = tk.StringVar(value="existing")
        self.new_node_name_var = tk.StringVar()

        self.var1_name_var = tk.StringVar()
        self.var1_value_var = tk.StringVar()
        self.var2_name_var = tk.StringVar()
        self.var2_value_var = tk.StringVar()
        self.var3_name_var = tk.StringVar()
        self.var3_value_var = tk.StringVar()

        self._build_ui()
        self.refresh("")
        self.refresh("2")

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        left_col = ttk.Frame(main)
        center_col = ttk.Frame(main)
        right_col = ttk.Frame(main)

        left_col.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
        center_col.grid(row=0, column=1, sticky="nsw", padx=(0, 12))
        right_col.grid(row=0, column=2, sticky="nsw")

        ttk.Label(left_col, text="Relations Window Primary").grid(row=0, column=0, sticky="w", pady=(0, 6))

        ttk.Radiobutton(
            left_col, text="Existing", variable=self.node_mode,
            value="existing"
        ).grid(row=1, column=0, sticky="w", pady=(0, 4))

        ttk.Label(left_col, text="Primary Node Type").grid(row=2, column=0, sticky="w")
        self.node_label_listbox = tk.Listbox(left_col, exportselection=False, height=5, width=40)
        self.node_label_listbox.grid(row=3, column=0, sticky="ew", pady=(0, 6))
        self.node_label_listbox.bind("<<ListboxSelect>>", lambda event: self.refresh(""))

        ttk.Label(left_col, text="Primary Node").grid(row=4, column=0, sticky="w")
        self.section_name_listbox = tk.Listbox(left_col, exportselection=False, height=5, width=40)
        self.section_name_listbox.grid(row=5, column=0, sticky="ew", pady=(0, 6))

        ttk.Radiobutton(
            left_col, text="New Item", variable=self.node_mode,
            value="new"
        ).grid(row=6, column=0, sticky="w", pady=(0, 4))

        self.new_node_name_entry = ttk.Entry(left_col, textvariable=self.new_node_name_var, width=40)
        self.new_node_name_entry.grid(row=7, column=0, sticky="ew")

        ttk.Label(center_col, text="Relationship").grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.relation_selected_listbox = tk.Listbox(center_col, exportselection=False, height=5, width=40)
        self.relation_selected_listbox.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        prop1 = ttk.Frame(center_col)
        prop1.grid(row=2, column=0, sticky="ew", pady=(0, 4))
        ttk.Entry(prop1, textvariable=self.var1_name_var, width=12).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Entry(prop1, textvariable=self.var1_value_var, width=30).pack(side=tk.LEFT)

        prop2 = ttk.Frame(center_col)
        prop2.grid(row=3, column=0, sticky="ew", pady=(0, 4))
        ttk.Entry(prop2, textvariable=self.var2_name_var, width=12).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Entry(prop2, textvariable=self.var2_value_var, width=30).pack(side=tk.LEFT)

        prop3 = ttk.Frame(center_col)
        prop3.grid(row=4, column=0, sticky="ew", pady=(0, 4))
        ttk.Entry(prop3, textvariable=self.var3_name_var, width=12).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Entry(prop3, textvariable=self.var3_value_var, width=30).pack(side=tk.LEFT)

        ttk.Label(right_col, text="Relations Window Secondary").grid(row=0, column=0, sticky="w", pady=(0, 6))

        ttk.Label(right_col, text="Secondary Node Type").grid(row=1, column=0, sticky="w")
        self.node_label2_listbox = tk.Listbox(right_col, exportselection=False, height=5, width=40)
        self.node_label2_listbox.grid(row=2, column=0, sticky="ew", pady=(0, 6))
        self.node_label2_listbox.bind("<<ListboxSelect>>", lambda event: self.refresh("2"))

        ttk.Label(right_col, text="Secondary Node").grid(row=3, column=0, sticky="w")
        self.section_name2_listbox = tk.Listbox(right_col, exportselection=False, height=5, width=40)
        self.section_name2_listbox.grid(row=4, column=0, sticky="ew", pady=(0, 6))

        node_types = self.getAllNodes()
        self._populate_listbox(self.node_label_listbox, node_types)
        self._populate_listbox(self.node_label2_listbox, node_types)
        self._populate_listbox(self.relation_selected_listbox, self.getAllRelations())

        if node_types:
            self.node_label_listbox.selection_set(0)
            self.node_label2_listbox.selection_set(0)

        button_frame = ttk.Frame(main)
        button_frame.grid(row=1, column=0, columnspan=3, sticky="w", pady=(12, 0))

        ttk.Button(button_frame, text="Done", command=self.close).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Delete", command=self._handle_delete).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Rename", command=self._handle_rename).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Create", command=self._handle_create).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Refresh", command=self._handle_refresh).pack(side=tk.LEFT)

    def _populate_listbox(self, listbox, values):
        listbox.delete(0, tk.END)
        for value in values:
            listbox.insert(tk.END, value)

    def _get_selected_listbox_value(self, listbox):
        selection = listbox.curselection()
        if not selection:
            return ""
        return listbox.get(selection[0])

    def _build_values(self):
        return {
            "node_exist": self.node_mode.get() == "existing",
            "new_node": self.node_mode.get() == "new",
            "node_label": [
                self._get_selected_listbox_value(self.node_label_listbox)] if self._get_selected_listbox_value(
                self.node_label_listbox) else [],
            "node_label2": [
                self._get_selected_listbox_value(self.node_label2_listbox)] if self._get_selected_listbox_value(
                self.node_label2_listbox) else [],
            "section_name": [
                self._get_selected_listbox_value(self.section_name_listbox)] if self._get_selected_listbox_value(
                self.section_name_listbox) else [],
            "section_name2": [
                self._get_selected_listbox_value(self.section_name2_listbox)] if self._get_selected_listbox_value(
                self.section_name2_listbox) else [],
            "relation_selected": [
                self._get_selected_listbox_value(self.relation_selected_listbox)] if self._get_selected_listbox_value(
                self.relation_selected_listbox) else [],
            "new_node_name": self.new_node_name_var.get(),
            "var1_name": self.var1_name_var.get(),
            "var1_value": self.var1_value_var.get(),
            "var2_name": self.var2_name_var.get(),
            "var2_value": self.var2_value_var.get(),
            "var3_name": self.var3_name_var.get(),
            "var3_value": self.var3_value_var.get(),
        }

    def _handle_create(self):
        values = self._build_values()
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

    def _handle_delete(self):
        self.delete_node(self._build_values())
        self._handle_refresh()

    def _handle_rename(self):
        self.rename_node(self._build_values())
        self._handle_refresh()

    def _handle_refresh(self):
        self.refresh("")
        self.refresh("2")

    def close(self):
        if getattr(self, "db", None) is not None:
            self.db.close()
            self.db = None
        if getattr(self, "root", None) is not None:
            self.root.destroy()
            self.root = None

    def create_new_node(self, ntype, nname):
        if ntype not in (None, "") and nname not in (None, ""):
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
        atype = ""
        btype = ""
        if len(values["node_label"]) > 0:
            atype = values["node_label"][0]
        if len(values["node_label2"]) > 0:
            btype = values["node_label2"][0]

        bname = ""
        rtype = ""
        if len(values["section_name"]) > 0:
            aname = values["section_name"][0]
        if len(values["relation_selected"]) > 0:
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
            if not (aname in (None, "")) and not (bname in (None, "")) and not (atype in (None, "")) and not (
                    btype in (None, "")):
                response, summary, keys = self.db.driver.execute_query(
                    CypherBuilder().merge_line("a", atype, "aname")
                    .merge_line("b", btype, "bname")
                    .relation_complex("a", "b", rtype, rel_props)
                    .return_line().text(),
                    aname=aname,
                    bname=bname
                )
                a1 = ""
                b1 = ""
                for record in response:
                    a1 = record.data().get("a").get("name")
                    b1 = record.data().get("b").get("name")
                print(a1, "has a", rtype, "relation with", b1)
            else:
                print("Some critical value was missing")

    def delete_node(self, values):
        atype, aname = self.get_atype_aname(values)
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_line("n", atype, "dname")
            .custom_line("DETACH DELETE n;").text(),
            dname=aname
        )
        print(atype, aname, "has been deleted.")

    def get_atype_aname(self, values):
        atype = values["node_label"][0]
        aname = ""
        if len(values["section_name"]) > 0:
            aname = values["section_name"][0]
        return atype, aname

    def getList(self, item_type):
        return_this = []
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_all_line("n", item_type)
            .return_line().text()
        )
        for record in response:
            return_this.append(record.data().get("n").get("name"))
        return_this.sort()

        return return_this

    def getPerson(self):
        return self.getList("Person")

    def getAllNodes(self):
        return_this = []
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().custom_line(
                """MATCH (n) 
                    RETURN DISTINCT labels(n) AS name;"""
            ).text()
        )
        for record in response:
            labels = record.data().get("name")
            if labels not in (None, ""):
                for label in labels:
                    if label not in return_this:
                        return_this.append(label)
        return_this.sort()

        return return_this

    def getAllRelations(self):
        return_this = []
        response, summary, keys = self.db.driver.execute_query(
            CypherBuilder().custom_line(
                """MATCH (n)-[r]-() 
                    RETURN DISTINCT TYPE(r) AS name;"""
            ).text()
        )
        for record in response:
            return_this.append(record.data().get("name"))
        return_this.sort()

        return return_this

    def read(self):
        self.root.mainloop()

    def refresh(self, section=""):
        if section == "":
            node_type = self._get_selected_listbox_value(self.node_label_listbox) or "Person"
            neo_list = self.getList(node_type)
            self._populate_listbox(self.section_name_listbox, neo_list)
        else:
            node_type = self._get_selected_listbox_value(self.node_label2_listbox) or "Person"
            neo_list = self.getList(node_type)
            self._populate_listbox(self.section_name2_listbox, neo_list)

        self._populate_listbox(self.relation_selected_listbox, self.getAllRelations())
        self.refresh_relationship_values()
        self.refresh_new_node_name()

    def refresh_new_node_name(self):
        self.new_node_name_var.set("")

    def refresh_relationship_values(self):
        self.var1_name_var.set("")
        self.var1_value_var.set("")
        self.var2_name_var.set("")
        self.var2_value_var.set("")
        self.var3_name_var.set("")
        self.var3_value_var.set("")

    def rename_node(self, values):
        atype, aname = self.get_atype_aname(values)
        neo_name = values["new_node_name"]
        results, summary, keys = self.db.driver.execute_query(
            CypherBuilder().match_line("n", atype, "nname")
            .custom_line("SET n.name = \"" + neo_name + "\"")
            .return_line().text(),
            nname=aname
        )
        n1 = ""
        for record in results:
            n1 = record.data().get("n").get("name")
        print("Record", n1, "has been updated.")

if __name__ == "__main__":
        window = RelationWindow()
        window.read()