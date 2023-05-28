from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ

class N4JSciFiLoc:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_planet_city(self, planet, city):
        response, summary, keys = self.driver.execute_query(
            "MERGE (p :Planet {name: $pname})"
            "MERGE (c :City {name: $cname})"
            "MERGE (c)-[:WITHIN]->(p)"
            "RETURN c, p",
            pname=planet,
            cname=city
        )
        for record in response:
            c1 =record.data().get("c").get("name")
            p1 =record.data().get("p").get("name")
        print(c1, "is a city on", p1)

    def create_planet_template(self, planet, template):
        response, summary, keys = self.driver.execute_query(
            "MERGE (p :Planet {name: $pname})"
            "MERGE (t :Template {name: $tname})"
            "MERGE (p)-[:TEMPLATE]->(t)"
            "RETURN p, t",
            pname=planet,
            tname=template
        )
        for record in response:
            p1 =record.data().get("p").get("name")
            t1 =record.data().get("t").get("name")
        print(p1, "has template:", t1)

    def create_star_system(self, star):
        response, summary, keys = self.driver.execute_query(
            "MERGE (s :Star {name: $sname})"
            "RETURN s",
            sname = star
        )
        for record in response:
            print(record.data().get("s").get("name"),"was added to the database.")

    def create_series_star(self, series, star):
        self.create_star_system(star)
        response, summary, keys = self.driver.execute_query(
            """MERGE (t :Series_TV {name: $tname})
            MERGE (s :Star {name: $sname})
            MERGE (s)-[:WITHIN]->(t)
            RETURN s, t;""",
            sname = star,
            tname = series
        )
        for record in response:
            s1 = record.data().get("s").get("name")
            t1 = record.data().get("t").get("name")
        print(s1, "is within", t1)

    def create_star_planet(self, star, planet):
        response, summary, keys = self.driver.execute_query(
            """MERGE (p :Planet {name: $pname})
            MERGE (s :Star {name: $sname})
            MERGE (p)-[:WITHIN]->(s)
            RETURN p,s;""",
            sname = star,
            pname = planet
        )
        for record in response:
            s1 = record.data().get("s").get("name")
            p1 = record.data().get("p").get("name")
        print(p1, "orbits", s1)

    def create_universe_star(self, universe, star):
        self.create_star_system(star)
        response, summary, keys = self.driver.execute_query(
            """MERGE (u :Universe {name: $uname})
            MERGE (s :Star {name: $sname})
            MERGE (s)-[:WITHIN]->(u)
            RETURN s, u;""",
            sname = star,
            uname = universe
        )
        for record in response:
            s1 = record.data().get("s").get("name")
            u1 = record.data().get("u").get("name")
        print(s1, "is within", u1)

    def create_loc(self, location):
        response, summary, keys = self.driver.execute_query(
            "MERGE (l :Location {name: $name})"
            "RETURN l",
            name = location
        )
        for record in response:
            print(record.data().get("l").get("name"),"was added to the database as a location.")


if __name__ == "__main__":
    print("This is where standalone tests of n4j_loc would go.")