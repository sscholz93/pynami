# -*- coding: utf-8 -*-
"""
Schema for default values
"""
from marshmallow import fields

from .base import BaseSearchSchema, BaseModel


class Baseadmin(BaseModel):
    """
    Base data class for all default values and their id mapping.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<{self.type}({self.descriptor}, Id: {self.id})>'

    def __str__(self):
        return f'{self.descriptor}'

    @property
    def type(self):
        """str: Last part of the |NAMI| class structure which is stored in the
        ``representedClass`` attribute for all the default values."""
        return self.representedClass.split(".")[-1]


class BaseadminSchema(BaseSearchSchema):
    """
    Schema class for the :class:`Baseadmin` class

    All the default values only consist of the same four attributes
    """
    __model__ = Baseadmin

    name = fields.String()
    """str: Name of this value. This will be empty in many cases."""
