import pandas as pd
import n4j_db.n4j_db as database

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.nation.create_continent_nation("Asia", "China")
    db.nation.create_continent_nation("Asia", "Qarac")
    db.nation.create_continent_nation("Asia", "Russia")
    db.nation.create_continent_nation("Europe", "Kaznia")
    db.nation.create_continent_nation("Europe", "Markovia")
    db.nation.create_continent_nation("Europe", "Russia")
    db.nation.create_continent_nation("North America", "Canada")
    db.nation.create_continent_nation("North America", "United States")
    db.nation.create_continent_nation("South America", "Corto Maltese")

    db.close()