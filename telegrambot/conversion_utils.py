from typing import Literal
import os

import constants 

E_N_DELIMITER = constants.E_N_DELIMITER

def conversion(grid:str, mode=Literal['utm_to_rso','rso_to_utm']):
    assert mode in ['utm_to_rso','rso_to_utm'], "Mode is invalid"
    easting, northing = grid.split(E_N_DELIMITER)
    assert (len(easting)==6) and (len(northing)==6), "Easting or Northing is not 6 digits"
    easting, northing = int(easting), int(northing)

    if mode == "utm_to_rso":
        easting = easting + 300000 - 21460
        northing = northing + 43
        
    elif mode == "rso_to_utm":
        easting = easting - 300000 + 21460
        northing = northing - 43

    return easting, northing