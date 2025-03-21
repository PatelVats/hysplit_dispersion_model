import shutil
import subprocess
import os
from typing import List, Tuple

def generate_control_file(
    start_time: Tuple[int, int, int, int],
    num_locations: int,
    locations: List[Tuple[float, float, float]],
    run_time: int,
    vert_motion_method: int,
    top_of_model: float,
    num_met_files: int,
    met_dir: str,
    met_files: List[str],  # Changed from met_filename1 and met_filename2
    num_species: int,
    identification: str,
    emission_rate: float,
    emission_hours: float,
    release_start: Tuple[int, int, int, int, int],
    num_grids: int,
    grid_center: Tuple[float, float],
    grid_spacing: Tuple[float, float],
    grid_span: Tuple[float, float],
    output_dir: str,
    output_filename: str,
    num_vert_levels: int,
    height_levels: int,
    sampling_start: Tuple[int, int, int, int, int],
    sampling_stop: Tuple[int, int, int, int, int],
    avg_now_max: Tuple[int, int, int],
    num_species_dep: int,
    particle_properties: Tuple[float, float, float],
    pollutant_props: List[float],
    henry_constants: List[float],
    radioactive_decay: float,
    resuspension_factor: float,
    output_file: str = "CONTROL"

):
    """
    Generates a CONTROL file for HYSPLIT with the given parameters.
    Also creates a duplicate file named "default_conc" with the same content.
    """
    with open(output_file, "w") as file:
        file.write(f"{start_time[0]:02d} {start_time[1]:02d} {start_time[2]:02d} {start_time[3]:02d}\n")
        file.write(f"{num_locations}\n")
        
        for loc in locations:
            file.write(f"{loc[0]:.6f} {loc[1]:.6f} {loc[2]:.1f}\n")
        
        file.write(f"{run_time}\n")
        file.write(f"{vert_motion_method}\n")
        file.write(f"{top_of_model:.1f}\n")
        file.write(f"{num_met_files}\n")
    
        for met_file in met_files:
            file.write(f"{met_dir}\n")
            file.write(f"{met_file}\n")

        
        file.write(f"{num_species}\n")
        file.write(f"{identification}\n")
        file.write(f"{emission_rate:.1f}\n")
        file.write(f"{emission_hours:.16f}\n")
        file.write(f"{release_start[0]:02d} {release_start[1]:02d} {release_start[2]:02d} {release_start[3]:02d} {release_start[4]:02d}\n")
        file.write(f"{num_grids}\n")
        file.write(f"{grid_center[0]:.1f} {grid_center[1]:.1f}\n")
        file.write(f"{grid_spacing[0]:.3f} {grid_spacing[1]:.3f}\n")
        file.write(f"{grid_span[0]:.1f} {grid_span[1]:.1f}\n")
        file.write(f"{output_dir}\n")
        file.write(f"{output_filename}\n")
        file.write(f"{num_vert_levels}\n")
        file.write(f"{height_levels}\n")
        file.write(f"{sampling_start[0]:02d} {sampling_start[1]:02d} {sampling_start[2]:02d} {sampling_start[3]:02d} {sampling_start[4]:02d}\n")
        file.write(f"{sampling_stop[0]:02d} {sampling_stop[1]:02d} {sampling_stop[2]:02d} {sampling_stop[3]:02d} {sampling_stop[4]:02d}\n")
        file.write(f"{avg_now_max[0]:02d} {avg_now_max[1]:02d} {avg_now_max[2]:02d}\n")
        file.write(f"{num_species_dep}\n")
        file.write(f"{particle_properties[0]:.1f} {particle_properties[1]:.1f} {particle_properties[2]:.1f}\n")
        file.write(f"{' '.join(map(str, pollutant_props))}\n")
        file.write(f"{' '.join(map(str, henry_constants))}\n")
        file.write(f"{radioactive_decay:.1f}\n")
        file.write(f"{resuspension_factor:.1f}\n")

    print(f"✅ CONTROL file '{output_file}' has been successfully created.")

    shutil.copy(output_file, "default_conc")
    print("✅ File 'default_conc' has been created as a duplicate of 'CONTROL'.")

def create_ascdata_cfg(output_file: str = "ASCDATA.CFG"):
    """
    Creates ASCDATA.CFG file with constant values.
    """
    content = """\
-90.0   -180.0  lat/lon of lower left corner
1.0     1.0     lat/lon spacing in degrees
180     360     lat/lon number of data points
2               default land use category
0.2             default roughness length (m)
'../bdyfiles/'  directory of files
"""
    
    with open(output_file, "w") as file:
        file.write(content)

    print(f"✅ ASCDATA.CFG file '{output_file}' has been successfully created.")

def create_setup_cfg(output_file: str = "SETUP.CFG"):
    """
    Creates SETUP.CFG file with the specified content.
    """
    content = """ &SETUP
 tratio = 0.75,
 initd = 0,
 kpuff = 0,
 khmax = 9999,
 kmixd = 0,
 kmix0 = 150,
 kzmix = 0,
 kdef = 0,
 kbls = 1,
 kblt = 0,
 idsp = 1,
 conage = 24,
 gemage = 48,
 numpar = 2500,
 qcycle = 1.0,
 efile = 'EMITIMES',
 tkerd = 0.18,
 tkern = 0.18,
 hscale = 10800.0,
 vscales = 5.0,
 vscaleu = 200.0,
 ninit = 1,
 ndump = 0,
 ncycl = 0,
 pinpf = 'PARINIT',
 poutf = 'PARDUMP',
 mgmin = 10,
 kmsl = 0,
 maxpar = 1000000,
 cpack = 1,
 cmass = 0,
 dxf = 1.0,
 dyf = 1.0,
 dzf = 0.01,
 ichem = 0,
 maxdim = 1,
 kspl = 1,
 krnd = 6,
 frhs = 1.0,
 frvs = 0.01,
 frts = 0.1,
 frhmax = 3.0,
 splitf = 1.0,
 cmtfn = ' ',
 wvert = .TRUE.,
 /
"""
    
    with open(output_file, "w") as file:
        file.write(content)

    print(f"✅ SETUP.CFG file '{output_file}' has been successfully created.")

def create_emitimes(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    duration: int,
    lat: float,
    lon: float,
    height: float,
    rate: float,
    area: float,
    heat: float,
    output_file: str = "EMITIMES"
):
    """
    Creates EMITIMES file with the specified content.
    """
    content = f"""YYYY MM DD HH    DURATION(hhhh) #RECORDS
YYYY MM DD HH MM DURATION(hhmm) LAT LON HGT(m) RATE(/h) AREA(m2) HEAT(w)
{year:04d} {month:02d} {day:02d} {hour:02d} 9999 1
{year:04d} {month:02d} {day:02d} {hour:02d} {minute:02d} {duration:04d} {lat:.6f} {lon:.6f} {height:.1f} {rate:.1f} {area:.6f} {heat:.1f}
"""
    
    with open(output_file, "w") as file:
        file.write(content)

    print(f"✅ EMITIMES file '{output_file}' has been successfully created.")

def run_hysplit():
    """
    Runs the HYSPLIT model, concentration plotting, and modify_kml.py script.
    """
    try:
        print("🚀 Running HYSPLIT Model...")
        subprocess.run(["../exec/hycs_std"], check=True)
        print("✅ HYSPLIT Model Run Completed.")

        print("📊 Running Concentration Plot...")
        subprocess.run(["../exec/concplot", "-icdump", "-a3"], check=True)
        print("✅ Concentration Plot Generated.")

        print("🛠 Running KML Modification Script...")
        subprocess.run(["python3", "modify_kml.py"], check=True)
        print("✅ KML Modification Completed.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running command: {e}")
    except FileNotFoundError:
        print("❌ Error: One of the required files or programs is missing.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def run_hysplit_model(params):
    try:
        generate_control_file(**params)
        create_ascdata_cfg()
        # create_setup_cfg()
        
        # # Extract parameters for EMITIMES from the existing params
        # create_emitimes(
        #     year=2025,
        #     month=3,
        #     day=5,
        #     hour=18,
        #     minute=0,
        #     duration=2400,
        #     lat=25.159446,
        #     lon=55.429969,
        #     height=7.0,
        #     rate=1.0,
        #     area=15000.0,
        #     heat=0.0
        # )

        run_hysplit()
    except Exception as e:
        print(f"Error in run_hysplit_model: {str(e)}")
        raise
