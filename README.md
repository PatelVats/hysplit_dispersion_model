# HYSPLIT Dispersion Model

This repository contains a complete and fully functional setup of the **HYSPLIT (Hybrid Single-Particle Lagrangian Integrated Trajectory)** model tailored for **Ubuntu 20.04.6 LTS**. It supports both **trajectory simulations** and **dispersion modeling**, with built-in configurations for a variety of atmospheric pollutants:

- PM2.5  
- PM10  
- CO  
- NO₂  
- O₃  
- NO  
- H₂S  
- SO₂  
- NH₃  

## 📦 Repository Contents

- ✅ Precompiled HYSPLIT executables for Linux
- ✅ Scripts for both trajectory and dispersion runs
- ✅ Customizable control files for each pollutant
- ✅ Sample input/output files
- ✅ Utility scripts for automation and visualization

## 🛠️ Requirements

- Ubuntu 20.04.6 LTS
- Standard build tools (e.g., `gfortran`, `make`, `libx11-dev`)
- Python 3 (for optional plotting and post-processing)
- Meteorological data (e.g., GDAS1, NAM12) in appropriate format

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/PatelVats/hysplit_dispersion_model.git
cd hysplit_dispersion_model
```

### 2. Set Executable Permissions
```bash
chmod +x ./exec/*
```

### 3. Set Environment Variables
Ensure the following environment variables point to correct directories:

- HYSPLIT_DIR – path to this repo
- METEO_DIR – path to meteorological input files
- WORK_DIR – working/output directory for simulations

You can set them in your .bashrc or directly in the terminal:

```bash
export HYSPLIT_DIR=$HOME/hysplit_dispersion_model
export METEO_DIR=$HOME/hysplit_dispersion_model/data
export WORK_DIR=$HOME/hysplit_dispersion_model/output
```

### 4. Run a Simulation
- Trajectory Simulation

```bash
./run_trajectory.sh
```
- Dispersion Modeling

```bash
./run_dispersion.sh
```

## Pollutant Customization
All pollutants can be customized via their respective configuration files in the config/ directory. You can adjust:

- Emission rate and duration
- Release height and location
- Pollutant type and units

Edit the relevant CONTROL and SETUP.CFG files for each simulation.

## Output & Visualization
Simulation results are stored in the output/ directory. Post-processing and plotting tools (Python-based) can be used to visualize:

- Pollutant concentration maps
- Time-evolving plume behavior
- Trajectory paths

Optional scripts and examples are provided in the utils/ or docs/ folder.

## Directory Structure

```bash
hysplit_dispersion_model/
├── exec/              # HYSPLIT executables
├── config/            # CONTROL and SETUP files for pollutants
├── run_trajectory.sh  # Run script for trajectory simulation
├── run_dispersion.sh  # Run script for dispersion modeling
├── data/              # Meteorological input files
├── output/            # Model output files
├── docs/              # Additional guides or templates
└── utils/             # Visualization or automation scripts (if any)
```

## References

- NOAA HYSPLIT: https://www.ready.noaa.gov/HYSPLIT.php
- Official Documentation: https://www.ready.noaa.gov/HYSPLIT_welcome.php

## License

This repository is intended for academic, research, and educational purposes only. Please refer to [NOAA's license](https://www.ready.noaa.gov/HYSPLIT_agree.php) for further information.
