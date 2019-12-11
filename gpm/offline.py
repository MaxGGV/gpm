# coding: utf-8
from os.path import split

import geopandas
from geopy.geocoders import Nominatim

import gpm
from gpm.load import get_local_adress_dataset, load_iris_local, preprocess

folder_source, _ = split(gpm.__file__)
ADRESS_COL_NAME = "full_address"


##################################
# OLD
##################################

def geocode_offline(adress='1327 Harding Place, Charlotte, North Caroline'):
    geolocator = Nominatim()
    location = geolocator.geocode(adress)
    lat, lng = location.latitude, location.longitude
    res = str(lat) + ',' + str(lng)
    return res


##################################
#  Input data preprocessing
##################################

# 1°) Get get_data
# 2°) Add lat, lng with geocoder if not present (either online or offline geocoding)
# 3°) Get insee shapefile
# 4°) Merge 2 datasets


if __name__ == '__main__':
    df = get_local_adress_dataset(N=100)
    df = preprocess(df, to_geopandas=True)
    #places_insee = load_insee_local()
    places_iris = load_iris_local()
    result = geopandas.tools.sjoin(df, places_iris, how="left")
