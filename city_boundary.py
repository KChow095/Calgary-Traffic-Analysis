import csv
import re
import folium
from folium.features import DivIcon

import pandas as pd
import numpy as np


# parses csv file and retrieves a list of boundary coordinates
def get_boundary_coordinates(file_name):
    with open(file_name) as file:
        # creates a reader object to allow for iteration of each row
        reader = csv.reader(file)

        # stores the header rows from csv
        header_row = next(reader)

        # stores the data containing
        boundary_data_row = next(reader)

        coordinate_str = ''

        # retrieve coordinate data from boundary data row
        for str in boundary_data_row:
            data = re.sub('[a-zA-Z()]', '', str).strip()

            # store coordinates in list
            if data != '':
                coordinate_str += data

    coordinates = [x.strip() for x in coordinate_str.split(',')]

    return coordinates


# splits coordinates into a list of latitude and longitude values
def get_coordinate_list(coordinates):
    lat = []
    long = []

    for coordinate in coordinates:
        split_coordinates = coordinate.split(' ')

        long.append(float(split_coordinates[0]))
        lat.append(float(split_coordinates[1]))

    coordinate_list = [lat,long]

    return coordinate_list


# divides a line from coordinate_A to coordinate_B into 11 points
def get_plot_points(coordinate_A, coordinate_B):
    step_size_lat = (coordinate_A[0] - coordinate_B[0]) / 10
    step_size_long = (coordinate_A[1] - coordinate_B[1]) / 10

    lat_points = []
    long_points = []

    if step_size_lat != 0:
        current_lat = coordinate_B[0]

        for i in range(11):
            lat_points.append(current_lat)
            current_lat += step_size_lat

        long_points = [coordinate_A[1]]*11

    if step_size_long != 0:
        current_long = coordinate_B[1]

        for i in range(11):
            long_points.append(current_long)
            current_long += step_size_long

        lat_points = [coordinate_A[0]]*11

    points_list = []

    for i in range(11):
        points_list.append([lat_points[i],long_points[i]])

    return points_list


# draw boundary on folium map
def draw_boundary_lines(top_left, top_right, bottom_left, bottom_right, m):
    top_line = [top_left,top_right]
    bottom_line = [bottom_left, bottom_right]
    left_line = [top_left,bottom_left]
    right_line = [top_right,bottom_right]

    lines = [top_line,bottom_line,left_line,right_line]

    for line in lines:
        draw_line = folium.PolyLine(locations=line, weight=3, color='red')
        m.add_child(draw_line)


# draws a 10x10 grid on folium map
def draw_grid_lines(top_coordinates, bottom_coordinates, left_coordinates, right_coordinates, m):
    for i in range(11):
        vertical_points = [top_coordinates[i],bottom_coordinates[i]]
        vertical_lines = folium.PolyLine(locations=vertical_points, weight=3, color='red')
        m.add_child(vertical_lines)

        horizontal_points = [left_coordinates[i], right_coordinates[i]]
        horizontal_lines = folium.PolyLine(locations=horizontal_points, weight=3, color='red')
        m.add_child(horizontal_lines)


# retrieves a list of cell coordinates
def get_cell_boundaries(lat_coordinates, long_coordinates):
    cells = []

    for row in range(len(long_coordinates)-1):
        north_bound = long_coordinates[row][0]
        south_bound = long_coordinates[row + 1][0]

        for col in range(len(lat_coordinates)-1):
            west_bound = lat_coordinates[col][1]
            east_bound = lat_coordinates[col + 1][1]

            cell = [north_bound, east_bound, south_bound, west_bound]
            cells.append(cell)

    return cells


# draw cell number
def draw_cell_number(cells, m):
    cell_counter = 1

    for cell in cells:
        cell_num = cell_counter

        lat_center = (cell[2] - cell[0]) / 2 + cell[0]
        long_center = (cell[1] - cell[3]) / 2 + cell[3]

        center_coordinates = [lat_center, long_center]

        folium.Marker(center_coordinates, icon=DivIcon(icon_size=(100, 13),
                                                       icon_anchor=(4, 5),
                                                       html="<div style='font-size: 7pt'><b>%s</b></div>" % cell_num
                                                       )).add_to(m)

        cell_counter += 1


def main():
    # UNCOMMENT THE CODE BELOW IF RUNNING USING PYTHON SCRIPT RATHER THAN JUPYTER NOTEBOOK
    '''
    boundary_coordinates = get_boundary_coordinates('City_Boundary_layer.csv')
    coordinate_list = get_coordinate_list(boundary_coordinates)

    south = min(coordinate_list[0])
    north = max(coordinate_list[0])
    west = min(coordinate_list[1])
    east = max(coordinate_list[1])

    nw = [north, west]
    ne = [north, east]
    se = [south, east]
    sw = [south, west]

    top_coordinates = get_plot_points(ne,nw)
    right_coordinates = get_plot_points(se,ne)
    bottom_coordinates = get_plot_points(se,sw)
    left_coordinates = get_plot_points(sw,nw)

    m = folium.Map(location=[51.0447, -114.0719], zoom_start=10)
    draw_grid_lines(top_coordinates, bottom_coordinates, left_coordinates, right_coordinates, m)

    cells = get_cell_boundaries(top_coordinates, left_coordinates)
    draw_cell_number(cells, m)

    m.save('testing.html')
    '''


if __name__ == "__main__":
    main()