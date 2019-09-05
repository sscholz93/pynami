"""
NAMI library in python

This module contains the main class :class:`NaMi` and a few simple exception
definitions.
"""
import json
import requests
from tabulate import tabulate
import pytoml as toml

from .schemas import (SearchMitgliedSchema, MitgliedSchema, BaseadminSchema,
                      NotificationSchema, HistoryEntrySchema, StatsSchema,
                      SearchActivitySchema, ActivitySchema,
                      SearchAusbildungSchema, AusbildungSchema,
                      MitgliedHistorySchema)
from .constants import URLS
from .search import SearchSchema


class NamiResponseTypeError(Exception):
    """.. deprecated:: 0.1"""
    pass


class NamiResponseSuccessError(Exception):
    """
    This is being raised when the response 'success' field is not :data:`True`.
    """
    pass


class NamiHTTPError(Exception):
    """Raised when the HTTP status code was not as expected!"""
    pass


class NaMi(object):
    """
    Main class for communication with the |DPSG| |NAMI|

    Example:
        .. code-block::

            with NaMi() as nami:
                nami.auth(username='MITGLIEDSNUMMER', password='PASSWORD')
                table = []
                for mgl in nami.search():
                    table.append(mgl.tabulate())
                print(tabulate(table, headers="keys"))

    Args:
        config (:obj:`dict`, optional): Authorization configuration
    """
    def __init__(self, config={}):
        self.s = requests.Session()
        self.__config = config
        """dict: Contains authorization information and after that a few ids"""

    def _check_response(self, response):
        """
        Check a requests response object if the |NAMI| response looks ok.
        This currently checks some very basic things.

        Raises:
            NamiHTTPError: When |HTTP| communication failes
            NamiResponseSuccessError: When the |NAMI| returns an error
        """
        if response.status_code != requests.codes.ok:
            raise NamiHTTPError(f'HTTP Error. Status Code: '
                                f'{response.status_code}')

        rjson = response.json()
        if not rjson['success']:
            raise NamiResponseSuccessError(f"succes state from NAMI was "
                                           f"{rjson['message']} {rjson}")

        # allowed response types are: OK, INFO, WARN, ERROR, EXCEPTION
        if rjson['responseType'] not in ['OK', 'INFO', None]:
            print(f"responseType from NAMI was {rjson['responseType']}")

        return rjson['data']


    def auth(self, username=None, password=None):
        """
        Authenticate against the |NAMI| |API|. This stores the jsessionId
        cookie in the requests session. Therefore this needs to be called only
        once.

        This also stores your id (not the Mitgliednummer) for later pruposes.

        Args:
            username (:obj:`str`, optional): The |NAMI| username. Which is your
                Mitgliedsnummer
            password (:obj:`str`, optional): Your NAMI password

        Returns:
            :class:`requests.Session`: The requests session, including the
            auth cookie
        """
        if not username or not password:
            username = self.__config['username']
            password = self.__config['password']

        payload = {
            'Login': 'API',
            'username': username,
            'password': password
        }

        url = f"{URLS['SERVER']}{URLS['AUTH']}"
        r = self.s.post(url, data=payload)
        if r.status_code != 200:
            raise ValueError('Authentication failed!')

        # Get the id of the user
        myself = self.search(mitgliedsNummer = username)
        print(myself)
        if len(myself) == 1:
            self.__config['mitgliedsnummer'] = myself[0].id
        else:
            raise ValueError(f'Received {len(myself)} search results while '
                             f'searching for myself!')

        return self.s

    def __enter__(self):
        self.auth()
        return self

    def logout(self):
        """This should be called at the end of the communication. It is called
        when exiting through the :meth:`~contextmnager.__exit__` method.
        """
        url = f"{URLS['SERVER']}{URLS['LOGOUT']}"
        r = self.s.get(url)
        if r.status_code != 204:
            self._check_response(r)

    def __exit__(self, exception_type, exception_value, traceback):
        try:
            self.logout()
        except NamiHTTPError as ex:
            print(f'NamiHTTPError during logout: {ex}')
        if exception_type is None:
            return True

    def _get_baseadmin(self, key, gruppierung=None):
        """Base function for retrieving all core lists from the |NAMI|

        Args:
            key (:obj:`str`): Name of the wanted items
            gruppierung (:obj:`int`): In some cases the URL is a bit different
                and an additional Gruppierungsnummer is nesseccary.
        """
        url = f"{URLS['SERVER']}{URLS[key.upper()]}"
        if gruppierung:
            url += f'{gruppierung}/'
        if key.lower() == 'Beitragsart'.lower():
            url += f"{self.__config['stammesnummer']}/"
        params = {'gruppierung': self.__config['stammesnummer'],
                  'mitglied': self.__config['mitgliedsnummer'],
                  'page': 1,
                  'start': 0,
                  'limit': 1000}
        r = self.s.get(url, params=params)
        return BaseadminSchema().load(self._check_response(r), many=True)

    @property
    def countries(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: List of all
        possible countries with their names and ids"""
        return self._get_baseadmin('Land')

    @property
    def regionen(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: All Possible
        Bundeslaender"""
        return self._get_baseadmin('Region')

    @property
    def zahlungskonditionen(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: Every paying
        method (either bank transfer or debit)"""
        return self._get_baseadmin('Zahlungskondition')

    @property
    def beitragsarten(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: Each possible
        fee"""
        return self._get_baseadmin('Beitragsart')

    @property
    def geschlecht(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: You can choose
        between three genders: male, female and diverse."""
        return self._get_baseadmin('Geschlecht')

    @property
    def staaten(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: A quite long list
        of different nationalities"""
        return self._get_baseadmin('Staat')

    @property
    def konfessionen(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: All denominations
        """
        return self._get_baseadmin('Konfession')

    @property
    def mgltypes(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: You can have one
        of three different member types"""
        return self._get_baseadmin('MglType')

    @property
    def status_list(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: If you are
        active, inactiv or already deleted"""
        return self._get_baseadmin('Status_List')

    @property
    def tagList(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: A different list
        of fee types but with basically the same content. This one is used for
        searching members."""
        return self._get_baseadmin('TagList')

    @property
    def bausteine(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: Choose |DPSG|
        training parts"""
        return self._get_baseadmin('Baustein')

    @property
    def subdivision(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: Which division
        you are associated with. This one is only used for searching."""
        return self._get_baseadmin('Untergliederung')

    @property
    def activities(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: Functional
        activities"""
        return self._get_baseadmin('Alle_Taetigkeiten')

    @property
    def ebenen(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: Structural layers
        in the |DPSG|"""
        return self._get_baseadmin('Ebene')

    @property
    def ebene1(self):
        """:obj:`list` of :class:`~pynami.schemas.Baseadmin`: You can choose
        a Diözese which you belong to."""
        return self._get_baseadmin('Ebene1')

    @property
    def stats(self):
        """
        :class:`~pynami.schemas.Stats`: Contains counts from different tiers.
        The actual list of :class:`pynami.schemas.StatCategory` is in the
        'statsCategories' attribute.
        """
        url = f"{URLS['SERVER']}{URLS['STATS']}"
        r = self.s.get(url)
        return StatsSchema().load(self._check_response(r))

    @property
    def notifications(self):
        """
        :obj:`list` of :class:`~.schemas.Notification`: All current
        notifications (like tier changes of members). In the |NAMI| these are
        displayed in the dashboard.
        """
        url = f"{URLS['SERVER']}{URLS['NOTIFICATIONS']}"
        params = {'page': 1,
                  'start': 0,
                  'limit': 10000}
        r = self.s.get(url, params=params)
        return NotificationSchema().load(self._check_response(r), many=True)

    @property
    def history(self):
        """
        :obj:`list` of :class:`~.schemas.HistoryEntry`: Last editing events
        like updating and creating members.In the |NAMI| these are displayed in
        the dashboard.
        """
        url = f"{URLS['SERVER']}{URLS['HISTORY']}"
        params = {'page': 1,
                  'start': 0,
                  'limit': 10000}
        r = self.s.get(url, params=params)
        return HistoryEntrySchema().load(self._check_response(r), many=True)

    def ebene2(self, ebene1):
        """
        You can choose a Bezirk which you belong to.

        Args:
            ebene1 (int): Group id of a Diözese

        Returns:
            :obj:`list` of :class:`~pynami.schemas.Baseadmin`: List of possible
            Bezirken you are associated with"""
        return self._get_baseadmin('Ebene2', ebene1)

    def ebene3(self, ebene2):
        """
        You can choose a Stamm which you belong to.

        Args:
            ebene1 (int): Group id of a Bezirk

        Returns:
            :obj:`list` of :class:`~pynami.schemas.Baseadmin`: List of possible
            Stämmen you are associated with"""
        return self._get_baseadmin('Ebene3', ebene2)

    def mgl_activities(self, mgl):
        """
        List of all activities of a member

        Args:
            mgl (int): Member id (not |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~pynami.schemas.Activity`: All activities of
            the member (even those which have already ended)
        """
        url = f"{URLS['SERVER']}{URLS['MGL_TAETIGKEITEN']}{mgl}/flist"
        params = {'page': 1,
                  'start': 0,
                  'limit': 10000}
        r = self.s.get(url, params=params)
        return SearchActivitySchema().load(self._check_response(r), many=True)

    def get_activity(self, mgl, id_):
        """
        Get an activity by its id.

        Args:
            mgl (int): Member id (not |DPSG| Mitgliedsnummer)
            id_ (int): Id of the activity. This will probably originate from an
                activity search result, e.g. by calling :meth:`mgl_activities`.

        Returns:
            :class:`~.schemas.Activity`: The Activity object containing all
            details.
        """
        url = f"{URLS['SERVER']}{URLS['MGL_TAETIGKEITEN']}{mgl}/{id_}"
        r = self.s.get(url)
        return ActivitySchema().load(self._check_response(r))

    def update_activity(self, mgl, act):
        """
        Update an activity

        Args:
            mgl (int): Member id (not |DPSG| Mitgliedsnummer)
            act (:class:`~.schemas.Activity`): Updated data set. The activity
                id is taken form this data set.

        Returns:
            :class:`~.schemas.Activity`: A new updated object

        Warning:
            This has not been tested yet!
        """
        url = f"{URLS['SERVER']}{URLS['MGL_TAETIGKEITEN']}{mgl}/{act.id}"
        userjson = ActivitySchema().dumps(act.data)
        print(userjson)
        req = requests.Request('PUT', url,
                               json=userjson)
        prereq = self.s.prepare_request(req)
        print(prereq.body)
#        r = self.s.put(url, json=ActivitySchema().dumps(act.data))
#        return ActivitySchema().load(self._check_response(r))
        return True

    def mgl_ausbildungen(self, mglId):
        """
        Get all trainings from a Mitglied.

        Args:
            mglId (int): Member id (not |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.schemas.SearchAusbildung`: All trainings
            of the member
        """
        url = f"{URLS['SERVER']}{URLS['AUSBILDUNG']}{mglId}/flist"
        params = {'page': 1,
                  'start': 0,
                  'limit': 10000}
        r = self.s.get(url, params=params)
        data = self._check_response(r)
        return SearchAusbildungSchema().load(data, many=True)

    def get_ausbildung(self, mglId, id_):
        """
        Get a training by its id.

        Args:
            mglId (int): Member id (not |DPSG| Mitgliedsnummer)
            id_ (int): Id of the training. This will probably originate from an
                training search result, e.g. by calling
                :meth:`mgl_ausbildungen`.

        Returns:
            :class:`~.schemas.Ausbildung`: The Ausbildung object containing all
            details about the training.
        """
        url = f"{URLS['SERVER']}{URLS['AUSBILDUNG']}{mglId}/{id_}"
        r = self.s.get(url)
        return AusbildungSchema().load(self._check_response(r))

    def update_ausbildung(self, mglId, ausbildung):
        """
        Update an activity

        Args:
            mgl (int): Member id (not |DPSG| Mitgliedsnummer)
            ausbildung (:class:`~.schemas.Ausbildung`): Updated data set. The
                training id is taken form this data set.

        Returns:
            :class:`~.schemas.Ausbildung`: A new updated object

        Warning:
            This has not been tested yet!
        """
        url = f"{URLS['SERVER']}{URLS['AUSBILDUNG']}{mglId}/{ausbildung.id}"
        r = self.s.put(url, json=AusbildungSchema().dumps(ausbildung.data))
        return AusbildungSchema().load(self._check_response(r))

    def mgl_history(self, mglId, ext=True):
        """
        Get all history changes from a Mitglied.

        Args:
            mglId (int): Member id (not |DPSG| Mitgliedsnummer)
            ext (:obj:`bool`, optional): If the extended history format should
                be used. Defaults to :data:`True`.

        Returns:
            :obj:`list` of :class:`~.schemas.HistoryEntry`: All history entries
            of the member
        """
        key = 'MGL_HISTORY_EXT' if ext else 'MGL_HISTORY'
        url = f"{URLS['SERVER']}{URLS[key]}{mglId}/flist"
        params = {'page': 1,
                  'start': 0,
                  'limit': 10000}
        r = self.s.get(url, params=params)
        return HistoryEntrySchema().load(self._check_response(r), many=True)

    def get_mgl_history(self, mglId, id_, ext=True):
        """
        Get a member history entry by its id.

        Args:
            mglId (int): Member id (not |DPSG| Mitgliedsnummer)
            id_ (int): Id of the entry. May originate from a search result,
                e.g. by calling :meth:`mgl_history`.
            ext (:obj:`bool`, optional): If the extended history format should
                be used. Defaults to :data:`True`.

        Returns:
            :class:`~.schemas.MitgliedHistory`: The object containing all vital
            information about this history entry.
        """
        key = 'MGL_HISTORY_EXT' if ext else 'MGL_HISTORY'
        url = f"{URLS['SERVER']}{URLS[key]}{mglId}/{id_}"
        r = self.s.get(url)
        return MitgliedHistorySchema().load(self._check_response(r))

    def search_all(self, filterString='', searchString='', sortproperty=None,
                   sortdirection='ASC'):
        """
        Search function for filtering the whole member list with limited
        filter options.

        It is also possible to sort the results.

        Args:
            filterString (:obj:`str`, optional): Filter attribute.
            searchString (:obj:`str`, optional): You can search within the
                chosen filter attribute. The Format must match the type of the
                filter attribute.
            sortproperty (:obj:`str`, optional): Attribute by wich the results
                shall be sorted.
            sortdirection (:obj:`str`, optional): Direction of sorting. Can
                take the values ``ASC`` (wich is the default) and ``DESC``.

        Returns:
            :obj:`list` of :class:`~pynami.schemas.SearchMitglied`: The search
            results
        """
        sdirvalid = {'ASC', 'DESC'}
        if sortdirection not in sdirvalid:
            raise ValueError(f"search_all: 'sortdirection' must be one of "
                             f"{sdirvalid} but is {sortdirection}.")
        sort = None
        if sortproperty:
            keys = SearchMitgliedSchema.__dict__['_declared_fields'].keys()
            if sortproperty not in keys:
                raise ValueError(f"search_all: value of 'sortproperty' is not "
                                 f"in the list of allowed values!")
            sort = '[{"property":' + f'"{sortproperty}"' + \
                   f',"direction":"{sortdirection}"' + '}]'

        url = f"{URLS['SERVER']}{URLS['SEARCH_ALL']}" + \
              f"{self.__config['stammesnummer']}/flist"
        params = {'filterString': filterString,
                  'searchString': searchString,
                  'page': 1,
                  'start': 0,
                  'limit': 10000,
                  'sort': sort}
        r = self.s.get(url, params=params)
        return SearchMitgliedSchema().load(self._check_response(r), many=True)

    def search(self, **kwargs):
        """
        Run a search for members

        Todo:
            * Check search terms and formatting. Also some search keys can only
                be used mutually exclusive.

        Args:
            **kwargs: Search keys and words. Be advised that some search words
                must  have a certain formatting or can only take a limited
                amount of values.

        Returns:
            :obj:`list` of :class:`~.schemas.SearchMitglied`: The search
            results
        """
        # this is just a default search
        if not kwargs:
            kwargs.update({'mglStatusId': 'AKTIV',
                           'mglTypeId': 'MITGLIED'})

        # this defaults should avoid pagination
        params = {
            'searchedValues': SearchSchema().dumps(kwargs,
                                                   separators=(',', ':')),
            'page': 1,
            'start': 0,
            'limit': 10000
        }
        print(params)
        r = self.s.get(f"{URLS['SERVER']}{URLS['SEARCH']}", params=params)
        print(r.request.body)
        return SearchMitgliedSchema().load(self._check_response(r), many=True)

    def mitglied(self, mglid, method='GET', stammesnummer=None, **kwargs):
        """
        Gets or updates a Mitglied.

        The keyword arguments are passed on to the |HTTP| communication

        Args:
            mglid (int): ID of the Mitglied. This is not the |NAMI|
                Mitgliedsnummer
            method (:obj:`str`): |HTTP| Method. Should be ``GET`` or ``PUT``,
                defaults to ``GET``.
            stammesnummer (:obj:`int`, optional): The |DPSG| Stammesnummer,
                e.g. ``131913``. The default (:data:`None`) takes the value
                from the internal attribute :attr:`~NaMi.__config`.

        Returns:
            :class:`~pynami.schemas.Mitglied`: The retrieved or respectively
            updated Mitglied. Note that the
            :attr:`~pynami.schemas.MitliedSchema.austrittsdatum` attribute is
            not part of the returned data set.
        """
        if not stammesnummer:
            stammesnummer = self.__config['stammesnummer']
        url = f"{URLS['SERVER']}{URLS['GETMGL']}{stammesnummer}/{mglid}"
        r = self.s.request(method, url, **kwargs)
        return MitgliedSchema().load(self._check_response(r))


if __name__ == '__main__':
    import os
    """import logging
    import http.client

    http.client.HTTPConnection.debuglevel = 1
    logging.basicConfig(level=logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True"""

    search = {
        'mglStatusId': 'AKTIV',
        'mglTypeId': 'MITGLIED',
        'untergliederungId': [1, 2],
        'taetigkeitId': 1,
    }
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'pynami.conf'), 'r') as cfg:
        config = toml.load(cfg)
    with NaMi(config['nami']) as nami:
        table = []
#       print(nami.search())
        for mgl in nami.search(**search):
            # print(mgl.data['email'])
            # by default you should only show what the search returns
            table.append(mgl.tabulate())

            # but you can also fetch the actual user object with more data
            # beware to not kill the API with numerous requests
            # details = mgl.get_mitglied(nami)
            # table.append(details.tabulate())

        print(tabulate(table, headers="keys"))

        # print(user.data['kontoverbindung'])
        # user.data['spitzname'] = 'Proff'

        kv = {"id":"147855", "zahlungsKonditionId":1, "mitgliedsNummer":64697,
              "institut":"Spard-Bank West", "kontoinhaber":"Sebastian Scholz",
              "kontonummer":"5024161", "bankleitzahl":"33060592",
              "iban":"DE15330605920005024161","bic":""}
        # user.data['kontoverbindung'] = kv
        # print(user.kontoverbindung)
        # user.update(nami)
        user = nami.mitglied('63868')
        print(user.id)
#        print(nami.mgl_history(user.id))
#        print(nami.get_mgl_history(user.id, nami.mgl_history(user.id)[0].id))
#        print(nami.mgl_ausbildungen(user.id))
#        print([nami.get_ausbildung(user.id, x.id)
#               for x in nami.mgl_ausbildungen(user.id)])
#        act = nami.get_activity(user.id, nami.mgl_activities(user.id)[0].id)
#        print(act)
#        nami.update_activity(user.id, act)
#        user.kontoverbindung.bic = "GENODED1SPW"
        # print(MitgliedSchema().dumps(user.data, separators=(',', ':')))
#        user.update(nami)

#        print(nami.countries)
#        print(nami.regionen)
#        print(nami.zahlungskonditionen)
#        print(nami.beitragsarten)
#        print(nami.geschlecht)
#        print(len(nami.staaten))
#        print(nami.konfessionen)
#        print(nami.mgltypes)
#        print(nami.search_all(filterstring='geburtsdatum',
#                              searchstring='1993-01-02 00:00:00',
#                              sortproperty='entries_vorname'))
#        print(nami.history)
#        print(nami.notifications)
#        print(nami.stats.statscategories)
#        print(nami.status_list)
#        print(nami.tagList)
#        print(nami.bausteine)
#        print(nami.subdivision)
#        print(nami.activities)
#        print(nami.ebenen)
#        print(nami.ebene1)
#        print(nami.ebene2(nami.ebene1[0].id))
#        print(nami.ebene3(nami.ebene2(nami.ebene1[0].id)[0].id))
#        mylist = [[x.descriptor, x.id] for x in nami.ebenen]
#        print(mylist)
#        import csv
#        import sys
#        w = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)
#        print(w.writerows(mylist))
