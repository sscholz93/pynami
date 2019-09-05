[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# pynami
This is a basic implementation that accesses the [DPSG NAMI API](https://nami.dpsg.de) and offers some primitives.
Currently this is in **alpha** state. Anything may change at any time.

## features
currently only some very basic things are supported:
* search
* show (some) details for a *Mitglied*
* update / change a *Mitglied*

this is not intended to be a ready solution, but a building block to build your own things

## structure
`pynami.nami` is sort of the library
`namitool.py` builds upon this for some samples.

## documentation
Use this readme for pynami.
General documenation for the NAMI api is very few and partially outdated at [DPSG Confluence](https://doku.dpsg.de/display/NAMI/API)
You can also check the NAMI Forums at https://ncm.dpsg.de/

## similar projects
There are other projects that can help you access the DPSG NAMI API:
* java: https://github.com/fabianlipp/jnami
* node: https://github.com/platdesign/node-nami-api-client
* php: https://github.com/DaSchaef/NBAS


## setup
Use `python3`
```bash
git clone https://github.com/webratz/pynami.git
cd pynami
virtualenv venv
pip install -r requirements.txt

# create config file  ~/.pynami.conf
# sample can be found in pynami/pynami.conf.sample

cd pynami
./namitool.py
```


## search

### keywords
this shows a sorted json with all allowed values and types for a search request
```json
{
  "alterBis": "",
  "alterVon": "",
  "bausteinIncludedId": [
  ],
  "ebeneId": null,
  "funktion": "",
  "grpName": "",
  "grpNummer": "",
  "gruppierung1Id": null,
  "gruppierung2Id": [
  ],
  "gruppierung3Id": [
  ],
  "gruppierung4Id": [
  ],
  "gruppierung5Id": [
  ],
  "gruppierung6Id": [
  ],
  "inGrp": false,
  "mglStatusId": null,
  "mglTypeId": [
  ],
  "mglWohnort": "",
  "mitAllenTaetigkeiten": false,
  "mitgliedsNummber": "",
  "nachname": "",
  "organisation": "",
  "privacy": "",
  "searchName": "",
  "searchType": "MITGLIEDER",
  "spitzname": "",
  "taetigkeitId": [
  ],
  "tagId": [
  ],
  "untergliederungId": [
    2
  ],
  "unterhalbGrp": false,
  "vorname": "",
  "withEndedTaetigkeiten": false,
  "zeitschriftenversand": false
}
```
