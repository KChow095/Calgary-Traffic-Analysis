import csv
import re
import folium
from geojson import MultiLineString
from operator import itemgetter

import pandas as pd
import numpy as np


# parses csv file and retrieves a list of boundary coordinates
def get_street(file_name):
    speedlimit=pd.read_csv(file_name)
    streets=speedlimit["multiline"]
    multiline =[]
    for line in speedlimit["multiline"]:
        length=len(re.sub('[a-zA-Z]', '', line).strip())
        multiline.append(re.sub('[a-zA-Z]', '', line).strip()[2:length-2].split('), ('))

    SpeedandLine=pd.DataFrame({'Name':speedlimit['STREET_NAME'],'Speed':speedlimit['SPEED'],'Line':multiline})

    return SpeedandLine


def draw_line(speedline,colours,m):

    for i in range(len(speedline)):
        
        colour=colours[speedline['Speed'][i]]
        for line in speedline['Line'][i]:
            pointlist=[]

            for point in line.split(","):
                longitude=float(point.split()[0].strip())
                latitude=float(point.split()[1].strip())
                pointlist.append([latitude,longitude])
            draw_line = folium.PolyLine(locations=pointlist, weight=4, color=colour).add_to(m)




            