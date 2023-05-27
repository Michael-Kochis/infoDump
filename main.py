import pandas as pd
import n4j_db.n4j_db as database

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.series_t.create_series_person("Arrow", "Edward Fyers")
    db.common.within("Person", "Amanda Waller", "Universe", "Arrowverse")
    db.series_t.create_series_person("Arrow", "Leo Mueller")
    db.rel_person.create_mask_kia("Green Arrow", "Leo Mueller", "Arrow - S1E5", "arrow")

    db.close()