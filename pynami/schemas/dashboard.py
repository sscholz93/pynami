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
    def __repr__(self):
        return f'<Notification({self.entries_entryDate}: ' + \
               f'{self.entries_operation})>'

    def __str__(self):
        return f'{self.entries_operation}'


class NotificationSchema(BaseSearchSchema):
    """
    Schema class for the :class:`Notification` class
    """
    __model__ = Notification

    entries_objectId = fields.Integer()
    entries_objectClass = fields.String()
    entries_entryDate = fields.DateTime()
    entries_id = fields.Integer()
    entries_newObject = fields.String(allow_none=True)
    entries_actorId = fields.Integer()
    entries_actor = fields.String()
    entries_changedFields = fields.String(allow_none=True)
    entries_operation = fields.String()
    entries_completeChanges = fields.String(allow_none=True)
    entries_originalObject = fields.String(allow_none=True)


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
    count = fields.Integer()


class StatsSchema(BaseSchema):
    """
    Schema class for the :class:`Stats` class
    """
    __model__ = Stats
    nrMitglieder = fields.Integer()
    statsCategories = fields.List(fields.Nested(StatCatSchema))
