"""
:class:`~marshmallow.Schema` classes corresponding to the |NAMI| data structure

Pretty much everything in this module depends on functions from the
:mod:`marshmallow` module.

Todo:
    * Include Bills
    * Include validation when neccessary
"""
import json
from collections import OrderedDict
from marshmallow import fields, post_load, pre_load, post_dump

from .base import BaseSchema


class NamiKonto:
    """
    Holds information about bank account and payment method of the member.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<Kontodaten(Id: {self.id})>'

    def __str__(self):
        return f'{self.zahlungsKondition}'


class NamiKontoSchema(BaseSchema):
    """
    Schema class for bank account and payment method information.

    This Schema will is :std:doc:`nested <nesting>` inside a
    :class:`MitgliedSchema` and there should be no other use for it.
    """
    id = fields.String()
    zahlungsKonditionId = fields.Integer()
    mitgliedsNummer = fields.Integer()
    institut = fields.String()
    kontoinhaber = fields.String()
    kontonummer = fields.String()
    bankleitzahl = fields.String()
    iban = fields.String()
    bic = fields.String()
    zahlungsKondition = fields.String(load_only=True)

    @post_load
    def make_konto(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            NamiKonto: Main class for this Schema
        """
        return NamiKonto(**data)

    @pre_load
    def id_to_str(self, data):
        """
        For some reason the |NAMI| gives the id of the payment details as an
        :obj:`integer <int>`, but when you want to update a member it has be a
        :obj:`string <str>`. Therefore this method converts incoming ids to a
        :obj:`str` object before loading them by making use of the
        :func:`~marshmallow.decorators.pre_load` decorator.

        Args:
            data (dict): Data dictionary to be loaded

        Returns:
            dict: Corrected data dictionary
        """
        data['id'] = f'{data["id"]}'
        return data

    @post_dump
    def double_dump(self, data):
        """
        Incoming data sets are nicely formatted :mod:`json` strings which can
        be loaded easily into the Schema but when you update a Mitglied all
        payment details have to formatted into a :mod:`json` string and all
        attributes have to be in a certain order.
        To achieve this the :func:`~marshmallow.decorators.post_dump` decorator
        is used.

        Args:
            data (dict): Already dumped data set

        Returns:
            str: A :mod:`json` formatted string
        """
        return json.dumps(data, separators=(',', ':'))


class NamiBaseadminIdField(fields.Field):
    """
    For the general :class:`BaseadminSchema` class the id of the actual entry
    can either by a :obj:`str` oder :obj:`int` so that there is the need for a
    custom :class:`~marshmallow.fields.Field`.
    """
    def _deserialize(self, value, attr, data):
        try:
            return int(value)
        except ValueError:
            return str(value)


class SearchMitglied:
    """
    Main class for a Mitglied which came up as a search result. Unfortunately
    there cannot be just one Mitglied class because the search results lack
    crucal imformation (e.g. payment details).
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<SearchMitglied({self.descriptor})>'

    def __str__(self):
        return f'{self.descriptor}'

    def table_view(self):
        """
        Prepare nicely formatted output

        Returns:
            dict: All data entries which are not in the blacklist
        """
        field_blacklist = ['representedClass', 'mglType',
                           'staatsangehoerigkeit', 'status', 'geschlecht',
                           'eintrittsdatum', 'id', 'wiederverwendenFlag',
                           'descriptor', 'version', 'lastUpdated', 'id_id']
        return {k: v for k, v in self.data.items() if v is not None
                and v != '' and k not in field_blacklist}

    def tabulate(self, elements=None):
        """
        Prepare ordered tabulated output

        Args:
            elements (:obj:`list` of :obj:`str`, optional): List of keys which
                shall be included in the table

        Returns:
            :class:`~collections.OrderedDict`: Specified data entries
        """
        d = OrderedDict()
        if not elements:
            elements = ['mitgliedsNummer', 'vorname', 'nachname',
                        'geburtsDatum']
        for k in elements :
            d[k] = self.data[k]
        return d

    def get_mitglied(self, nami):
        """
        Create a real :class:`Mitglied` form the search result by getting the
        corresponding data set through the member id.

        Args:
            nami (:class:`~pynami.nami.NaMi`): Main |NAMI| class

        Returns:
            Mitglied: The Mitglied object corresponding to this search result.
        """
        return nami.mitglied(self.id_id, 'GET')


class SearchMitgliedSchema(BaseSchema):
    """
    Schema class for :class:`SearchMitglied`.

    For some reason attribute naming in the |NAMI| is a bit inconsistent
    between a Mitglied which comes up as a search result and one that is
    addressed directly by its id.
    """
    descriptor = fields.String()
    entries_austrittsDatum = fields.DateTime(attribute='austrittsDatum',
                                             allow_none=True)
    entries_beitragsarten = fields.String(attribute='beitragsarten')
    entries_eintrittsdatum = fields.DateTime(attribute='eintrittsdatum')
    entries_email = fields.String(attribute="email")
    entries_emailVertretungsberechtigter = \
        fields.String(attribute="emailVertretungsberechtigter",
                      allow_none=True)
    entries_ersteTaetigkeitId = \
        fields.Integer(attribute='ersteTaetigkeitId', allow_none=True)
    entries_ersteUntergliederungId = \
        fields.Integer(attribute='ersteUntergliederungId', allow_none=True)
    entries_fixBeitrag = fields.String(attribute="fixBeitrag", allow_none=True)
    entries_geburtsDatum = fields.DateTime(attribute='geburtsDatum')
    entries_genericField1 = fields.String(attribute="genericField1",
                                          allow_none=True)
    entries_genericField2 = fields.String(attribute="genericField2",
                                          allow_none=True)
    entries_geschlecht = fields.String(attribute='geschlecht')
    entries_id = fields.Integer(attribute='id')
    entries_jungpfadfinder = fields.String(attribute='jungpfadfinder')
    entries_konfession = fields.String(attribute='konfession')
    entries_kontoverbindung = fields.String(attribute='kontoverbindung')
    entries_lastUpdated = fields.DateTime(attribute='lastUpdated')
    entries_mglType = fields.String(attribute='mglType')
    entries_mitgliedsNummer = fields.Integer(attribute='mitgliedsNummer')
    entries_nachname = fields.String(attribute='nachname')
    entries_pfadfinder = fields.String(attribute='pfadfinder')
    entries_rover = fields.String(attribute='rover')
    entries_rowCssClass = fields.String(attribute='rowCssClass')
    entries_spitzname = fields.String(attribute='spitzname')
    entries_staatangehoerigkeitText = \
        fields.String(attribute='staatangehoerigkeitText')
    entries_staatsangehoerigkeit = \
        fields.String(attribute='staatsangehoerigkeit')
    entries_status = fields.String(attribute='status')
    entries_stufe = fields.String(attribute='stufe')
    entries_pfadfinder = fields.String(attribute='pfadfinder')
    entries_telefax = fields.String(attribute='telefax')
    entries_telefon1 = fields.String(attribute='telefon1')
    entries_telefon2 = fields.String(attribute='telefon2')
    entries_telefon3 = fields.String(attribute='telefon3')
    entries_version = fields.Integer(attribute='version')
    entries_vorname = fields.String(attribute='vorname')
    entries_pfadfinder = fields.String(attribute='pfadfinder')
    entries_wiederverwendenFlag = \
        fields.Boolean(attribute='wiederverwendenFlag')
    entries_woelfling = fields.String(attribute='woelfling')
    id = fields.Integer(attribute='id_id')
    representedClass = fields.String(attribute='representedClass')
    entries_gruppierung = fields.String(allow_none=True)
    entries_gruppierungId = fields.String(allow_none=True)

    @post_load
    def make_user(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            SearchMitglied: Main class for this Schema
        """
        return SearchMitglied(**data)


class Mitglied(object):
    """
    Main class representing a |NAMI| Mitglied

    This class overwrites the :meth:`~object.__getattr__` and
    :meth:`~object.__setattr__` methods so that attributes of this class can be
    handled in a convinient way. It is intended to be instantiated by calling
    the :meth:`~marshmallow.Schema.load` method on a corresponding data
    dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs

    def __repr__(self):
        return f'<Mitglied({self.nachname}, {self.vorname})>'

    def __str__(self):
        return f'{self.vorname} {self.nachname}'

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return self.data[name]

    def __setattr__(self, name, value):
        try:
            super().__setattr__(name, value)
        except AttributeError:
            self.data[name] = value

    def table_view(self):
        """
        Prepare nicely formatted output

        Returns:
            dict: All data entries which are not in the blacklist
        """
        field_blacklist = ['genericField1']
        return {k: v for k, v in self.data.items() if v is not None
                and v != '' and k not in field_blacklist}

    def tabulate(self, elements=None):
        """
        Prepare ordered tabulated output

        Args:
            elements (:obj:`list` of :obj:`str`, optional): List of keys which
                shall be included in the table

        Returns:
            :class:`~collections.OrderedDict`: Specified data entries
        """
        d = OrderedDict()
        if not elements:
            elements = ['mitgliedsNummer', 'vorname', 'nachname',
                        'geburtsDatum', 'strasse', 'stufe']
        for k in elements :
            d[k] = self.data[k]
        return d

    def update(self, nami):
        """
        Writes the possibly changed values to the |NAMI|

        Args:
            nami (:class:`~pynami.nami.NaMi`): Main class for communication
                with the |NAMI|

        Returns:
            Mitglied: The new Mitglied as it is returned by the |NAMI|
        """
        userjson = MitgliedSchema().dump(self.data)
        return nami.mitglied(self.id, 'PUT', json=userjson)


class MitgliedSchema(BaseSchema):
    """
    Schema class for a :class:`Mitglied`
    """
    austrittsDatum = fields.DateTime(allow_none=True, load_only=True)
    beitragsart = fields.String(allow_none=True)
    beitragsartId = fields.Integer(allow_none=True)
    eintrittsdatum = fields.DateTime()
    email = fields.String()
    emailVertretungsberechtigter = fields.String()
    ersteTaetigkeit = fields.String(allow_none=True)
    ersteTaetigkeitId = fields.Integer(allow_none=True, load_only=True)
    ersteUntergliederung = fields.String(allow_none=True)
    ersteUntergliederungId = fields.Integer(allow_none=True, load_only=True)
    fixBeitrag = fields.String(allow_none=True)
    geburtsDatum = fields.DateTime()
    genericField1 = fields.String(allow_none=True)
    genericField2 = fields.String(allow_none=True)
    geschlecht = fields.String()
    geschlechtId = fields.Integer(allow_none=True)
    gruppierung = fields.String()
    gruppierungId = fields.Integer(allow_none=True)
    id = fields.Integer()
    jungpfadfinder = fields.String(allow_none=True)
    konfession = fields.String(allow_none=True)
    konfessionId = fields.Integer(allow_none=True)
    kontoverbindung = fields.Nested(NamiKontoSchema)
    land = fields.String()
    landId = fields.Integer()
    lastUpdated = fields.DateTime(load_only=True)
    mglType = fields.String()
    mglTypeId = fields.String(load_only=True)
    mitgliedsNummer = fields.Integer(load_only=True)
    nachname = fields.String()
    nameZusatz = fields.String(allow_none=True)
    ort = fields.String(allow_none=True)
    pfadfinder = fields.String(allow_none=True)
    plz = fields.String(allow_none=True)
    region = fields.String(allow_none=True)
    regionId = fields.Integer(allow_none=True)
    rover = fields.String(allow_none=True)
    sonst01 = fields.Boolean(allow_none=True)
    sonst02 = fields.Boolean(allow_none=True)
    spitzname = fields.String(allow_none=True)
    staatsangehoerigkeit = fields.String(allow_none=True)
    staatsangehoerigkeitId = fields.Integer(allow_none=True)
    staatsangehoerigkeitText = fields.String(allow_none=True)
    status = fields.String(allow_none=True)
    strasse = fields.String(allow_none=True)
    stufe = fields.String(allow_none=True)
    telefax = fields.String(allow_none=True)
    telefon1 = fields.String(allow_none=True)
    telefon2 = fields.String(allow_none=True)
    telefon3 = fields.String(allow_none=True)
    version = fields.Integer()
    vorname = fields.String(allow_none=True)
    wiederverwendenFlag = fields.Boolean()
    woelfling = fields.String(allow_none=True)
    zeitschriftenversand = fields.Boolean(allow_none=True)

    class Meta(BaseSchema.Meta):
        """
        Extended :class:`marshmallow.Schema.Meta` class for further
        configuration
        """
        ordered = True
        """bool: This is nesseccary for the payment deatils to be dumped in the
        corrent order."""

    @post_load
    def make_user(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            Mitglied: Main class for this Schema
        """
        return Mitglied(**data)


class Baseadmin(object):
    """
    Base data class for all default values and their id mapping.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<{self.type}({self.descriptor}, Id: {self.id})>'

    def __str__(self):
        return f'{self.descriptor}'

    @property
    def type(self):
        """str: Last part of the |NAMI| class structure which is stored in the
        ``representedClass`` attribute for all the default values."""
        return self.representedClass.split(".")[-1]


class BaseadminSchema(BaseSchema):
    """
    Schema class for the :class:`Baseadmin` class

    All the default values only consist of the same four attributes
    """
    descriptor = fields.String()
    name = fields.String()
    representedClass = fields.String()
    id = NamiBaseadminIdField()

    @post_load
    def make_baseadmin(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            Baseadmin: Main class for this Schema
        """
        return Baseadmin(**data)


class Notification:
    """
    Main class for notification like tier changes of a mitglied.

    In the |NAMI| the notifications are displayed in the dashboard.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<Notification({self.entries_entryDate}: ' + \
               f'{self.entries_operation})>'

    def __str__(self):
        return f'{self.entries_operation}'


class NotificationSchema(BaseSchema):
    """
    Schema class for the :class:`Notification` class
    """
    entries_objectId = fields.Integer()
    entries_objectClass = fields.String()
    entries_entryDate = fields.DateTime()
    descriptor = fields.String()
    entries_id = fields.Integer()
    entries_newObject = fields.String(allow_none=True)
    representedClass = fields.String()
    entries_actorId = fields.Integer()
    entries_actor = fields.String()
    entries_changedFields = fields.String(allow_none=True)
    entries_operation = fields.String()
    entries_completeChanges = fields.String(allow_none=True)
    id = fields.Integer()
    entries_originalObject = fields.String(allow_none=True)

    @post_load
    def make_notification(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            Notification: Main class for this Schema
        """
        return Notification(**data)


class HistoryEntry:
    """
    Main class for history entries

    This contains information about an update of a Mitglied which is displayed
    on the |NAMI| dashbiard.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<{self.type}({self.entries_entryDate}: ' + \
               f'{self.entries_actor}: {self.entries_completeChanges})>'

    def __str__(self):
        return f'{self.entries_operation}'

    @property
    def type(self):
        return self.representedClass.split('.')[-1]


class HistoryEntrySchema(BaseSchema):
    """
    Schema class for the :class:`HistoryEntry` class
    """
    entries_objectId = fields.Integer()
    entries_objectClass = fields.String()
    entries_entryDate = fields.DateTime()
    descriptor = fields.String()
    entries_id = fields.Integer()
    entries_newObject = fields.String(allow_none=True)
    representedClass = fields.String()
    entries_actorId = fields.Integer()
    entries_actor = fields.String()
    entries_changedFields = fields.String(allow_none=True)
    entries_operation = fields.String()
    entries_gruppierung = fields.String()
    entries_completeChanges = fields.String(allow_none=True)
    id = fields.Integer()
    entries_author = fields.String()
    entries_originalObject = fields.String(allow_none=True)
    entries_mitglied = fields.String(allow_none=True)

    @post_load
    def make_historyEntry(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            HistoryEntry: Main class for this Schema
        """
        return HistoryEntry(**data)


class Stats:
    """
    Main class for basic statistical entries.

    The information in this class is displayed in the |NAMI| dashboard in a pie
    chart.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<Stats({self.nrMitglieder} Mitglieder)>'

    def __str__(self):
        return f'{self.nrMitglieder} Mitglieder'


class StatCategory:
    """
    Main class for statistical tier numbers.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<StatCategory({self.name}: {self.count})>'

    def __str__(self):
        return f'{self.name}: {self.count}'


class StatCatSchema(BaseSchema):
    """
    Schema class for the :class:`StatCategory` class.

    This only contains the name of the tier and its number of members.
    """
    name = fields.String()
    count = fields.Integer()

    @post_load
    def make_statCat(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            StatCategory: Main class for this Schema
        """
        return StatCategory(**data)


class StatsSchema(BaseSchema):
    """
    Schema class for the :class:`Stats` class
    """
    nrMitglieder = fields.Integer()
    statsCategories = fields.List(fields.Nested(StatCatSchema))

    @post_load
    def make_stats(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            Stats: Main class for this Schema
        """
        return Stats(**data)


class SearchActivity:
    """
    Main class for activities wich come up as a search result.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<SearchActivity({self.entries_taetigkeit}, Id: {self.id})>'

    def __str__(self):
        return f'{self.entries_taetigkeit}'


class SearchActivitySchema(BaseSchema):
    """
    Schema class for the :class:`SearchActivity` class
    """
    entries_aktivBis = fields.DateTime(allow_none=True)
    entries_beitragsArt = fields.String()
    entries_caeaGroup = fields.String()
    entries_aktivVon = fields.DateTime(allow_none=True)
    descriptor = fields.String()
    representedClass = fields.String()
    entries_anlagedatum = fields.DateTime(allow_none=True)
    entries_caeaGroupForGf = fields.String()
    entries_untergliederung = fields.String()
    entries_taetigkeit = fields.String()
    entries_gruppierung = fields.String()
    id = fields.Integer()
    entries_mitglied = fields.String()

    @post_load
    def make_activity(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            SearchActivity: Main class for this Schema
        """
        return SearchActivity(**data)


class Activity:
    """
    Main class for activities directly obtained by their id.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<Activity({self.taetigkeit} ({self.untergliederung}), ' + \
               f'Id: {self.id})>'

    def __str__(self):
        return f'{self.taetigkeit} ({self.untergliederung})'


class ActivitySchema(BaseSchema):
    """
    Schema class for the :class:`Activity` class
    """
    id = fields.Integer()
    gruppierung = fields.String()
    gruppierungId = fields.Integer()
    taetigkeit = fields.String()
    taetigkeitId = fields.Integer(load_only=True)
    caeaGroup = fields.String()
    caeaGroupId = fields.Integer()
    caeaGroupForGf = fields.String()
    caeaGroupForGfId = fields.Integer()
    untergliederung = fields.String()
    untergliederungId = fields.Integer(load_only=True)
    aktivVon = fields.DateTime()
    aktivBis = fields.DateTime(allow_none=True)
    beitragsArtId = fields.Integer(allow_none=True, dump_only=True)

    @post_load
    def make_activity(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            Activity: Main class for this Schema
        """
        return Activity(**data)


class SearchAusbildung:
    """
    Main class for a training obtained as a search result.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<SearchAusbildung({self.entries_baustein}, Id: {self.id})>'

    def __str__(self):
        return f'{self.descriptor}'


class SearchAusbildungSchema(BaseSchema):
    """
    Schema class for the :class:`SearchAusbildung` class
    """
    entries_vstgTag = fields.DateTime()
    entries_veranstalter = fields.String()
    entries_vstgName = fields.String()
    entries_baustein = fields.String()
    id = fields.Integer()
    descriptor = fields.String()
    entries_id = fields.Integer()
    representedClass = fields.String()
    entries_mitglied = fields.String()

    @post_load
    def make_ausbildung(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            SearchAusbildung: Main class for this Schema
        """
        return SearchAusbildung(**data)


class Ausbildung:
    """
    Main class for a training obtained directly from its id.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<Ausbildung({self.baustein}, Id: {self.id})>'

    def __str__(self):
        return f'{self.baustein}'


class AusbildungSchema(BaseSchema):
    """
    Schema class for the :class:`Ausbildung` class
    """
    id = fields.Integer()
    baustein = fields.String()
    bausteinId = fields.Integer()
    mitglied = fields.String()
    vstgTag = fields.DateTime()
    vstgName = fields.String()
    veranstalter = fields.String()
    lastModifiedFrom = fields.String(load_only=True)

    @post_load
    def make_ausbildung(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            Ausbildung: Main class for this Schema
        """
        return Ausbildung(**data)


class MitgliedHistory:
    """
    Main class for a member revision history entry obtained directly from its
    id.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<MitgliedJistory({self.actor}, Id: {self.id})>'

    def __str__(self):
        return f'{self.actor}: {self.operation}'


class MitgliedHistorySchema(BaseSchema):
    """
    Schema class for the :class:`MitgliedHistory` class
    """
    id = fields.Integer()
    entryDate = fields.DateTime()
    actor = fields.String()
    gruppierung = fields.String()
    operation = fields.String()
    changedFields = fields.String(allow_none=True)

    @post_load
    def make_history(self, data):
        """
        Converts to main class after loading by making use of the
        :func:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary

        Returns:
            MitgliedHistory: Main class for this Schema
        """
        return MitgliedHistory(**data)
