Data analysis
==============
- Document here the project: gpm
- Description: Repository getting insee codes from input csv

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




