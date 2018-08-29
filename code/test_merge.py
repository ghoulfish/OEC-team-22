from merge import *
from dboec import *
import convert
from xml.dom import minidom
import unittest


class TestMerge(unittest.TestCase):

    def setUp(self):
        # Database class with system 11 Com
        self.comDB = Database()
        parsed = minidom.parse("test_files/11 Com.xml")
        data = convert.getOEC(parsed)
        self.comDB.update_xml(data)

        # Database class with system 11 UMi
        self.umiDB = Database()
        parsed = minidom.parse("test_files/11 UMi.xml")
        data = convert.getOEC(parsed)
        self.umiDB.update_xml(data)

        # Database class with systems 11 Com, 11 UMi, 14 And
        self.comToAnd = Database()
        data = convert.getOEC(minidom.parse("test_files/11 Com.xml"))
        self.comToAnd.update_xml(data)
        data = convert.getOEC(minidom.parse("test_files/11 Umi.xml"))
        self.comToAnd.update_xml(data)
        data = convert.getOEC(minidom.parse("test_files/14 And.xml"))
        self.comToAnd.update_xml(data)

        # Database class with systems 14 Her, 16 Cygni
        self.herToDel = Database()
        data = convert.getOEC(minidom.parse("test_files/14 Her.xml"))
        self.herToDel.update_xml(data)
        data = convert.getOEC(minidom.parse("test_files/16 Cygni.xml"))
        self.herToDel.update_xml(data)

        self.comB1 = Planet()
        self.comB1.name = ['11 Com b']

        self.comSt1 = Star()
        self.comSt1.name = ['11 Com']
        self.comSt1.planet = [self.comB1]
        self.comSt2 = Star()
        self.comSt2.name = ['11 Com']
        self.comSt2.planet = [self.comB1]

        self.sys1 = System()
        self.sys1.star = [self.comSt1]
        self.sys2 = System()
        self.sys2.star = [self.comSt1]

        self.comB2 = Planet()
        self.comB2.name = ['11 Com b']

        self.umiB = Planet()
        self.umiB.name = ['11 UMi b']
        self.umiSt = Star()
        self.umiSt.planet = [self.umiB]
        self.umiSys = System()
        self.umiSys.star = [self.umiSt]

    # merge() testing

    def testMergeWithSelf(self):
        '''Tests merging a Database with itself.
        '''
        mergedDB = merge(self.comDB, self.comDB)
        self.assertEqual(self.comDB == mergedDB, True)

    def testMergeTwoSystems(self):
        '''Tests merging two distinct Databases.
        '''
        # Creates Database containing systems 11 Com and 11 UMi
        comAndUmiDB = Database()
        data = convert.getOEC(minidom.parse("test_files/11 Com.xml"))
        comAndUmiDB.update_xml(data)
        data = convert.getOEC(minidom.parse("test_files/11 UMi.xml"))
        comAndUmiDB.update_xml(data)

        mergedDB = merge(self.umiDB, self.comDB)

        self.assertEqual(mergedDB == comAndUmiDB, True)

    def testMergeSystemWithSuperset(self):
        '''Tests merging two Databases where other contains oec.
        '''
        mergedDB = merge(self.comToAnd, self.comDB)
        self.assertEqual(self.comToAnd == mergedDB, True)

    def testMergeSystemWithSubset(self):
        '''Tests merging two Databases where oec contains other.
        '''
        mergedDB = merge(self.comDB, self.comToAnd)
        self.assertEqual(self.comToAnd == mergedDB, True)

    def testMergeTwoSystemsWithThree(self):
        '''Tests merging two Databases where that each have multiple systems.
        '''
        # Creates expected Database with all 5 systems
        expectedDB = Database()
        data = convert.getOEC(minidom.parse("test_files/11 Com.xml"))
        expectedDB.update_xml(data)
        data = convert.getOEC(minidom.parse("test_files/11 Umi.xml"))
        expectedDB.update_xml(data)
        data = convert.getOEC(minidom.parse("test_files/14 And.xml"))
        expectedDB.update_xml(data)
        data = convert.getOEC(minidom.parse("test_files/14 Her.xml"))
        expectedDB.update_xml(data)
        data = convert.getOEC(minidom.parse("test_files/16 Cygni.xml"))
        expectedDB.update_xml(data)

        mergedDB = merge(self.herToDel, self.comToAnd)

        self.assertEqual(mergedDB == expectedDB, True)

    # add_name() testing

    def testAddNameToName(self):
        '''Tests add_name when both objects each have one name.
        '''
        obj1 = dboec.System()
        obj1.name = ["Name 1"]
        obj2 = dboec.System()
        obj2.name = ["Name 2"]
        self.assertEqual(add_name(obj1, obj2) == ["Name 1", "Name 2"], True)

    def testAddNameEmpty(self):
        '''Tests add_name when both objects have no name.
        '''
        obj1 = dboec.System()
        obj1.name = []
        obj2 = dboec.System()
        obj2.name = []
        self.assertEqual(add_name(obj1, obj2) == [], True)

    def testAddNameWithOneEmpty(self):
        '''Tests add_name when one of the objects has no name.
        '''
        obj1 = dboec.System()
        obj1.name = ["Name 1"]
        obj2 = dboec.System()
        obj2.name = []
        self.assertEqual(add_name(obj1, obj2) == ["Name 1"], True)

    def testAddNameMultiple(self):
        '''Tests add_name when both objects each have multiple names.
        '''
        obj1 = dboec.System()
        obj1.name = ["Name 1", "Name 2", "Name 3"]
        obj2 = dboec.System()
        obj2.name = ["Name 4", "Name 5"]
        self.assertEqual(add_name(obj1, obj2) == ["Name 1", "Name 2", "Name 3",
                                                  "Name 4", "Name 5"], True)

    def testAddNameIdenticalNames(self):
        '''Tests add_name when both objects have the same name.
        '''
        obj1 = dboec.System()
        obj1.name = ["Name 1"]
        obj2 = dboec.System()
        obj2.name = ["Name 1"]
        self.assertEqual(add_name(obj1, obj2) == ["Name 1"], True)

    def testAddNameWithSubset(self):
        '''Tests add_name when obj1 contains obj2.
        '''
        obj1 = dboec.System()
        obj1.name = ["Name 1", "Name 2", "Name 3"]
        obj2 = dboec.System()
        obj2.name = ["Name 1", "Name 2"]
        self.assertEqual(add_name(obj1, obj2) == ["Name 1", "Name 2",
                                                  "Name 3"], True)

    def testAddNameWithSuperset(self):
        '''Tests add_name when obj2 contains obj1.
        '''
        obj1 = dboec.System()
        obj1.name = ["Name 1", "Name 2"]
        obj2 = dboec.System()
        obj2.name = ["Name 1", "Name 2", "Name 3"]
        self.assertEqual(add_name(obj1, obj2) == ["Name 1", "Name 2",
                                                  "Name 3"], True)

    # add_to_system() testing

    def testAddToSystemDifferentSystems(self):
        '''Tests that add_to_system on two distinct systems returns the second
        system.
        '''
        self.assertEqual(add_to_system(self.sys1, self.umiSys) == self.umiSys,
                         True)

    def testAddToSystemIdenticalSystems(self):
        '''Tests that add_to_system on two identical systems returns the that
        system.
        '''
        self.assertEqual(add_to_system(self.sys1, self.sys2) == self.sys2,
                         True)

    def testAddToSystemNewInfo(self):
        '''Tests add_to_system when the second system has attributes that the
        first doesn't.
        '''
        self.sys2.distance = 122.1
        self.sys2.declination = "+71 49 26.0466"
        retSys = add_to_system(self.sys1, self.sys2)
        self.assertEqual(retSys.distance == 122.1 and retSys.declination ==
                         "+71 49 26.0466", True)

    def testAddToSystemMissingInfo(self):
        '''Tests add_to_system when the second system doesn't have attributes
        that the first does.
        '''
        self.sys1.distance = 122.1
        self.sys1.declination = "+71 49 26.0466"
        retSys = add_to_system(self.sys1, self.sys2)
        self.assertEqual(retSys.distance == 122.1 and retSys.declination ==
                         "+71 49 26.0466", True)

    def testAddToSystemMergeInfo(self):
        '''Tests add_to_system when both systems have attributes the other
        doesn't.
        '''
        self.sys1.distance = 122.1
        self.sys2.declination = "+71 49 26.0466"
        retSys = add_to_system(self.sys1, self.sys2)
        self.assertEqual(retSys.distance == 122.1 and retSys.declination ==
                         "+71 49 26.0466", True)

    def testAddToSystemConflictingInfo(self):
        '''Tests add_to_system when the systems have conflicting attributes.
        '''
        self.sys1.distance = 122.1
        self.sys2.distance = 100
        retSys = add_to_system(self.sys1, self.sys2)
        self.assertEqual(retSys.distance == 122.1, True)

    def testAddToSystemDictConflict(self):
        '''Tests add_to_system when the systems have an attribute containing
        conflicting dictionaries.
        '''
        self.sys1.distance_attrs = {'errorplus': 2.8, 'errorminus': 3.5}
        self.sys2.distance_attrs = {'errorplus': 7, 'errorminus': 'abc'}
        retSys = add_to_system(self.sys1, self.sys2)
        self.assertEqual(retSys.distance_attrs == self.sys1.distance_attrs,
                         True)

    # add_to_star() testing

    def testAddToStarDifferentStars(self):
        '''Tests that add_to_star on two distinct stars returns the second
        star.
        '''
        self.assertEqual(add_to_star(self.comSt1, self.umiSt) == self.umiSt,
                         True)

    def testAddToStarIdenticalStars(self):
        '''Tests that add_to_star on two identical stars returns the that
        star.
        '''
        self.assertEqual(add_to_star(self.comSt1, self.comSt1) == self.comSt1,
                         True)

    def testAddToStarNewInfo(self):
        '''Tests add_to_star when the second star has attributes that the
        first doesn't.
        '''
        self.comSt2.mass = 2.7
        retStar = add_to_star(self.comSt1, self.comSt2)
        self.assertEqual(retStar.mass == 2.7, True)

    def testAddToStarMissingInfo(self):
        '''Tests add_to_star when the second star doesn't have attributes
        that the first does.
        '''
        self.comSt1.mass = 2.7
        retStar = add_to_star(self.comSt1, self.comSt2)
        self.assertEqual(retStar.mass == 2.7, True)

    def testAddToStarMergeInfo(self):
        '''Tests add_to_star when both stars have attributes the other
        doesn't.
        '''
        self.comSt1.mass = 2.7
        self.comSt2.radius = 19
        retStar = add_to_star(self.comSt1, self.comSt2)
        self.assertEqual(retStar.mass == 2.7 and retStar.radius == 19, True)

    def testAddToStarConflictingInfo(self):
        '''Tests add_to_star when the stars have conflicting attributes.
        '''
        self.comSt1.mass = 2.7
        self.comSt2.mass = 500
        retStar = add_to_star(self.comSt1, self.comSt2)
        self.assertEqual(retStar.mass == 2.7, True)

    def testAddToStarDictConflict(self):
        '''Tests add_to_star when the stars have an attribute containing
        conflicting dictionaries.
        '''
        self.comSt1.mass_attrs = {'errorplus': 0.3, 'errorminus': 0.3}
        self.comSt2.mass_attrs = {'errorplus': 'asdfghj', 'errorminus': 22}
        retStar = add_to_star(self.comSt1, self.comSt2)
        self.assertEqual(retStar.mass_attrs == self.comSt1.mass_attrs, True)

    # add_to_planet() testing

    def testAddToPlanetDifferentPlanets(self):
        '''Tests that add_to_planet on two distinct planets returns the second
        planet.
        '''
        self.assertEqual(add_to_planet(self.comB1, self.umiB) == self.umiB,
                         True)

    def testAddToPlanetIdenticalPlanets(self):
        '''Tests that add_to_planet on two identical planets returns the that
        planet.
        '''
        self.assertEqual(add_to_planet(self.comB1, self.comB1) == self.comB1,
                         True)

    def testAddToPlanetNewInfo(self):
        '''Tests add_to_planet when the second planet has attributes that the
        first doesn't.
        '''
        self.comB2.mass = 19.4
        retPlanet = add_to_planet(self.comB1, self.comB2)
        self.assertEqual(retPlanet.mass == 19.4, True)

    def testAddToPlanetMissingInfo(self):
        '''Tests add_to_planet when the second planet doesn't have attributes
        that the first does.
        '''
        self.comB1.mass = 19.4
        retPlanet = add_to_planet(self.comB1, self.comB2)
        self.assertEqual(retPlanet.mass == 19.4, True)

    def testAddToPlanetMergeInfo(self):
        '''Tests add_to_planet when both planets have attributes the other
        doesn't.
        '''
        self.comB1.mass = 19.4
        self.comB2.period = 326.03
        retPlanet = add_to_planet(self.comB1, self.comB2)
        self.assertEqual(retPlanet.mass == 19.4 and retPlanet.period == 326.03,
                         True)

    def testAddToPlanetConflictingInfo(self):
        '''Tests add_to_planet when the planets have conflicting attributes.
        '''
        self.comB1.mass = 19.4
        self.comB2.mass = 500
        retPlanet = add_to_planet(self.comB1, self.comB2)
        self.assertEqual(retPlanet.mass == 19.4, True)

    def testAddToPlanetDictConflict(self):
        '''Tests add_to_planet when the planets have an attribute containing
        conflicting dictionaries.
        '''
        self.comB1.mass_attrs = {'errorplus': 0.32, 'errorminus': 0.32}
        self.comB2.mass_attrs = {'errorplus': None, 'errorminus': 99}
        retPlanet = add_to_planet(self.comB1, self.comB2)
        self.assertEqual(retPlanet.mass_attrs == self.comB1.mass_attrs, True)

if __name__ == '__main__':
    unittest.main(exit=False)
