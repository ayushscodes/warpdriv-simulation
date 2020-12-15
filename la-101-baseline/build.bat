#!/bin/bash
python3 "$SUMO_HOME/tools/randomTrips.py"  -n osmSanitized.net.xml --fringe-factor 10 -p 0.258375 -o osmSanitized.passenger.trips.xml -e 3600 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 10000 --trip-attributes "departLane=\"random\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --validate -l -L
3