from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
import bcrypt

from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JLogin:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def get_login_roles(self, login):
        returnList = []
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().match_line("u", "Login", "uname")
                .return_line().text(),
            uname=login
        )
        for record in response:
            returnList.append(record.data().get("u").get("role"))
        return returnList

    def login(self, login, password):
        pcrypt = None
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().match_line("l", "Login", "lname")
                .return_line().text(),
            lname=login
        )
        for record in response:
            pcrypt = record.data().get("l").get("pwcrypt")
        if pcrypt in (None, ""):
            return False
        if bcrypt.checkpw(bytes(password, encoding='utf8'), pcrypt):
            return True
        else:
            return False

    def login_exists(self, login):
        l1 = ""
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().match_line("l", "Login", "lname")
            .return_line().text(),
            lname=login
        )
        for record in response:
            l1 = record.data().get("l").get("pwcrypt")
        if (l1 == ""):
            return False
        else:
            return True

    def register_login(self, login, password, role="Player"):
        cpass = bcrypt.hashpw(bytes(password, encoding= 'utf8'), bcrypt.gensalt(16))
        response, summary, keys = self.driver.execute_query(
            """MERGE (l :Login {name: $lname})
            SET l.pwcrypt = $pbc
            SET l.role = $rname
            RETURN l
            """,
            lname=login,
            pbc=cpass,
            rname=role
        )
        for record in response:
            l1 = record.data().get("l").get("name")
            l2 = record.data().get("l").get("pwcrypt")
            l3 = record.data().get("l").get("role")
        print("User: ", l1, ":", l2, "created with role", l3)

if __name__ == "__main__":
    print("This is where unit tests would go.")