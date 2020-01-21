Data analysis
==============
- Document here the project: gpm
- Description: Repository getting insee codes from input csv


Example of utilisation
=======================

first install package with pip::

    pip install git+git://github.com/lologibus2/gpm.git

Then call functions inside a Notebook for example

- **For INSEE codes**::

    from gpm.online import get_insee_batch
    data_path = "path_to_your_csv"
    df = get_insee_batch(csv_path=data_path, sep=';', save=False)
    df.head()

- **For IRIS codes**::

    from gpm.online import get_iris_batch
    data_path = "path_to_your_csv"
    df = get_iris_batch(csv_path=data_path, sep=';', save=False)
    df.head()

loading all iris Polygon take 1,5 minutes so if you want to try with multiple files you'd rather import iris_file first

You can also specify the **columns used to form the complete adress** in the correct order::

    from gpm.online import get_iris_batch
    from gpm.load import load_iris_url
    data_path = "path_to_your_csv"
    iris = load_iris_url()
    adress_cols = ['num_niv_type_voie', 'cd_postal', 'nom_ville']
    df = get_iris_batch(csv_path=data_path, sep=';', save=False, df_iris=iris, l_cols=adress_cols)
    df.head()

NB : For **Large datasets** the pipeline might take a while to run becaus of batch geocoding

If you want to save it to output csv just run::

    df = get_iris_batch(csv_path=data_path, sep=';', save=True)


Startup the project
=====================
The initial setup.

Create virtualenv and install the project::

  $ sudo apt-get install virtualenv python-pip python-dev
  $ deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt

Unittest test::

  $ make clean install test


Special installation required
=================================
Don't forget to install rtree along with::

    pip install rtree
    sudo apt-get update && apt-get install -y libspatialindex-dev

