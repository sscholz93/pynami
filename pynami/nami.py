"""
NAMI library in python

This module contains the main class :class:`NaMi` and a few simple exception
definitions.
"""
import json
import requests

from .constants import URLS, DEFAULT_PARAMS
from .schemas.activity import SearchActivitySchema, ActivitySchema
from .schemas.cogc import SearchBescheinigungSchema, BescheinigungSchema
from .schemas.dashboard import NotificationSchema, StatsSchema
from .schemas.default import BaseadminSchema
from .schemas.grpadmin import SearchInvoiceSchema, InvoiceSchema
from .schemas.history import HistoryEntrySchema, MitgliedHistorySchema
from .schemas.mgl import SearchMitgliedSchema, MitgliedSchema
from .schemas.search import SearchSchema
from .schemas.training import SearchAusbildungSchema, AusbildungSchema
from .schemas.tags import TagSchema, SearchTagSchema
from .util import open_download_pdf
from .tools import tabulate2x


class NamiResponseTypeError(Exception):
    """
    This is raised when the response type from the |NAMI| is not in list of
    allowed values or more specifically when the |NAMI| returns an error, a
    warning or an exception.
    """
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
        .. code-block:: python
            :caption: Connect to the |NAMI|, search for all active members
                      and print them in a tabulated form.

            from pynami.nami import NaMi
            from pynami.tools import tabulate2x

            with NaMi(username='MITGLIEDSNUMMER', password='PASSWORD') as nami:
                print(tabulate2x(nami.search()))

    Args:
        config (:obj:`dict`, optional): Authorization configuration
    """
    def __init__(self, config={}, **kwargs):
        self.s = requests.Session()
        self.__config = config
        """dict: Contains authorization information and after that a few ids"""
        self.__config.update(kwargs)

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
        if response.headers['Content-Type'] == 'application/pdf':
            return response.content
        rjson = response.json()
        if not rjson['success']:
            raise NamiResponseSuccessError(f"success state from NAMI was "
                                           f"{rjson['message']} {rjson}")

        # allowed response types are: OK, INFO, WARN, ERROR, EXCEPTION
        if rjson['responseType'] not in ['OK', 'INFO', None]:
            raise NamiResponseTypeError(f"{rjson['responseType']}: "
                                        f"{rjson['message']}")
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

        url = URLS['AUTH']
        r = self.s.post(url, data=payload)
        if r.status_code != 200:
            raise ValueError('Authentication failed!')

        # Get the id of the user
        myself = self.search(mitgliedsNummer=username)
        if len(myself) == 1:
            self.__config['id'] = myself[0].id
            self.__config['stammesnummer'] = myself[0].gruppierungId
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
        url = URLS['LOGOUT']
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

    def _get_baseadmin(self, key, grpId=None, mglId=None, taetigkeitId=None,
                       **kwargs):
        """Base function for retrieving all core lists from the |NAMI|

        Args:
            key (:obj:`str`): Name of the wanted items
            grpId (:obj:`int` or :obj:`str`, optional): Group id
            mglId (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer)
            taetigkeitId (:obj:`int`, optional): Id of an activity. A list of
                all possible ids can be found in the section
                :ref:`tables/activitytypes:Activity types`. This is only
                required for the URLs which needs to be formatted with this
                value.

        Keyword Args:
            gruppierung (:obj:`int` or :obj:`str`, optional): Group id, in case
                this differs from the group id in the |URL| (given by
                ``grpId``)
            mitglied (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer). This overwrites ``mglId``.

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: The returned
            default values
        """
        if not grpId:
            grpId = self.grpId
        url = URLS[key.upper()].format(grpId=str(grpId),
                                       taetigkeitId=taetigkeitId)
        params = {'gruppierung': str(grpId),
                  'mitglied': str(mglId) if mglId else self.myId,
                  'page': 1,
                  'start': 0,
                  'limit': 1000}
        params.update(kwargs)
        r = self.s.get(url, params=params)
        return BaseadminSchema().load(self._check_response(r), many=True)

    @property
    def grpId(self):
        """
        Group id of the user

        Returns:
            int

        """
        return self.__config['stammesnummer']

    @property
    def myId(self):
        """
        |NAMI| internal id of the user

        Returns:
            int

        """
        return self.__config['id']

    def countries(self, grpId=None, mglId=None):
        """
        Get default values

        Args:
            grpId (:obj:`int` or :obj:`str`, optional): Group id
            mglId (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: List of all
            possible countries with their names and ids
        """
        return self._get_baseadmin('Land', grpId, mglId)

    def regionen(self, grpId=None, mglId=None):
        """
        Get default values

        Args:
            grpId (:obj:`int` or :obj:`str`, optional): Group id
            mglId (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: All possible
            Bundeslaender"""
        return self._get_baseadmin('Region', grpId, mglId)

    def zahlungskonditionen(self, grpId=None, mglId=None):
        """
        Get default values

        Args:
            grpId (:obj:`int` or :obj:`str`, optional): Group id
            mglId (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: Every paying
            method (either bank transfer or debit)"""
        return self._get_baseadmin('Zahlungskondition', grpId, mglId)

    def beitragsarten_mgl(self, grpId=None, mglId=None):
        """
        Get default values

        Args:
            grpId (:obj:`int` or :obj:`str`, optional): Group id
            mglId (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: Each possible
            fee for a member"""
        return self._get_baseadmin('Beitragsart_mgl', grpId, mglId)

    def beitragsarten(self, grpId=None, mglId=None):
        """
        Get default values

        Args:
            grpId (:obj:`int` or :obj:`str`, optional): Group id
            mglId (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: Each possible
            fee type"""
        return self._get_baseadmin('Beitragsart', grpId, mglId)

    def geschlechter(self, grpId=None, mglId=None):
        """
        Get default values

        Args:
            grpId (:obj:`int` or :obj:`str`, optional): Group id
            mglId (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: You can choose
            between three genders: male, female and diverse."""
        return self._get_baseadmin('Geschlecht', grpId, mglId)

    def staaten(self, grpId=None, mglId=None):
        """
        Get default values

        Args:
            grpId (:obj:`int` or :obj:`str`, optional): Group id
            mglId (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: A quite long
            list of different nationalities"""
        return self._get_baseadmin('Staat', grpId, mglId)

    def konfessionen(self, grpId=None, mglId=None):
        """
        Get default values

        Args:
            grpId (:obj:`int` or :obj:`str`, optional): Group id
            mglId (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: All
            denominations
        """
        return self._get_baseadmin('Konfession', grpId, mglId)

    def mgltypes(self, grpId=None, mglId=None):
        """
        Get default values

        Args:
            grpId (:obj:`int` or :obj:`str`, optional): Group id
            mglId (:obj:`int` or :obj:`str`, optional): Member id (not the
                  |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: You can have one
            of three different member types"""
        return self._get_baseadmin('MglType', grpId, mglId)

    @property
    def status_list(self):
        """:obj:`list` of :class:`~.schemas.default.Baseadmin`: If you are
        active, inactiv or already deleted"""
        return self._get_baseadmin('Status_List')

    @property
    def tagList(self):
        """:obj:`list` of :class:`~.schemas.default.Baseadmin`: A different
        list of fee types but with basically the same content. This one is
        used for searching members.

        .. deprecated:: 0.3.3
            Only returns an empty list and has therefore become useless."""
        return self._get_baseadmin('TagList')

    @property
    def bausteine(self):
        """:obj:`list` of :class:`~.schemas.default.Baseadmin`: Choose |DPSG|
        training parts"""
        return self._get_baseadmin('Baustein')

    @property
    def subdivision(self):
        """:obj:`list` of :class:`~.schemas.default.Baseadmin`: Which division
        you are associated with. This one is only used for searching."""
        return self._get_baseadmin('Untergliederung')

    @property
    def activities(self):
        """:obj:`list` of :class:`~.schemas.default.Baseadmin`: Functional
        activities"""
        return self._get_baseadmin('Alle_Taetigkeiten')

    @property
    def ebenen(self):
        """:obj:`list` of :class:`~.schemas.default.Baseadmin`: Structural
        layersin the |DPSG|"""
        return self._get_baseadmin('Ebene')

    @property
    def ebene1(self):
        """:obj:`list` of :class:`~.schemas.default.Baseadmin`: You can choose
        a Diözese which you belong to."""
        return self._get_baseadmin('Ebene1')

    @property
    def gruppierungen(self):
        """:obj:`list` of :class:`~.schemas.default.Baseadmin`: Choose from a
        list of groups that you are associated with for member admin"""
        return self._get_baseadmin('Gruppierungen')

    @property
    def grpadmin_grps(self):
        """:obj:`list` of :class:`~.schemas.default.Baseadmin`: Choose from a
        list of groups that you are associated with for group admin"""
        return self._get_baseadmin('grpadmin_grps')

    @property
    def stats(self):
        """
        :class:`~.schemas.dashboard.Stats`: Contains counts from different
        tiers. The actual list of :class:`~.schemas.dashboard.StatCategory` is
        in the :attr:`~.schemas.dashboard.StatsSchema.statsCategories`
        attribute.
        """
        url = URLS['STATS']
        r = self.s.get(url)
        return StatsSchema().load(self._check_response(r))

    def notifications(self, sortproperty=None, sortdirection='ASC', **kwargs):
        """
        Dashboard function

        Returns:
            :obj:`list` of :class:`~.schemas.dashboard.Notification`: All
            current notifications (like tier changes of members). In the |NAMI|
            these are displayed in the dashboard.
        """
        url = URLS['NOTIFICATIONS']
        params = DEFAULT_PARAMS
        if sortproperty:
            params['sort'] = json.dumps([{'property': sortproperty,
                                          'direction': sortdirection}],
                                        separators=(',', ':'))
        params.update(kwargs)
        r = self.s.get(url, params=params)
        return NotificationSchema().load(self._check_response(r), many=True)

    def history(self, **kwargs):
        """
        Dashboard function

        Returns:
            :obj:`list` of :class:`~.schemas.history.HistoryEntry`: Last
            editing events like updating and creating members.In the |NAMI|
            these are displayed in the dashboard.
        """
        url = URLS['HISTORY']
        params = DEFAULT_PARAMS
        params.update(kwargs)
        r = self.s.get(url, params=params)
        return HistoryEntrySchema().load(self._check_response(r), many=True)

    def ebene2(self, ebene1):
        """
        You can choose a Bezirk which you belong to.

        Args:
            ebene1 (int): Group id of a Diözese

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: List of
            possible Bezirken you are associated with"""
        return self._get_baseadmin('Ebene2', ebene1,
                                   gruppierung=self.__config['stammesnummer'])

    def ebene3(self, ebene2):
        """
        You can choose a Stamm which you belong to.

        Args:
            ebene2 (int): Group id of a Bezirk

        Returns:
            :obj:`list` of :class:`~.schemas.default.Baseadmin`: List of
            possible Stämmen you are associated with"""
        return self._get_baseadmin('Ebene3', ebene2,
                                   gruppierung=self.__config['stammesnummer'])

    def invoices(self, groupId=None, **kwargs):
        """
        List of all invoices of a group

        Args:
            groupId (:obj:`int`, optional): Group id

        Returns:
            :obj:`list` of :class:`~.grpadmin.SearchInvoice`: All invoices of
            the specified group
        """
        if not groupId:
            groupId = self.__config['stammesnummer']
        url = f"{URLS['INVOICE']}{groupId}/flist"
        params = DEFAULT_PARAMS
        params.update(kwargs)
        r = self.s.get(url, params=params)
        return SearchInvoiceSchema().load(self._check_response(r), many=True)

    def invoice(self, groupId, invId):
        """
        Get an invoice by its id.

        Args:
            groupId (int): Group id
            invId (int): Id of the invoice. This will probably originate from
                a search result, e.g. by calling :meth:`invoices`.

        Returns:
            :class:`~.grpadmin.Invoice`: The Invoice object containing all
            details.
        """
        url = f"{URLS['INVOICE']}{groupId}/{invId}"
        r = self.s.get(url)
        return InvoiceSchema().load(self._check_response(r))

    def download_invoice(self, id_, **kwargs):
        """
        Downloads and opens an invoice as a pdf document.

        Args:
            id_ (int): Id of the invoice (not the regular invoice number)
            **kwargs: See :meth:`~pynami.util.open_download_pdf`.
        """
        url = URLS['INVOICE_PDF']
        params = {'id': id_}
        r = self.s.get(url, params=params)
        open_download_pdf(self._check_response(r), **kwargs)

    def tk_auf_grp(self, grpId, mglId, **kwargs):
        """
        Get all possible activities for a certain group

        Args:
            grpId (:obj:`int` or :obj:`str`): Group id
            mglId (:obj:`int` or :obj:`str`): Member id (not the |DPSG|
                    Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.default.Baseadmin`: List of possible
            activities
        """
        return self._get_baseadmin('TK_AUF_GRP', grpId, mglId, **kwargs)

    def tk_grp(self, grpId, mglId, **kwargs):
        """
        Get all possible groups for an activity

        Args:
            grpId (:obj:`int` or :obj:`str`): Group id
            mglId (:obj:`int` or :obj:`str`): Member id (not the |DPSG|
                    Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.default.Baseadmin`: List of possible
            groups
        """
        return self._get_baseadmin('TK_GRP', grpId, mglId, **kwargs)

    def tk_ug(self, grpId, mglId, taetigkeitId, **kwargs):
        """
        Get all possible subdivision for an activity

        Args:
            grpId (:obj:`int` or :obj:`str`): Group id
            mglId (:obj:`int` or :obj:`str`): Member id (not the |DPSG|
                    Mitgliedsnummer)
            taetigkeitId (int): Id of the activity. A list of all possible ids
                can be found in the section
                :ref:`tables/activitytypes:Activity types`.

        Returns:
            :obj:`list` of :class:`~.default.Baseadmin`: List of possible
            subdivision
        """
        return self._get_baseadmin('TK_UG', grpId, mglId, taetigkeitId,
                                   **kwargs)

    def tk_caea_grp(self, grpId, mglId, taetigkeitId, **kwargs):
        """
        Get all possible access rights for an activity

        Args:
            grpId (:obj:`int` or :obj:`str`): Group id
            mglId (:obj:`int` or :obj:`str`): Member id (not the |DPSG|
                    Mitgliedsnummer)
            taetigkeitId (int): Id of the activity. A list of all possible ids
                can be found in the section
                :ref:`tables/activitytypes:Activity types`.

        Returns:
            :obj:`list` of :class:`~.default.Baseadmin`: List of possible
            access rights
        """
        return self._get_baseadmin('TK_CAEA_GRP', grpId, mglId, taetigkeitId,
                                   **kwargs)

    def mgl_activities(self, mgl):
        """
        List of all activities of a member

        Args:
            mgl (int): Member id (not |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.activity.Activity`: All activities of
            the member (even those which have already ended)
        """
        url = f"{URLS['MGL_TAETIGKEITEN']}{mgl}/flist"
        params = DEFAULT_PARAMS
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
            :class:`~.activity.Activity`: The Activity object containing all
            details.
        """
        url = f"{URLS['MGL_TAETIGKEITEN']}{mgl}/{id_}"
        r = self.s.get(url)
        return ActivitySchema().load(self._check_response(r))

    def update_activity(self, mgl, act):
        """
        Update an activity

        Args:
            mgl (int): Member id (not |DPSG| Mitgliedsnummer)
            act (:class:`~.activity.Activity`): Updated data set. The activity
                id is taken form this data set.

        Returns:
            :class:`~.activity.Activity`: A new updated object

        Warning:
            This has not been tested yet!
        """
        url = f"{URLS['MGL_TAETIGKEITEN']}{mgl}/{act.id}"
        userjson = ActivitySchema().dumps(act)
        # print(userjson)
        # req = requests.Request('PUT', url,
        #                        json=userjson)
        # prereq = self.s.prepare_request(req)
        # print(prereq.body)
        r = self.s.put(url, json=userjson)
        return ActivitySchema().load(self._check_response(r))

    def mgl_ausbildungen(self, mglId):
        """
        Get all trainings from a Mitglied.

        Args:
            mglId (int): Member id (not |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.training.SearchAusbildung`: All trainings
            of the member
        """
        url = f"{URLS['AUSBILDUNG']}{mglId}/flist"
        params = DEFAULT_PARAMS
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
            :class:`~.training.Ausbildung`: The Ausbildung object containing
            all details about the training.
        """
        url = f"{URLS['AUSBILDUNG']}{mglId}/{id_}"
        r = self.s.get(url)
        return AusbildungSchema().load(self._check_response(r))

    def update_ausbildung(self, mglId, ausbildung):
        """
        Update a training

        Args:
            mgl (int): Member id (not |DPSG| Mitgliedsnummer)
            ausbildung (:class:`~.training.Ausbildung`): Updated data set. The
                training id is taken form this data set.

        Returns:
            :class:`~.training.Ausbildung`: A new updated object

        Warning:
            This has not been tested yet!
        """
        url = f"{URLS['AUSBILDUNG']}{mglId}/{ausbildung.id}"
        r = self.s.put(url, json=AusbildungSchema().dumps(ausbildung))
        return AusbildungSchema().load(self._check_response(r))

    def mgl_history(self, mglId, ext=True):
        """
        Get all history changes from a Mitglied.

        Args:
            mglId (int): Member id (not |DPSG| Mitgliedsnummer)
            ext (:obj:`bool`, optional): If the extended history format should
                be used. Defaults to :data:`True`.

        Returns:
            :obj:`list` of :class:`~.history.HistoryEntry`: All history entries
            of the member
        """
        key = 'MGL_HISTORY_EXT' if ext else 'MGL_HISTORY'
        url = f"{URLS[key]}{mglId}/flist"
        params = DEFAULT_PARAMS
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
            :class:`~.history.MitgliedHistory`: The object containing all vital
            information about this history entry.
        """
        key = 'MGL_HISTORY_EXT' if ext else 'MGL_HISTORY'
        url = f"{URLS[key]}{mglId}/{id_}"
        r = self.s.get(url)
        return MitgliedHistorySchema().load(self._check_response(r))

    def tags(self, mglId, **kwargs):
        """
        Get all tags of a member

        Args:
            mglId (int): Member id (not |DPSG| Mitgliedsnummer)

        Returns:
            :obj:`list` of :class:`~.tags.SearchTag`: List of the search
            results
        """
        url = URLS['TAGS'].format(mglId=mglId)
        params = DEFAULT_PARAMS
        params.update(kwargs)
        r = self.s.get(url, params=params)
        return SearchTagSchema().load(self._check_response(r), many=True)

    def get_tag(self, mglId, tagId):
        """
        Get a tag by its id

        Args:
            mglId (int): Member id (not |DPSG| Mitgliedsnummer)
            tagId(int): Tag id

        Returns:
            :class:`~.tags.Tag`: The tag object with all important details
        """
        url = URLS['GET_TAG'].format(mglId=mglId, tagId=tagId)
        return TagSchema().load(self._check_response(self.s.get(url)))

    def bescheinigungen(self, **kwargs):
        """
        Get all certificates of inspection

        Returns:
            :obj:`list` of :class:`~.schemas.cogc.SearchBescheinigung`: A list
            of all your certificates of inspection
        """
        url = f"{URLS['FZ']}flist"
        params = DEFAULT_PARAMS
        params.update(kwargs)
        r = self.s.get(url, params=params)
        data = self._check_response(r)
        return SearchBescheinigungSchema().load(data, many=True)

    def get_bescheinigung(self, id_):
        """
        View a certificate of inspection by its id

        Args:
            id_ (int): The internal id of the certificate

        Returns:
            :class:`~.schemas.cogc.Bescheinigung`: An object holding all
            important details about the inspection
        """
        url = f"{URLS['FZ']}{id_}"
        r = self.s.get(url)
        return BescheinigungSchema().load(self._check_response(r))

    def download_bescheinigung(self, id_, **kwargs):
        """
        Open a certificate as a |PDF| file

        Args:
            id_ (int): Internal id of the certificate
            **kwargs: See :meth:`~pynami.util.open_download_pdf`.
        """
        url = f"{URLS['FZ']}download-pdf-eigene-bescheinigung"
        params = {'id': id_}
        r = self.s.get(url, params=params)
        open_download_pdf(self._check_response(r), **kwargs)

    def download_beantragung(self, **kwargs):
        """
        Open the application form for a certificate of good conduct as a |PDF|
        file.

        Args:
            **kwargs: See :meth:`~pynami.util.open_download_pdf`.
        """
        url = URLS['BEANTRAGUNG']
        r = self.s.get(url)
        open_download_pdf(self._check_response(r), **kwargs)

    def search_all(self, grpId=None, filterString=None, searchString='',
                   sortproperty=None, sortdirection='ASC', **kwargs):
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
            :obj:`list` of :class:`~.mgl.SearchMitglied`: The search
            results
        """
        assert sortdirection in ['ASC', 'DESC']
        params = DEFAULT_PARAMS
        if sortproperty:
            keys = SearchMitgliedSchema.__dict__['_declared_fields'].keys()
            assert sortproperty in keys
            params.update({'sort': json.dumps([{'property': sortproperty,
                                                'direction': sortdirection}],
                                              separators=(',', ':'))})
        if grpId is None:
            grpId = self.__config['stammesnummer']
        url = URLS['SEARCH_ALL'].format(gruppierung=grpId)
        if filterString:
            params.update({'filterString': filterString,
                           'searchString': searchString})
        params.update(kwargs)
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
            :obj:`list` of :class:`~.mgl.SearchMitglied`: The search
            results

        See also:
            :class:`~.search.SearchSchema` for a complete list of search
            keys
        """
        # this is just a default search
        if not kwargs:
            kwargs.update({})
        params = DEFAULT_PARAMS
        params['searchedValues'] = SearchSchema().dumps(kwargs,
                                                        separators=(',', ':'))
        r = self.s.get(URLS['SEARCH'], params=params)
        return SearchMitgliedSchema().load(self._check_response(r), many=True)

    def mitglied(self, mglId=None, method='GET', grpId=None, **kwargs):
        """
        Gets or updates a Mitglied.

        The keyword arguments are passed on to the |HTTP| communication

        Args:
            mglId (:obj:`int`, optional): ID of the Mitglied. This is not the
                |DPSG| Mitgliedsnummer. Defaults to the user.
            method (:obj:`str`): |HTTP| Method. Should be ``'GET'`` or
                ``'PUT'``, defaults to ``'GET'``.
            grpId (:obj:`int`, optional): The |DPSG| Stammesnummer,
                e.g. ``131913``. The default (:data:`None`) takes the value
                from the internal attribute :attr:`__config`.

        Returns:
            :class:`~.mgl.Mitglied`: The retrieved or respectively updated
            Mitglied. Note that the
            :attr:`~.mgl.MitgliedSchema.austrittsDatum` attribute is not part
            of the returned data set.
        """
        if not mglId:
            mglId = self.__config['id']
        if not grpId:
            grpId = self.__config['stammesnummer']
        url = URLS['GETMGL'].format(gruppierung=grpId, mitglied=mglId)
        r = self.s.request(method, url, **kwargs)
        return MitgliedSchema().load(self._check_response(r))


if __name__ == '__main__':
    import os
    from configparser import ConfigParser
    # import cProfile, pstats, io
    # pr = cProfile.Profile(builtins=False, subcalls=False)
    # from .tools import make_csv, send_emails
    # import logging
    # import http.client

    # http.client.HTTPConnection.debuglevel = 1
    # logging.basicConfig(level=logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True

    search = {
        'mglStatusId': 'AKTIV',
        'mglTypeId': 'MITGLIED',
        'untergliederungId': [2, 3],
        'taetigkeitId': [1, 6]
    }
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '.pynami.conf'))
    with NaMi(dict(config['nami'])) as nami:
        import code
        code.interact(local=locals())
        # pr.enable()
        # print(tabulate2x(nami.search(**search)))
        # print(tabulate2x(nami.search()))
        # for mitglied in nami.search():
        #     print(nami.mitglied(mitglied.id))
        # print(send_emails(nami.search(**search), open_browser=False))
        # user = nami.mitglied()
        # print(user.id)

        # print(user.data['kontoverbindung'])
        # user.data['spitzname'] = 'Chuck Norris'
        # user.update(nami)

        # print(tabulate2x(nami.tags(user.id)))
        # print(nami.get_tag(user.id, nami.tags(user.id)[0].id))
        # print(tabulate2x(nami.tk_auf_grp(100103, user.id)))
        # print(tabulate2x(nami.tk_grp(100103, user.id)))
        # print(tabulate2x(nami.tk_ug(100103, user.id, 6)))
        # print(tabulate2x(nami.tk_caea_grp(100103, user.id, 6)))
        # nami.download_beantragung()
        # print(nami.bescheinigungen())
        # print(nami.get_bescheinigung(nami.bescheinigungen()[0].id))
        # nami.download_bescheinigung(nami.bescheinigungen()[0].id)
        # print(tabulate2x(nami.gruppierungen))
        # print(tabulate2x(nami.grpadmin_grps))
        # print(nami.invoices())
        # print(nami.invoice(100103, nami.invoices()[0].id))
        # nami.download_invoice(nami.invoices()[0].id)
        # print(nami.mgl_history(user.id))
        # print(nami.get_mgl_history(user.id, nami.mgl_history(user.id)[0].id))
        # print(tabulate2x(nami.mgl_ausbildungen(user.id)))
        # print([nami.get_ausbildung(user.id, x.id)
        #       for x in nami.mgl_ausbildungen(user.id)])
        # print(tabulate2x(nami.mgl_activities(user.id)))
        # act = nami.get_activity(user.id, nami.mgl_activities(user.id)[0].id)
        # print(act)
        # nami.update_activity(user.id, act)
        # print(MitgliedSchema().dumps(user.data, separators=(',', ':')))
        # user.update(nami)

        # print(tabulate2x(nami.countries()))
        # print(tabulate2x(nami.regionen()))
        # print(tabulate2x(nami.zahlungskonditionen()))
        # print(tabulate2x(nami.beitragsarten()))
        # print(tabulate2x(nami.beitragsarten_mgl()))
        # print(tabulate2x(nami.geschlechter()))
        # print(tabulate2x(nami.staaten()))
        # print(tabulate2x(nami.konfessionen()))
        # print(tabulate2x(nami.mgltypes()))
        # print(tabulate2x(nami.search_all(filterString='vorname',
        #                                 searchString='Sebastian',
        #                                 sortproperty='entries_nachname')))
        # print(nami.history(filterString='interval', searchString='4'))
        # print(tabulate2x(nami.notifications(filterString='interval',
        #                                     searchString='4')))
        # print(nami.stats.statsCategories)
        # print(nami.status_list)
        # print(nami.tagList)
        # print(nami.bausteine)
        # print(nami.subdivision)
        # print(tabulate2x(nami.activities))
        # print(tabulate2x(nami.ebenen))
        # print(tabulate2x(nami.ebene1))
        # print(tabulate2x(nami.ebene2(nami.ebene1[0].id)))
        # print(tabulate2x(nami.ebene3(nami.ebene2(nami.ebene1[0].id)[0].id)))
        # print(make_csv(nami.ebenen))
        # pr.disable()
        # pr.print_stats('cumulative')
