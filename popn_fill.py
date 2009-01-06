# -*- coding: utf-8 -*-

import sys, csv
from lxml import etree
import functools
from templatemaker import Comparator
import codecs

class svgfactory(object):
    def __init__(self, elem, **kwargs):
        self.fn = functools.partial(
                    etree.Element, 
                    '{http://www.w3.org/2000/svg}%s' % elem, 
                    nsmap = {"svg": "http://www.w3.org/2000/svg"}, 
                    **kwargs)

    def __call__(self, *args, **kwargs):
        str_kwargs = dict((x, unicode(kwargs[x])) for x in kwargs)
        str_args = [unicode(x) for x in args]
        return self.fn(*str_args, **str_kwargs)

svg = svgfactory("svg")
circle = svgfactory("circle")
line = svgfactory("line")
text = svgfactory("text")

def parse_table(data):
    return [line.split("\t") for line in data]

def populations():
    res = []
    cities = csv.reader(open("cities1000.txt", "rb"), dialect=csv.excel_tab)
    popn = sorted(
            ((int(x[14]), x[1], float(x[4]), float(x[5])) for x in cities), 
            reverse=True)
    return popn

def main(startx=0, starty=0, color="#000", res=None, multiple=2, r=20,
         hilite="#f00", opacity=0.1, threshold=1):
    if res is None:
        res = svg(width="720", height="360", style="background-color: white;")
    cities = populations()
    pmax = cities[0][0] # scale as ratio of areas
    print cities[0][0], cities[0][1]
    # therefore rmax**2 / ract**2 = pmax / pact
    # => ract**2 = rmax**2*pact / pmax
    # => ract = (rmax**2 * pact * pmax**-1)**0.5
    
    def ract(pact, r=r, pmax=pmax):
        return (r**2 * float(pact) * float(pmax)**-1)**0.5
    
    xmin = str(startx); xmax = str(multiple*360 + startx)
    ymin = str(starty); ymax = str(multiple*180 + starty)    
    # # border
    # res.append(line(x1=xmin, x2=xmax, y1=ymin, y2=ymin, strokewidth="1", 
    #                 stroke="black"))
    # res.append(line(x1=xmin, x2=xmax, y1=ymax, y2=ymax, strokewidth="1", 
    #                 stroke="black"))
    # res.append(line(x1=xmax, x2=xmax, y1=ymin, y2=ymax, strokewidth="1", 
    #                 stroke="black"))
    # res.append(line(x1=xmin, x2=xmin, y1=ymin, y2=ymax, strokewidth="1", 
    #                 stroke="black"))

    for i in cities:
        x, y = (i[3]+180) * multiple + startx, (i[2]-90) * -multiple + starty
        radius = ract(i[0])
        if radius > threshold:
            res.append(circle(cy=str(y), cx=str(x), r=radius, 
                       style="stroke-width: 0.5; fill: %s; stroke: none; \
                              opacity: %s" % (color, opacity),
                       id=unicode(i[1]+str(x)+str(y), encoding="utf-8")))
    return res
    
if __name__ == "__main__":
    res = main(
        res = svg(width="1440", height="720", 
                  style="background-color: white;"),
        r = 40,
        multiple = 4
    )
    tree = etree.ElementTree(res)
    tree.write(open(sys.argv[1], "wb"))
    