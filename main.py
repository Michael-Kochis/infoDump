import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()

    db.business.create_city_corp_type("Star City", "Redwood United Bank", "Bank")
    db.group.create_group_member("Star City Police Department", "Stan Washington", "officer")

    db.close()