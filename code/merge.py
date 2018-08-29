import dboec
import datetime


def merge(other, oec):
    for sys1 in other.system:
        for sys2 in oec.system:
            sys2 = add_to_system(sys1, sys2)
        if not sys1.mk:
            sys1.mk = True
            sys1.mod = True
            sys1._star += sys1.star
            oec.system.append(sys1)

    # change lastupdate
    for sys in oec.system:
        if sys.mod:
            for st in sys.star:
                for pl in st.planet:
                    pl.lastupdate = datetime.date.today().strftime("%y/%m/%d")
        else:
            for st in sys.star:
                if st.mod:
                    for pl in st.planet:
                        pl.lastupdate = datetime.date.today().strftime("%y/%m/%d")
                else:
                    for pl in st.planet:
                        if pl.mod:
                            pl.lastupdate = datetime.date.today().strftime("%y/%m/%d")

    # change mk and mod for every system, star, planet
    for sys in oec.system:
        sys.mk = False
        sys.mod = False
        for st in sys.star:
            st.mk = False
            st.mod = False
            for pl in st.planet:
                pl.mk = False
                pl.mod = False
    return oec


def add_name(obj1, obj2):
    '''merge the name of two objects
    '''
    name = []
    for i in obj1.name:
        if i not in name:
            name.append(i)
    for j in obj2.name:
        if j not in name:
            name.append(j)
    return name


def add_to_system(sys1, sys2):
    '''merge attribution in sys1 and sys2 into db
    '''
    if sys2.match(sys1):
        sys1.mk = True
        sys2.mk = True
        for sys_attr in sys1.__dict__:
            if sys_attr == "name":
                if not set(sys1.name) <= set(sys2.name):
                    sys2.mod = True
                    sys2.name = add_name(sys1, sys2)
            elif sys_attr == "star":
                for st1 in sys1.__dict__["star"]:
                    for st2 in sys2.__dict__["star"]:
                        st2 = add_to_star(st1, st2)
                    if not st1.mk:
                        st1.mk = True
                        sys2.mod = True
                        sys2._star.append(st1)
                        sys2.star.append(st1)
            #elif sys_attr == "planet":
                #for pl1 in sys1.__dict__["planet"]:
                    #for pl2 in sys2.__dict__["planet"]:
                        #pl2 = add_to_planet(pl1, pl2)
                    #if not pl1.mk:
                        #pl1.mk = True
                        #sys2.mod = True
                        #sys2.planet.append(pl1)
            elif (sys_attr != "_star" and
                  sys_attr != "_planet" and
                  sys_attr != "binary" and
                  sys_attr != "mk" and
                  sys_attr != "mod"):
                if sys1.__dict__[sys_attr] != None:
                    if type(sys1.__dict__[sys_attr]) == dict:
                        for attr in sys1.__dict__[sys_attr]:
                            if (sys1.__dict__[sys_attr][attr] != None and
                                    sys1.__dict__[sys_attr][attr] != sys2.__dict__[sys_attr][attr]):
                                sys2.mod = True
                                sys2.__dict__[sys_attr][attr] = sys1.__dict__[sys_attr][attr]
                    else:
                        if sys1.__dict__[sys_attr] != sys2.__dict__[sys_attr]:
                            sys2.mod = True
                            sys2.__dict__[sys_attr] = sys1.__dict__[sys_attr]
    return sys2


def add_to_star(st1, st2):
    '''merge attribution in st1 and st2 into sys
    '''
    # two stars are same
    if set(st1.name) & set(st2.name) != set():
        st1.mk = True
        st2.mk = True
        for st_attr in st1.__dict__:
            if st_attr == "name":
                if not set(st1.name) <= set(st2.name):
                    st2.mod = True
                    st2.name = add_name(st1, st2)
            elif st_attr == "planet":
                for pl1 in st1.__dict__["planet"]:
                    for pl2 in st2.__dict__["planet"]:
                        pl2 = add_to_planet(pl1, pl2)
                    if not pl1.mk:
                        pl1.mk = True
                        st2.mod = True
                        st2.planet.append(pl1)
            elif st_attr != "mk" and st_attr != "mod":
                if st1.__dict__[st_attr] != None:
                    if type(st1.__dict__[st_attr]) == dict:
                        for attr in st1.__dict__[st_attr]:
                            if (st1.__dict__[st_attr][attr] != None and
                                    st1.__dict__[st_attr][attr] != st2.__dict__[st_attr][attr]):
                                st2.mod = True
                                st2.__dict__[st_attr][attr] = st1.__dict__[st_attr][attr]
                    else:
                        if st1.__dict__[st_attr] != st2.__dict__[st_attr]:
                            st2.mod = True
                            st2.__dict__[st_attr] = st1.__dict__[st_attr]
    return st2


def add_to_planet(pl1, pl2):
    '''merge attribution in pl1 and pl2 into st
    '''
    # two planets are same
    if set(pl1.name) & set(pl2.name) != set():
        pl1.mk = True
        pl2.mk = True
        for pl_attr in pl1.__dict__:
            if pl_attr == "name":
                if not set(pl1.name) <= set(pl2.name):
                    pl2.mod = True
                    pl2.name = add_name(pl1, pl2)
            elif (pl_attr != "mk" and
                  pl_attr != "list" and
                  pl_attr != "lastupdate" and
                  pl_attr != "mod"):
                if pl1.__dict__[pl_attr] != None:
                    if type(pl1.__dict__[pl_attr]) == dict:
                        for attr in pl1.__dict__[pl_attr]:
                            if (pl1.__dict__[pl_attr][attr] != None and
                                    pl1.__dict__[pl_attr][attr] != pl2.__dict__[pl_attr][attr]):
                                pl2.mod = True
                                pl2.__dict__[pl_attr][attr] = pl1.__dict__[pl_attr][attr]
                    else:
                        if pl1.__dict__[pl_attr] != pl2.__dict__[pl_attr]:
                            pl2.mod = True
                            pl2.__dict__[pl_attr] = pl1.__dict__[pl_attr]
    return pl2
