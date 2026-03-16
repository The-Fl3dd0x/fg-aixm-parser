from lxml import etree
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
g_nsmap = {
    "aixm": "http://www.aixm.aero/schema/5.1.1",
    "message": "http://www.aixm.aero/schema/5.1.1/message"
}

def parse(aixmFile):
    tree = etree.parse(aixmFile)
    root = tree.getroot()
    for star in root.xpath("//message:hasMember/aixm:StandardInstrumentArrival", namespaces=g_nsmap):
        parseStar(star)

def parseStar(star: etree.Element):
    starTs = star.xpath("aixm:timeSlice/aixm:StandardInstrumentArrivalTimeSlice", namespaces=g_nsmap)[0]
    if starTs == None:
        return
    name = starTs.findtext("aixm:designator", "", g_nsmap)
    runways = starTs.findall("aixm:arrival/aixm:LandingTakeoffAreaCollection/aixm:runway", g_nsmap)
    runwaysTxt = ""
    for rw in runways:
        rwtxt = rw.get("{http://www.w3.org/1999/xlink}title")
        if rwtxt == None:
            rwtxt = ""
        runwaysTxt += rwtxt + ' '
    airport = starTs.find("aixm:airportHeliport", g_nsmap)
    if airport == None:
        print("airport is None!")
        return
    airporttxt = airport.get("{http://www.w3.org/1999/xlink}title", "")

    g_Stars.append(STAR(name, airporttxt, runwaysTxt, [], []))

def parseSid(feature: etree.Element):
    return

def parseAppr(feature: etree.Element):
    return

if __name__ == "__main__":
    parse("../ED_Procedure.xml")
    for star in g_Stars:
        print(star.name, " ", star.airport, " ", star.runways)