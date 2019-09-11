# -*- coding: utf-8 -*-
"""
This module defines some constants needed for communication with the |NAMI|.
"""

from enum import Enum


class UgId(Enum):
    """Untergliederungs ID"""
    WOE = 1
    JUFFI = 2
    PFADI = 3
    ROVER = 4
    STAVO = 5

    def __str__(self):
        return f'{self.value}'


URLS = {'SERVER': 'https://nami.dpsg.de/ica/rest',
        'AUTH': '/nami/auth/manual/sessionStartup',
        'SEARCH': '/nami/search-multi/result-list',
        'GETMGL': '/nami/mitglied/filtered-for-navigation/'
                  'gruppierung/gruppierung/',
        'LOGOUT': '/nami/auth/logout',
        'MGLTYPE': '/nami/enum/mgltype',
        'LAND': '/baseadmin/land/',
        'ZAHLUNGSKONDITION': '/baseadmin/zahlungskondition/',
        'REGION': '/baseadmin/region/',
        'BEITRAGSART': '/namiBeitrag/beitragsartmgl/gruppierung/',
        'GESCHLECHT': '/baseadmin/geschlecht/',
        'STAAT': '/baseadmin/staatsangehoerigkeit/',
        'KONFESSION': '/baseadmin/konfession/',
        'SEARCH_ALL': '/nami/mitglied/filtered-for-navigation/gruppierung'
                      '/gruppierung/',
        'HISTORY': '/dashboard/history-entries/flist',
        'NOTIFICATIONS': '/dashboard/notification-entries/flist',
        'STATS': '/dashboard/stats/stats',
        'STATUS_LIST': '/nami/search-multi/status-list',
        'TAGLIST': '//tagging/getTagList',
        'BAUSTEIN': '/module/baustein',
        'UNTERGLIEDERUNG': '/orgadmin/untergliederung',
        'ALLE_TAETIGKEITEN': '/nami/search-multi/all-visible-taetigkeiten',
        'EBENE': '/orgadmin/ebene/',
        'EBENE1': '/nami/search-multi/ebene/1',
        'EBENE2': '/nami/search-multi/ebene/2/gruppierung1/',
        'EBENE3': '/nami/search-multi/ebene/3/gruppierung2/',
        'MGL_TAETIGKEITEN': '/nami/zugeordnete-taetigkeiten/'
                            'filtered-for-navigation/gruppierung-mitglied/'
                            'mitglied/',
        'AUSBILDUNG': '/nami/mitglied-ausbildung/filtered-for-navigation/'
                      'mitglied/mitglied/',
        'MGL_HISTORY': '/nami/mitglied-history/filtered-for-navigation/'
                       'mitglied/mitglied/',
        'MGL_HISTORY_EXT': '/nami/mitglied-history-with-values/'
                           'filtered-for-navigation/mitglied/mitglied/',
        'GRUPPIERUNGEN': '/nami/gruppierungen/filtered-for-navigation/'
                         'gruppierung/node/root',
        'GRPADMIN_GRPS': '/nami/gruppierungen-for-grpadmin/parentgruppierung/'
                         '/node/root',
        'INVOICE': '/nami/rechin-for-grpadmin/rechin/gruppierung/',
        'INVOICE_PDF': '/nami/rechin-for-grpadmin/pdf',
        'FZ': '/nami/fz/eigene-bescheinigungen/',
        'BEANTRAGUNG': '/fz-beantragen/download-beantragung'}
"""dict: Holds all default |URL|s"""
