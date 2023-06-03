import pandas as pd
import n4j_db.n4j_db as database
from n4j_db.n4j_cypher_builder import CypherBuilder

if __name__ == "__main__":
    db = database.N4J_DB()

    db.series_t.create_series_city("Arrow", "Coast City")
    db.series_t.create_series_person("Arrow", "Carter Bowen")
    db.rel_person.create_mother_of("Janice Bowen", "Carter Bowen")
    db.business.create_city_corp_type("Star City", "Starling General", "Hospital")

    db.close()