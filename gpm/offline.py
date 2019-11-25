# coding: utf-8
import json
from os.path import split

import geopandas
import pandas as pd
from pandas.io.json import json_normalize
from scipy import spatial
from shapely.geometry import Point, Polygon, MultiPolygon

import gpm
from geopy.geocoders import Nominatim

folder_source, _ = split(gpm.__file__)
ADRESS_COL_NAME = "full_address"


def is_point_in_path(x, y, poly):
    """
    x, y -- x and y coordinates of point
    poly -- a list of tuples [(x, y), (x, y), ...]
    """
    num = len(poly)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                 (poly[j][1] - poly[i][1])):
            c = not c
        j = i
    return c


def get_closest_point(lat, lng, df):
    l_coords = df[['lat', 'lng']].values
    tree = spatial.KDTree(l_coords)
    res = tree.query([(lat, lng)])
    return res


def geocode_offline(adress='1327 Harding Place, Charlotte, North Caroline'):
    geolocator = Nominatim()
    location = geolocator.geocode(adress)
    lat, lng = location.latitude, location.longitude
    res = str(lat) + ',' + str(lng)
    return res


class insee(object):
    """
    Get raw csv from opendata, add polygon column for geopandas future use
    :return: DataFrame
    """

    def __init__(self):
        PATH = "gpm/data/correspondance-code-insee-code-postal.csv".format(folder_source)
        df = pd.read_csv(PATH, nrows=3000, sep=';')
        df['lat'], df['lng'] = df['geo_point_2d'].str.split(',', 1).str
        df['lat'], df['lng'] = df['lat'].apply(float), df['lng'].apply(float)
        self.df = df
        self.geo_shape_preprocess()

    def geo_shape_preprocess(self):
        col = 'geo_shape'
        self.df[col] = self.df[col].apply(lambda x: json.loads(x))
        self.df = self.df.join(json_normalize(self.df[col].tolist()).add_prefix(col)).drop([col], axis=1)
        self.df = self.df[self.df.geo_shapetype == 'Polygon']
        # self.df['geo_shapecoordinates'] = self.df.apply(lambda x: x['geo_shapecoordinates'][0], axis=1)
        # remove len >2
        self.df['len'] = self.df.apply(lambda x: len(x.geo_shapecoordinates), axis=1)
        print(self.df.shape)
        self.df = self.df[self.df['len'] == 1]
        # self.df['len_list'] = self.df.apply(lambda x: len(x.geo_shapecoordinates[0]), axis=1)
        # print(self.df.iloc[89, :])
        self.df["geometry"] = self.df.apply(lambda row: Polygon(row.geo_shapecoordinates[0]), axis=1)

    def to_geopandas(self):
        self.df = geopandas.GeoDataFrame(self.df, geometry="geometry")
        self.df = self.df.loc[self.df.is_valid]
        cols2keep = ['Code INSEE', 'geometry']
        return self.df[cols2keep]


def get_data(to_geopandas=True, geocode=True):
    PATH = "gpm/data/data_gouv_example.csv".format(folder_source)
    df = pd.read_csv(PATH)
    sep = " "
    df[ADRESS_COL_NAME] = df['adresse'].astype(str) + sep + df['postcode'].astype(str) + sep + df['city'].astype(str)
    if geocode:
        df['latlng'] = df.apply(lambda x: str(geocode_offline(x[ADRESS_COL_NAME])), axis=1)
        df['lat'], df['lng'] = df['latlng'].str.split(',', 1).str
        df['lat'], df['lng'] = df['lat'].apply(float), df['lng'].apply(float)
    if to_geopandas:
        df['geometry'] = df.apply(lambda row: Point(row['lng'], row['lat']), axis=1)
        df = geopandas.GeoDataFrame(df, geometry="geometry")
        #df.crs = {"init": "epsg:4326"}
    cols2keep = ['full_address', 'lat', 'lng', 'geometry']
    return df[cols2keep]


if __name__ == '__main__':
    df = get_data(to_geopandas=True)
    insee = insee()
    places_insee = insee.to_geopandas()
    print(places_insee.shape)
    #result = geopandas.tools.sjoin(df, places_insee, how="left")
