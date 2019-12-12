# coding: utf-8

"""French address geolocalizer API """
import csv
import io

import geopandas
import pandas as pd
import requests
import slumber
from gpm.load import ADRESS_COL_NAME, preprocess, load_iris_local, load_iris_url

from gpm.decorators import simple_time_tracker
from termcolor import colored

URL = "https://api-adresse.data.gouv.fr"


###################
#  Single address
###################

def get_insee_single(address):
    """Get INSEE code from an address
    address: str
    Return (longitude, latitde)
    """
    feat = get_all_single(address=address)
    insee_code = retrieve_insee(feat)
    return insee_code


def get_all_single(address):
    api = slumber.API(URL)
    resources = api.search.get(q=address)
    return resources["features"][0]


def retrieve_insee(feature):
    """Retrieve the address from a feature
    """
    return feature['properties']["citycode"]


def lonlat(feature):
    """Longitude and latitude from a GeoJSON feature
    """
    return feature["geometry"]["coordinates"]


######################################
#  Batch INSEE csv via call to gouv API
######################################

# @simple_time_tracker
def get_insee_batch(csv_path='gpm/data/test_batch_api.csv', save=False, sep=','):
    """
    Get input csv and add INSEE code columns column named code_insee
    :param save: save outputfile to csv if True
    :param csv_path: path to csv file
    :return: dataframe
    """
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
    df_test = df
    cols.append('result_citycode')
    df = df[cols]
    df.rename(columns={"result_citycode": "code_insee"}, inplace=True)
    if save:
        output_name = csv_path.split('.')[0] + '_insee.csv'
        df.to_csv(output_name, index=False)
        print(colored("output file saved with INSEE codes: \n {}".format(output_name), "blue"))
    return df, df_test


#########################################################
#  Batch IRIS via geopandas and local iris dataset
#########################################################

def get_iris_batch(csv_path='gpm/data/groupama_input.csv', sep=',', save=False, df_iris=None):
    """
    Get input csv with predefined set of columns and add IRIS code
    :param df_iris: iris dataframe from load_iris_local function (saves time)
    :param save:
    :param csv_path:
    :param sep:
    :return:
    """
    df = pd.read_csv(csv_path, sep=sep)
    cols = list(df)
    df[ADRESS_COL_NAME] = df['num_niv_type_voie'].astype(str) + " " + df['cd_postal'].astype(str) + " " + df[
        'nom_ville'].astype(str)
    df = preprocess(df, to_geopandas=True, geocode=True)
    if df_iris == None:
        # places_iris = load_iris_local()  # 30 seconds to load
        places_iris = load_iris_url()  # 30 seconds to load
    else:
        places_iris = df_iris
    result = geopandas.tools.sjoin(df, places_iris, how="left")
    cols.append('code_iris')
    if save:
        output_name = csv_path.split('.')[0] + '_iris.csv'
        df.to_csv(output_name, index=False)
        print(colored("output file saved with IRIS codes: \n {}".format(output_name), "blue"))
    return result[cols]


if __name__ == '__main__':
    # path = 'gpm/data/data_gouv_example.csv'
    # q = "34 rue Raynouard, Paris"
    # code_insee = get_insee_single(q)
    # all = get_all_single(q)
    # print(code_insee)
    # _, df = get_insee_batch()
    df = get_iris_batch(csv_path='gpm/data/groupama_input.csv', sep=';')
