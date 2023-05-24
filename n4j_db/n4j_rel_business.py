from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ

class N4JRelBusiness:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_office_region(self, business, region):
            response, summary, keys = self.driver.execute_query(
                """MERGE (b :Business {name: $bname})
                MERGE (r :Region {name: $rname})
                MERGE (b)-[:OFFICE]->(r)
                RETURN b,r;
                """,
                bname=business,
                rname=region
            )
            for record in response:
                b1 = record.data().get("b").get("name")
                r1 = record.data().get("r").get("name")
            print(b1, "has offices in", r1)

if __name__ == "__main__":
    print("This is where the debugging would go.")