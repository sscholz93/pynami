# -*- coding: utf-8 -*-
"""
Schemas for history entries
"""
from marshmallow import fields

from .base import BaseSchema, BaseSearchSchema, BaseModel


class HistoryEntry(BaseModel):
    """
    Main class for history entries

    This contains information about an update of a Mitglied which is displayed
    on the |NAMI| dashbiard.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<{self.type}({self.entries_entryDate}: ' + \
               f'{self.entries_actor}: {self.entries_completeChanges})>'

    def __str__(self):
        return f'{self.entries_operation}'

    @property
    def type(self):
        return self.representedClass.split('.')[-1]


class HistoryEntrySchema(BaseSearchSchema):
    """
    Schema class for the :class:`HistoryEntry` class
    """
    __model__ = HistoryEntry

    entries_objectId = fields.Integer()
    entries_objectClass = fields.String()
    entries_entryDate = fields.DateTime()
    entries_id = fields.Integer()
    entries_newObject = fields.String(allow_none=True)
    entries_actorId = fields.Integer()
    entries_actor = fields.String()
    entries_changedFields = fields.String(allow_none=True)
    entries_operation = fields.String()
    entries_gruppierung = fields.String()
    entries_completeChanges = fields.String(allow_none=True)
    entries_author = fields.String()
    entries_originalObject = fields.String(allow_none=True)
    entries_mitglied = fields.String(allow_none=True)


class MitgliedHistory(BaseModel):
    """
    Main class for a member revision history entry obtained directly from its
    id.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<MitgliedJistory({self.actor}, Id: {self.id})>'

    def __str__(self):
        return f'{self.actor}: {self.operation}'


class MitgliedHistorySchema(BaseSchema):
    """
    Schema class for the :class:`MitgliedHistory` class
    """
    __model__ = MitgliedHistory

    id = fields.Integer()
    entryDate = fields.DateTime()
    actor = fields.String()
    gruppierung = fields.String()
    operation = fields.String()
    changedFields = fields.String(allow_none=True)
