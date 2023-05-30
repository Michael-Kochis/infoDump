from neo4j import GraphDatabase
from n4j_db.n4j_cypher_builder import CypherBuilder

from . import n4j_aspect,n4j_business, n4j_commons,n4j_group, n4j_loc, \
    n4j_person, n4j_rel_business, n4j_rel_person, n4j_planet, n4j_sci_fi_loc, \
    n4j_series_book, n4j_series_comic, n4j_series_movie, n4j_series_tv, \
    n4j_species, n4j_template, n4j_title,\
    n4j_universe,n4j_vehicle

from dotenv import load_dotenv
from os import environ

class N4J_DB:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

        self.aspect = n4j_aspect.N4JAspect(self.driver)
        self.business = n4j_business.N4JBusiness(self.driver)
        self.common = n4j_commons.N4JCommons(self.driver)
        self.group = n4j_group.N4JGroup(self.driver)
        self.person = n4j_person.N4JPerson(self.driver)
        self.planet = n4j_planet.N4JPlanet(self.driver)
        self.loc = n4j_loc.N4JLoc(self.driver)
        self.rel_business = n4j_rel_business.N4JRelBusiness(self.driver)
        self.rel_person = n4j_rel_person.N4JRelPerson(self.driver)
        self.sci_fi_loc = n4j_sci_fi_loc.N4JSciFiLoc(self.driver)
        self.series_b = n4j_series_book.N4JSeriesBook(self.driver)
        self.series_c = n4j_series_comic.N4JSeriesComic(self.driver)
        self.series_m = n4j_series_movie.N4JSeriesMovie(self.driver)
        self.series_t = n4j_series_tv.N4JSeriesTV(self.driver)
        self.species = n4j_species.N4JSpecies(self.driver)
        self.template = n4j_template.N4JTemplate(self.driver)
        self.title = n4j_title.N4JTitle(self.driver)
        self.vehicle = n4j_vehicle.N4JVehicle(self.driver)
        self.universe = n4j_universe.N4JUniverse(self.driver)

    def close(self):
        self.driver.close()

