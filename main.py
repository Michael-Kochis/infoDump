import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.series_m.create_series_person("Star Wars Movies", "Watto")
    db.species.create_person_species("Watto", "Toydarian")

    db.close()