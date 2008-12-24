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

def main(city, startx=0, starty=0, color="#000", res=None, multiple=2.5, r=1):
    if res is None:
        res = svg()
    cities = compare(city)
    opacityscale = 3
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
    for c in cities:
        x, y = (c[3]+180) * multiple + startx, (c[2]-90) * -multiple + starty
        opacity = (float(c[0])/len(city)) ** opacityscale
        res.append(circle(cy=str(y), cx=str(x), r=str(r), 
                   style="stroke-width: 0; fill: %s; opacity: %s" % 
                                                        (color, opacity),
                   id=unicode(c[1]+str(x)+str(y), encoding="utf-8")))
    return res
    
if __name__ == "__main__":
    res = main("London", multiple=1, r=float(1)/2.5)
    res = main("New York", multiple=1, r=float(1)/2.5, startx=360, res=res)
    res = main("Paris", multiple=1, r=float(1)/2.5, starty=180, res=res)
    res = main("M\314\210nchen", multiple=1, r=float(1)/2.5, starty=180, startx=360, res=res)
    tree = etree.ElementTree(res)
    tree.write(open(sys.argv[1], "wb"))
    