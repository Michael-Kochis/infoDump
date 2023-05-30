import pandas as pd
import n4j_db.n4j_db as database

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.nation.create_series_t_nation("Arrow", "Corto Maltese")
    db.nation.create_series_t_nation("Supergirl", "Kaznia")
    db.nation.create_series_t_nation("Black Lightning", "Markovia")

    db.close()