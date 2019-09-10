[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# pynami
This is a basic implementation that accesses the [DPSG NAMI API](https://nami.dpsg.de) and offers some primitives.
Currently this is in **alpha** state. Anything may change at any time.

## Features
Here is a list of the things are currently supported:
* Search for a *Mitglied*
* Show details for a *Mitglied*
* Update / change a *Mitglied*
* View *Ausbildungen* of a *Mitglied*
* View history of a *Mitglied*
* Search, view and update *Tätigkeiten*
* Get all the default values and their ids (e.g. nationalities). This will become important when you want to create e.g. a *Mitglied*
* Dashboard functionality:
  * View notifications
  * View group history entries
  * View statistics about your group
* Group admin stuff:
  * View and download invoices as pdf
* *Führungszeugnis*:
  * Download application form as pdf
  * View and download certificate of inspections

## Todo
Since there is currently no working test setup for the NAMI some things cannot be tested (without endangering the production system).
* Creating a *Mitglied*/*Tätigkeit*
* Deleting a *Mitglied*/*Tätigkeit*
* *Stufenwechsel*
* Edit a *Ausbildung*

## Requirements
You need to have at least [Python 3.6](https://www.python.org/downloads/release/python-360/) for this to work.

## Installation
Just download or clone this repository and run the following command in the top directory (where [setup.py](setup.py) is located).
```bash
pip install [-e] .
```
Use the `-e` option if you want to edit the source files.

## Documentation
Documentation of this package is available at [ReadtheDocs](https://pynami.readthedocs.io/en/latest/). This also covers a lot of the NAMI API.
General documenation for the NAMI API is very few and partially outdated at [DPSG Confluence](https://doku.dpsg.de/display/NAMI/API).
You can also check the NAMI community forums at https://ncm.dpsg.de/.

## Similar projects
There are other projects that can help you access the DPSG NAMI API:
* java: https://github.com/fabianlipp/jnami
* node: https://github.com/platdesign/node-nami-api-client
* php: https://github.com/DaSchaef/NBAS

## Credits
The base of this package is taken from https://github.com/webratz/pynami.
