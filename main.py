import pandas as pd
import n4j_db.n4j_db as database

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.planet.create_planet_continent("Terra", "Africa")
    db.planet.create_planet_continent("Terra", "Antarctica")
    db.planet.create_planet_continent("Terra", "Asia")
    db.planet.create_planet_continent("Terra", "Australia")
    db.planet.create_planet_continent("Terra", "Europe")
    db.planet.create_planet_continent("Terra", "North America")
    db.planet.create_planet_continent("Terra", "South America")

    db.close()