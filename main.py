import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.business.create_city_business("Star City", "Papp Motel")
    db.rel_business.create_business_address("Papp Motel", "1700 Broadway")

    db.close()