import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.person.create_person("Count Dooku")
    db.person.create_mask("Darth Tyranus", "Count Dooku")
    db.title.create_person_title("Count Dooku", "Count Dooku of Serenno")

    db.close()