import merge
import convert
import dboec
import requests
import csv
from xml.dom import minidom
import unittest


class TestConvert(unittest.TestCase):

    # Test getOEC(node)

    def testGetOEC(self):
        ''' Tests that getOEC produces the correct dict when reading a parsed
        XML file.
        '''
        dom = minidom.parse("test_files/11 Com.xml")
        systemsDict = convert.getOEC(dom)
        expectedDict = {'system': {'distance': '88.9', 'distance_attrs': {'errorminus': '1.7', 'errorplus': '1.7'}, 'star': {'planet': {'lastupdate': '15/09/20', 'periastrontime': '2452899.6', 'mass_attrs': {'errorminus': '1.5', 'type': 'msini', 'errorplus': '1.5'}, 'name': '11 Com b', 'semimajoraxis': '1.29', 'discoveryyear': '2008', 'periastrontime_attrs': {'errorminus': '1.6', 'errorplus': '1.6'}, 'discoverymethod': 'RV', 'eccentricity_attrs': {'errorminus': '0.005', 'errorplus': '0.005'}, 'list': 'Confirmed planets', 'period': '326.03', 'periastron_attrs': {'errorminus': '1.5', 'errorplus': '1.5'}, 'mass': '19.4', 'period_attrs': {'errorminus': '0.32', 'errorplus': '0.32'}, 'eccentricity': '0.231', 'semimajoraxis_attrs': {'errorminus': '0.05', 'errorplus': '0.05'}, 'periastron': '94.8', 'description': '11 Com b is a brown dwarf-mass companion to the intermediate-mass star 11 Comae Berenices.'}, 'magB_attrs': {'errorminus': '0.02', 'errorplus': '0.02'}, 'mass_attrs': {'errorminus': '0.3', 'errorplus': '0.3'}, 'name': ['11 Com', '11 Comae Berenices', 'HD 107383', 'HIP 60202', 'TYC 1445-2560-1', 'SAO 100053', 'HR 4697', 'BD+18 2592', '2MASS J12204305+1747341'], 'spectraltype': 'G8 III', 'radius_attrs': {'errorminus': '2', 'errorplus': '2'}, 'magV': '4.74', 'metallicity_attrs': {'errorminus': '0.09', 'errorplus': '0.09'}, 'magK': '2.282', 'magJ': '2.943', 'metallicity': '-0.35', 'magH': '2.484', 'radius': '19', 'temperature': '4742', 'magB': '5.74', 'mass': '2.7', 'magJ_attrs': {'errorminus': '0.334', 'errorplus': '0.334'}, 'magH_attrs': {'errorminus': '0.268', 'errorplus': '0.268'}, 'temperature_attrs': {'errorminus': '100', 'errorplus': '100'}, 'magK_attrs': {'errorminus': '0.346', 'errorplus': '0.346'}}, 'name': '11 Com', 'declination': '+17 47 34', 'videolink': 'http://youtu.be/qyJXJJDrEDo', 'rightascension': '12 20 43'}}
        self.assertEqual(systemsDict == expectedDict, True)

    # Test dictAdd(d, key, item)

    def testDictAddWhenKeyDoesNotExist(self):
        ''' Tests adding a key, value pair to an empty dict.
        '''
        self.emptyDict = {}
        convert.dictAdd(self.emptyDict, 'Name', 'Alice')
        expectedDict = {'Name': 'Alice'}
        self.assertEqual(self.emptyDict == expectedDict, True)

    def testDictAddWhenKeyHasOneItem(self):
        ''' Tests adding a value to a key that already has a single value.
        '''
        self.dictWithNoLists = {'Name': 'Alice', 'Courses': 'C01'}
        convert.dictAdd(self.dictWithNoLists, 'Courses', 'D27')
        expectedDict = {'Name': 'Alice', 'Courses': ['C01', 'D27']}
        self.assertEqual(self.dictWithNoLists == expectedDict, True)

    def testDictAddWhenKeyHasList(self):
        ''' Tests adding a value to a key that already has a list value.
        '''
        self.dictWithLists = {'Name': 'Bob', 'Courses': ['C01', 'C37', 'C73']}
        convert.dictAdd(self.dictWithLists, 'Courses', 'C43')
        expectedDict = {'Name': 'Bob', 'Courses': ['C01', 'C37', 'C73', 'C43']}
        self.assertEqual(self.dictWithLists == expectedDict, True)

    # Test hasAttr(node)

    def testHasAttrOnNonElementNode(self):
        ''' Tests that hasAttr returns False when checking a node that isn't
        a tag.
        '''
        doc = minidom.parseString("<tag>element</tag>")
        self.assertEqual(convert.hasAttr(doc), False)

    def testHasAttrFalse(self):
        ''' Tests that hasAttr returns False when checking if <tag> has
        attributes.
        '''
        doc = minidom.parseString("<tag>element</tag>")
        self.assertEqual(convert.hasAttr(doc.childNodes[0]), False)

    def testHasAttrWhenOneAttr(self):
        ''' Tests that hasAttr returns True when <tag> has one attribute.
        '''
        doc = minidom.parseString("<tag num='3'>element</tag>")
        self.assertEqual(convert.hasAttr(doc.childNodes[0]), True)

    def testHasAttrWhenMultipleAttr(self):
        ''' Tests that hasAttr returns True when <tag> has multiple attributes.
        '''
        xml = "<mass errorminus='0.3' errorplus='0.3'>2.7</mass>"
        doc = minidom.parseString(xml)
        self.assertEqual(convert.hasAttr(doc.childNodes[0]), True)

    # Test attr(node, values)

    def testAttrOnDocumentNode(self):
        ''' Tests that attr returns None when checking a node that isn't a tag.
        '''
        doc = minidom.parseString("<tag>element</tag>")
        self.assertEqual(convert.attr(doc, None) == None, True)

    def testAttrOnAttributelessNode(self):
        ''' Tests attr on a tag that has no attributes.
        '''
        doc = minidom.parseString("<tag>element</tag>")
        self.assertEqual(convert.attr(doc.childNodes[0], None) ==
                         {'tag': None}, True)

    def testAttrOnNodeWithAttributes(self):
        ''' Tests attr on a tag that has one attribute.
        '''
        doc = minidom.parseString("<tag num='3'>element</tag>")
        self.assertEqual(convert.attr(doc.childNodes[0], {}) == {
            'tag': {'#attributes': {'num': '3'}}}, True)

if __name__ == '__main__':
    unittest.main(exit=False)
