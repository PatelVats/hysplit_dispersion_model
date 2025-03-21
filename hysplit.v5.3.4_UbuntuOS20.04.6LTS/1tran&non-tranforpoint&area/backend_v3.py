# This code solves the problem of point and area source emission on top of transient and non-transient simulation handling

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import shutil
import subprocess
from datetime import datetime, timedelta

app = FastAPI()

class HysplitInput(BaseModel):
    start_time: tuple
    num_locations: int
    locations: list
    run_time: int  # Total run time in hours
    vert_motion_method: int
    top_of_model: float
    num_met_files: int
    met_dir: str
    met_filename: str
    num_species: int
    identification: str
    emission_rate: float
    emission_hours: float
    release_start: tuple
    num_grids: int
    grid_center: tuple
    grid_spacing: tuple
    grid_span: tuple
    output_dir: str
    output_filename: str
    num_vert_levels: int
    height_levels: int
    sampling_start: tuple
    sampling_stop: tuple
    avg_now_max: tuple
    num_species_dep: int
    particle_properties: tuple
    pollutant_props: tuple
    henry_constants: tuple
    radioactive_decay: float
    resuspension_factor: float
    transient_mode: bool
    interval: int

def is_point_source(location):
    return len(location) == 3

def is_area_source(location):
    return len(location) == 6

def generate_control_file(data: HysplitInput, output_file="CONTROL", current_time=None, run_time=1, sim_number=1):
    with open(output_file, "w") as file:
        if current_time:
            file.write(f"{current_time[0]:02d} {current_time[1]:02d} {current_time[2]:02d} {current_time[3]:02d}\n")
        else:
            file.write(f"{data.start_time[0]:02d} {data.start_time[1]:02d} {data.start_time[2]:02d} {data.start_time[3]:02d}\n")
        
        # Include all sources (both area and point) in the CONTROL file
        file.write(f"{len(data.locations)}\n")
        
        # Write area sources first
        for loc in data.locations:
            if is_area_source(loc):
                file.write(f"{loc[0]:.6f} {loc[1]:.6f} {loc[2]:.1f}\n")
        
        # Then write point sources
        for loc in data.locations:
            if is_point_source(loc):
                file.write(f"{loc[0]:.6f} {loc[1]:.6f} {loc[2]:.1f}\n")
        
        file.write(f"{run_time if run_time is not None else data.run_time}\n")
        file.write(f"{data.vert_motion_method}\n")
        file.write(f"{data.top_of_model:.1f}\n")
        file.write(f"{data.num_met_files}\n")
        
        for i in range(data.num_met_files):
            file.write(f"{data.met_dir}\n")
            file.write(f"{data.met_filename}\n")
        
        file.write(f"{data.num_species}\n")
        file.write(f"{data.identification}\n")
        file.write(f"{data.emission_rate:.1f}\n")
        file.write(f"{data.emission_hours:.1f}\n")
        file.write(f"{data.release_start[0]:02d} {data.release_start[1]:02d} {data.release_start[2]:02d} {data.release_start[3]:02d} {data.release_start[4]:02d}\n")
        file.write(f"{data.num_grids}\n")
        file.write(f"{data.grid_center[0]:.1f} {data.grid_center[1]:.1f}\n")
        file.write(f"{data.grid_spacing[0]:.3f} {data.grid_spacing[1]:.3f}\n")
        file.write(f"{data.grid_span[0]:.1f} {data.grid_span[1]:.1f}\n")
        file.write(f"{data.output_dir}\n")
        file.write(f"{data.output_filename}_{sim_number}\n")  # Append simulation number to output filename
        file.write(f"{data.num_vert_levels}\n")
        file.write(f"{data.height_levels}\n")
        file.write(f"{data.sampling_start[0]:02d} {data.sampling_start[1]:02d} {data.sampling_start[2]:02d} {data.sampling_start[3]:02d} {data.sampling_start[4]:02d}\n")
        file.write(f"{data.sampling_stop[0]:02d} {data.sampling_stop[1]:02d} {data.sampling_stop[2]:02d} {data.sampling_stop[3]:02d} {data.sampling_stop[4]:02d}\n")
    #  Calculate the appropriate avg_now_max value based on the interval
        interval_hours = data.interval // 60  # Convert minutes to hours
        avg_now_max = list(data.avg_now_max)  # Convert tuple to list for modification
        avg_now_max[1] = interval_hours  # Update the middle value      
        file.write(f"{avg_now_max[0]:02d} {avg_now_max[1]:02d} {avg_now_max[2]:02d}\n")
        file.write(f"{data.num_species_dep}\n")
        file.write(f"{data.particle_properties[0]:.1f} {data.particle_properties[1]:.1f} {data.particle_properties[2]:.1f}\n")
        file.write(f"{' '.join(map(str, data.pollutant_props))}\n")
        file.write(f"{' '.join(map(str, data.henry_constants))}\n")
        file.write(f"{data.radioactive_decay:.1f}\n")
        file.write(f"{data.resuspension_factor:.1f}\n")

    shutil.copy(output_file, "default_conc")

def create_ascdata_cfg(output_file="ASCDATA.CFG"):
    content = """\
-90.0   -180.0  lat/lon of lower left corner
1.0     1.0     lat/lon spacing in degrees
180     360     lat/lon number of data points
2               default land use category
0.2             default roughness length (m)
'/home/oizom/Desktop/HYSPLIT/hysplit.v5.3.4_UbuntuOS20.04.6LTS/bdyfiles/'  directory of files
"""
    
    with open(output_file, "w") as file:
        file.write(content)


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

def create_emitimes(data: HysplitInput, output_file: str = "EMITIMES", current_time=None, duration=None):
    area_sources = [loc for loc in data.locations if is_area_source(loc)]
    
    if not area_sources:
        print("No area sources found. EMITIMES file not created.")
        return False

    with open(output_file, "w") as file:
        file.write("YYYY MM DD HH    DURATION(hhhh) #RECORDS\n")
        file.write("YYYY MM DD HH MM DURATION(hhmm) LAT LON HGT(m) RATE(/h) AREA(m2) HEAT(w)\n")
        
        if current_time:
            year, month, day, hour = current_time
        else:
            year, month, day, hour = data.start_time
        minute = 0  # Assuming minute is always 0, adjust if needed
        
        if duration is None:
            duration = int(data.emission_hours * 60)  # Convert hours to minutes
        else:
            duration = int(duration * 60)  # Convert hours to minutes
        
        file.write(f"{year:04d} {month:02d} {day:02d} {hour:02d} 9999 {len(area_sources)}\n")
        
        for loc in area_sources:
            lat, lon, height, length, width, angle = loc
            area = length * width  # Calculate area
            heat = 0.0  # Assuming heat is always 0, adjust if needed
            
            file.write(f"{year:04d} {month:02d} {day:02d} {hour:02d} {minute:02d} {duration:04d} "
                       f"{lat:.6f} {lon:.6f} {height:.1f} {data.emission_rate:.1f} {area:.6f} {heat:.1f}\n")

    print(f"✅ EMITIMES file '{output_file}' has been successfully created.")
    return True



def run_hysplit(sim_number):

    try:

        subprocess.run("../exec/hycs_std", shell=True, check=True)

        # Update the command to include the simulation number

        subprocess.run(f"../exec/concplot -icdump_{sim_number} -a3", shell=True, check=True)

        

        # Call the modify_kml script with the updated output filename

        input_kml = r"/home/oizom/Desktop/HYSPLIT/hysplit.v5.3.4_UbuntuOS20.04.6LTS/1tran&non-tranforpoint&area/HYSPLIT_ps.kml"

        output_kml = f"/home/oizom/Desktop/HYSPLIT/hysplit.v5.3.4_UbuntuOS20.04.6LTS/1tran&non-tranforpoint&area/modified_HYSPLIT_ps_{sim_number}.kml"

        

        subprocess.run(["python", "modify_kml.py", input_kml, output_kml], check=True)  # Call the modify_kml script

        

    except subprocess.CalledProcessError as e:

        raise HTTPException(status_code=500, detail=f"Error while running command: {e}")

    except FileNotFoundError:

        raise HTTPException(status_code=404, detail="One of the required files or programs is missing.")

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
@app.post("/run_hysplit/")
async def run_hysplit_model(data: HysplitInput):
    create_ascdata_cfg()

    # Create EMITIMES file if there are area sources
    emitimes_created = create_emitimes(data)

    # Create SETUP.CFG only if EMITIMES was created
    if emitimes_created:
        create_setup_cfg()

    if data.transient_mode:
        # For transient mode, run a single simulation for the entire run_time
        generate_control_file(data, run_time=data.run_time, sim_number=1)
        run_hysplit(1)
    else:
        # For non-transient mode, run multiple simulations
        start_datetime = datetime(2000 + data.start_time[0], data.start_time[1], data.start_time[2], data.start_time[3])
        end_datetime = start_datetime + timedelta(hours=data.run_time)
        interval_timedelta = timedelta(minutes=data.interval)
        
        sim_number = 1
        current_datetime = start_datetime
        while current_datetime < end_datetime:
            current_time = [current_datetime.year % 100, current_datetime.month, current_datetime.day, current_datetime.hour]
            run_time = min(data.interval // 60, (end_datetime - current_datetime).total_seconds() // 3600)
            
            # Update EMITIMES for each simulation if area sources exist
            if emitimes_created:
                create_emitimes(data, current_time=current_time, duration=run_time)
            
            generate_control_file(data, current_time=current_time, run_time=run_time, sim_number=sim_number)
            run_hysplit(sim_number)
            
            current_datetime += interval_timedelta
            sim_number += 1

    return {"message": "HYSPLIT model run successfully."}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)