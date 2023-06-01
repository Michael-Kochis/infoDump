import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()

    db.bloodline.create_branch("Celts", "Bretons")
    db.bloodline.create_branch("Celts", "Woads")
    db.bloodline.create_branch("Bretons", "Armorica")
    db.bloodline.create_branch("Persian", "Iranian")
    db.bloodline.create_branch("Iranian", "Sarmatian")

    db.close()