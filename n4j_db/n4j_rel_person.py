from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JRelPerson:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_kia(self, killer, victim, when, how):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("p1", "Person", "kname")
                .merge_line("p2", "Person", "vname")
                .custom_line("MERGE (p1)-[:KILLED {when: $when, how: $how}]->(p2)")
                .return_line().text(),
            kname = killer,
            vname = victim,
            when = when,
            how = how
        )
        for record in response:
            k1 = record.data().get("p1").get("name")
            v1 = record.data().get("p2").get("name")
        print(k1, "killed", v1)

    def create_father_of(self, father, child):
            response, summary, keys = self.driver.execute_query(
                """MERGE (p1 :Person {name: $fname})
                MERGE (p2 :Person {name: $cname})
                MERGE (p2)-[:FATHER]->(p1)
                RETURN p1, p2;
                """,
                fname=father,
                cname=child
            )
            for record in response:
                f = record.data().get("p1").get("name")
                c = record.data().get("p2").get("name")
            print(f, "is the father of", c)

    def create_mentor(self, student, teacher):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("m", "Person", "mname")
                .merge_line("s", "Person", "sname")
                .relation_basic("s", "m", "MENTOR")
                .return_line().text(),
            mname=teacher,
            sname=student
        )
        for record in response:
            m1 = record.data().get("m").get("name")
            s1 = record.data().get("s").get("name")
        print(m1, "is the mentor of", s1)


    def create_mother_of(self, mother, child):
        response, summary, keys = self.driver.execute_query(
            """MERGE (p1 :Person {name: $mname})
            MERGE (p2 :Person {name: $cname})
            MERGE (p2)-[:MOTHER]->(p1)
            RETURN p1, p2;
            """,
            mname=mother,
            cname=child
        )
        for record in response:
            m = record.data().get("p1").get("name")
            c = record.data().get("p2").get("name")
        print(m, "is the mother of", c)


    def create_mask_kia(self, killer, victim, when, how):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("m", "Mask", "kname")
                .merge_line("p2", "Person", "vname")
                .custom_line("MERGE (m)-[:KILLED {when: $time, how: $method}]->(p2)")
                .return_line().text(),
            kname=killer,
            vname=victim,
            time=when,
            method=how
        )
        for record in response:
            m1 = record.data().get("m").get("name")
            p1 = record.data().get("p2").get("name")
        print(m1, "killed", p1)

    def create_mask_on_mask_kia(self, killer, victim, when, how):
        response, summary, keys = self.driver.execute_query(
            """MERGE (m1 :Mask {name: $kname})
            MERGE (m2 :Mask {name: $vname})
            MERGE (m1)-[:KILLED {when: $when, how: $how}]->(m2)
            """,
            kname=killer,
            vname=victim,
            when=when,
            how=how
        )

    def create_owns_business(self, owner, business):
        response, summary, keys = self.driver.execute_query(
            """MERGE (p :Person {name: $pname})
            MERGE (b :Business {name: $bname})
            MERGE (p)-[:OWNS]->(b)
            RETURN b, p
            """,
            pname=owner,
            bname=business
        )
        for record in response:
            b1 = record.data().get("b").get("name")
            p1 = record.data().get("p").get("name")
        print(p1, "is the owner of", b1)


if __name__ == "__main__":
    print("This is where the debugging would go.")