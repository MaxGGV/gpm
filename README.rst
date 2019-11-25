Data analysis
==============
- Document here the project: gpm
- Description: Repository getting insee codes from input csv


Example of utilisation
=======================

first install package with pip::

    pip install git+git://github.com/lologibus2/gpm.git

Then call functions inside a Notebook for example::

    from gpm.online import get_insee_batch
    data_path = "path_to_your_csv"
    df = get_insee_batch(csv_path=data_path, sep=';', save=False)
    df.head()

If you want to save it to output csv just run::

    df = get_insee_batch(csv_path=data_path, sep=';', save=True)


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




