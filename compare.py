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
text = svgfactory("text")
def parse_table(data):
    return [line.split("\t") for line in data]
    
def compare(city, limit=1):
    res = []
    city = city.lower()
    cities = parse_table(open("cities1000.txt"))
    for i in cities:
        comp = Comparator(city, i[1].lower())
        subseq = comp.longest_substring()
        if len(subseq) > limit:
            res.append((len(subseq), i[2], float(i[4]), float(i[5])))
    return sorted(res, reverse=True)

def main(city):
    res = svg()
    limit = 1
    multiple = 2.5
    opacityscale = 2
    opacityconstant = 0.5
    xmin = "0"; xmax = str(multiple*360)
    ymin = "0"; ymax = str(multiple*180)
    cities = compare(city, limit=3)
    r = 2
    color = "#000"
    hilite = "#f00"
    res.append(line(x1=xmin, x2=xmax, y1=ymin, y2=ymin, strokewidth="1", 
                    stroke="black"))
    res.append(line(x1=xmin, x2=xmax, y1=ymax, y2=ymax, strokewidth="1", 
                    stroke="black"))
    res.append(line(x1=xmax, x2=xmax, y1=ymin, y2=ymax, strokewidth="1", 
                    stroke="black"))
    res.append(line(x1=xmin, x2=xmin, y1=ymin, y2=ymax, strokewidth="1", 
                    stroke="black"))
    t = text(x=str((multiple-0.25)*360), y=str((multiple-0.25)*180),
             style="font-family: Helvetica;")
    t.text = city
    res.append(t)
    for i in cities:
        x, y = (i[3]+180) * multiple, (i[2]-90) * -multiple
        scale = float(i[0])/len(city)
        oscale = scale ** opacityscale
        opacity = opacityconstant * oscale
        if oscale == 1:
            res.append(circle(cy=str(y), cx=str(x), r=str(r), 
                       style="stroke-width: 0; fill: %s; opacity: %s" % 
                                                            (hilite, 1),
                       id=unicode(i[1]+str(x)+str(y), encoding="utf-8")))            
        else:
            res.append(circle(cy=str(y), cx=str(x), r=str(r), 
                       style="stroke-width: 0.5; fill: white; stroke: %s; \
                              opacity: %s" % (color, opacity),
                       id=unicode(i[1]+str(x)+str(y), encoding="utf-8")))
            
    tree = etree.ElementTree(res)
    tree.write(open(city+".svg", "wb"))
    
if __name__ == "__main__":
    main(sys.argv[1])