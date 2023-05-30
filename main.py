import pandas as pd
import n4j_db.n4j_db as database

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.nation.create_continent_nation("Asia", "Qarac")
    db.nation.create_continent_nation("Europe", "Lichtenstein")
    db.nation.create_continent_nation("Asia", "Georgia")
    db.nation.create_continent_nation("Asia", "Saudi Arabia")

    db.close()