import argparse

from gp_crawler import gp_crawler
from season_crawler import season_crawler

url = "https://fiaresultsandstatistics.motorsportstats.com/series/formula-one"


def list_calendar(cal):
    print("Season 2020 calendar :")
    for key in list(cal.keys()):
        print(" > %10s : %s" % (key, cal[key][1]))

def plot_drivers_laps(gp_names, cal):
    for gp_name in gp_names:
        if not (gp_name in list(cal.keys())):
            print("GP \"%s\" not found !" % gp_name)
            continue
        
        gp = gp_crawler(cal[gp_name][0], gp_name)
        gp.plot_drivers_laps()

def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("-g", "--gp_name", required=False, help="GP to plot data for", nargs="+", default="all")
    ap.add_argument("-l", "--list_gp", required=False, help="List all gps", action="store_true",)

    args = ap.parse_args()

    season_2020 = season_crawler(url)
    season_2020_cal = season_2020.get_calendar()

    if args.list_gp:
        list_calendar(season_2020_cal)
        return
    
    gp_name = list(season_2020_cal.keys())
    if args.gp_name != "all":
        gp_name = args.gp_name

    plot_drivers_laps(gp_name, season_2020_cal)

if __name__ == "__main__":
    main()