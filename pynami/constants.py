# -*- coding: utf-8 -*-
"""
This module defines some constants needed for communication with the |NAMI|.
"""

from enum import Enum

BASE_URL = 'https://nami.dpsg.de/ica/rest'
"""str: Base |URL| of the server"""
DEFAULT_PARAMS = {'page': 1,
                  'start': 0,
                  'limit': 10000}
"""dict: Default parameters to avoid pagination. The |NAMI| uses 5000 as limit
when using the `show all` option."""


class UgId(Enum):
    """Untergliederungs ID"""
    WOE = 1
    JUFFI = 2
    PFADI = 3
    ROVER = 4
    STAVO = 5

    def __str__(self):
        return f'{self.value}'


class URLMetaClass(type):
    """
    Meta class for :class:`URLS`

    Makes the class accessible like a dict and prepends the base url when this
    is done. The relative |URL| string can be retrieved in the usual way as
    attributes.
    """
    def __getitem__(cls, key):
        return BASE_URL + super().__getattribute__(key)


class URLS(metaclass=URLMetaClass):
    SERVER = ''
    AUTH = '/nami/auth/manual/sessionStartup'
    SEARCH = '/nami/search-multi/result-list'
    GETMGL = '/nami/mitglied/filtered-for-navigation/gruppierung/' + \
        'gruppierung/{gruppierung}/{mitglied}'
    LOGOUT = '/nami/auth/logout'
    MGLTYPE = '/nami/enum/mgltype'
    LAND = '/baseadmin/land/'
    ZAHLUNGSKONDITION = '/baseadmin/zahlungskondition/'
    REGION = '/baseadmin/region/'
    BEITRAGSART_MGL = '/namiBeitrag/beitragsartmgl/gruppierung/{grpId}/'
    BEITRAGSART = '/namiBeitrag/beitragsart/gruppierung/{grpId}/'
    GESCHLECHT = '/baseadmin/geschlecht/'
    STAAT = '/baseadmin/staatsangehoerigkeit/'
    KONFESSION = '/baseadmin/konfession/'
    SEARCH_ALL = '/nami/mitglied/filtered-for-navigation/gruppierung/' + \
        'gruppierung/{gruppierung}/flist'
    HISTORY = '/dashboard/history-entries/flist'
    NOTIFICATIONS = '/dashboard/notification-entries/flist'
    STATS = '/dashboard/stats/stats'
    STATUS_LIST = '/nami/search-multi/status-list'
    TAGLIST = '//tagging/getTagList'
    BAUSTEIN = '/module/baustein'
    UNTERGLIEDERUNG = '/orgadmin/untergliederung'
    ALLE_TAETIGKEITEN = '/nami/search-multi/all-visible-taetigkeiten'
    EBENE = '/orgadmin/ebene/'
    EBENE1 = '/nami/search-multi/ebene/1'
    EBENE2 = '/nami/search-multi/ebene/2/gruppierung1/{grpId}/'
    EBENE3 = '/nami/search-multi/ebene/3/gruppierung2/{grpId}/'
    MGL_TAETIGKEITEN = '/nami/zugeordnete-taetigkeiten/' + \
        'filtered-for-navigation/gruppierung-mitglied/mitglied/'
    AUSBILDUNG = '/nami/mitglied-ausbildung/filtered-for-navigation/' + \
        'mitglied/mitglied/'
    MGL_HISTORY = '/nami/mitglied-history/filtered-for-navigation/mitglied' + \
        '/mitglied/'
    MGL_HISTORY_EXT = '/nami/mitglied-history-with-values/' + \
        'filtered-for-navigation/mitglied/mitglied/'
    GRUPPIERUNGEN = '/nami/gruppierungen/filtered-for-navigation/' + \
        'gruppierung/node/root'
    GRPADMIN_GRPS = '/nami/gruppierungen-for-grpadmin/parentgruppierung/' + \
        'node/root'
    INVOICE = '/nami/rechin-for-grpadmin/rechin/gruppierung/'
    INVOICE_PDF = '/nami/rechin-for-grpadmin/pdf'
    FZ = '/nami/fz/eigene-bescheinigungen/'
    BEANTRAGUNG = '/fz-beantragen/download-beantragung'
    TK_AUF_GRP = '//nami/taetigkeitaufgruppierung/filtered/gruppierung/' + \
        'gruppierung/{grpId}/'