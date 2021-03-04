python $SUMO_HOME/tools/randomTrips.py -n test-grid.net.xml -o test-grid-demand.trips.xml -e 600 -p 20 --fringe-factor 10 --vehicle-class passenger --vclass passenger --prefix veh --validate


python $SUMO_HOME/tools/randomTrips.py -n osm.net.xml --fringe-factor 10 -p 0.5 -o osm.passengerBaseline.trips.xml -e 3600 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 3000 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --lanes --validate -l -L
