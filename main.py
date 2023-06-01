import pandas as pd
import n4j_db.n4j_db as database

if __name__ == "__main__":
    db = database.N4J_DB()
    #cypher = CypherBuilder()

    db.common.within("Person", "Vortigern", "Universe", "Pendragon")
    db.bloodline.create_person_bloodline("Vortigern", "Scanian")
    db.bloodline.create_person_bloodline("Vortigern", "Brythonic")
    db.bloodline.create_branch("Swedish", "Scanian")
    db.bloodline.create_branch("Dane", "Swedish")
    db.bloodline.create_branch("Welsh", "Brythonic")
    db.bloodline.create_branch("Dane", "Jute")
    db.close()