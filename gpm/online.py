# coding: utf-8

"""French address geolocalizer API
"""
import csv
import io

import pandas as pd
import requests
import slumber
from gpm.decorators import simple_time_tracker

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


###################
#  Batch csv
###################

@simple_time_tracker
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
    # Send reuqest to gouv api
    with open(csv_path, 'rb') as f:
        res = requests.post(url, files={'data': f})
    # Format output file
    df = pd.read_csv(io.StringIO(res.text), sep=sep)
    cols.append('result_citycode')
    df = df[cols]
    df.rename(columns={"result_citycode": "code_insee"}, inplace=True)
    if save:
        output_name = csv_path.split('.')[0] + '_insee.csv'
        df.to_csv(output_name, index=False)
    return df


if __name__ == '__main__':
    path = 'gpm/data/data_gouv_example.csv'
    q = "34 rue Raynouard, Paris"
    code_insee = get_insee_single(q)
    print(code_insee)
    df = get_insee_batch(csv_path=path ,save=False)
