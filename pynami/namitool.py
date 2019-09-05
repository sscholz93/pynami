#!/usr/bin/env python
# this is a sample tool that demonstrates some usage cases
import os
from tabulate import tabulate # pylint: disable=E0401
import pytoml as toml
from nami import NaMi

# load config
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'pynami.conf'), 'r') as cfg:
    config = toml.load(cfg)

nami = NaMi(config['nami'])
nami.auth()


def update_mitglied(mglid):
    """
    sample: get a mitglied, change the spitzname and save
    """
    # fetch data and load into schema to get a Mitglied object
    user = nami.get_mitglied_obj(mglid)

    # update the spitzname field
    user.spitzname = 'foobar'

    # save the changes
    user.update(nami)


# update_mitglied(220695)
