import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    #print(cypher.merge_line("u", "Universe", "uname").return_line().text())

    db.rel_person.create_mentor("Nahdar Vebb", "Kit Fisto")
    db.series_t.create_series_person("Clone Wars", "Gree")
    db.species.create_person_species("Gree", "Republic Clone")
    db.sci_fi_loc.create_series_star("Clone Wars", "Bestine")
    db.sci_fi_loc.create_universe_star("Star Wars", "Bespin")

    db.close()