import pandas as pd
import n4j_db.n4j_db as database

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.sci_fi_loc.create_star_planet("Rodia", "Rodia")
    db.sci_fi_loc.create_planet_template("Rodia", "Swamp World")
    db.sci_fi_loc.create_planet_template("Rodia", "Food Importer")

    db.close()