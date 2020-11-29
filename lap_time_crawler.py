import requests
from bs4 import BeautifulSoup
import lxml
import re
import ast
import math

import numpy as np
import matplotlib.pyplot as plt


class lap_time_crawler:
    def __init__(self, url, name):
        self.name = name
        self.url = url
        self.dic_laptime = None
        self.drivers = None
        self.script = None

    def get_url_script_part(self):
        # Get the script part of the webpage
        source = requests.get(self.url).text
        soup = BeautifulSoup(source, 'lxml')
        body = soup.find('body')
        script = str(body.script)        

        self.script = script

        return script

    def get_all_drivers(self, script=None):
        if script == None:
            if self.script == None:
                self.get_url_script_part()
            
            script = self.script
        
        driver_regex = r",\"driver\":{\"type\":\"Driver\",\"name\":\"(.+?)\""

        #Fina all drivers 
        drivers = re.findall(driver_regex, script)

        self.drivers = drivers
        return drivers

    def get_laptime_dic(self, drivers=None):
        lap_regex = r"\"facts\".*?%s.*?,\"laps\":\[(.*?)\]"

        if drivers == None:
            if self.drivers == None:
                self.get_all_drivers()
            
            drivers = self.drivers

        dic_laptime = {}
        for driver in drivers:
            # Fin lap time
            lap_re = re.search(lap_regex % driver, self.script)

            # Make lap arrays into easier dic
            laps = np.array([])
            time = np.array([])

            lap_long_dic = ast.literal_eval("[%s]" % lap_re.group(1))
            for lap in lap_long_dic:
                
                laps = np.append(laps, int(lap['lap']))
                time = np.append(time, int(lap['time']))

            lap_list = [laps, time]

            dic_laptime[driver] = lap_list

        self.dic_laptime = dic_laptime

        return dic_laptime

    def get_average_laptime(self):
        if self.dic_laptime == None:
            self.get_laptime_dic()

        laps = np.array([])

        for key in list(self.dic_laptime.keys()):
            laps = np.append(laps, self.dic_laptime[key][1])
        
        return np.mean(laps)

    def get_normalized_laps(self, driver):

        average_mean = self.get_average_laptime()

        if not (driver in list(self.dic_laptime.keys())):
            print ("Could not find driver %s !" % driver)
            return None

        laps = self.dic_laptime[driver][1]

        # Some GP has lap times at 0 
        #   Probably an encoding issue
        laps = laps[laps != 0]

        laps = laps / average_mean

        return laps

    def get_normalized_laps_no_over(self, driver, max_value=10):

        average_mean = self.get_average_laptime()

        if not (driver in list(self.dic_laptime.keys())):
            print ("Could not find driver %s !" % driver)
            return None

        laps = self.dic_laptime[driver][1]

        # Some GP has lap times at 0 
        #   Probably an encoding issue
        laps = laps[laps != 0]

        laps = laps / average_mean

        # Remove outliers
        laps = laps[laps <= max_value]

        return laps

    def get_normalized_laps_all_driver(self):
        if self.dic_laptime == None:
            self.get_laptime_dic()
        
        dic_norm = {}
        for key in list(self.dic_laptime.key()):
            dic_norm[key] = self.get_normalized_laps(key)

        return dic_norm

    def plot_drivers_all_laps(self, drivers="all"):
        if self.dic_laptime == None:
            self.get_laptime_dic()
        
        if drivers == "all":
            drivers = self.drivers

        plots = len(drivers)

        if plots >= 6:
            plot_per_line = int(math.sqrt(plots))
            lines = math.ceil(plots / plot_per_line)
        else:
            plot_per_line = 1
            lines = plots

        fig, axs = plt.subplots(lines, plot_per_line, sharex=True, sharey=True)
        
        plot = 0
        line = 0
        for driver in drivers:
            if plot_per_line > 2:
                axs[line, plot].plot(self.dic_laptime[driver][0].tolist(),self.dic_laptime[driver][1].tolist())
                axs[line, plot].set_xlabel("Laps")
                axs[line, plot].set_ylabel("Time")
                axs[line, plot].set_title('%s' % driver)
            else:
                axs[line].plot(self.dic_laptime[driver][0].tolist(),self.dic_laptime[driver][1].tolist())
                axs[line].set_xlabel("Laps")
                axs[line].set_ylabel("Time")
                axs[line].set_title('%s' % driver)
            
            plot = plot + 1
            if plot == plot_per_line:
                plot = 0
                line = line + 1
    
        fig.suptitle("%s lap times" % self.name, fontsize=20)
        plt.show()


