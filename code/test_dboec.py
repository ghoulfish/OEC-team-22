import dboec
import convert
import csv
from xml.dom import minidom
import unittest


class TestDboec(unittest.TestCase):

    def setUp(self):
        self.p1 = dboec.Planet()
        self.p2 = dboec.Planet()
        self.p3 = dboec.Planet()

    # Test Database

    def testUpdateCsvName(self):
        '''Tests update_csv on a small version of the EU database with two
        planets.
        '''
        data = []
        with open("test_files/small_eu.csv", 'rb') as f:
            cr = csv.reader(f, delimiter=',')
            my_list = list(cr)
            for row in my_list:
                data.append(row)
        dat = convert.getEU(data)
        db = dboec.Database()
        db.update_csv(dat, dboec.attr_eu)

        self.assertEqual(db.system[0].name == ['11 Com'] and
                         db.system[1].name == ['11 Oph'], True)

    def testUpdateXmlName(self):
        '''Tests update_xml on an XML file containing the 11 Com system.'''
        # Parse XML with system 11 Com
        parsed = minidom.parse("test_files/11 Com.xml")
        data = convert.getOEC(parsed)
        db = dboec.Database()
        db.update_xml(data)
        self.assertEqual(db.pldata[0].name, ['11 Com b'])

    # Test System

    def testGetPlanet(self):
        '''Tests get_planet on two planets that each have one name.'''
        self.p1.name = ['Planet 1']
        self.p2.name = ['Planet 2']

        st1 = dboec.Star()
        st1.planet = [self.p1]

        st2 = dboec.Star()
        st2.planet = [self.p2]

        system = dboec.System()
        system.star = [st1, st2]

        self.assertEqual(system.get_planet(), ['Planet 1', 'Planet 2'])

    def testMatch(self):
        '''Tests that match returns True on two stars that each have a planet
        with a common name.
        '''
        self.p1.name = ['Planet 1']
        self.p2.name = ['Planet 1']

        st1 = dboec.Star()
        st1.planet = [self.p1]

        st2 = dboec.Star()
        st2.planet = [self.p2]

        system1 = dboec.System()
        system1.star = [st1]
        system2 = dboec.System()
        system2.star = [st2]

        self.assertEqual(system1.match(system2), True)

    def testMatchMultiplePlanets(self):
        '''Tests that match returns True on two stars that each have two
        planets that have common names.
        '''
        self.p1.name = ['Planet 1']
        self.p2.name = ['Planet 1']
        self.p3.name = ['Planet 3']

        st1 = dboec.Star()
        st1.planet = [self.p1, self.p3]

        st2 = dboec.Star()
        st2.planet = [self.p2, self.p3]

        system1 = dboec.System()
        system1.star = [st1]
        system2 = dboec.System()
        system2.star = [st2]

        self.assertEqual(system1.match(system2), True)

    def testSystemEq(self):
        '''Tests __eq__ on two System objects with identical properties.'''
        self.p1.name = ['Planet 1']
        self.p1.eccentricity = 0.231

        self.p2.name = ['Planet 1']
        self.p2.eccentricity = 0.231

        s1 = dboec.System()
        s1.planet = [self.p1]
        s2 = dboec.System()
        s2.planet = [self.p2]

        self.assertEqual(s1 == s2, True)

    def testSystemNotEq(self):
        '''Tests __eq__ on two System objects with different planets.'''
        self.p1.name = ['Planet Name A']
        self.p2.name = ['Planet Name B']

        s1 = dboec.System()
        s1.planet = [self.p1]
        s2 = dboec.System()
        s2.planet = [self.p2]

        self.assertEqual(s1 == s2, False)

    # Test Planet

    def testPlanetEq(self):
        '''Tests __eq__ on two Planet objects with identical properties.'''       
        self.p1.name = ['Planet Name 1', 'Planet Name 2']
        self.p1.mass = 19.4
        self.p1.period = 326.03

        self.p2.name = ['Planet Name 1', 'Planet Name 2']
        self.p2.mass = 19.4
        self.p2.period = 326.03

        self.assertEqual(self.p1 == self.p2, True)

    def testPlanetNotEq(self):
        '''Tests __eq__ on two Planet objects with identical properties.'''
        self.p1.name = ['Planet Name A']
        self.p2.name = ['Planet Name B']
        self.assertEqual(self.p1 == self.p2, False)

    def testCreatePl(self):
        '''Tests that createPl inserts the Planet into the Database's planet
        list.
        '''
        newPlanet = {'name': '11 Com b'}
        system = dboec.System()

        db = dboec.Database()
        db.system = [system]
        db.createPl(newPlanet, system)

        self.assertEqual(db.pldata[0].name == [newPlanet.get('name')], True)

if __name__ == '__main__':
    unittest.main(exit=False)
