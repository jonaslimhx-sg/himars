GRIDS_DELIMITER = "\n"
E_N_DELIMITER = " "

start_message = """
4th Himars Battery 
3SG Douglas reporting for ICT!

Refer to /fmsn for fmsn check setups.

- I can griddle and degriddle in RSO.
- I can convert grid formats. 
- I can perform fmsn checks.
- I can perform deployment checks (http://13.229.238.40:8100)

⬇️ Check out the Menu
"""

guide = """
Helper Commands
Tap & Hold on to commands to copy

Setup FP
/set_utm_fp 3xxxxx 1xxxxx

Setup DOF
/set_dof 4000

Setup Griddle Table
/set_griddle
45 34
ACBWEFWW
AWECWECI

Get DOF or FP or Griddle Table
/get_fp
/get_dof
/get_griddle
"""

set_griddle = """
[INFO] 
- Separate E and N GI with a space
- Separate GI and Alphabets with line break.

Example:
48 52
RDBNSEQITPJGWCMXHZKYAVUFLO
RMBAOXITFNPDZSHVCEWKGULQJY
"""

griddle = """
[INFO] Send the RSO coordinates.
- Separate E and N with a space.
- Separate grids with a line break.
- Without the Prefix 6 and 01

Example:
39234 50234
42231 49020
"""

degriddle = """
[INFO] Send the Griddles.
- Separate E N with a space.
- Separate grids with a line break.
- Case insensitive.

Example:
aswf wekw
AeWf Qefg
"""

rso_to_utm = """
[INFO] Send the RSO grids
- Include Prefix 6 and 1

Example:
612343 124345
612345 134555
"""
utm_to_rso = """
[INFO] Send the UTM grids
- Include prefix 3 and 1

Example:
312343 124345
412345 134555
"""

fmsn_fdo =  """
[INFO]
- Norminal: 20-70km
- Vertical: 30-65km
- JEH: 8-15km 
- Delay Fuse recommend Vert Traj
- Point Sheaf 1 Rocket need GPS
- Overhead Firing +/- 100mils

Fmsn Format:
UTM.E UTM.N Ammo Traj
312123 123412 jtj vert 
312321 123412 jeh nom
"""

fmsn_fo = """
[INFO]
- Norminal: 20-70km
- Vertical: 30-65km
- JEH: 8-15km 
- Delay Fuse recommend Vert Traj
- Point Sheaf 1 Rocket need GPS
- Overhead Firing +/- 100mils

Fmsn Format:
RSO.E RSO.N Ammo Traj
612123 123412 jtj vert 
612321 123412 jeh nom
"""