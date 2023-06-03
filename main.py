import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()

    db.series_t.create_series_person("Arrow", "Scott Morgan")
    db.business.create_city_bank("Star City", "Star City Trust")
    db.series_t.create_series_city("Arrow", "Keystone City")
    db.business.create_universe_corp("Arrowverse", "Stagg Industries")

    db.close()