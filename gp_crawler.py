import requests
from bs4 import BeautifulSoup
import lxml
import re
import ast

import urllib.parse as urllib

from lap_time_crawler import lap_time_crawler


class gp_crawler:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.hostname = urllib.urlparse(url).hostname

    def get_laptime_url(self):
        source = requests.get(self.url).text
        soup = BeautifulSoup(source, 'lxml')

        links = soup.select('a')
        for ahref in links:
            if ahref.text == "Lap Times":
                href = ahref.get('href')
                break
        
        return "http://" + self.hostname + href

    def laptime_crawler(self):
        crawler = lap_time_crawler(self.get_laptime_url(), self.name)

        return crawler

    def plot_drivers_laps(self, drivers="all"):

        crawler = self.laptime_crawler()

        crawler.plot_drivers_all_laps(drivers=drivers)
        return

