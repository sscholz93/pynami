# -*- coding: utf-8 -*-
"""
Schemas for trainings
"""
from marshmallow import fields

from .base import BaseSchema, BaseSearchSchema, BaseModel, BaseSearchModel


class SearchAusbildung(BaseSearchModel):
    """
    Main class for a training obtained as a search result.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    _tabkeys = ['id', 'vstgTag', 'baustein']

    def __repr__(self):
        return f'<SearchAusbildung({self.baustein}, Id: {self.id})>'


class SearchAusbildungSchema(BaseSearchSchema):
    """
    Schema class for the :class:`SearchAusbildung` class
    """
    __model__ = SearchAusbildung

    entries_vstgTag = fields.DateTime(attribute='vstgTag')
    """:class:`~datetime.datetime`: Day of the training event"""
    entries_veranstalter = fields.String(attribute='veranstalter')
    """str: Who organized the event (e.g. a `Bezirk`)"""
    entries_vstgName = fields.String(attribute='vstgName')
    """str: Name of the event"""
    entries_baustein = fields.String(attribute='baustein')
    """str: Name of the training (e.g. ``'Baustein 3a'``)"""
    entries_id = fields.Integer(attribute='id_')
    """int: |NAMI| id of this training entry"""
    entries_mitglied = fields.String(attribute='mitglied')
    """str: Who absolved the training"""


class Ausbildung(BaseModel):
    """
    Main class for a training obtained directly from its id.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<Ausbildung({self.baustein}, Id: {self.id})>'

    def __str__(self):
        return f'{self.baustein}'


class AusbildungSchema(BaseSchema):
    """
    Schema class for the :class:`Ausbildung` class
    """
    __model__ = Ausbildung

    id = fields.Integer()
    """int: |NAMI| id"""
    baustein = fields.String()
    """str: Name of the training (e.g. ``'Baustein 3a'``)"""
    bausteinId = fields.Integer()
    """int: Id of the training"""
    mitglied = fields.String()
    """str: Who absolved the training"""
    vstgTag = fields.DateTime()
    """:class:`~datetime.datetime`: Day of the training event"""
    vstgName = fields.String()
    """str: Name of the event"""
    veranstalter = fields.String()
    """str: Who organized the event (e.g. a `Bezirk`)"""
    lastModifiedFrom = fields.String(load_only=True)
    """str: Who did the last change to this entry"""
