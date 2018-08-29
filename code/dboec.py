import re

attr_eu = ["name", "alternate_names", "empty_attrs", "mass", ["mass_error_max", "mass_error_min", "mass_detection_type"], "orbital_period", ["orbital_period_error_max", "orbital_period_error_min"], "semi_major_axis", ["semi_major_axis_error_max", "semi_major_axis_error_min"], "eccentricity", ["eccentricity_error_max", "eccentricity_error_min"], "omega", ["omega_error_max", "omega_error_min"], "tperi", ["tperi_error_max", "tperi_error_min"], "temp_calculated", [None, None], None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", "tzero_tr", ["tzero_tr_error_max", "tzero_tr_error_min", None], None, "empty_attrs", None, "empty_attrs", [], [], "tperi", ["tperi_error_max", "tperi_error_min"], None, "empty_attrs", None, "empty_attrs", "radius", ["radius_error_max", "radius_error_min"], "inclination", ["inclination_error_max", "inclination_error_min"], None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", None, None, [], None, None, "discovered", "detection_type", "updated", None, None, "star_name", "star_alternate_names", "empty_attrs", "star_age", ["star_age_error_min", "star_age_error_max"], "star_mass", ["star_mass_error_max", "star_mass_error_min"], "star_radius", ["star_radius_error_max", "star_radius_error_min"], "mag_v", [None, None], "mag_i", [None, None], "mag_j", [None, None], "mag_h", [None, None], "mag_k", [None, None], None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", "star_teff", ["star_teff_error_max", "star_teff_error_min"], "star_metallicity", ["star_metallicity_error_max", "star_metallicity_error_min"], "star_sp_type", "empty_attrs", "star_name", None, "empty_attrs", None, [None, None], None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", "dec", None, None, None]

attr_nasa = ["pl_name", None, "empty_attrs", "pl_bmassj", ["pl_bmassjerr1", "pl_bmassjerr2", "pl_bmassprov"], "pl_orbper", ["pl_orbpererr1", "pl_orbpererr2"], "pl_orbsmax", ["pl_orbsmaxerr1", "pl_orbsmaxerr2"], "pl_orbeccen", ["pl_orbeccenerr1", "pl_orbeccenerr2"], "pl_orblper", ["pl_orblpererr1", "pl_orblpererr2"], "pl_orbtper", ["pl_orbtpererr1", "pl_orbtpererr2"], "pl_eqt", ["pl_eqterr1", "pl_eqterr2"], None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", "pl_tranmid", ["pl_tranmiderr1", "pl_tranmiderr2", "pl_tsystemref"], None, "empty_attrs", None, "empty_attrs", "[]", "[]", "pl_orbtper", ["pl_orbtpererr1", "pl_orbtpererr2"], None, "empty_attrs", None, "empty_attrs", "pl_radj", ["pl_radjerr1", "pl_radjerr2"], "pl_orbincl", ["pl_orbinclerr1", "pl_orbinclerr2"], None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", None, None, "[]", None, None, "pl_disc", "pl_discmethod", "rowupdate", None, None, "pl_hostname", None, "empty_attrs", "st_age", ["st_ageerr1", "st_ageerr2"], "st_mass", ["st_masserr1", "st_masserr2"], "st_rad", ["st_raderr1", "st_raderr2"], "st_optmag", ["st_optmagerr", "st_optmagerr"], "st_bj", ["st_bjerr", "st_bjerr"], "st_j", ["st_jerr", "st_jerr"], "st_h", ["st_herr", "st_herr"], "st_k", ["st_kerr", "st_kerr"], None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", "st_teff", ["st_tefferr1", "st_tefferr2"], "st_metfe", ["st_metfeerr1", "st_metfeerr2"], "st_spstr", "empty_attrs", "pl_hostname", None, "empty_attrs", "st_dist", ["st_disterr1", "st_disterr2"], None, "empty_attrs", None, "empty_attrs", None, "empty_attrs", "dec_str", "ra_str", None, None]


pattern = re.compile(".*_attrs")


class Database:
    '''A database object with list of systems and list of planets
    '''
    def __init__(self):
        '''Initial the database
        (Database) -> None
        '''
        self.system = []
        self.pldata = []

    def __str__(self):
        '''print the database
        (Database) -> None
        '''
        res = ""
        for sys in self.system:
            res += str(sys)
        return res

    def __eq__(self, other):
        '''Return True if all the two Databases contain the same list of systems
        and planet data.
        (Database, Database) -> bool
        '''
        if type(other) is type(self):

            # Checks all systems in self are in other
            for system in self.system:
                matchFound = False
                for otherSystem in other.system:
                    if system == otherSystem:
                        matchFound = True
                        continue
                if not matchFound:
                    return False

            # Checks all systems in other are in self
            for system in other.system:
                matchFound = False
                for selfSystem in self.system:
                    if system == selfSystem:
                        matchFound = True
                        continue
                if not matchFound:
                    return False
            return True
        else:
            return False

    def update_csv(self, data, attr_list):
        '''auto update the given list converted from csv into the database
        (Database, list of dict, list of attribution) -> None
        '''
        for pl in data:
            newpl = Planet()
            newpl.name.append(pl[attr_list[0]])
            if pl[attr_list[1]] != None:
                newpl.name += pl[attr_list[1]].split(",")
            l = []
            for n in newpl.name:
                n = n.strip()
                l.append(n)
            newpl.name = l
            #while "" in newpldata["name"]:
                #newpldata["name"].remove("")
            #newpl.name_attrs = attr_list[2]
            newpl.mass = pl[attr_list[3]]
            newpl.mass_attrs["errorplus"] = pl[attr_list[4][0]]
            newpl.mass_attrs["errorminus"] = pl[attr_list[4][1]]
            newpl.mass_attrs["type"] = pl[attr_list[4][2]]
            newpl.period = pl[attr_list[5]]
            newpl.period_attrs["errorplus"] = pl[attr_list[6][0]]
            newpl.period_attrs["errorminus"] = pl[attr_list[6][1]]
            newpl.semimajoraxis = pl[attr_list[7]]
            newpl.semimajoraxis_attrs["errorplus"] = pl[attr_list[8][0]]
            newpl.semimajoraxis_attrs["errorminus"] = pl[attr_list[8][1]]
            newpl.eccentricity = pl[attr_list[9]]
            newpl.eccentricity_attrs["errorplus"] = pl[attr_list[10][0]]
            newpl.eccentricity_attrs["errorminus"] = pl[attr_list[10][1]]
            newpl.periastron = pl[attr_list[11]]
            newpl.periastron_attrs["errorplus"] = pl[attr_list[12][0]]
            newpl.periastron_attrs["errorminus"] = pl[attr_list[12][1]]
            newpl.periastrontime = pl[attr_list[13]]
            newpl.periastrontime_attrs["errorplus"] = pl[attr_list[14][0]]
            newpl.periastrontime_attrs["errorminus"] = pl[attr_list[14][1]]
            newpl.temperature = pl[attr_list[15]]
            newpl.temperature_attrs["errorplus"] = pl[attr_list[16][0]]
            newpl.temperature_attrs["errorminus"] = pl[attr_list[16][1]]
            newpl.age = pl[attr_list[17]]
            #newpl.age_attrs = pl[attr_list[18]]
            newpl.ascendingnode = pl[attr_list[19]]
            #newpl.ascendingnode_attrs = pl[attr_list[20]]
            newpl.longitude = pl[attr_list[21]]
            #newpl.longitude_attrs = pl[attr_list[22]]
            newpl.transittime = pl[attr_list[23]]
            newpl.transittime_attrs["errorplus"] = pl[attr_list[24][0]]
            newpl.transittime_attrs["errorminus"] = pl[attr_list[24][1]]
            newpl.transittime_attrs["unit"] = pl[attr_list[24][2]]
            newpl.positionangle = pl[attr_list[25]]
            #newpl.positionangle_attrs = pl[attr_list[26]]
            newpl.spectraltype = pl[attr_list[27]]
            #newpl.spectraltype_attrs = pl[attr_list[28]]
            #newpl.separation = pl[attr_list[29]]
            #newpl.separation_attrs = pl[attr_list[30]]
            newpl.maximumrvtime = pl[attr_list[31]]
            newpl.maximumrvtime_attrs["errorplus"] = pl[attr_list[32][0]]
            newpl.maximumrvtime_attrs["errorminus"] = pl[attr_list[32][1]]
            newpl.impactparameter = pl[attr_list[33]]
            #newpl.impactparameter_attrs = pl[attr_list[34]]
            newpl.spinorbitalignment = pl[attr_list[35]]
            #newpl.spinorbitalignment_attrs = pl[attr_list[36]]
            newpl.radius = pl[attr_list[37]]
            newpl.radius_attrs["errorplus"] = pl[attr_list[38][0]]
            newpl.radius_attrs["errorminus"] = pl[attr_list[38][1]]
            newpl.inclination = pl[attr_list[39]]
            newpl.inclination_attrs["errorplus"] = pl[attr_list[40][0]]
            newpl.inclination_attrs["errorminus"] = pl[attr_list[40][1]]
            newpl.meananomaly = pl[attr_list[41]]
            #newpl.meananomaly_attrs = pl[attr_list[42]]
            newpl.magJ = pl[attr_list[43]]
            #newpl.magJ_attrs = pl[attr_list[44]]
            newpl.magH = pl[attr_list[45]]
            #newpl.magH_attrs = pl[attr_list[46]]
            newpl.magK = pl[attr_list[47]]
            #newpl.magK_attrs = pl[attr_list[48]]
            newpl.magI = pl[attr_list[49]]
            #newpl.magI_attrs = pl[attr_list[50]]
            newpl.metallicity = pl[attr_list[51]]
            newpl.new = pl[attr_list[52]]
            #newpl.list = pl[attr_list[53]]
            newpl.istransiting = pl[attr_list[54]]
            newpl.description = pl[attr_list[55]]
            newpl.discoveryyear = pl[attr_list[56]]
            newpl.discoverymethod = pl[attr_list[57]]
            newpl.lastupdate = pl[attr_list[58]]
            newpl.image = pl[attr_list[59]]
            newpl.imagedescription = pl[attr_list[60]]

            newst = Star()
            newst.name.append(pl[attr_list[61]])
            if pl[attr_list[62]] != None:
                newst.name += pl[attr_list[62]].split(",")
            l = []
            for n in newst.name:
                n = n.strip()
                l.append(n)
            newst.name = l
            #newst.name_attrs = pl[attr_list[63]]
            newst.planet.append(newpl)
            newst.age = pl[attr_list[64]]
            newst.age_attrs["errorplus"] = pl[attr_list[65][0]]
            newst.age_attrs["errorminus"] = pl[attr_list[65][1]]
            newst.mass = pl[attr_list[66]]
            newst.mass_attrs["errorplus"] = pl[attr_list[67][0]]
            newst.mass_attrs["errorminus"] = pl[attr_list[67][1]]
            newst.radius = pl[attr_list[68]]
            newst.radius_attrs["errorplus"] = pl[attr_list[69][0]]
            newst.radius_attrs["errorminus"] = pl[attr_list[69][1]]
            newst.magV = pl[attr_list[70]]
            newst.magV_attrs["errorplus"] = pl[attr_list[71][0]]
            newst.magV_attrs["errorminus"] = pl[attr_list[71][1]]
            newst.magB = pl[attr_list[72]]
            newst.magB_attrs["errorplus"] = pl[attr_list[73][0]]
            newst.magB_attrs["errorminus"] = pl[attr_list[73][1]]
            newst.magJ = pl[attr_list[74]]
            newst.magJ_attrs["errorplus"] = pl[attr_list[75][0]]
            newst.magJ_attrs["errorminus"] = pl[attr_list[75][1]]
            newst.magH = pl[attr_list[76]]
            newst.magH_attrs["errorplus"] = pl[attr_list[77][0]]
            newst.magH_attrs["errorminus"] = pl[attr_list[77][1]]
            newst.magK = pl[attr_list[78]]
            newst.magK_attrs["errorplus"] = pl[attr_list[79][0]]
            newst.magK_attrs["errorminus"] = pl[attr_list[79][1]]
            newst.magI = pl[attr_list[80]]
            #newst.magI_attrs = pl[attr_list[81]]
            newst.magR = pl[attr_list[82]]
            #newst.magR_attrs = pl[attr_list[83]]
            newst.magU = pl[attr_list[84]]
            #newst.magU_attrs = pl[attr_list[85]]
            newst.temperature = pl[attr_list[86]]
            newst.temperature_attrs["errorplus"] = pl[attr_list[87][0]]
            newst.temperature_attrs["errorminus"] = pl[attr_list[87][1]]
            newst.metallicity = pl[attr_list[88]]
            newst.metallicity_attrs["errorplus"] = pl[attr_list[89][0]]
            newst.metallicity_attrs["errorminus"] = pl[attr_list[89][1]]
            newst.spectraltype = pl[attr_list[90]]
            #newst.spectraltype_attrs = pl[attr_list[91]]

            newsys = System()
            newsys.name.append(pl[attr_list[92]])
            if pl[attr_list[93]] != None:
                newsys.name += pl[attr_list[93]].split(",")
            l = []
            for n in newsys.name:
                n = n.strip()
                l.append(n)
            newsys.name = l
            #newsys.name_attrs = pl[attr_list[94]]
            newsys.star.append(newst)
            newsys.planet.append(newpl)
            newsys.distance = pl[attr_list[95]]
            newsys.distance_attrs["errorplus"] = pl[attr_list[96][0]]
            newsys.distance_attrs["errorminus"] = pl[attr_list[96][1]]
            newsys.magH = pl[attr_list[97]]
            #newsys.magH_attrs = pl[attr_list[98]]
            newsys.magJ = pl[attr_list[99]]
            #newsys.magJ_attrs = pl[attr_list[100]]
            newsys.magK = pl[attr_list[101]]
            #newsys.magK_attrs = pl[attr_list[102]]
            newsys.declination = pl[attr_list[103]]
            newsys.rightascension = pl[attr_list[104]]
            newsys.spectraltype = pl[attr_list[105]]
            newsys.videolink = pl[attr_list[106]]

            # if the sys is already in db, append the pl to the st in sys
            marker = False
            for sys in self.system:
                if set(sys.name) & set(newsys.name) != set():
                    sys.star[0].planet.append(newpl)
                    sys.planet.append(newpl)
                    marker = True
                    break
            if not marker:
                self.system.append(newsys)
            self.pldata.append(newpl)

    def update_xml(self, data):
        '''auto update the given dict converted from xml into the database
        (Database, dict) -> None
        '''
        sys = data["system"]
        # if the system is of type dict, then there is only one system
        if type(sys) == dict:
            newsys = self.createSys(sys)
            self.system.append(newsys)
        # else there are many systems, loop through each one to create system object
        else:
            for eachsys in sys:
                newsys = self.createSys(eachsys)
                self.system.append(newsys)

    def createSys(self, system):
        '''Create A system object based on the given system data
        '''
        newsys = System()
        for sysattr in system:
            if pattern.match(sysattr) and sysattr != "name_attrs":
                for each in system[sysattr]:
                    getattr(newsys, sysattr)[each] = system[sysattr][each]
            elif (sysattr != "star" and sysattr != "binary" and
                  sysattr != "name" and sysattr != "planet"):
                setattr(newsys, sysattr, system[sysattr])
            elif sysattr == "name" and type(system[sysattr]) == str:
                newsys.name.append(system[sysattr])
            elif sysattr == "name":
                setattr(newsys, sysattr, system[sysattr])
            elif sysattr == "star":
                st = system["star"]
                if type(st) == list:
                    for eachst in st:
                        newst = self.createSt(eachst, newsys)
                        newsys._star.append(newst)
                else:
                    newst = self.createSt(st, newsys)
                    newsys._star.append(newst)
            elif sysattr == "planet":
                pl = system["planet"]
                if type(pl) == list:
                    for eachpl in pl:
                        newpl = self.createPl(eachpl, newsys)
                        newsys._planet.append(newpl)
                else:
                    newpl = self.createPl(pl, newsys)
                    newsys._planet.append(newpl)
            else:
                bina = system["binary"]
                newbin = self.createBin(bina, newsys)
                newsys.binary.append(newbin)
        return newsys

    def createBin(self, binary, system):
        '''Create a binary object based on the given binary and system data
        '''
        newbin = Binary()
        newbin.system = system
        for binattr in binary:
            if (pattern.match(binattr) and binattr != "separation_attrs" and binattr != "name_attrs"):
                if type(binary[binattr]) == dict:
                    for each in binary[binattr]:
                        getattr(newbin, binattr)[each] = binary[binattr][each]
                else:
                    for eachattr in binary[binattr]:
                        for each in eachattr:
                            getattr(newbin, binattr)[each] = eachattr[each]
            elif (binattr != "star" and binattr != "binary" and
                  binattr != "name" and binattr != "planet"):
                setattr(newbin, binattr, binary[binattr])
            elif binattr == "name" and type(binary[binattr]) == str:
                newbin.name.append(binary[binattr])
            elif binattr == "name":
                setattr(newbin, binattr, binary[binattr])
            elif binattr == "star":
                st = binary["star"]
                if type(st) == list:
                    for eachst in st:
                        newst = self.createSt(eachst, system)
                        newbin.star.append(newst)
                else:
                    newst = self.createSt(st, system)
                    newbin.star.append(newst)
            elif binattr == "planet":
                pl = binary["planet"]
                if type(pl) == list:
                    for eachpl in pl:
                        newpl = self.createPl(eachpl, system)
                        newbin.planet.append(newpl)
                else:
                    newpl = self.createPl(pl, system)
                    newbin.planet.append(newpl)
            else:
                bina = binary["binary"]
                if type(bina) == list:
                    for eachbin in bina:
                        binbin = self.createBin(eachbin, system)
                        newbin.binary.append(binbin)
                else:
                    binbin = self.createBin(bina, system)
                    newbin.binary.append(binbin)
        return newbin

    def createSt(self, star, system):
        '''Create a star object based on the given star and system data
        '''
        newst = Star()
        for stattr in star:
            if stattr == "name" and type(star[stattr]) == str:
                newst.name.append(star[stattr])
            elif pattern.match(stattr) and stattr != "name_attrs":
                for each in star[stattr]:
                    getattr(newst, stattr)[each] = star[stattr][each]
            elif stattr != "planet" or stattr == "name":
                setattr(newst, stattr, star[stattr])
            else:
                pl = star["planet"]
                if type(pl) == list:
                    for eachpl in pl:
                        newpl = self.createPl(eachpl, system)
                        newst.planet.append(newpl)
                else:
                    newpl = self.createPl(pl, system)
                    newst.planet.append(newpl)
        system.star.append(newst)
        return newst

    def createPl(self, planet, system):
        '''Create a planet object based on the given planet and system object
        '''
        newpl = Planet()
        for plattr in planet:
            if plattr == "name" and type(planet[plattr]) == str:
                newpl.name.append(planet[plattr])
            elif (pattern.match(plattr) and plattr != "separation_attrs" and
                  plattr != "name_attrs"):
                if type(planet[plattr]) == dict:
                    for each in planet[plattr]:
                        getattr(newpl, plattr)[each] = planet[plattr][each]
                else:
                    for eachattr in planet[plattr]:
                        for each in eachattr:
                            getattr(newpl, plattr)[each] = eachattr[each]
            else:
                setattr(newpl, plattr, planet[plattr])
        self.pldata.append(newpl)
        system.planet.append(newpl)
        return newpl


class System:
    '''A system object
    '''
    def __init__(self):
        '''Initialize a system object, the feature can be set afterwards
        '''
        self.name = []
        self.name_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.star = []
        self._star = []
        self.binary = []
        self.planet = []
        self._planet = []
        self.distance = None
        self.distance_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                               'unit': None, 'upperlimit': None, 'lowerlimit': None,
                               'type': None}
        self.magH = None
        self.magH_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magJ = None
        self.magJ_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magK = None
        self.magK_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.declination = None
        self.rightascension = None
        self.spectraltype = None
        self.videolink = None
        self.mk = False
        self.mod = False

    def __str__(self):
        '''Return a string to represent the system
        '''
        res = "system: " + str(self.name) + "\n"
        self_attr = self.__dict__.keys()
        for i in self_attr:
            if i != "star" and i != "binary" and i != "_star":
                if getattr(self, i):
                    res += "    " + str(i) + ": " + str(getattr(self, i)) + "\n"
            elif i == "star":
                for st in getattr(self, i):
                    res += str(st)
        return res

    def get_planet(self):
        '''Get the planet list
        '''
        res = []
        for st in self.star:
            for pl in st.planet:
                for p in pl.name:
                    if p not in res:
                        res.append(p)
        return res

    def match(self, other):
        '''Compare if the two system have the same planets
        '''
        return set(other.get_planet()) & set(self.get_planet()) != set()

    def __eq__(self, other):
        '''Return True if all the properties of self and other are the same
        (including order of lists), False otherwise
        (System, System) -> bool
        '''
        if type(other) is type(self):
            p1 = dict(self.__dict__)
            p2 = dict(other.__dict__)

            # Ignores the object's non-system properties during comparison
            del p1['mk']
            del p2['mk']
            del p1['_star']
            del p2['_star']
            return p1 == p2
        else:
            return False


class Binary:
    '''A binary object
    '''
    def __init__(self):
        '''Initialize a binary object, features can be set afterwards
        '''
        self.name = []
        self.name_attrs = []
        self.magB = None
        self.magB_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magV = None
        self.magV_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magR = None
        self.magR_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magI = None
        self.magI_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magJ = None
        self.magJ_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magH = None
        self.magH_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magK = None
        self.magK_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.separation = []
        self.separation_attrs = []
        self.positionangle = None
        self.positionangle_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                    'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                    'type': None}
        self.period = None
        self.period_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                             'unit': None, 'upperlimit': None, 'lowerlimit': None,
                             'type': None}
        self.inclination = None
        self.inclination_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                  'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                  'type': None}
        self.transittime = None
        self.transittime_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                  'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                  'type': None}
        self.semimajoraxis = None
        self.semimajoraxis_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                    'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                    'type': None}
        self.eccentricity = None
        self.eccentricity_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                   'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                   'type': None}
        self.longitude = None
        self.periastron = None
        self.periastron_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                 'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                 'type': None}
        self.periastrontime = None
        self.periastrontime_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                     'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                     'type': None}
        self.ascendingnode = None
        self.ascendingnode_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                    'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                    'type': None}
        self.binary = []
        self.star = []
        self.planet = []
        self.system = None

    def __eq__(self, other):
        '''Return True if all the properties of self and other are the same
        (including order of lists), False otherwise
        (Binary, Binary) -> bool
        '''
        if type(other) is type(self):
            p1 = dict(self.__dict__)
            p2 = dict(other.__dict__)

            # Compares the Binary dictionaries' system values after removing
            # the binary attribute to prevent infinite recursive comparison
            system1 = p1.get('system')
            system1.binary = []
            system2 = p2.get('system')
            system2.binary = []
            commonSystem = system1 == system2

            # Removes system attributes from these Binaries to compare them
            del p1['system']
            del p2['system']

            return p1 == p2 and commonSystem
        else:
            return False


class Star:
    '''A Star object
    '''
    def __init__(self):
        '''Initialize a star object, features can be set afterwards
        '''
        self.name = []
        self.name_attrs = []
        self.planet = []
        self.age = None
        self.age_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                          'unit': None, 'upperlimit': None, 'lowerlimit': None,
                          'type': None}
        self.mass = None
        self.mass_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.radius = None
        self.radius_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                             'unit': None, 'upperlimit': None, 'lowerlimit': None,
                             'type': None}
        self.magV = None
        self.magV_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magB = None
        self.magB_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magJ = None
        self.magJ_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magH = None
        self.magH_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magK = None
        self.magK_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magI = None
        self.magI_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magR = None
        self.magR_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magU = None
        self.magU_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.temperature = None
        self.temperature_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                  'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                  'type': None}
        self.metallicity = None
        self.metallicity_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                  'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                  'type': None}
        self.spectraltype = None
        self.spectraltype_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                   'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                   'type': None}
        self.mk = False
        self.mod = False

    def __str__(self):
        '''Return a string to represent the star
        '''
        res = "    star: " + str(self.name) + "\n"
        self_attr = self.__dict__.keys()
        for i in self_attr:
            if i != "planet":
                if getattr(self, i):
                    res += "        " + str(i) + ": " + str(getattr(self, i)) + "\n"
            else:
                for pl in getattr(self, i):
                    res += str(pl)

        return res

    def __eq__(self, other):
        '''Return True if all the properties of self and other are the same
        (including order of lists), False otherwise
        (Star, Star) -> bool
        '''
        if type(other) is type(self):
            p1 = dict(self.__dict__)
            p2 = dict(other.__dict__)

            # Ignores the object's non-star properties during comparison
            del p1['mk']
            del p2['mk']
            return p1 == p2
        else:
            return False


class Planet:
    '''A planet object
    '''
    def __init__(self):
        '''Initialize the planet object, features can be set afterwards
        '''
        self.name = []
        self.name_attrs = []
        self.mass = None
        self.mass_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.period = None
        self.period_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                             'unit': None, 'upperlimit': None, 'lowerlimit': None,
                             'type': None}
        self.semimajoraxis = None
        self.semimajoraxis_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                    'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                    'type': None}
        self.eccentricity = None
        self.eccentricity_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                   'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                   'type': None}
        self.periastron = None
        self.periastron_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                 'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                 'type': None}
        self.periastrontime = None
        self.periastrontime_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                     'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                     'type': None}
        self.temperature = None
        self.temperature_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                  'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                  'type': None}
        self.age = None
        self.age_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                          'unit': None, 'upperlimit': None, 'lowerlimit': None,
                          'type': None}
        self.ascendingnode = None
        self.ascendingnode_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                    'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                    'type': None}
        self.longitude = None
        self.longitude_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                'type': None}
        self.transittime = None
        self.transittime_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                  'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                  'type': None}
        self.positionangle = None
        self.positionangle_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                    'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                    'type': None}
        self.spectraltype = None
        self.spectraltype_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                   'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                   'type': None}
        self.separation = []
        self.separation_attrs = []
        self.maximumrvtime = None
        self.maximumrvtime_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                    'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                    'type': None}
        self.impactparameter = None
        self.impactparameter_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                      'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                      'type': None}
        self.spinorbitalignment = None
        self.spinorbitalignment_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                         'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                         'type': None}
        self.radius = None
        self.radius_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                             'unit': None, 'upperlimit': None, 'lowerlimit': None,
                             'type': None}
        self.inclination = None
        self.inclination_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                  'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                  'type': None}
        self.meananomaly = None
        self.meananomaly_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                                  'unit': None, 'upperlimit': None, 'lowerlimit': None,
                                  'type': None}
        self.magJ = None
        self.magJ_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magH = None
        self.magH_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magK = None
        self.magK_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.magI = None
        self.magI_attrs = {'error': None, 'errorplus': None, 'errorminus': None,
                           'unit': None, 'upperlimit': None, 'lowerlimit': None,
                           'type': None}
        self.metallicity = None
        self.new = None
        self.list = []
        self.istransiting = None
        self.description = None
        self.discoveryyear = None
        self.discoverymethod = None
        self.lastupdate = None
        self.image = None
        self.imagedescription = None
        self.mk = False
        self.mod = False

    def __str__(self):
        '''Return a string to represent the planet
        '''
        res = "        planet: " + str(self.name) + "\n"
        self_attr = self.__dict__.keys()
        for i in self_attr:
            if i != 'system':
                if getattr(self, i):
                    res += "            " + str(i) + ": "
                    res += str(getattr(self, i)) + "\n"
        return res

    def __eq__(self, other):
        '''Return True if all the properties of self and other are the same
        (including order of lists), False otherwise
        (Planet, Planet) -> bool
        '''
        p1 = dict(self.__dict__)
        p2 = dict(other.__dict__)

        # Ignores the object's non-planet properties during comparison
        del p1['lastupdate']
        del p2['lastupdate']
        del p1['mk']
        del p2['mk']
        return p1 == p2

if __name__ == '__main__':

    import convert
    import csv
    import requests
    import merge
    import gzip
    import get_xml
    from xml.dom import minidom

    #url1 = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
    #with requests.Session() as s:
        #download = s.get(url1)
        #with open("systems.xml.gz", "wb") as gz:
            #gz.write(download.content)
    #g_file = gzip.GzipFile("systems.xml.gz")
    #open("systems.xml", "w+").write(g_file.read())
    #g_file.close()
    #data_oec = minidom.parse("systems.xml")
    #dat1 = convert.getOEC(data_oec)
    #d1 = Database()
    #d1.update_xml(dat1)

    #d2 = Database()
    #url2 = "http://exoplanet.eu/catalog/csv"
    #data2 = []
    #with requests.Session() as s:
        #download = s.get(url2)
        #decoded_content = download.content.decode('utf-8')
        #cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        #my_list = list(cr)
        #for row in my_list:
            #data2.append(row)
    #dat2 = convert.getEU(data2)
    #d2.update_csv(dat2, attr_eu)

    #d3 = Database()
    #url3 = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=*"
    #data3 = []
    #with requests.Session() as s:
        #download = s.get(url3)
        #decoded_content = download.content.decode('utf-8')
        #cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        #my_list = list(cr)
        #for row in my_list:
            #data3.append(row)
    #dat3 = convert.getNASA(data3)
    #d3.update_csv(dat3, attr_nasa)

    #dm1 = merge.merge(d2, d1)
    #dm2 = merge.merge(d3, dm1)

    #for sys in dm2.system:
        #get_xml.toXml(sys)

    #get_xml.toXml(dm1.system[0])


    #a=[]
    #for i in dm2.system:
        #for j in i.name:
            #if "1938" in j:
                #a.append(i)
    #b=[]
    #for i in d2.system:
        #for j in i.name:
            #if "1938" in j:
                #b.append(i)
    #c=[]
    #for i in d3.system:
        #for j in i.name:
            #if "1938" in j:
                #c.append(i)
