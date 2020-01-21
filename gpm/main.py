#################
#  Offline : csv => csv enriched
#  Online : csv => csv enriched
#  Online : address => INSEE code
#  Offline : address => INSEE code
#################


def get_insee_batch(path, online=False):
    """
    Get Code INSEE from a list of addresses
    :param path: path to csv file
    :param online: True if research done from api.gouv
    :return: list of addresses with corresponding INSEE codes
    """

    pass


def get_insee_online(path):
    pass


if __name__ == "__main__":
    from gpm.online import get_iris_batch
    from gpm.load import load_iris_url, load_iris_local

    data_path = "/Users/jeanbizot/Documents/projets/GROUPAMA/gpm/gpm/data/data2_code.csv"
    iris = load_iris_local()
    adress_cols = ['num_niv_type_voie', 'Code postal', 'nom_ville']
    df = get_iris_batch(csv_path=data_path, sep=';', save=False, df_iris=iris, l_cols=adress_cols, N=1000)
    df.sample(20)
