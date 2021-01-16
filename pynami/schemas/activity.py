# -*- coding: utf-8 -*-
"""
Schemas for activities
"""
from marshmallow import fields

from .base import BaseSchema, BaseSearchSchema, BaseModel, BaseSearchModel


class SearchActivity(BaseSearchModel):
    """
    Main class for activities wich come up as a search result.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    _tabkeys = ['id', 'taetigkeit', 'untergliederung', 'aktivVon', 'aktivBis']

    def __repr__(self):
        return f'<SearchActivity({self.taetigkeit} ' + \
            '({self.untergliederung}), Id: {self.id})>'

    def __str__(self):
        return f'{self.taetigkeit} ({self.untergliederung})'

    def get_activity(self, nami, mglId):
        """
        Create a real :class:`Activity` form the search result by getting the
        corresponding data set through the activity id.

        Args:
            nami (:class:`~pynami.nami.NaMi`): Main |NAMI| class
            mglId (int): Member id (not |DPSG| Mitgliedsnummer)

        Returns:
            Activity: The activity object corresponding to this search result.
        """
        return nami.get_activity(mglId, self.id)


class SearchActivitySchema(BaseSearchSchema):
    """
    Schema class for the :class:`SearchActivity` class
    """
    __model__ = SearchActivity

    entries_aktivBis = fields.Date(allow_none=True, attribute='aktivBis')
    """:class:`~datetime.datetime`: End date"""
    entries_beitragsArt = fields.String(attribute='beitragsArt')
    """str: Fee type"""
    entries_caeaGroup = fields.String(attribute='caeaGroup')
    """str: Access rights for the group"""
    entries_aktivVon = fields.Date(allow_none=True, attribute='aktivVon')
    """:class:`~datetime.datetime`: Start date"""
    entries_anlagedatum = fields.DateTime(allow_none=True,
                                          attribute='anlageDatum')
    """:class:`~datetime.datetime`: Creation date"""
    entries_caeaGroupForGf = fields.String(attribute='caeaGroupForGf')
    """str: Access rights for sub group"""
    entries_untergliederung = fields.String(attribute='untergliederung')
    """str: Tier or group association"""
    entries_taetigkeit = fields.String(attribute='taetigkeit')
    """str: Kind of activity"""
    entries_gruppierung = fields.String(attribute='gruppierung')
    """str: Group associated wiht the activity"""
    entries_mitglied = fields.String(attribute='mitglied')
    """str: Member"""


class Activity(BaseModel):
    """
    Main class for activities directly obtained by their id.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    _tabkeys = ['id', 'taetigkeit', 'aktivVon', 'aktivBis']

    def __repr__(self):
        return f'<Activity({self.taetigkeit} ({self.untergliederung}), ' + \
               f'Id: {self.id})>'

    def __str__(self):
        return f'{self.taetigkeit} ({self.untergliederung})'


class ActivitySchema(BaseSchema):
    """
    Schema class for the :class:`Activity` class
    """
    __model__ = Activity

    id = fields.Integer()
    """int: Id"""
    gruppierung = fields.String()
    """str: Group associated wiht the activity"""
    gruppierungId = fields.Integer()
    """int: Group id"""
    taetigkeit = fields.String()
    """str: Kind of activity"""
    taetigkeitId = fields.Integer(load_only=True)
    """int: Activity id"""
    caeaGroup = fields.String()
    """str: Access rights for the group"""
    caeaGroupId = fields.Integer()
    """int: Access right id"""
    caeaGroupForGf = fields.String()
    """str: Access rights for sub group"""
    caeaGroupForGfId = fields.Integer()
    """int: Access right id"""
    untergliederung = fields.String()
    """str: Tier or group association"""
    untergliederungId = fields.Integer(load_only=True)
    """int: tier or sub group id"""
    aktivVon = fields.Date()
    """:class:`~datetime.datetime`: Start date"""
    aktivBis = fields.Date(allow_none=True)
    """:class:`~datetime.datetime`: End date"""
    beitragsArtId = fields.Integer(allow_none=True, dump_only=True)
    """int: Fee type"""
