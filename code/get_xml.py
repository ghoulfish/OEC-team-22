from xml.dom import minidom
import xml.etree.ElementTree as ET

# attributes that are shown on a xml are listed as following in a certain order
# (not in ascending order)
sys_attr = ["name", "rightascension", "declination", "distance", "spectraltype",
            "magJ", "magH", "magK", "binary", "_star", "_planet", "videolink"]
bin_attr = ["name", "magB", "magV", "magR", "magI", "magJ", "magH", "magK",
            "separation", "positionangle", "period", "inclination",
            "transittime", "semimajoraxis", "eccentricity", "longitude",
            "periastron", "periastrontime", "ascendingnode", "star", "binary",
            "planet"]
st_attr = ["name", "mass", "radius", "magV", "magU", "magB", "magR", "magI",
           "magJ", "magH", "magK", "temperature", "age", "metallicity",
           "spectraltype", "planet"]
pl_attr = ["name", "list", "spectraltype", "mass", "radius", "separation",
           "positionangle", "magI", "magJ", "magH", "magK", "age",
           "impactparameter", "period", "semimajoraxis", "eccentricity",
           "spinorbitalignment", "periastron", "periastrontime",
           "metallicity", "longitude", "ascendingnode", "maximumrvtime",
           "meananomaly", "inclination", "temperature", "description",
           "discoverymethod", "transittime", "istransiting", "new",
           "lastupdate", "discoveryyear", "image", "imagedescription"]


# a helper function to properly indent the xml string
# so that the string is being pretty printed in the xml file
def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# convert a system object to a xml element tree, so that it can be write into an xml file
def toXml(sys):
    # use Element tree to build the xml string
    system = ET.Element("system")
    for i in sys_attr:
        # for each attributes of the system object, create a sub element of the system element
        if i == "name":
            for eachname in getattr(sys, i):
                ET.SubElement(system, i).text = eachname.decode('utf-8')
        elif (i == "distance" or i == "magH" or i == "magJ" or i == "magK"):
            # deal with those attributes of system that contains attributes itself
            with_attr(i, sys, system)
        elif i == "_star":
            if len(getattr(sys, i)) != 0:
                stToXml(system, sys)
        elif i == "binary":
            if len(getattr(sys, i)) != 0:
                binToXml(system, sys)
        elif i == "_planet":
            if len(getattr(sys, i)) != 0:
                plToXml(system, sys)
        else:
            if getattr(sys, i):
                ET.SubElement(system, "%s" % i).text = getattr(sys, i).decode('utf-8')
    # get the first name of the system, make it the xml file name
    if type(getattr(sys, "name")) == str:
        sysname = getattr(sys, "name")
    else:
        sysname = getattr(sys, "name")[0]
    # indent the xml string
    indent(system)
    tree = ET.ElementTree(system)
    # write the xml string in to the xml file
    tree.write(open("%s.xml" % sysname, "w"), encoding='utf-8')
    return ("%s.xml" % sysname)


# convert a binary object to a xml element tree
def binToXml(system, sys):
    bina = sys.binary
    for eachbin in bina:
        # the binary should be a sub element of the given system or the given binary element
        binary = ET.SubElement(system, "binary")
        for n in bin_attr:
            if n == "name":
                for eachname in getattr(eachbin, n):
                    ET.SubElement(binary, n).text = (eachname).decode('utf-8')
            elif (n == "positionangle" or n == "magB" or n == "magV" or
                  n == "magR" or n == "magI" or n == "magJ" or n == "magH" or
                  n == "magK" or n == "period" or n == "inclination" or
                  n == "transittime" or n == "semimajoraxis" or
                  n == "eccentricity" or n == "periastron" or
                  n == "periastrontime" or n == "ascendingnode"):
                # deal with those attributes of binary that contains attributes itself
                with_attr(n, eachbin, binary)
            elif n == "star":
                if len(getattr(eachbin, n)) != 0:
                    stToXml(binary, eachbin)
            elif n == "binary":
                if len(getattr(eachbin, n)) != 0:
                    binToXml(binary, eachbin)
            elif n == "planet":
                if len(getattr(eachbin, n)) != 0:
                    plToXml(binary, eachbin)
            # one binary might have two separation, so deal with it separately
            elif n == "separation":
                if type(getattr(eachbin, n)) == list:
                    seplist = getattr(eachbin, n)
                    sepattrlist = getattr(eachbin, "%s_attrs" % n)
                    i = 0
                    while i < len(seplist):
                        if len(sepattrlist[i]) == 3:
                            (ET.SubElement(binary, n,
                                           errorminus=sepattrlist[i]['errorminus'].decode('utf-8'),
                                           errorplus=sepattrlist[i]['errorplus'].decode('utf-8'),
                                           unit=sepattrlist[i]['unit'].decode('utf-8')).
                             text) = seplist[i]
                        elif len(sepattrlist[i]) == 2:
                            (ET.SubElement(binary, n,
                                           errorminus=sepattrlist[i]['errorminus'].decode('utf-8'),
                                           errorplus=sepattrlist[i]['errorplus'].decode('utf-8')).
                             text) = seplist[i]
                        elif len(sepattrlist[i]) == 1:
                            (ET.SubElement(binary, n,
                                           unit=sepattrlist[i]['unit'].decode('utf-8')).
                             text) = seplist[i]
                        else:
                            ET.SubElement(binary, n).text = seplist[i]
                        i += 1
                else:
                    with_attr(n, eachbin, binary)
            else:
                if getattr(eachbin, n):
                    ET.SubElement(binary, "%s" %n).text = getattr(eachbin, n).decode('utf-8')


# convert a star object to a xml element tree
def stToXml(system, sys):
    st = sys.star
    for eachst in st:
        # the star should be a sub element of the given system or the given binary element
        star = ET.SubElement(system, "star")
        for j in st_attr:
            if j == "name":
                for eachname in getattr(eachst, j):
                    ET.SubElement(star, j).text = eachname.decode('utf-8')
            elif (j == "mass" or j == "radius" or j == "magV" or j == "magU" or
                  j == "magB" or j == "magR" or j == "magI" or j == "magJ" or
                  j == "magH" or j == "magK" or j == "temperature" or
                  j == "age" or j == "metallicity" or j == "spectraltype"):
                # deal with those attributes of star that contains attributes itself
                with_attr(j, eachst, star)
            elif (j == "planet"):
                if len(getattr(eachst, j)) != 0:
                    plToXml(star, eachst)
            else:
                if getattr(eachst, j):
                    ET.SubElement(star, "%s" % j).text = getattr(eachst, j).decode('utf-8')


# convert a planet object to a xml element tree
def plToXml(star, eachst):
    pl = eachst.planet
    for eachpl in pl:
        # a planet object should be a sub element of the given star or binary or system element
        planet = ET.SubElement(star, "planet")
        for k in pl_attr:
            if k == "name":
                for eachname in getattr(eachpl, k):
                    ET.SubElement(planet, k).text = eachname.decode('utf-8')
            elif (k == "spectraltype" or k == "mass" or k == "radius" or
                  k == "positionangle" or k == "magI" or
                  k == "magJ" or k == "magH" or k == "magK" or k == "age" or
                  k == "impactparameter" or k == "period" or
                  k == "semimajoraxis" or k == "eccentricity" or
                  k == "spinorbitalignment" or k == "periastron" or
                  k == "periastrontime" or k == "longitude" or
                  k == "ascendingnode" or k == "maximumrvtime" or
                  k == "meananomaly" or k == "inclination" or
                  k == "temperature" or k == "transittime"):
                # deal with those attributes of planet that contains attributes itself
                with_attr(k, eachpl, planet)
            # one planet might have two or more list or separation attributes, so deal with them separately
            elif k == "list":
                if type(getattr(eachpl, k)) == list:
                    for eachlist in getattr(eachpl, k):
                        ET.SubElement(planet, k).text = eachlist.decode('utf-8')
                else:
                    ET.SubElement(planet, k).text = getattr(eachpl, k).decode('utf-8')
            elif k == "separation":
                if type(getattr(eachpl, k)) == list:
                    seplist = getattr(eachpl, k)
                    sepattrlist = getattr(eachpl, "%s_attrs" % k)
                    i = 0
                    while i < len(seplist):
                        if len(sepattrlist[i]) == 3:
                            (ET.SubElement(planet, k,
                                           errorminus=sepattrlist[i]['errorminus'].decode('utf-8'),
                                           errorplus=sepattrlist[i]['errorplus'].decode('utf-8'),
                                           unit=sepattrlist[i]['unit'].decode('utf-8')).
                             text) = seplist[i]
                        elif len(sepattrlist[i]) == 2:
                            (ET.SubElement(planet, k,
                                           errorminus=sepattrlist[i]['errorminus'].decode('utf-8'),
                                           errorplus=sepattrlist[i]['errorplus'].decode('utf-8')).
                             text) = seplist[i]
                        elif len(sepattrlist[i]) == 1:
                            (ET.SubElement(planet, k,
                                           unit=sepattrlist[i]['unit'].decode('utf-8')).
                             text) = seplist[i]
                        else:
                            ET.SubElement(planet, k).text = seplist[i]
                        i += 1
                else:
                    with_attr(k, eachpl, planet)
            else:
                if getattr(eachpl, k):
                    (ET.SubElement(planet, "%s" % k).text) = getattr(eachpl, k).decode('utf-8')


# a helper function to deal with those attributes of an element that contains attributes itself
def with_attr(attr, item, element):
    attrs = "%s_attrs" % attr
    if getattr(item, attr):
        subelem = ET.SubElement(element, attr)
        subelem.text = getattr(item, attr).decode('utf-8')
        # there are at most seven attributes "error", "errorplus", "errorminus"
        # "unit", "upperlimit", "lowerlimit", "type"
        if getattr(item, attrs):
            for i in getattr(item, attrs):
                if i == 'error' and getattr(item, attrs)['error']:
                    subelem.set(i, getattr(item, attrs)['error'].decode('utf-8'))
                elif i == 'errorplus' and getattr(item, attrs)['errorplus']:
                    subelem.set(i, getattr(item, attrs)['errorplus'].decode('utf-8'))
                elif i == 'errorminus' and getattr(item, attrs)['errorminus']:
                    subelem.set(i, getattr(item, attrs)['errorminus'].decode('utf-8'))
                elif i == 'unit' and getattr(item, attrs)['unit']:
                    subelem.set(i, getattr(item, attrs)['unit'].decode('utf-8'))
                elif i == 'upperlimit' and getattr(item, attrs)['upperlimit']:
                    subelem.set(i, getattr(item, attrs)['upperlimit'].decode('utf-8'))
                elif i == 'lowerlimit' and getattr(item, attrs)['lowerlimit']:
                    subelem.set(i, getattr(item, attrs)['lowerlimit'].decode('utf-8'))
                elif i == 'type' and getattr(item, attrs)['type']:
                    subelem.set(i, getattr(item, attrs)['type'].decode('utf-8'))


if __name__ == '__main__':
    import dboec
    import convert

    oecd = minidom.parse("systemexample.xml")
    data = convert.getOEC(oecd)
    d1 = dboec.Database()
    d1.update_xml(data)

    print(d1)
    for system in d1.system:
        print(system.name)
        toXml(system)
