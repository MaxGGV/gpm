# -*- coding: UTF-8 -*-
import csv
import io
import pandas as pd
import geocoder
import requests
from termcolor import colored

from gpm.decorators import simple_time_tracker

from arcgis.gis import GIS
from arcgis.geocoding import get_geocoders, batch_geocode

# Arcgis API
pwd = "Pim62Z_pZm49Ver"
username = "lologibus2"

# Bing API
bing_key = "AkD8xlCWJPLgo3TmNt8DokHix1klCyhw50IpR0mR7mrn9Ee0eS4Gmi6ajSZjDMyg"

# HERE API
# lologibus77@gmail.com
here_app_id = "L9A8g1WqFIETCd5pyC3c"
here_app_key = "t6e-UcwJ8O9GaaDKTSAZAA"


def processs_geojson(g):
    """
    get information from geocoder
    :param g: geocoder instance
    :return:
    """
    # print('\n')
    if g.ok:
        res = str(g.osm['y']) + ',' + str(g.osm['x'])
    else:
        res = ','
    # print(colored(res, 'blue'))
    return res


class geo_coder(object):
    """
    geocoder returning (lat, lng) from address
    either online or offline
    """

    def __init__(self, kind='arcgis', offline=False):
        self.options = ['osm', 'here', 'arcgis', 'bing']
        self.kind = kind
        self.offline = offline

    # @simple_time_tracker
    def geocode(self, address, session):
        # url = 'http://localhost/nominatim/'
        if self.offline:
            url = 'localhost'
            self.g = geocoder.osm(address, url=url, session=session)
        if self.kind == 'arcgis':
            self.g = geocoder.arcgis(address, session=session)
        if self.kind == 'here':
            self.g = geocoder.here(address, session=session, app_id=here_app_id, app_code=here_app_key)
        if self.kind == 'bing':
            self.g = geocoder.bing(address, session=session, key=bing_key)
        res = processs_geojson(self.g)
        return res

    def run(self, addresses):
        """
        extract city, Country, and
        :return:
        """
        res = []
        l_addresses = [addresses] if type(addresses) != list else addresses
        with requests.Session() as session:
            for address in l_addresses:
                res.append(self.geocode(address, session))
        return res


##################################
#  Batch geocoding
##################################

@simple_time_tracker
def batch_geocode(l_adress, kind='arcgis'):
    if kind == 'arcgis':
        gis = GIS("http://www.arcgis.com", username=username, password=pwd)
        # use the first of GIS's configured geocoders
        geocoder = get_geocoders(gis)[0]
        results = batch_geocode(l_adress)
        lats = [r['location']['x'] for r in results]
        lngs = [r['location']['y'] for r in results]
        return lats, lngs


def batch_geocode_gouv(csv_path='gpm/data/test_batch_api.csv', save=False, sep=','):
    """
    geocode from gouv opendata API, only working for french geoloc
    advantages : free, no limit, and faster
    disadvantages : only for France
    :param csv_path:
    :param save:
    :param sep:
    :return:
    """
    URL = "https://api-adresse.data.gouv.fr"
    url = URL + '/search/csv'
    # Get columns
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=sep)
        cols = reader.fieldnames
    # Send request to gouv api
    with open(csv_path, 'rb') as f:
        res = requests.post(url, files={'data': f})
    # Format output file
    df = pd.read_csv(io.StringIO(res.text), sep=sep)
    cols.extend(['latitude', 'longitude'])
    df = df[cols]
    df.rename(columns={"latitude": "lat", "longitude": "lng"}, inplace=True)
    return df


if __name__ == '__main__':
    add = ["34 rue Raynouard 75016 Paris", "11 rue d'Hauteville 75010 Paris", "110 rue de Rivoli, Paris"]
    for kind in ['here', 'arcgis', 'bing']:
        print(colored(kind, "green"))
        gecod = geo_coder(offline=False, kind=kind)
        res = gecod.run(add)
        print('\n')
    lats, lngs = batch_geocode(add)
