
import requests
from bs4 import BeautifulSoup
import lxml
import re
import ast
import urllib.parse as urllib

class season_crawler():
    def __init__(self, url):
        self.url = url
        self.hostname = urllib.urlparse(url).hostname
        self.source = requests.get(url).text
        self.soup = BeautifulSoup(self.source, 'html.parser')

    def get_calendar(self):
        calendar = {}
        # Find out where the calendar is
        h2s = self.soup.select('h2')
        for h2 in h2s:
            if h2.text == "Calendar":
                div = h2.parent

        # Find out where the event and date are
        table = div.find('table')
        table_head = table.find('thead')
        date_idx = 0
        gp_idx = 0
        idx = 0
        rows = table_head.find_all('tr')
        for row in rows:
            cols = row.find_all('th')
            for col in cols:        
                if col.text == "Date":
                    date_idx = idx
                if col.text == "Event":
                    gp_idx = idx
                idx = idx + 1
        
        tables_body = table.find_all('tbody')

        for table in tables_body:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                
                links = cols[gp_idx].select('a')
                for link in links:
                    link = link.get("href")
                    break
                
                link = link.replace("/classification", "/session-facts")

                calendar[cols[gp_idx].text] = ["http://" + self.hostname + link, cols[date_idx].text]

        return calendar

    def get_drivers(self):
        drivers = []

        # Find out where the Drivers are
        h2s = self.soup.select('h2')
        for h2 in h2s:
            if h2.text == "Entry List":
                div = h2.parent

        # Find out where the drivers are
        table = div.find('table')
        table_head = table.find('thead')
        driver_idx = 0
        idx = 0
        rows = table_head.find_all('tr')
        for row in rows:
            cols = row.find_all('th')
            for col in cols:        
                if col.text == "Drivers":
                    driver_idx = idx
                idx = idx + 1
        
        tables_body = table.find_all('tbody')

        for table in tables_body:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                
                drivers.append(cols[driver_idx].text)
        
        return drivers

