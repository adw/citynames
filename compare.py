import sys
from lxml import etree
from functools import partial
from templatemaker import Comparator


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
    cities = parse_table(open("cities1000.txt"))
    for c in cities:
        comp = Comparator(city, c[2].lower())
        subseq = comp.longest_substring()
        if len(subseq) > 1:
            res.append((len(subseq), c[2], float(c[4]), float(c[5])))
    return sorted(res, reverse=True)

def main(city):
    res = svg()
    cities = compare(city)
    multiple = 2.5
    xmin = "0"; xmax = str(multiple*360)
    ymin = "0"; ymax = str(multiple*180)
    r = 1
    res.append(line(x1=xmin, x2=xmax, y1=ymin, y2=ymin, strokewidth="1", 
                    stroke="black"))
    res.append(line(x1=xmin, x2=xmax, y1=ymax, y2=ymax, strokewidth="1", 
                    stroke="black"))
    res.append(line(x1=xmax, x2=xmax, y1=ymin, y2=ymax, strokewidth="1", 
                    stroke="black"))
    res.append(line(x1=xmin, x2=xmin, y1=ymin, y2=ymax, strokewidth="1", 
                    stroke="black"))
    for c in cities:
        x, y = (c[3]+180) * multiple, (c[2]-90) * -multiple
        opacity = (float(c[0])/len(city))**2
        res.append(circle(cy=str(y), cx=str(x), r=str(r), 
                   style="stroke-width: 0; fill: #000; opacity: %s" % opacity, 
                   id=unicode(c[1]+str(x)+str(y), encoding="utf-8")))
    tree = etree.ElementTree(res)
    tree.write(open(city+".svg", "wb"))
    
if __name__ == "__main__":
    main(sys.argv[1])