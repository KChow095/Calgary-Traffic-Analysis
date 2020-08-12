import numpy as np

def get_cell_number(cell_boundaries, latitude, longitude):
    '''
    Processes a list of coordinates and determines the grid cell that the coordinate belongs to.
    This function returns a list of the cells in the order that the coordinates have been processed.
    '''
    cell_list = []

    for i in range(len(latitude)):
        current_lat = latitude[i]
        current_long = longitude[i]

        for cell in range(len(cell_boundaries)):
            if(current_lat <= cell_boundaries[cell][0] and current_lat >= cell_boundaries[cell][2]
                    and current_long <= cell_boundaries[cell][1] and current_long >= cell_boundaries[cell][3]):
                cell_list.append(cell+1)
                break

            if(cell == len(cell_boundaries)-1):
                cell_list.append(-1)

    return cell_list