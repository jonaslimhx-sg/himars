import math
from typing import Literal, Tuple

def range_check(target_easting:int, target_northing:int, ammo:Literal["jtj","jeh"], traj:Literal["nom","vert"]) -> Tuple[str, int, int]:
    firing_easting, firing_northing = map(int, open("firing_point.txt","r").read().split(" "))
    # Get Range
    delta_easting = target_easting - firing_easting
    delta_northing = target_northing - firing_northing
    acute = abs(math.atan(delta_easting/delta_northing))

    # get_dof
    if delta_easting > 0:
        
        if delta_northing > 0:
            # Q1
            dof = (acute / (math.pi * 2)) * 6400
        else: 
            # Q4
            dof = ((math.pi - acute) / (math.pi * 2))* 6400
    else:
        if delta_northing > 0:
            # Q2
            dof = (1 - (acute / (math.pi * 2))) * 6400
        else: 
            # Q3
            dof = ((acute + math.pi) / (math.pi * 2)) * 6400
    
    # get_range
    range = round(math.sqrt((delta_easting**2) + delta_northing**2)/1000,2)
    dof = round(dof)
    
    # response: check ammo & traj
    range_check = "✅ Range Check"

    if (traj == "nom") and (not 20000 <= range <= 70000):
        range_check = "❌ Range Check: Nom 20-70km"
    if (traj == "vert") and (not 30000 <= range <= 65000):
        range_check = "❌ Range Check: Vert 30-65km"
    if (ammo == "jeh") and (not 8000 <= range <= 15000):
        range_check = "❌ Range Check: JEH 8-15km"

    return range_check, range, dof

def overhead_firing_check(calculated_dof: int):

    deployment_dof = int(open("dof.txt", "r").read())
    dof_check = "✅ Overhead Firing Check"

    if not (deployment_dof - 100 <= calculated_dof <= deployment_dof + 100):
        dof_check = "❌ Overhead Firing +/- 100mils"

    return dof_check
