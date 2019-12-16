import time
from os.path import split
import random

import geopandas
import pandas as pd
import numpy as np
from termcolor import colored

from gpm.decorators import simple_time_tracker
from gpm.geocod import geo_coder
from shapely.geometry import Point

import gpm

from os.path import split
folder_source, _ = split(gpm.__file__)
data_path = "{}/data/groupama_input.csv".format(folder_source)


#################
# IRIS
#################
@simple_time_tracker
def load_iris_url(save=False):
    """
    load IRIS geoshape file
    :return:
    """
    url = "https://public.opendatasoft.com/explore/dataset/contours-iris/download/?format=geojson&timezone=Europe/Berlin"
    iris = geopandas.read_file(url)
    if save:
        filename = "gpm/data/contours-iris.json"
        iris.to_file(filename, driver="GeoJSON")
    return iris

@simple_time_tracker
def load_iris_local():
    path = folder_source + '/data/' + 'contours-iris.json'
    iris = geopandas.read_file(path, driver="GeoJSON")
    return iris


#################
# INSEE file
#################

def load_insee_url(save=False):
    """
    load INSEE geoshape file
    :return:
    """
    url = "https://public.opendatasoft.com/explore/dataset/correspondance-code-insee-code-postal/download/?format=shp&timezone=Europe/Berlin"
    insee = geopandas.read_file(url)
    if save:
        filename = "gpm/data/insee.json"
        insee.to_file(filename, driver="GeoJSON")
    return insee


def load_insee_local():
    path = folder_source + '/data/' + 'insee.json'
    insee = geopandas.read_file(path, driver="GeoJSON")
    return insee


##################################
#  Input data preprocessing
##################################
ADRESS_COL_NAME = "full_address"


def get_online_adress_dataset(save=False, N_samples=2000):
    """
    Get clean dataset of addresses from url
    Addresses comes with INSEE codes, lat and lng.
    Usefull to test geocoder and final script
    :param save: if true generates a test sample dataset
    :return:
    """
    N = random.randint(1, 40)
    url = "https://adresse.data.gouv.fr/data/ban/export-api-gestion/latest/ban/ban-{}.csv.gz".format(str(N))
    cols = ['numero', 'nom_voie', 'code_postal', 'nom_commune', 'code_insee']
    df = pd.read_csv(url, sep=';')[cols]
    # df = pd.read_csv(url, sep=';')
    df = df[~df.code_postal.isnull()]
    df['code_postal'] = df['code_postal'].apply(int)
    df = df.sample(N_samples)
    if save:
        df[['code_postal', 'code_insee']].to_csv('gpm/data/test_sample_codeInsee.csv', index=False)
        df.pop('code_insee')
        df.to_csv('gpm/data/test_sample.csv', index=False)
    return df


def get_local_adress_dataset(N=100):
    """
    Get sample of clean dataset from url
    With all columns adding full addres columns
    :return:
    """
    sep = " "
    PATH = "gpm/data/address-01-sample-2000.csv"
    df = pd.read_csv(PATH)
    df['code_postal'] = df.code_postal.apply(str).str.zfill(5)
    df[ADRESS_COL_NAME] = df['numero'].astype(str) + sep + df['nom_voie'].astype(str) + sep + df['nom_commune'].astype(
        str) + sep + df['code_postal'].astype(str)
    df = df.rename(columns={"lat": "true_lat", "lng": "true_lng"})
    df = df.sample(N).reset_index(drop=True)
    return df


def preprocess(df, to_geopandas=True, geocode=True):
    """
    :param df: df with full_adress col
    :param to_geopandas:
    :param geocode:
    :return: same df with geocoding and geopandas transformation
    """
    if geocode:
        kind = "here"
        print("Geocoding using {} API in process".format(kind))
        tic = time.time()
        # apply function one by one
        geocod = geo_coder(offline=False, kind=kind)
        df['latlng'] = df.apply(lambda x: geocod.run(x[ADRESS_COL_NAME])[0], axis=1)
        t = round(time.time() - tic, 2)
        print("in {} seconds \n".format(t))
        df['lat'], df['lng'] = df['latlng'].str.split(',', 1).str
        df['lat'], df['lng'] = df['lat'].apply(float), df['lng'].apply(float)
        #Batch
        #df['lat'], df['lng'] = batch_geocode(df[ADRESS_COL_NAME].values)
    if to_geopandas:
        df['geometry'] = df.apply(lambda row: Point(row['lng'], row['lat']), axis=1)
        df = geopandas.GeoDataFrame(df, geometry="geometry")
        df.crs = {"init": "epsg:4326"}
    # cols2keep = ['full_address', 'lat', 'lng', 'geometry']
    return df


if __name__ == '__main__':
    # df = get_data()
    # df = preprocess(df.sample(20))
    # df = get_online_label_data(save=True)
    # df = load_insee_url(save=True)
    pass
