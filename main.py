import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    #print(cypher.merge_line("u", "Universe", "uname").return_line().text())

    db.universe.create_universe("RWBY")

    db.close()