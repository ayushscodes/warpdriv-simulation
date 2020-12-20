# run sumo cli
$SUMO_HOME/bin/sumo -c osm.sumocfg -b 0 -e 3600 --threads 4 -t 

# Random trips (length, lane, speed weighting | binomial arrival w rate=4)
python3 $SUMO_HOME/tools/randomTrips.py  -n osmSanitized.net.xml --fringe-factor 10 -p 0.25 -o osmSanitized.passenger.trips.xml -e 3600 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 3000 --trip-attributes "departLane=\"random\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --validate -l -L

# Gaussian random trips | 3600 s total time | mean = 1800 | std = 600 | peak_vehicle_rate = 10
python3 $SUMO_HOME/tools/randomTripsModified.py  -n osmSanitized.net.xml --fringe-factor 10 -o osmSanitizedGaussian.passenger.trips.xml -e 3600 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 3000 --trip-attributes "departLane=\"random\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --validate -l -L --mu 1800 --sigma 600 --peak-vehicle-rate 10 