import xml.etree.cElementTree as ET
from dataclasses import dataclass
from typing import List

@dataclass
class SID:
    name: str
    runways: str
    waypoints: List[str]
    transitions: list

@dataclass
class STAR:
    name: str
    airport: str
    runways: str
    waypoints: List[str]
    transitions: List[str]

@dataclass
class Approach:
    name: str
    waypoints: list
    transitions: list

g_Sids: List[SID] = list()
g_Stars: List[STAR] = list()
g_Apprs: List[Approach] = list()

def parse(aixmFile):
    tree = ET.parse(aixmFile)
    root = tree.getroot()
    for messageMember in root:
        if not messageMember.tag == "{http://www.aixm.aero/schema/5.1.1/message}hasMember":
            continue
        for feature in messageMember:
            if feature.tag == "{http://www.aixm.aero/schema/5.1.1}StandardInstrumentArrival":
                parseStar(feature)
            elif feature.tag == "{http://www.aixm.aero/schema/5.1.1}StandardInstrumentDeparture":
                parseSid(feature)
            elif feature.tag == "{http://www.aixm.aero/schema/5.1.1}InstrumentApproachProcedure":
                parseAppr(feature)

def parseStar(feature: ET.Element):
    starTs = feature.find("{http://www.aixm.aero/schema/5.1.1}timeSlice/{http://www.aixm.aero/schema/5.1.1}StandardInstrumentArrivalTimeSlice")
    if starTs == None:
        return
    name = starTs.findtext("{http://www.aixm.aero/schema/5.1.1}designator", "")
    runways = starTs.findall("{http://www.aixm.aero/schema/5.1.1}arrival/{http://www.aixm.aero/schema/5.1.1}LandingTakeoffAreaCollection/{http://www.aixm.aero/schema/5.1.1}runway")
    runwaysTxt = ""
    for rw in runways:
        rwtxt = rw.get("{http://www.w3.org/1999/xlink}title")
        if rwtxt == None:
            rwtxt = ""
        runwaysTxt += rwtxt + ' '
    airport = starTs.find("{http://www.aixm.aero/schema/5.1.1}airportHeliport")
    if airport == None:
        print("airport is None!")
        return
    airporttxt = airport.get("{http://www.w3.org/1999/xlink}title", "")

    g_Stars.append(STAR(name, airporttxt, runwaysTxt, [], []))

def parseSid(feature: ET.Element):
    return

def parseAppr(feature: ET.Element):
    return

if __name__ == "__main__":
    parse("ED_Procedure.xml")
    for star in g_Stars:
        print(star.name, " ", star.airport, " ", star.runways)