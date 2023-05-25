import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.person.create_mask("Deathstroke", "Slade Wilson")
    db.title.create_mask_title("Deathstroke", "Terminator")
    db.rel_person.create_mask_kia("Deadshot", "James Holder", "Arrow - S1E3", "rifle")

    db.close()