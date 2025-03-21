function calculateMetFiles(startTime, runTime) {
    const start = new Date(startTime[0], startTime[1] - 1, startTime[2], startTime[3]);
    const end = new Date(start.getTime() + runTime * 60 * 60 * 1000);
    
    const metFiles = [];
    let currentDate = new Date(start);
    
    while (currentDate <= end) {
        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, '0');
        const day = String(currentDate.getDate()).padStart(2, '0');
        const fileName = `20250320_gfs0p25`;
        
        if (!metFiles.includes(fileName)) {
            metFiles.push(fileName);
        }
        
        // Move to the next day
        currentDate.setDate(currentDate.getDate() + 1);
        currentDate.setHours(0, 0, 0, 0);  // Reset to start of day
    }
    
    return metFiles;
}

document.getElementById('hysplitForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const startTime = document.getElementById('startTime').value.split(',').map(Number);
    const location = document.getElementById('location').value.split(',').map(Number);
    const runTime = parseInt(document.getElementById('runTime').value);

    const metFiles = calculateMetFiles(startTime, runTime);
    console.log("Met Files:", metFiles);  

    const fullJson = {
        start_time: startTime,
        num_locations: 1,
        locations: [location],
        run_time: runTime,
        vert_motion_method: 0,
        top_of_model: 10000.0,
        num_met_files: metFiles.length,
        met_dir: "/home/oizom/Downloads/",
        met_files: metFiles,
        num_species: 1,
        identification: "TEST",  // Constant value
        emission_rate: 1.0,
        emission_hours: 0.166666667,
        release_start: [0, 0, 0, 0, 0],
        num_grids: 1,
        grid_center: [0.0, 0.0],
        grid_spacing: [0.008, 0.008],
        grid_span: [30.0, 30.0],
        output_dir: "./",
        output_filename: "cdump",
        num_vert_levels: 1,
        height_levels: 100,
        sampling_start: [0, 0, 0, 0, 0],
        sampling_stop: [0, 0, 0, 0, 0],
        avg_now_max: [0, 1, 0],
        num_species_dep: 1,
        particle_properties: [5.0, 6.0, 1.0],
        pollutant_props: [0.0, 0.0, 0.0, 0.0, 0.0],
        henry_constants: [0.0, 0.0, 0.0],
        radioactive_decay: 0.0,
        resuspension_factor: 0.0
    };

    document.getElementById('output').textContent = JSON.stringify(fullJson, null, 2);

    // Send to backend
    fetch('http://localhost:8000/run-hysplit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(fullJson),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('HYSPLIT model run successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error running HYSPLIT model. Check console for details.');
    });
});
