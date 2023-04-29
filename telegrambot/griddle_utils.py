import json
from datetime import date
from typing import Literal, Union, Tuple
import random


def degriddle(input:str, mode:Literal["easting","northing"]):
    
    assert isinstance(input,str) and (len(input) == 1), "Invalid Input. Input should be single alphabet character"
    assert mode in ["easting","northing"], "Invalid Mode. Either 'easting' or 'northing'"

    contents = open("griddle_table.txt", "r").read()
    e_gi, n_gi, easting_alphabets, northing_alphabets = get_griddle_contents(contents)

    e_num = [ e_gi+i for i in range(len(easting_alphabets)) ]
    n_num = [ n_gi+i for i in range(len(northing_alphabets)) ]
    input = input.upper()

    return e_num[easting_alphabets.index(input)] if mode == "easting" else n_num[northing_alphabets.index(input)]

def griddle(input:str, mode:Literal["easting","northing"], first_griddle:bool=False):

    assert isinstance(input,str), "Invalid Input"
    assert mode in ["easting","northing"], "Invalid Mode. Either 'easting' or 'northing'"

    contents = open("griddle_table.txt", "r").read()
    e_gi, n_gi, easting_alphabets, northing_alphabets = get_griddle_contents(contents)
    
    e_num = [ e_gi+i for i in range(len(easting_alphabets)) ]
    n_num = [ n_gi+i for i in range(len(northing_alphabets)) ]

    if first_griddle:
        
        input = int(input)
        if mode == "easting":
            assert e_gi <= input, "Easting GI is invalid"
        elif mode == "northing":
            assert n_gi <= input, "Northing GI is invalid"

        return easting_alphabets[e_num.index(input)] if mode == "easting" else northing_alphabets[n_num.index(input)]
    
    else: 

        input: str = input[-1]

        if mode == "easting":

            indexes_with_matching_last_num = [i for i,v in enumerate(e_num) if str(v)[-1] == input]

            return easting_alphabets[random.choice(indexes_with_matching_last_num)]

        if mode == "northing":

            indexes_with_matching_last_num = [i for i,v in enumerate(n_num) if str(v)[-1] == input]

            return northing_alphabets[random.choice(indexes_with_matching_last_num)]

def get_griddle_contents(input:str) -> Tuple[int,int,list,list]:
    contents = input.split("\n")
    assert len(contents) == 3, "Invalid Set Griddle Entry"

    gi: list = contents[0].split(" ")
    assert len(gi) == 2, "Invalid GI Entry"
    e_gi, n_gi = int(gi[0]), int(gi[1])

    easting_alphabets: list = [*contents[1]]
    northing_alphabets: list = [*contents[2]]
    assert len(easting_alphabets) == len(northing_alphabets), "Num(Easting_Alphabets) != Num(Northing_Alphabets)"

    return e_gi, n_gi, easting_alphabets, northing_alphabets

if __name__ == "__main__":
    
    print(griddle("55", mode="easting", first_griddle=True), griddle("40", "easting"))