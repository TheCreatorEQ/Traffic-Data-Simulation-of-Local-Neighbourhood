import os
import sys
import traci
import csv

# Assuming SUMO_HOME environment variable is set
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

sumoBinary = "sumo-gui"  # Use "sumo-gui" for graphical interface, or "sumo" for command line
sumoCmd = [sumoBinary, "-c", "grid.sumocfg"]

# File path for the CSV output
csv_file_path = "vehicle_locations.csv"

# Start SUMO as a subprocess and then connect to it
traci.start(sumoCmd)

# Open a CSV file to write the vehicle data
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Time", "VehicleID", "PositionX", "PositionY"])
    
    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            current_time = traci.simulation.getTime()  # Get the current simulation time
            vehicle_ids = traci.vehicle.getIDList()
            
            for vehicle_id in vehicle_ids:
                position = traci.vehicle.getPosition(vehicle_id)
                # Write the current time, vehicle ID, and position to the CSV file
                writer.writerow([current_time, vehicle_id, position[0], position[1]])
                
    finally:
        # Properly close the connection to the simulation
        traci.close()

print(f"Vehicle location data has been written to {csv_file_path}")
