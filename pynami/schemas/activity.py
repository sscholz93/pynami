# -*- coding: utf-8 -*-
"""
Schemas for activities
"""
from marshmallow import fields

from .base import BaseSchema, BaseSearchSchema, BaseModel


class SearchActivity(BaseModel):
    """
    Main class for activities wich come up as a search result.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<SearchActivity({self.entries_taetigkeit}, Id: {self.id})>'

    def __str__(self):
        return f'{self.entries_taetigkeit}'


class SearchActivitySchema(BaseSearchSchema):
    """
    Schema class for the :class:`SearchActivity` class
    """
    __model__ = SearchActivity

    entries_aktivBis = fields.DateTime(allow_none=True)
    """:class:`~datetime.datetime`: End date"""
    entries_beitragsArt = fields.String()
    """str: Fee type"""
    entries_caeaGroup = fields.String()
    """str: Access rights for the group"""
    entries_aktivVon = fields.DateTime(allow_none=True)
    """:class:`~datetime.datetime`: Start date"""
    entries_anlagedatum = fields.DateTime(allow_none=True)
    """:class:`~datetime.datetime`: Creation date"""
    entries_caeaGroupForGf = fields.String()
    """str: Access rights for sub group"""
    entries_untergliederung = fields.String()
    """str: Tier or group association"""
    entries_taetigkeit = fields.String()
    """str: Kind of activity"""
    entries_gruppierung = fields.String()
    """str: Group associated wiht the activity"""
    entries_mitglied = fields.String()
    """str: Member"""


class Activity(BaseModel):
    """
    Main class for activities directly obtained by their id.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
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
    aktivVon = fields.DateTime()
    """:class:`~datetime.datetime`: Start date"""
    aktivBis = fields.DateTime(allow_none=True)
    """:class:`~datetime.datetime`: End date"""
    beitragsArtId = fields.Integer(allow_none=True, dump_only=True)
    """int: Fee type"""
