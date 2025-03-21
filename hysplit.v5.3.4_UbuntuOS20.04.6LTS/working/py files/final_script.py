
import shutil
import subprocess

def generate_control_file(
    start_time, num_locations, locations, run_time, vert_motion_method, top_of_model,
    num_met_files, met_dir, met_filename, num_species, identification, emission_rate,
    emission_hours, release_start, num_grids, grid_center, grid_spacing, grid_span,
    output_dir, output_filename, num_vert_levels, height_levels, sampling_start,
    sampling_stop, avg_now_max, num_species_dep, particle_properties, pollutant_props,
    henry_constants, radioactive_decay, resuspension_factor, output_file="CONTROL"
):
    """
    Generates a CONTROL file for HYSPLIT with the given parameters.
    Also creates a duplicate file named "default_conc" with the same content.
    """

    # Write the CONTROL file
    with open(output_file, "w") as file:
        file.write(f"{start_time[0]:02d} {start_time[1]:02d} {start_time[2]:02d} {start_time[3]:02d}\n")
        file.write(f"{num_locations}\n")
        
        for loc in locations:
            file.write(f"{loc[0]:.6f} {loc[1]:.6f} {loc[2]:.1f}\n")
        
        file.write(f"{run_time}\n")
        file.write(f"{vert_motion_method}\n")
        file.write(f"{top_of_model:.1f}\n")
        file.write(f"{num_met_files}\n")
        file.write(f"{met_dir}\n")
        file.write(f"{met_filename}\n")
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

    # Create default_conc as a copy of CONTROL
    shutil.copy(output_file, "default_conc")
    print("✅ File 'default_conc' has been created as a duplicate of 'CONTROL'.")

def create_ascdata_cfg(output_file="ASCDATA.CFG"):
    """
    Creates ASCDATA.CFG file with constant values.
    """
    content = """\
-90.0   -180.0  lat/lon of lower left corner
1.0     1.0     lat/lon spacing in degrees
180     360     lat/lon number of data points
2               default land use category
0.2             default roughness length (m)
'C:/HYSPLIT/bdyfiles/'  directory of files
"""
    
    with open(output_file, "w") as file:
        file.write(content)

    print(f"✅ ASCDATA.CFG file '{output_file}' has been successfully created.")

def run_hysplit():
    """
    Runs the HYSPLIT model, concentration plotting, and modify_kml.py script.
    """
    try:
        # Step 1: Run HYSPLIT model
        print("🚀 Running HYSPLIT Model...")
        subprocess.run("../exec/hycs_std", shell=True, check=True)
        print("✅ HYSPLIT Model Run Completed.")

        # Step 2: Run concentration plotting
        print("📊 Running Concentration Plot...")
        subprocess.run("../exec/concplot -icdump -a3", shell=True, check=True)
        print("✅ Concentration Plot Generated.")

        # Step 3: Modify KML File
        print("🛠 Running KML Modification Script...")
        subprocess.run("python modify_kml.py", shell=True, check=True)
        print("✅ KML Modification Completed.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running command: {e}")
    except FileNotFoundError:
        print("❌ Error: One of the required files or programs is missing.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

# Example usage with sample values
generate_control_file(
    start_time=(25, 3, 20, 12),
    # num_locations=5,
    # locations=[
    #     (25.229985, 55.366551, 5.0),
    #     (25.267412, 55.335341, 7.0),
    #     (25.137616, 55.233719, 10.0),
    #     (25.145899, 55.233292, 3.0),
    #     (25.78, 56.07, 7.0)
    # ],
    num_locations=1,
    locations=[
        (25.780000, 57.070000, 7.0)
    ],
    run_time=6,
    vert_motion_method=0,
    top_of_model=10000.0,
    num_met_files=1,
    met_dir="/home/oizom/Downloads/",
    met_filename="20250320_gfs0p25",
    num_species=1,
    identification="TEST",
    emission_rate=1.0,
    emission_hours=0.166666667,
    release_start=(0, 0, 0, 0, 0),
    num_grids=1,
    grid_center=(0.0, 0.0),
    grid_spacing=(0.005, 0.005),
    grid_span=(30.0, 30.0),
    output_dir="./",
    output_filename="cdump",
    num_vert_levels=1,
    height_levels=100,
    sampling_start=(0, 0, 0, 0, 0),
    sampling_stop=(0, 0, 0, 0, 0),
    avg_now_max=(0, 1, 0),
    num_species_dep=1,
    particle_properties=(5.0, 6.0, 1.0),
    pollutant_props=(0.0, 0.0, 0.0, 0.0, 0.0),
    henry_constants=(0.0, 0.0, 0.0),
    radioactive_decay=0.0,
    resuspension_factor=0.0
)

# Create ASCDATA.CFG file
create_ascdata_cfg()

# Run HYSPLIT model and subsequent processes
run_hysplit()
