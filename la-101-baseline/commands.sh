# run sumo cli
$SUMO_HOME/bin/sumo -c osm.sumocfg -b 0 -e 3600 --threads 4 -t 

# Random trips (length, lane, speed weighting | binomial arrival w rate=4)
python3 $SUMO_HOME/tools/randomTrips.py  -n osmSanitized.net.xml --fringe-factor 10 -p 0.25 -o osmSanitized.passenger.trips.xml -e 3600 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 3000 --trip-attributes "departLane=\"random\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --validate -l -L

# Gaussian random trips | 3600 s total time | mean = 1800 | std = 600 | peak_vehicle_rate = 10
python3 $SUMO_HOME/tools/randomTripsModified.py  -n osmSanitized.net.xml --fringe-factor 10 -o osmSanitizedGaussian.passenger.trips.xml -e 3600 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 3000 --trip-attributes "departLane=\"random\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --validate -l -L --mu 1800 --sigma 600 --peak-vehicle-rate 10 


# LA multi model traffic demand generation
python $SUMO_HOME/tools/ptlines2flows.py -n osm.net.xml -e 10800 -p 600 --random-begin --seed 42 --ptstops osm_stops.add.xml --ptlines osm_ptlines.xml -o osm_pt.rou.xml --ignore-errors --vtype-prefix pt_ --stopinfos-file stopinfos.xml --routes-file vehroutes.xml --trips-file trips.trips.xml --min-stops 0 --extend-to-fringe --verbose
python $SUMO_HOME/tools/randomTripsModified.py -n osm.net.xml --fringe-factor 10 -o osm.passengerPeakGaussian.trips.xml -e 10800 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 3000 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --validate -l -L --mu 5400 --sigma 1800 --peak-vehicle-rate 2
python $SUMO_HOME/tools/randomTrips.py -n osm.net.xml --fringe-factor 10 -p 10 -o osm.busIntervened.trips.xml -e 10800 --vehicle-class bus --vclass bus --prefix bus --min-distance 6000 --fringe-start-attributes "departSpeed=\"max\"" --trip-attributes "departLane=\"best\"" --validate
python $SUMO_HOME/tools/randomTrips.py -n osm.net.xml --fringe-factor 40 -p 100 -o osm.rail_urban.trips.xml -e 10800 --vehicle-class rail_urban --vclass rail_urban --prefix urban --fringe-start-attributes "departSpeed=\"max\"" --min-distance 6000 --trip-attributes "departLane=\"best\"" --validate


# LA Final Simulation Run | Baseline peak hour traffic
python $SUMO_HOME/tools/randomTripsModified.py -n osm.net.xml --fringe-factor 10 -o osm.passengerPeakGaussian.trips.xml -e 10800 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 3000 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --validate -l -L --mu 5400 --sigma 1800 --peak-vehicle-rate 2


# HOV Redemption Modeling
python $SUMO_HOME/tools/randomTrips.py -n osm_hov.net.xml --fringe-factor 10 -p 0.5 -o osm.passengerBaseline.trips.xml -e 3600 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 3000 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --validate -l -L
python $SUMO_HOME/tools/randomTrips.py -n osm_hov.net.xml --fringe-factor 10 -p 1.28 -o osm.hov.trips.xml -e 3600 --vehicle-class hov --vclass hov --prefix hov --min-distance 3000 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --validate -l -L

