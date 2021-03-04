import os, sys
import optparse
import random
from scipy.stats import cauchy
import numpy as np
import xml.etree.ElementTree as ET


def vot_distribution(sample_size, loc=10, scale=3):
    x = np.linspace(cauchy.ppf(0.01), cauchy.ppf(0.99), 1000)
    rv = cauchy(loc, scale)
    y = rv.pdf(x)
    samples = rv.rvs(size=size)
    return samples


def responsive_price(current_speed, target_speed, tau=10, delta=1):
    if current_speed < target_speed:
        tau += delta
    if current_speed > target_speed:
        tau -= delta
    return tau


def redeem_credits(vot, karma_balance, current_hov_rate):
    if current_hov_rate <= vot and karma_balance >= current_hov_rate:
        return True, karma_balance - current_hov_rate
    return False, karma_balance


def convert_net_hov():
    netfile = "white-paper-simulations/osm_hov.net.xml"
    tree = ET.parse(netfile)
    root = tree.getroot()

    for edge in root.iter("edge"):
        if "name" in edge.attrib and edge.attrib["name"] == "Santa Monica Freeway":
            hov_lane = edge[-2]
            # print(hov_lane, hov_lane.attrib["index"])
            hov_lane.set("disallow", "passenger")
            current_allowed = hov_lane.attrib["allow"]
            new_allowed = current_allowed.replace("passenger ", '')
            hov_lane.set("allow", new_allowed)

    tree.write("osm_hov.net.xml")


def get_lane_ids():
    # Get hov and gp lane ids for Santa Monica Highway

    netfile = "white-paper-simulations/osm_hov.net.xml"
    tree = ET.parse(netfile)
    root = tree.getroot()

    hov_ids, gp_ids = set(), set()

    # get lane ids for hov and gp lanes
    for edge in root.iter("edge"):
        if "name" in edge.attrib and edge.attrib["name"] == "Santa Monica Freeway":
            hov_lane = edge[-2]
            gp_lane = edge[-3]
            hov_lane_id = hov_lane.attrib["id"]
            gp_lane_id = gp_lane.attrib["id"]
            hov_ids.add(hov_lane_id)
            gp_ids.add(gp_lane_id)
            # print(hov_lane, hov_lane.attrib["index"])
    return hov_ids, gp_ids


def get_lane_stats(hov_ids, gp_ids):
    # aggregate hov and gp stats for HOV converted net

    edgefile = "white-paper-simulations/edgelane_stats.xml"
    tree = ET.parse(edgefile)
    root = tree.getroot()

    occupancy_list, density_list, speed_list, sampled_seconds_list = [], [], [], []

    for edge in root.iter("edge"):
        if "id" in edge.attrib and lane.attrib["id"] in hov_ids:
            occupancy, density, speed = lane.attrib["occupancy"], lane.attrib["density"], lane.attrib["speed"]
            sampledSeconds = lane.attrib["sampledSeconds"]
            occupancy_list.append(occupancy)
            density_list.append(density)
            speed_list.append(speed)
            sampled_seconds_list.append(sampledSeconds)
    
    return occupancy_list, density_list, speed_list, sampled_seconds_list


if __name__ == "__main__":
    # convert_net_hov()
