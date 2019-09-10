# -*- coding: utf-8 -*-
"""
Schemas for trainings
"""
from marshmallow import fields

from .base import BaseSchema, BaseSearchSchema, BaseModel


class SearchAusbildung(BaseModel):
    """
    Main class for a training obtained as a search result.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<SearchAusbildung({self.entries_baustein}, Id: {self.id})>'

    def __str__(self):
        return f'{self.descriptor}'


class SearchAusbildungSchema(BaseSearchSchema):
    """
    Schema class for the :class:`SearchAusbildung` class
    """
    __model__ = SearchAusbildung

    entries_vstgTag = fields.DateTime()
    entries_veranstalter = fields.String()
    entries_vstgName = fields.String()
    entries_baustein = fields.String()
    entries_id = fields.Integer()
    entries_mitglied = fields.String()


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
    baustein = fields.String()
    bausteinId = fields.Integer()
    mitglied = fields.String()
    vstgTag = fields.DateTime()
    vstgName = fields.String()
    veranstalter = fields.String()
    lastModifiedFrom = fields.String(load_only=True)
