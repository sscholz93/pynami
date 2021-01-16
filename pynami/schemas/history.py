# -*- coding: utf-8 -*-
"""
Schemas for history entries
"""
from marshmallow import fields

from .base import BaseSchema, BaseSearchSchema, BaseModel, BaseSearchModel


class HistoryEntry(BaseSearchModel):
    """
    Main class for history entries

    This contains information about an update of a Mitglied which is displayed
    on the |NAMI| dashbiard.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    _tabkeys = ['id', 'entryDate', 'actor', 'operation', 'changedFields']

    def __repr__(self):
        return f'<{self.type}({self.entryDate}: ' + \
               f'{self.actor}: {self.completeChanges})>'

    def __str__(self):
        return f'{self.operation}'

    def get_history(self, nami, mglId, ext=True):
        """
        Create a real :class:`MitgliedHistory` form the search result by
        getting the corresponding data set through the history entry id.

        Args:
            nami (:class:`~pynami.nami.NaMi`): Main |NAMI| class
            mglId (int): Member id (not |DPSG| Mitgliedsnummer)
            ext (:obj:`bool`, optional): If the extended history format should
                be used. Defaults to :data:`True`.

        Returns:
            MitgliedHistory: The activity object corresponding to this search
            result.
        """
        return nami.get_mgl_history(mglId, self.id, ext)


class HistoryEntrySchema(BaseSearchSchema):
    """
    Schema class for the :class:`HistoryEntry` class
    """
    __model__ = HistoryEntry

    entries_objectId = fields.Integer(attribute='objectId')
    """int: Object id (not the |NAMI| id for addressing the entry)"""
    entries_objectClass = fields.String(attribute='objectClass')
    """str: |NAMI| class"""
    entries_entryDate = fields.DateTime(attribute='entryDate')
    """:class:`~datetime.datetime`: Date of the event"""
    entries_id = fields.Integer(attribute='id_')
    """int: |NAMI| id"""
    entries_newObject = fields.String(allow_none=True, attribute='newObject')
    """str: Updated object ('e.g. a Mitglied)"""
    entries_actorId = fields.Integer(attribute='actorId')
    """int: Id of the person who created the change"""
    entries_actor = fields.String(attribute='actor')
    """str: Name of the person who created the change including the id"""
    entries_changedFields = fields.String(allow_none=True,
                                          attribute='changedFields')
    """str: Which fields have been changed. This may be empty."""
    entries_operation = fields.String(attribute='operation')
    """str: What kind of action has been done."""
    entries_gruppierung = fields.String(attribute='gruppierung')
    """str: Group name including its id"""
    entries_completeChanges = fields.String(allow_none=True,
                                            attribute='completeChanges')
    """str: More details about the changes. This may be empty."""
    entries_author = fields.String(attribute='author')
    """str: Who did this"""
    entries_originalObject = fields.String(allow_none=True,
                                           attribute='originalObject')
    """str: The object before the change. This may be empty for a
    ``GruppierungsHistoryEntry``."""
    entries_mitglied = fields.String(allow_none=True, attribute='mitglied')
    """str: Almost the same as :attr:`entries_author`"""


class MitgliedHistory(BaseModel):
    """
    Main class for a member revision history entry obtained directly from its
    id.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    _tabkeys = ['id', 'entryDate', 'actor', 'operation', 'changedFields']

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
