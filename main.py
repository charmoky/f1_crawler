import argparse

import numpy as np
import matplotlib.pyplot as plt

from gp_crawler import gp_crawler
from season_crawler import season_crawler
from lap_time_crawler import lap_time_crawler



url = "https://fiaresultsandstatistics.motorsportstats.com/series/formula-one"


def list_calendar(cal):
    print("Season 2020 calendar :")
    for key in list(cal.keys()):
        print(" > %10s : %s" % (key, cal[key][1]))

def list_drivers(season):
    drivers = season.get_drivers()
    print("Drivers :")
    for driver in drivers:
        print(" > %s" % driver)


def plot_drivers_laps(gp_names, cal):
    for gp_name in gp_names:
        if not (gp_name in list(cal.keys())):
            print("GP \"%s\" not found !" % gp_name)
            continue
        
        gp = gp_crawler(cal[gp_name][0], gp_name)
        gp.plot_drivers_laps()

def get_driver_normalized_laps(gp_names, cal, drivers):
    
    for driver in drivers:
        laps = []
        gp_names_list = []
        for gp_name in gp_names:
            if not (gp_name in list(cal.keys())):
                print("GP \"%s\" not found !" % gp_name)
                continue
            print("Getting GP \'%s\' info..." % gp_name)
            gp = gp_crawler(cal[gp_name][0], gp_name)
            lap = gp.laptime_crawler()
            if lap == None:
                continue
            gp_names_list.append(gp_name)
            laps.append(lap.get_normalized_laps_no_over(driver, max_value=5))
        
        # Plotting GPs
        fig, axs = plt.subplots()
        axs.violinplot(laps)
        axs.set_ylabel("Normalized lap time")
        axs.get_xaxis().set_tick_params(direction='out')
        axs.xaxis.set_ticks_position('bottom')
        axs.set_xticks(np.arange(1, len(gp_names_list) + 1))
        axs.set_xticklabels(gp_names_list)
        axs.set_xlim(0.25, len(gp_names_list) + 0.75)
        axs.set_xlabel('Grand Prix')

        axs.plot()

        fig.suptitle("%s normalized lap times" % driver, fontsize=20)
        plt.show()

        return

        
def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("-d", "--drivers", required=False, help="Plot normalized times", nargs="+", default="None")
    ap.add_argument("-n", "--normalized", required=False, help="Plot normalized times", action="store_true", default="all")
    ap.add_argument("-g", "--gp_name", required=False, help="GP to plot data for", nargs="+", default="all")
    ap.add_argument("-l", "--list", required=False, help="List all gps and drivers", action="store_true")

    args = ap.parse_args()

    season_2020 = season_crawler(url)
    season_2020_cal = season_2020.get_calendar()

    if args.list:
        list_calendar(season_2020_cal)
        list_drivers(season_2020)
        return
    
    gp_name = list(season_2020_cal.keys())
    if args.gp_name != "all":
        gp_name = args.gp_name

    if args.normalized:
        get_driver_normalized_laps(gp_name, season_2020_cal, args.drivers)
    else:
        plot_drivers_laps(gp_name, season_2020_cal)

if __name__ == "__main__":
    main()