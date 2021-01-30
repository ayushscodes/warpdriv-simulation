import os, sys
import optparse
import random

tools = os.path.join(os.environ["SUMO_HOME"], "tools")
sys.path.append(tools)

import traci
import sumolib


def get_options(args=None):
    optParser = optparse.OptionParser()
    optParser.add_option(
        "-n", "--net-file", dest="netfile", help="define the net file (mandatory)"
    )
    optParser.add_option(
        "-c", "--sumo-config", dest="config", help="sumo config file(mandatory)"
    )
    optParser.add_option(
        "-e", "--end", default=10800, type="int", help="end time (default 60s)"
    )
    optParser.add_option(
        "-r",
        "--reroute-step",
        default=3600,
        type="int",
        help="time step for rerouting vehicles",
    )
    optParser.add_option(
        "--num-roads",
        default=100,
        type="int",
        help="top n roads to reroute vehicles away from",
    )
    optParser.add_option(
        "--num-vehicles",
        default=500,
        type="int",
        help="percent of current vehicles to reroute",
    )

    options, _ = optParser.parse_args(args=args)
    return options


def misc():
    print("router device travel times----")
    print(traci.vehicle.getParameter("veh25", "device.rerouting.edge:-5-4"))

    # use sumolib custom reroutePath(currentEdge, toEdge)
    traci_route = traci.simulation.findRoute("5-0", "4-3", routingMode=0)

    print("travel times (these are adjusted based on mean speeds) ------")
    for edgeID in parsed_modified_route:
        print(traci.edge.getTraveltime(edgeID))


def get_top_congested_roads_with_times(net, traci, n):
    all_edges = net.getEdges()
    edges_times_list = [
        (edge, traci.edge.getTraveltime(edge.getID())) for edge in all_edges
    ]
    edges_times_list.sort(reverse=True, key=lambda x: x[1])
    return edges_times_list[:n]


def remove_congested_roads_from_net(net, top_congested_roads):
    for edge in top_congested_roads:
        net.removeEdge(edge)
    net.removeOutgoingEdges(top_congested_roads)
    return net


def parse_route_to_edges(route):
    if route[0]:
        return [edge.getID() for edge in route[0]]


def reroute_vehicles(traci, netfile, num_roads, num_vehicles):

    # read net from sumolib and initiate modified net for custom rerouting
    net = sumolib.net.readNet(netfile)
    top_congested_roads_with_times = get_top_congested_roads_with_times(
        net, traci, num_roads
    )
    top_congested_roads = [item[0] for item in top_congested_roads_with_times]
    modified_net = remove_congested_roads_from_net(net, top_congested_roads)

    # pick randomized set of vehicles to reroute
    current_vehicles = traci.vehicle.getIDList()
    current_vehicles = list(current_vehicles)
    random.shuffle(current_vehicles)
    print("total vehicles right now: ", len(current_vehicles))
    vehicles_to_reroute = current_vehicles[:num_vehicles]

    for vehID in vehicles_to_reroute:
        print("rerouting vehicle:", vehID)
        current_road = traci.vehicle.getRoadID(vehID)
        # ignore vehicles on the junctions and rails
        if ":" not in current_road and "urban" not in vehID:
            current_edge = net.getEdge(current_road)
            destination_edge = net.getEdge(traci.vehicle.getRoute(vehID)[-1])

            # compute modified route
            modified_route = modified_net.getShortestPath(
                current_edge, destination_edge
            )

            parsed_modified_route = parse_route_to_edges(modified_route)

            # setRoute(vehID, route) if route is non-empty
            if parsed_modified_route:
                traci.vehicle.setRoute(vehID, parsed_modified_route)


def traci_simulate(options):
    """
    Simulate run with custom rerouter on chosen vehicles
    """

    # reroute flag for debugging
    reroute = True

    # set SUMO binary and options
    sumoBinary = "/usr/local/opt/sumo/share/sumo/bin/sumo"
    sumoCmd = [sumoBinary, "-c", options.config, "--threads", "4"]

    # start traci with above sumo command
    traci.start(sumoCmd)

    for i in range(options.end):
        # simulate next step and reroute
        if reroute and i == options.reroute_step:
            print("Rerouting vehicles at step: ", i)
            reroute_vehicles(
                traci, options.netfile, options.num_roads, options.num_vehicles
            )

        traci.simulationStep()

    traci.close()


def main(options):
    traci_simulate(options)


if __name__ == "__main__":
    main(get_options())
