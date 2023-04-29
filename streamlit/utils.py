from typing import Tuple, Dict, List, Union
import numpy as np
import math

def empty_or_None(input:Union[str,None]):
    return input if input else ""

def unzip(input: List[tuple]):
    easting, northing, label = zip(*input)
    return easting, northing, label

def get_easting_northing(text:str) ->Tuple[int,int]:
    easting, northing = text.split(" ")
    assert (len(easting)==6) and (len(northing)==6), "Easting or Northing is not 6 digit"
    return int(easting), int(northing)

def rso_2_utm(rso:str) ->str:
    rso_e, rso_n = get_easting_northing(rso)
    utm_e = int(rso_e) - 300000 + 21460
    utm_n = int(rso_n) - 43
    return f"{utm_e} {utm_n}"
    
def utm_2_rso(utm:str) ->str:
    utm_e, utm_n = get_easting_northing(utm)
    rso_e = utm_e + 300000 - 21460
    rso_n = utm_n + 43
    return f"{rso_e} {rso_n}"

# Range Table and Mils Table in development - matrix element processing
def inverse_mil(mil):
    new = mil + 3200
    return new if new < 6400 else new - 6400

def get_delta_matrix(input:list):
    arr = np.array(input)
    delta_matrix = np.tril(arr[:,np.newaxis] - arr)
    return delta_matrix

def get_easting_northing_matrix(data):
    easting = []
    northing = []
    labels = []

    for platoon_name, grids in data.items():
        for platoon_element, grid in grids.items():
            e, n = get_easting_northing(grid)
            easting.append(e)
            northing.append(n)
            labels.append(platoon_element)
            
    return get_delta_matrix(easting), get_delta_matrix(northing), labels

def get_range_table(dx,dy):
    range_matrix = np.sqrt(np.square(dx) + np.square(dy)).astype(int)
    return range_matrix

## Development - single element processing
def get_arrow_dxdy(dof:str, factor:int):
    
    dof = int(dof)
    if dof <= 1600:         # Q1
        acute_rad = ((1600 - dof)/3200) * math.pi
        dx, dy = math.tan(acute_rad)*factor, factor
    if 1600 < dof <= 3200:  # Q4
        acute_rad = ((3200 - dof)/3200) * math.pi
        dx, dy = math.tan(acute_rad)*factor, -factor
    if 3200 < dof <= 4800:  # Q3
        acute_rad = ((dof - 3200)/3200) * math.pi   
        dx, dy = -math.tan(acute_rad)*factor, -factor
    if 4800 < dof <= 6400:  # Q2
        acute_rad ((6400 - dof)/3200) * math.pi
        dx, dy = -math.tan(acute_rad)*factor, factor
    return dx, dy

def get_delta(from_coord:str, to_coord:str) ->Tuple[int,int]:
    from_e, from_n = get_easting_northing(from_coord)
    to_e, to_n = get_easting_northing(to_coord)
    return (to_e - from_e), (to_n - from_n)

def get_range(delta_e:int, delta_n:int) ->int:
    return round((delta_e**2 + delta_n**2)**0,5)

def get_mil(delta_e:int, delta_n:int) ->int:
    acute = abs(math.atan(delta_e/delta_n))
    if delta_e > 0:
        if delta_n > 0:
            mils = (acute / (math.pi * 2)) * 6400
        else :
            mils = ((acute / (math.pi * 2)) + 1 ) * 6400
    else:
        if delta_n > 0:
            mils = (1 - (acute / (math.pi * 2))) * 6400
        else:
            mils = ((acute + math.pi) / (math.pi * 2)) * 6400
    return round(mils)