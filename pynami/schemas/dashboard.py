# -*- coding: utf-8 -*-
"""
Schemas for dashboard functionalities
"""
from marshmallow import fields

from .base import BaseSchema, BaseSearchSchema, BaseModel


class Notification(BaseModel):
    """
    Main class for notification like tier changes of a mitglied.

    In the |NAMI| the notifications are displayed in the dashboard.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    _tabkeys = ['entryDate', 'operation']

    def __repr__(self):
        return f'<Notification({self.entryDate}: ' + \
               f'{self.operation})>'

    def __str__(self):
        return f'{self.operation}'


class NotificationSchema(BaseSearchSchema):
    """
    Schema class for the :class:`Notification` class
    """
    __model__ = Notification

    entries_objectId = fields.Integer(attribute='objectId')
    """int: Object id"""
    entries_objectClass = fields.String(attribute='objectClass')
    """str: |NAMI| class"""
    entries_entryDate = fields.DateTime(attribute='entryDate')
    """:class:`~datetime.datetime`: Date of the event"""
    entries_id = fields.Integer(attribute='id_')
    """int: Id of the event"""
    entries_newObject = fields.String(allow_none=True, attribute='newObject')
    """str: New object"""
    entries_actorId = fields.Integer(attribute='actorId')
    """int: Id of the person who started the event"""
    entries_actor = fields.String(attribute='actor')
    """str: The person who started the event"""
    entries_changedFields = fields.String(allow_none=True,
                                          attribute='changedFields')
    """str: Which fields have been changed. This may be empty."""
    entries_operation = fields.String(attribute='operation')
    """str: The nature of the change"""
    entries_completeChanges = fields.String(allow_none=True,
                                            attribute='completeChanges')
    """str: More details about the changes. This may be empty."""
    entries_originalObject = fields.String(allow_none=True,
                                           attribute='originalObject')
    """str: Old object. This may be empty"""


class Stats(BaseModel):
    """
    Main class for basic statistical entries.

    The information in this class is displayed in the |NAMI| dashboard in a pie
    chart.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<Stats({self.nrMitglieder} Mitglieder)>'

    def __str__(self):
        return f'{self.nrMitglieder} Mitglieder'


class StatCategory(BaseModel):
    """
    Main class for statistical tier numbers.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<StatCategory({self.name}: {self.count})>'

    def __str__(self):
        return f'{self.name}: {self.count}'


class StatCatSchema(BaseSchema):
    """
    Schema class for the :class:`StatCategory` class.

    This only contains the name of the tier and its number of members.
    """
    __model__ = StatCategory

    name = fields.String()
    """str: Name of the tier/group"""
    count = fields.Integer()
    """int: Number of members in the group"""


class StatsSchema(BaseSchema):
    """
    Schema class for the :class:`Stats` class
    """
    __model__ = Stats

    nrMitglieder = fields.Integer()
    """int: Total number of members in the group"""
    statsCategories = fields.List(fields.Nested(StatCatSchema))
    """:obj:`list` of :class:`StatCategory`: Detailed information on the
    partitions"""
