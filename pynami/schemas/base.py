# -*- coding: utf-8 -*-
"""
This module contains some base classes
"""
from marshmallow import Schema, pre_load, fields, post_load


class BaseModel:
    """
    Base class for all the main classes.
    
    It stores all data entries as instance attributes.
    """
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)


class BaseSchema(Schema):
    """
    Base class for all Schemas in this module

    It handles the formatting of dates so that the fields in the derived
    classes can be standard :class:`~marshmallow.fields.DateTime` field.
    
    Note:
        This class can not be used on its own but only as a derived class.
    """
    __model__ = None
    """class: Main class which this Schema is modelling. Each derived class
    must define this attribute."""

    class Meta:
        """
        This Base Meta class defines the default date and time format.
        """
        datetimeformat = '%Y-%m-%d %H:%M:%S'
        """str: Default |NAMI| datetime format"""
        dateformat = datetimeformat
        """str: Default |NAMI| datetime format"""

    @pre_load
    def correctEmptyDates(self, data, **kwargs):
        """
        Replace empty datetime strings with :data:`None`

        This method loops over all fields of the derived Schema class and
        where it finds a :class:`~marshmallow.fields.DateTime` field and an
        empty string in the data :obj:`dict` it replaces this value with
        :data:`None`.

        To achieve that this is applied before loading this method is decorated
        with :func:`~marshmallow.decorators.pre_load` decorator.

        Args:
            data (dict): Data dictionary which is about to be loaded

        Returns:
            dict: Adjusted data dictionary
        """
        for key in data.keys():
            if isinstance(self.__class__.__dict__['_declared_fields'][key],
                          fields.DateTime):
                if data[key] == '':
                    data[key] = None
        return data
    
    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


class BaseSearchSchema(BaseSchema):
    """
    Base class for all schemas that describe search results.
    
    All search results share the same three attributes.
    """
    
    id = fields.Raw()
    """:obj:`int` ore :obj:`str`: Internal id of the object This is an integer
    in most cases."""
    descriptor = fields.String()
    """str: Object description. In some cases the same as 
    :attr:`representedClass`."""
    representedClass = fields.String()
    """str: |NAMI| class structure"""