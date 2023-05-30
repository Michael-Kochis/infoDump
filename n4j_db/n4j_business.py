from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ

class N4JBusiness:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_city_bank(self, city, business):
        response, summary, keys = self.driver.execute_query(
            """MERGE (c :City {name: $cname})
            MERGE (b :Bank :Business :Corporation {name: $bname})
            MERGE (b)-[:WITHIN]->(c)
            RETURN b, c;
            """,
            bname=business,
            cname=city
        )
        for record in response:
            b1 = record.data().get("b").get("name")
            c1 = record.data().get("c").get("name")
        print(b1, "is a bank in", c1)

    def create_city_business(self, city, business):
        response, summary, keys = self.driver.execute_query(
            """MERGE (c :City {name: $cname})
            MERGE (b :Business {name: $bname})
            MERGE (b)-[:WITHIN]->(c)
            RETURN b, c;
            """,
            bname = business,
            cname = city
        )
        for record in response:
            b1 = record.data().get("b").get("name")
            c1 = record.data().get("c").get("name")
        print(b1, "is a business in", c1)

    def create_city_corp(self, city, business):
        response, summary, keys = self.driver.execute_query(
            """MERGE (c :City {name: $cname})
            MERGE (b :Business :Corporation {name: $bname})
            MERGE (b)-[:WITHIN]->(c)
            RETURN b, c;
            """,
            bname=business,
            cname=city
        )
        for record in response:
            b1 = record.data().get("b").get("name")
            c1 = record.data().get("c").get("name")
        print(b1, "is a corporation in", c1)

    def create_corp_owns_business(self, corp, business):
        response, summary, keys = self.driver.execute_query(
            """MERGE (c :Corporation {name: $cname})
            MERGE (b :Business :Corporation {name: $bname})
            MERGE (c)-[:OWNS]->(b)
            RETURN b, c;
            """,
            bname=business,
            cname=corp
        )
        for record in response:
            b1 = record.data().get("b").get("name")
            c1 = record.data().get("c").get("name")
        print(c1, "owns", b1)