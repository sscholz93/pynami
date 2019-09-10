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
    """int: Object id (not the |NAMI| id for addressing the entry)"""
    entries_objectClass = fields.String()
    """str: |NAMI| class"""
    entries_entryDate = fields.DateTime()
    """:class:`~datetime.datetime`: Date of the event"""
    entries_id = fields.Integer()
    """int: |NAMI| id"""
    entries_newObject = fields.String(allow_none=True)
    """str: Updated object ('e.g. a Mitglied)"""
    entries_actorId = fields.Integer()
    """int: Id of the person who created the change"""
    entries_actor = fields.String()
    """str: Name of the person who created the change including the id"""
    entries_changedFields = fields.String(allow_none=True)
    """str: Which fields have been changed. This may be empty."""
    entries_operation = fields.String()
    """str: What kind of action has been done."""
    entries_gruppierung = fields.String()
    """str: Group name including its id"""
    entries_completeChanges = fields.String(allow_none=True)
    """str: More details about the changes. This may be empty."""
    entries_author = fields.String()
    """str: Who did this"""
    entries_originalObject = fields.String(allow_none=True)
    """str: The object before the change. This may be empty for a
    ``GruppierungsHistoryEntry``."""
    entries_mitglied = fields.String(allow_none=True)
    """str: Almost the same as :attr:`entries_author`"""


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
    """int: |NAMI| id"""
    entryDate = fields.DateTime()
    """:class:`~datetime.datetime`: Date of the event"""
    actor = fields.String()
    """str: Name of the person who created the change including the id"""
    gruppierung = fields.String()
    """str: Group name including its id"""
    operation = fields.String()
    """str: What kind of action has been done."""
    changedFields = fields.String(allow_none=True)
    """str: Which fields have been changed. This may be empty."""
