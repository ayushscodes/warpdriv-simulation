import os, sys

tools = os.path.join(os.environ["SUMO_HOME"], "tools")
sys.path.append(tools)
import traci

SIMULATION_STEPS = 600

def traci_base_test():
    """
    test traci with SUMO - simple case
    """
    import traci

    sumoBinary = "/usr/local/opt/sumo/share/sumo/bin/sumo"
    sumoCmd = [sumoBinary, "-c", "test-grid.sumocfg"]

    traci.start(sumoCmd)
    step = 0
    edgeID = "4-3"
    while step < 10:
        traci.simulationStep()
        print(f"step: {step} | speed {traci.edge.getLastStepMeanSpeed(edgeID)}")
        step += 1

    traci.close()


def traci_reroute_vehicle():
    """
    Test setRoute API
    """
    import traci

    sumoBinary = "/usr/local/opt/sumo/share/sumo/bin/sumo-gui"
    sumoCmd = [sumoBinary, "-c", "test-grid.sumocfg"]

    traci.start(sumoCmd)
    vehID = "veh1"
    route = ["6-5", "5-4", "4-3"]
    for i in range(SIMULATION_STEPS):
        
        # pick a vehID

        # retrieve vehID's current edge

        # setRoute(vehID, route)

        #simulate next step
        traci.simulationStep()
        current_vehicles = traci.vehicle.getIDList()
        if i == 20: 
            traci.vehicle.setRoute(vehID, route)
        if vehID in set(current_vehicles):
            print(f"step: {i} | roadID {traci.vehicle.getRoadID(vehID)}")

    traci.close()


if __name__ == "__main__":
    # traci_base_test()
    traci_reroute_vehicle()
