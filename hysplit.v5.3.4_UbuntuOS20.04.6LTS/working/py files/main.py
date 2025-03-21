from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple
import hysplit_runner
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class HYSPLITParams(BaseModel):
    start_time: Tuple[int, int, int, int]
    num_locations: int
    locations: List[Tuple[float, float, float]]
    run_time: int
    vert_motion_method: int
    top_of_model: float
    num_met_files: int
    met_dir: str
    met_files: List[str]
    num_species: int
    identification: str
    emission_rate: float
    emission_hours: float
    release_start: Tuple[int, int, int, int, int]
    num_grids: int
    grid_center: Tuple[float, float]
    grid_spacing: Tuple[float, float]
    grid_span: Tuple[float, float]
    output_dir: str
    output_filename: str
    num_vert_levels: int
    height_levels: int
    sampling_start: Tuple[int, int, int, int, int]
    sampling_stop: Tuple[int, int, int, int, int]
    avg_now_max: Tuple[int, int, int]
    num_species_dep: int
    particle_properties: Tuple[float, float, float]
    pollutant_props: List[float]
    henry_constants: List[float]
    radioactive_decay: float
    resuspension_factor: float

@app.post("/run-hysplit")
async def run_hysplit(params: HYSPLITParams):
    try:
        print("Received parameters:", params.dict())  # Add this line
        hysplit_runner.run_hysplit_model(params.dict())
        
        # Check if the output KML file exists
        kml_file = f"{params.output_dir}/{params.output_filename}.kml"
        if not os.path.exists(kml_file):
            raise HTTPException(status_code=500, detail="KML file not generated")
        
        # Read the KML file content
        with open(kml_file, "r") as f:
            kml_content = f.read()
        
        return {"message": "HYSPLIT model run successfully", "kml_content": kml_content}
    except Exception as e:
        print(f"Error in run_hysplit: {str(e)}")  # Add this line
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
