# -*- coding: utf-8 -*-
"""
Schemas for tags
"""
from marshmallow import fields

from .base import BaseModel, BaseSearchSchema, BaseSchema, BaseSearchModel


class Tag(BaseModel):
    """
    Base data class for a tag

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<Tag({self.tag}, Id: {self.id})>'

    def __str__(self):
        return f'{self.tag}'


class TagSchema(BaseSchema):
    """
    Schema class for the :class:`Tag` class
    """
    __model__ = Tag

    id = fields.Integer()
    """int: Id of this tag"""
    tag = fields.String()
    """str: Actual value of the tag"""
    tagId = fields.Integer()
    """int: Same as :attr:`id`"""
    mitglied = fields.String()
    """str: Surname and first name of the member this tag belongs to"""
    mitgliedId = fields.Integer()
    """int: Member id (not |DPSG| Mitgliedsnummer)"""


class SearchTag(BaseSearchModel):
    """
    Base data class for a tag that came up as a search result.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    pass


class SearchTagSchema(BaseSearchSchema):
    """
    Schema class for the :class:`SearchBescheinigung` class
    """
    __model__ = SearchTag

    entries_tag = fields.String(attribute='tag')
    """str: Actual value of the tag"""
    entries_identitaet = fields.String(attribute='identitaet')
    """str: Identity of the member with the |DPSG| Mitgliedsnummer"""
