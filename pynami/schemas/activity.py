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
    entries_beitragsArt = fields.String()
    entries_caeaGroup = fields.String()
    entries_aktivVon = fields.DateTime(allow_none=True)
    entries_anlagedatum = fields.DateTime(allow_none=True)
    entries_caeaGroupForGf = fields.String()
    entries_untergliederung = fields.String()
    entries_taetigkeit = fields.String()
    entries_gruppierung = fields.String()
    entries_mitglied = fields.String()


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
