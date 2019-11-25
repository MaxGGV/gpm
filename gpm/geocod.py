# -*- coding: UTF-8 -*-
import geocoder
import requests

from gpm.decorators import simple_time_tracker


def processs_geojson(g):
    """
    get information from geocoder
    :param g: geocoder instance
    :return:
    """
    if g.ok:
        res = str(g.osm['y']) + ',' + str(g.osm['x'])
    else:
        print(g)
    return res


class geo_coder(object):
    """
    geocoder returning (lat, lng) from address
    either online or offline
    """

    def __init__(self, kind='arcgis', offline=False):
        self.options = ['osm', 'bing', 'arcgis']
        self.kind = kind
        self.options.remove(kind)
        self.offline = offline

    @simple_time_tracker
    def geocode(self, address, session):
        # url = 'http://localhost/nominatim/'
        if self.offline:
            url = 'localhost'
            self.g = geocoder.osm(address, url=url, session=session)
        else:
            self.g = geocoder.arcgis(address, session=session)
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


if __name__ == '__main__':
    add = ["34 rue Raynouard, Paris, France", "11 rue dHauteville, 75010 Paris"]
    gecod = geo_coder(offline=False)
    res = gecod.run(add)
    print(res)
