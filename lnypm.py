# -*- coding: utf-8 -*-

import sys
from lxml import etree
from functools import partial
from templatemaker import Comparator
import codecs

def svgfactory(elem, **kwargs):
    return partial(etree.Element, '{http://www.w3.org/2000/svg}%s' % elem, 
                   nsmap = {"svg": "http://www.w3.org/2000/svg"}, **kwargs)

svg = svgfactory("svg")
circle = svgfactory("circle")
line = svgfactory("line")
text = svgfactory("text")

def parse_table(data):
    return [line.split("\t") for line in data]
    
def compare(city):
    res = []
    city = city.lower()
    cities = parse_table(open("cities1000.txt", "rb"))
    for c in cities:
        comp = Comparator(city, c[1].lower())
        subseq = comp.longest_substring()
        if len(subseq) > 1:
            res.append((len(subseq), c[2], float(c[4]), float(c[5])))
    return sorted(res, reverse=True)

def main(city, startx=0, starty=0, color="#000", res=None, multiple=2.5, r=2,
         hilite="#f00"):
    if res is None:
        res = svg(width="720", height="360", style="background-color: white;")
    cities = compare(city.encode("latin-1"))
    opacityscale = 3
    opacityconstant = 0.5
    xmin = str(startx); xmax = str(multiple*360 + startx)
    ymin = str(starty); ymax = str(multiple*180 + starty)
    res.append(line(x1=xmin, x2=xmax, y1=ymin, y2=ymin, strokewidth="1", 
                    stroke="black"))
    res.append(line(x1=xmin, x2=xmax, y1=ymax, y2=ymax, strokewidth="1", 
                    stroke="black"))
    res.append(line(x1=xmax, x2=xmax, y1=ymin, y2=ymax, strokewidth="1", 
                    stroke="black"))
    res.append(line(x1=xmin, x2=xmin, y1=ymin, y2=ymax, strokewidth="1", 
                    stroke="black"))

    t = text(x=str((multiple-0.25)*360 + startx), 
             y=str((multiple-0.25)*180 + starty),
             style="font-family: Helvetica;")
    t.text = city
    defer = []
    res.append(t)
    for i in cities:
        x, y = (i[3]+180) * multiple + startx, (i[2]-90) * -multiple + starty
        scale = float(i[0])/len(city)
        oscale = scale ** opacityscale
        opacity = opacityconstant * oscale
        if oscale == 1:
            defer.append(i)
        else:
            res.append(circle(cy=str(y), cx=str(x), r=str(r), 
                       style="stroke-width: 0.5; fill: none; stroke: %s; \
                              opacity: %s" % (color, opacity),
                       id=unicode(i[1]+str(x)+str(y), encoding="utf-8")))
    for i in defer:
        x, y = (i[3]+180) * multiple + startx, (i[2]-90) * -multiple + starty
        scale = float(i[0])/len(city)
        oscale = scale ** opacityscale
        opacity = opacityconstant * oscale
        res.append(circle(cy=str(y), cx=str(x), r=str(r), 
                   style="stroke-width: 0; fill: %s; opacity: %s" % 
                                                        (hilite, 1),
                   id=unicode(i[1]+str(x)+str(y), encoding="utf-8")))
    return res
    
if __name__ == "__main__":
    res = main("London", multiple=1, r=1)
    res = main("New York", multiple=1, r=1, startx=360, res=res)
    res = main("Paris", multiple=1, r=1, starty=180, res=res)
    res = main(u"München", multiple=1, r=1, starty=180, startx=360, res=res)
    tree = etree.ElementTree(res)
    tree.write(open(sys.argv[1], "wb"))
    