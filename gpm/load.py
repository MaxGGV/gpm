from os.path import split
import random

import geopandas
import pandas as pd
import numpy as np
from gpm.geocod import geo_coder
from shapely.geometry import Point

import gpm

folder_source, _ = split(gpm.__file__)


#################
# INSEE file
#################

def load_insee_url():
    url = "https://public.opendatasoft.com/explore/dataset/correspondance-code-insee-code-postal/download/?format=shp&timezone=Europe/Berlin"
    insee = geopandas.read_file(url)
    return insee


def save_geojson(insee):
    """
    save data as geojson
    :param insee: geopandas DataFreame
    :return:
    """
    filename = "data/insee.json"
    insee.to_file(filename, driver="GeoJSON")


def load_insee_local():
    path = folder_source + '/data/' + 'insee.json'
    insee = geopandas.read_file(path, driver="GeoJSON")
    return insee


##################################
#  Input data preprocessing
##################################
ADRESS_COL_NAME = "full_address"


def get_online_label_data(save=False):
    N = random.randint(1, 40)
    url = "https://adresse.data.gouv.fr/data/ban/export-api-gestion/latest/ban/ban-{}.csv.gz".format(str(N))
    cols = ['numero', 'nom_voie', 'code_postal', 'nom_commune', 'code_insee']
    df = pd.read_csv(url, sep=';')[cols]
    df = df[~df.code_postal.isnull()]
    df['code_postal'] = df['code_postal'].apply(int)
    df = df.sample(1000)
    if save:
        df[['code_postal', 'code_insee']].to_csv('gpm/data/test_sample_codeInsee.csv', index=False)
        df.pop('code_insee')
        df.to_csv('gpm/data/test_sample.csv', index=False)
    return df


def get_data():
    sep = " "
    PATH = "gpm/data/address-01-sample-10.csv"
    df = pd.read_csv(PATH, sep=';')
    df['code_postal'] = df.code_postal.apply(str).str.zfill(5)
    df[ADRESS_COL_NAME] = df['numero'].astype(str) + sep + df['nom_voie'].astype(str) + sep + df['nom_commune'].astype(
        str) + sep + df['code_postal'].astype(str)
    return df


def preprocess(df, to_geopandas=True, geocode=True, offline=False):
    if geocode:
        forward_geocoder = geo_coder(offline=offline)
        list_addresses = df[ADRESS_COL_NAME].to_list()
        res = forward_geocoder.run(list_addresses)
        df['latlng'] = res
        df['lat'], df['lng'] = df['latlng'].str.split(',', 1).str
        df['lat'], df['lng'] = df['lat'].apply(float), df['lng'].apply(float)
    else:
        df['lat'] = np.random.uniform(48, 49, df.shape[0])
        df['lng'] = np.random.uniform(0, 2, df.shape[0])
    if to_geopandas:
        df['geometry'] = df.apply(lambda row: Point(row['lng'], row['lat']), axis=1)
        df = geopandas.GeoDataFrame(df, geometry="geometry", crs={'init': 'epsg:4326'})
    cols2keep = [ADRESS_COL_NAME, 'lat', 'lng', 'geometry']
    return df[cols2keep]


if __name__ == '__main__':
    #df = get_data()
    #df = preprocess(df.sample(20))
    df = get_online_label_data(save=True)
