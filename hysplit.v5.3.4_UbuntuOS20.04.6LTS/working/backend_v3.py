from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import shutil
import subprocess
from datetime import datetime, timedelta
from decimal import Decimal

app = FastAPI()

PREDEFINED_PROPERTIES = {
    'p3': {
        'particle_properties': (1.0, 1.35, 1.0),
        'pollutant_props': (0.0, 0.0, 0.0, 0.0, 0.0),
        'henry_constants': (0.0, 0.00008, 0.00008),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    },
    'p1': {
        'particle_properties': (2.5, 1.5, 1.0),
        'pollutant_props': (0.0, 0.0, 0.0, 0.0, 0.0),
        'henry_constants': (0.0, 0.00008, 0.00008),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    },
    'p2': {
        'particle_properties': (10.0, 1.5, 1.0),
        'pollutant_props': (0.0, 0.0, 0.0, 0.0, 0.0),
        'henry_constants': (0.0, 0.00008, 0.00008),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    },
    'g2': {
        'particle_properties': (0.0, 0.0, 0.0),
        'pollutant_props': (0.001, 28.0, 0.1, 1.0, 0.0003),
        'henry_constants': (0.0003, 0.0, 0.0),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    },
    'g1': {
        'particle_properties': (0.0, 0.0, 0.0),
        'pollutant_props': (0.001, 44.0, 0.5, 1.0, 0.03),
        'henry_constants': (0.03, 0.0, 0.0),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    },
    'g8': {
        'particle_properties': (0.0, 0.0, 0.0),
        'pollutant_props': (0.008, 64.0, 1.0, 1.0, 1.2),
        'henry_constants': (1.2, 0.0, 0.0),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    },
    'g3': {
        'particle_properties': (0.0, 0.0, 0.0),
        'pollutant_props': (0.005, 46.0, 0.5, 1.0, 0.01),
        'henry_constants': (0.01, 0.0, 0.0),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    },
    'g5': {
        'particle_properties': (0.0, 0.0, 0.0),
        'pollutant_props': (0.005, 48.0, 0.3, 1.0, 0.01),
        'henry_constants': (0.01, 0.0, 0.0),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    },
    'g6': {
        'particle_properties': (0.0, 0.0, 0.0),
        'pollutant_props': (0.005, 34.0, 0.5, 1.0, 0.1),
        'henry_constants': (0.1, 0.0, 0.0),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    },
    'g7': {
        'particle_properties': (0.0, 0.0, 0.0),
        'pollutant_props': (0.001, 30.0, 0.1, 1.0, 0.0002),
        'henry_constants': (0.0002, 0.0, 0.0),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    },
    'test': {
        'particle_properties': (0.0, 0.0, 0.0),
        'pollutant_props': (0.001, 28.0, 0.1, 1.0, 0.0003),
        'henry_constants': (0.0003, 0.0, 0.0),
        'radioactive_decay': 0.0,
        'resuspension_factor': 0.0
    }
}

class HysplitInput(BaseModel):
    compute: str
    start_time: tuple
    num_locations: int
    locations: list  # Now can contain [lat, lon, height, year, month, day, hour, minute, rate, area, heat, duration]
    run_time: int
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
    properties_key: str
    transient_mode: bool
    interval: int

def is_point_source(location):
    return len(location) == 4

def is_area_source(location):
    return len(location) == 5  # Updated to include rate and area

def generate_control_file(data: HysplitInput, output_file="CONTROL", current_time=None, run_time=None, sim_number=1):
    properties = PREDEFINED_PROPERTIES.get(data.properties_key)
    if not properties:
        raise HTTPException(status_code=400, detail=f"Invalid properties key: {data.properties_key}")

    with open(output_file, "w") as file:
        file.write(f"{(current_time or data.start_time)[0]:02d} {(current_time or data.start_time)[1]:02d} {(current_time or data.start_time)[2]:02d} {(current_time or data.start_time)[3]:02d}\n")
        
        file.write(f"{len(data.locations)}\n")
        
        for location in data.locations:
            lat, lon, height = location[:3]
            file.write(f"{lat:.2f} {lon:.2f} {height:.1f}\n")
        
        file.write(f"{run_time if run_time is not None else data.run_time}\n")
        file.write(f"{data.vert_motion_method}\n")
        file.write(f"{data.top_of_model:.1f}\n")
        file.write(f"{data.num_met_files}\n")
        
        met_files = data.met_filename.split(',')
        for i in range(data.num_met_files):
            file.write(f"{data.met_dir}\n")
            file.write(f"{met_files[i].strip()}\n")
        
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
        file.write(f"{data.output_filename}_{sim_number}\n")
        
        file.write(f"{data.num_vert_levels}\n")
        file.write(f"{data.height_levels}\n")
        
        file.write(f"{data.sampling_start[0]:02d} {data.sampling_start[1]:02d} {data.sampling_start[2]:02d} {data.sampling_start[3]:02d} {data.sampling_start[4]:02d}\n")
        file.write(f"{data.sampling_stop[0]:02d} {data.sampling_stop[1]:02d} {data.sampling_stop[2]:02d} {data.sampling_stop[3]:02d} {data.sampling_stop[4]:02d}\n")
        
        interval_hours = data.interval // 60
        avg_now_max = list(data.avg_now_max)
        avg_now_max[1] = interval_hours
        
        file.write(f"{avg_now_max[0]:02d} {avg_now_max[1]:02d} {avg_now_max[2]:02d}\n")
        
        file.write(f"{data.num_species_dep}\n")
        file.write(f"{properties['particle_properties'][0]:.8f} {properties['particle_properties'][1]:.8f} {properties['particle_properties'][2]:.8f}\n")
        file.write(" ".join(f"{Decimal(str(prop)):.8f}" for prop in properties['pollutant_props']) + "\n")
        file.write(" ".join(f"{Decimal(str(const)):.8f}" for const in properties['henry_constants']) + "\n")
        file.write(f"{Decimal(str(properties['radioactive_decay'])):.8f}\n")
        file.write(f"{Decimal(str(properties['resuspension_factor'])):.8f}\n")

    shutil.copy(output_file, "default_conc")

def generate_traj_control_file(data: HysplitInput, output_file="CONTROL", sim_number=1):
    with open(output_file, "w") as file:
        file.write(f"{data.start_time[0]:02d} {data.start_time[1]:02d} {data.start_time[2]:02d} {data.start_time[3]:02d}\n")
        file.write(f"{data.num_locations}\n")
        
        for loc in data.locations:
            lat, lon, height = loc[:3]  # Take only the first 3 elements for trajectory
            file.write(f"{lat:.6f} {lon:.6f} {height:.1f}\n")
        
        file.write(f"{data.run_time}\n")
        file.write(f"{data.vert_motion_method}\n")
        file.write(f"{data.top_of_model:.1f}\n")
        file.write(f"{data.num_met_files}\n")
        
        met_files = data.met_filename.split(',')
        for i in range(data.num_met_files):
            file.write(f"{data.met_dir}\n")
            file.write(f"{met_files[i].strip()}\n")
        
        file.write(f"{data.output_dir}\n")
        file.write(f"tdump\n")

    # Copy the content to default_traj file
    shutil.copy(output_file, "default_traj")


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
 initd = 4,
 kpuff = 0,
 khmax = 9999,
 kmixd = 0,
 kmix0 = 150,
 kzmix = 0,
 kdef = 0,
 kbls = 1,
 kblt = 0,
 idsp = 1,
 conage = 1,
 gemage = 48,
 numpar = 2500,
 qcycle = 0.0,
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
 maxpar = 10000,
 cpack = 1,
 cmass = 0,
 dxf = 1.0,
 dyf = 1.0,
 dzf = 0.01,
 ichem = 0,
 maxdim = 1,
 kspl = 24,
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

def create_labels_cfg(output_file: str = "LABELS.CFG"):
    """
    Creates LABELS.CFG file with the specified content.
    """
    content = """ 'TITLE&','NOAA HYSPLIT MODEL&'
'MAPID&','Air Concentration&'
'LAYER&','Average&'
'UNITS&','Kg&'
'VOLUM&','/m3&'
'RELEASE&','enterlabel&'
"""
    
    with open(output_file, "w") as file:
        file.write(content)

    print(f"✅ LABELS.CFG file '{output_file}' has been successfully created.")

def create_emitimes(sources: list, output_file: str = "EMITIMES"):
    """
    Creates EMITIMES file with multiple sources in the specified format.
    
    :param sources: List of source dictionaries with full details
    :param output_file: Path to output EMITIMES file
    """
    # Validate input
    if not sources:
        raise ValueError("At least one source must be provided")
    
    # Write header and details
    with open(output_file, "w") as file:
        # First line: Header description
        file.write("YYYY MM DD HH    DURATION(hhhh) #RECORDS\n")
        
        # Second line: Column headers
        file.write("YYYY MM DD HH MM DURATION(hhmm) LAT LON HGT(m) RATE(/h) AREA(m2) HEAT(w)\n")
        
        # Third line: Year, month, day, hour, duration (9999 for continuous), number of records
        file.write(f"{sources[0]['year']:04d} {sources[0]['month']:02d} {sources[0]['day']:02d} {sources[0]['hour']:02d}    9999 {len(sources)}\n")
        
        # Write each source
        for source in sources:
            file.write(
                f"{source['year']:04d} {source['month']:02d} {source['day']:02d} "
                f"{source['hour']:02d} {source['minute']:02d} "
                f"{source['duration']:04d} "
                f"{source['lat']:.2f} {source['lon']:.2f} "
                f"{source['height']:.1f} {source['rate']:.1f} "
                f"{source['area']:.1f} {source['heat']:.1f}\n"
            )
    
    print(f"✅ EMITIMES file '{output_file}' has been successfully created.")

def run_hysplit(sim_number):
    try:
        subprocess.run("../exec/hycs_std", shell=True, check=True)
        # subprocess.run(f"../exec/concplot -icdump_{sim_number} -a3 +a1 -c51 -v6::139000000+5::255000000+4::255165000+3::255255000+2::144238144+1::211211211", shell=True, check=True)
        subprocess.run(f"../exec/concplot -icdump_{sim_number} -a3 +a0 -c51 -v5::255000000+4::255165000+3::255255000+2::144238144+1::211211211 -k1 -81", shell=True, check=True)
        # subprocess.run("../exec/con2asc cdump_1 > output.txt")
        # subprocess.run(f"../exec/concplot -icdump_{sim_number} -a3 +a1 -c51 -w1 -v6::139000000+5::255000000+4::255165000+3::255255000+2::144238144+1::211211211", shell=True, check=True)

        # Call the modify_kml script with the updated output filename
        input_kml = r"/home/oizom/Desktop/HYSPLIT/hysplit.v5.3.4_UbuntuOS20.04.6LTS/working/HYSPLIT_ps.kml"
        output_kml = f"/home/oizom/Desktop/HYSPLIT/hysplit.v5.3.4_UbuntuOS20.04.6LTS/working/modified_HYSPLIT_ps_{sim_number}.kml"

        subprocess.run(["python", "modify_kml.py", input_kml, output_kml], check=True)  # Call the modify_kml script

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error while running command: {e}")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="One of the required files or programs is missing.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.post("/run_hysplit/")
async def run_hysplit_endpoint(data: HysplitInput):
    try:
        if data.compute.lower() == "conc":
            return await run_dispersion_model(data)
        elif data.compute.lower() == "traj":
            return await run_trajectory_model(data)
        else:
            raise HTTPException(status_code=400, detail="Invalid compute type. Must be 'conc' or 'traj'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def run_dispersion_model(data: HysplitInput):
    # Prepare configuration files
    create_ascdata_cfg()
    create_setup_cfg()
    create_labels_cfg()
    
    # Prepare sources for EMITIMES
    sources = []
    for location in data.locations:
        # Unpack the extended location format
        lat, lon, height, year, month, day, hour, minute, rate, area, heat, duration = location
        
        sources.append({
            'lat': lat,
            'lon': lon,
            'height': height,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute,
            'rate': rate,
            'area': area,
            'heat': heat,
            'duration': duration
        })
    
    # Create EMITIMES file with all sources
    create_emitimes(sources)

    if data.transient_mode:
        generate_control_file(data, run_time=data.run_time, sim_number=1)
        run_hysplit(1)
    else:
        start_datetime = datetime(2000 + data.start_time[0], data.start_time[1], data.start_time[2], data.start_time[3])
        end_datetime = start_datetime + timedelta(hours=data.run_time)
        interval_timedelta = timedelta(minutes=data.interval)
        
        sim_number = 1
        current_datetime = start_datetime
        while current_datetime < end_datetime:
            current_time = [current_datetime.year % 100, current_datetime.month, current_datetime.day, current_datetime.hour]
            run_time = min(data.interval // 60, (end_datetime - current_datetime).total_seconds() // 3600)
            
            generate_control_file(data, current_time=current_time, run_time=run_time, sim_number=sim_number)
            run_hysplit(sim_number)
            
            current_datetime += interval_timedelta
            sim_number += 1

    return {"message": "HYSPLIT dispersion model run successfully."}

async def run_trajectory_model(data: HysplitInput):
    generate_traj_control_file(data)
    
    try:
        subprocess.run("../exec/hyts_std", shell=True, check=True)
        subprocess.run(f"../exec/trajplot -itdump -a3", shell=True, check=True)
        
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error while running trajectory model: {e}")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="One of the required files or programs is missing.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    return {"message": "HYSPLIT trajectory model run successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



'''
Example Json:
oizom@oizom-OptiPlex-3060:~/Desktop/HYSPLIT/hysplit.v5.3.4_UbuntuOS20.04.6LTS/working$ curl -X POST "http://localhost:8000/run_hysplit/" -H "Content-Type: application/json" -d '{
  "compute": "conc",
  "start_time": [25, 3, 21, 0],
  "num_locations": 2,
  "locations": [
    [25.267421, 55.335341, 7.0, 2025, 3, 21, 0, 0, 3.0, 100000.0, 500.0, 360],
    [24.271421, 55.339341, 8.0, 2025, 3, 21, 2, 0, 2.5, 0.0, 400.0, 360]
  ],
  "run_time": 6,
  "vert_motion_method": 0,
  "top_of_model": 10000.0,
  "num_met_files": 2,
  "met_dir": "/home/oizom/Downloads/",
  "met_filename": "20250320_gfs0p25, 20250321_gfs0p25",
  "num_species": 1,
  "identification": "DUBAI_SOURCES",
  "emission_rate": 1.0,
  "emission_hours": 1,
  "release_start": [0, 0, 0, 0, 0],
  "num_grids": 1,
  "grid_center": [25.269421, 55.337341],
  "grid_spacing": [0.05, 0.05],
  "grid_span": [5.0, 5.0],
  "output_dir": "./",
  "output_filename": "cdump",
  "num_vert_levels": 1,
  "height_levels": 100,
  "sampling_start": [25, 3, 21, 0, 0],
  "sampling_stop": [25, 3, 21, 23, 0],
  "avg_now_max": [0, 1, 0],
  "num_species_dep": 1,
  "properties_key": "test",
  "transient_mode": true,
  "interval": 60
}'
'''