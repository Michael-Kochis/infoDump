from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder

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

    def create_business_address(self, business, address):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("a", "Address", "aname")
                .merge_line("b", "Business", "bname")
                .relation_basic("b", "a", "HEADQUARTERS")
                .return_line().text(),
            aname=address,
            bname=business
        )
        for record in response:
            a1 = record.data().get("a").get("name")
            b1 = record.data().get("b").get("name")
        print(b1, "has headquarters at", a1)

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

    def create_series_business(self, series, business):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("s", "Series", "sname")
                .merge_line("b", "Business", "bname")
                .return_line().text(),
            sname=series,
            bname=business
        )
        for record in response:
            b1 = record.data().get("b").get("name")
            s1 = record.data().get("s").get("name")
        print(b1, "is a business in", s1)

    def create_series_corp(self, series, business):
        self.create_series_business(series, business)
        self.promote_business_to_corp(business)

    def promote_business_to_corp(self, business):
        response, summary, keys = self.driver.execute_query(
            """MATCH (b :Business {name: $bname})
            SET b :Corporation
            RETURN b
            """,
            bname=business
        )
        for record in response:
            b1 = record.data().get("b").get("name")
        print(b1, "is now a corporation.")

    def create_universe_business(self, universe, business):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("u", "Universe", "uname")
            .merge_line("b", "Business", "bname")
            .return_line().text(),
            uname=universe,
            bname=business
        )
        for record in response:
            b1 = record.data().get("b").get("name")
            u1 = record.data().get("u").get("name")
        print(b1, "is a business in", u1)

    def create_universe_corp(self, universe, business):
        self.create_universe_business(universe, business)
        self.promote_business_to_corp(business)


if __name__ == "__main__":
    print("This is where the debugging would go.")