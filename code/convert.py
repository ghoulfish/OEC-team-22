import csv
from xml.dom import minidom


# get oec data from xml file
def getOEC(node):
    if not node.hasChildNodes():
        if node.nodeType == node.TEXT_NODE:
            if node.data.strip() != '':
                return node.data.strip().encode('utf-8')
            else:
                return None
        else:
            return attr(node, None)
    else:
        childs = []
        for child in node.childNodes:
            if ((getOEC(child) != None) &
                    (child.nodeType != child.COMMENT_NODE)):
                    childs.append(getOEC(child))
        if len(childs) == 1:
            return attr(node, childs[0])
        else:
            newd = {}
            for child in childs:
                if type(child) == dict:
                    for i in child:
                        dictAdd(newd, i, child[i])
                elif type(child) == str:
                    dictAdd(newd, '#text', child)
                else:
                    print("ERROR")
            return attr(node, newd)


# a helper function for adding element into a dictionary
def dictAdd(d, key, item):
    if key in d:
        if type(d[key]) != list:
            l = []
            l.append(d[key])
            l.append(item)
            d[key] = l
        else:
            d[key].append(item)
    else:
        d[key] = item


# a helper function to check if the node has attributes
def hasAttr(node):
    if node.nodeType == node.ELEMENT_NODE:
        if node.hasAttributes():
            return True
    return False


# a helper function to deal with when a node has attributes,
# we should add it to dictionary with an extra element called "_attrs"
def attr(node, values):
    if hasAttr(node):
        if type(values) == dict:
            newdict = {}
            for attribute in node.attributes.keys():
                newdict[str(attribute)] = str(node.attributes[attribute].value)
            dictAdd(values, '#attributes', newdict)
            return {str(node.nodeName): values}
        elif type(values) == str:
            newdict = {}
            for attribute in node.attributes.keys():
                newdict[str(attribute)] = str(node.attributes[attribute].value)
            return {str(node.nodeName): values,
                    "%s_attrs" % str(node.nodeName): newdict}
    else:
        if str(node.nodeName) == '#document':
            return values
        else:
            return {str(node.nodeName): values}


# get eu data from csv file
def getEU(data):
    res = []
    attr_list = data[0]
    attr_list[0] = attr_list[0][2:]
    data = data[1:]
    for i in range(len(data)):
        d = {}
        for j in range(len(data[i])):
            d[attr_list[j]] = data[i][j]
        d[None] = None
        res.append(d)
    for pl in res:
        if pl["detection_type"] == "Primary Transit":
            pl["detection_type"] = "transit"
        elif pl["detection_type"] == "Radial Velocity":
            pl["detection_type"] = "RV"
        elif pl["detection_type"] == "Imaging":
            pl["detection_type"] = "imaging"
        elif pl["detection_type"] == "Microlensing":
            pl["detection_type"] = "microlensing"
        pl["updated"] = pl["updated"][2:]
        pl["updated"] = pl["updated"].replace("-", "/")
        for attr in pl:
            if pl[attr] == "":
                pl[attr] = None
        if pl["dec"] != None:
            if pl["dec"][0] != "-":
                d = int(float(pl["dec"]) // 1)
                m = int((float(pl["dec"]) - d) * 60)
                s = int(((float(pl["dec"]) - d) * 60 - m) * 60)
                if len(str(d)) == 1:
                    d = "0" + str(d)
                if len(str(m)) == 1:
                    m = "0" + str(m)
                if len(str(s)) == 1:
                    s = "0" + str(s)
                pl["dec"] = "+" + str(d) + " " + str(m) + " " + str(s)
            else:
                d = int(float(pl["dec"][1:]) // 1)
                m = int((float(pl["dec"][1:]) - d) * 60)
                s = int(((float(pl["dec"][1:]) - d) * 60 - m) * 60)
                if len(str(d)) == 1:
                    d = "0" + str(d)
                if len(str(m)) == 1:
                    m = "0" + str(m)
                if len(str(s)) == 1:
                    s = "0" + str(s)
                pl["dec"] = "-" + str(d) + " " + str(m) + " " + str(s)
    return res


# get nasa data from csv file
def getNASA(data):
    res = []
    attr_list = data[0]
    data = data[1:]
    for i in range(len(data)):
        d = {}
        for j in range(len(data[i])):
            d[attr_list[j]] = data[i][j]
        d[None] = None
        res.append(d)
    for pl in res:
        pl["pl_bmassjerr2"] = pl["pl_bmassjerr2"][1:]
        pl["pl_orbpererr2"] = pl["pl_orbpererr2"][1:]
        pl["pl_orbsmaxerr2"] = pl["pl_orbsmaxerr2"][1:]
        pl["pl_orbeccenerr2"] = pl["pl_orbeccenerr2"][1:]
        pl["pl_orblpererr2"] = pl["pl_orblpererr2"][1:]
        pl["pl_orbtpererr2"] = pl["pl_orbtpererr2"][1:]
        pl["pl_eqterr2"] = pl["pl_eqterr2"][1:]
        pl["pl_tranmiderr2"] = pl["pl_tranmiderr2"][1:]
        pl["pl_tranmiderr2"] = pl["pl_tranmiderr2"][1:]
        pl["pl_radjerr2"] = pl["pl_radjerr2"][1:]
        pl["pl_orbinclerr2"] = pl["pl_orbinclerr2"][1:]
        if pl["pl_discmethod"] == "Transit":
            pl["pl_discmethod"] = "transit"
        elif pl["pl_discmethod"] == "Radial Velocity":
            pl["pl_discmethod"] = "RV"
        elif pl["pl_discmethod"] == "Imaging":
            pl["pl_discmethod"] = "imaging"
        elif pl["pl_discmethod"] == "Microlensing":
            pl["pl_discmethod"] = "microlensing"
        pl["rowupdate"] = pl["rowupdate"][2:]
        pl["rowupdate"] = pl["rowupdate"].replace("-", "/")
        pl["st_masserr2"] = pl["st_masserr2"][1:]
        pl["st_raderr2"] = pl["st_raderr2"][1:]
        pl["st_tefferr2"] = pl["st_tefferr2"][1:]
        pl["st_metfeerr2"] = pl["st_metfeerr2"][1:]
        pl["st_ageerr2"] = pl["st_ageerr2"][1:]
        pl["ra_str"] = pl["ra_str"].replace("h", " ")
        pl["ra_str"] = pl["ra_str"].replace("m", " ")
        pl["ra_str"] = pl["ra_str"].replace("s", "")
        if "." in pl["ra_str"]:
            pl["ra_str"] = pl["ra_str"][:pl["ra_str"].index(".")]
        pl["dec_str"] = pl["dec_str"].replace("d", " ")
        pl["dec_str"] = pl["dec_str"].replace("m", " ")
        pl["dec_str"] = pl["dec_str"].replace("s", "")
        if "." in pl["dec_str"]:
            pl["dec_str"] = pl["dec_str"][:pl["dec_str"].index(".")]
        pl["st_disterr2"] = pl["st_disterr2"][1:]
        for attr in pl:
            if pl[attr] == "":
                pl[attr] = None

    return res
