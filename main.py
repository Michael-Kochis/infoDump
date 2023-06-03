import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()

    db.series_t.create_series_person("Arrow", "Yao Fei")
    db.series_t.create_series_person("Arrow", "Shado Fei")
    db.person.create_mask("Shadow", "Shado Fei")
    db.rel_person.create_father_of("Yao Fei", "Shado Fei")

    db.close()