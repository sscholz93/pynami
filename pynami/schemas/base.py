# -*- coding: utf-8 -*-
"""
This module contains some base classes
"""
from collections import OrderedDict
from marshmallow import Schema, pre_load, fields, post_load

from ..util import validate_iban


class AccessError(AttributeError):
    pass


class BaseModel:
    """
    Base class for all the main classes.

    It stores all data entries as instance attributes.
    """
    _tabkeys = []
    """:obj:`list` of :obj:`str`: Default attributes names for tabulating and
    data export. This attribute is inherited and adapted to all Schema
    classes from :class:`~pynami.schemas.base.BaseModel`."""
    _field_blacklist = []
    """list: Attribute names which are to be skipped while preparing tabulated
    output"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getstate__(self):
        """
        Enable saving data through pickling

        Returns:
            dict: Returns the :obj:`~object.__dict__` attribute of the class.

        """
        return vars(self)

    def __setstate__(self, state):
        """
        Enable loading data with the :mod:`pickle` module

        Args:
            state (dict): Loaded data.

        Returns:
            :data:`None`

        """
        vars(self).update(state)

    def __setattr__(self, name, value):
        """
        Set certain fields to read-only

        Args:
            name (str): Attribute name.
            value: New value.

        Raises:
            AccessError: In case of invalid write access.

        Returns:
            :data:`None`

        """
        if name in ['id', 'id_'] and hasattr(self, name) \
            and getattr(self, name) is not None:
            raise AccessError('Id cannot be modified!')
        elif name == 'iban':
            value = validate_iban(value)
        super().__setattr__(name, value)

    def table_view(self, field_blacklist=None):
        """
        Prepare nicely formatted output

        Args:
            field_blacklist (:obj:`list` of :obj:`str`, optional): List of
                attributes to be skipped

        Returns:
            dict: All data entries which are not in the blacklist
        """
        return {k: v for k, v in vars(self).items() if v is not None
                and v != '' and k not in (self._field_blacklist if not
                field_blacklist else field_blacklist)}

    def tabulate(self, elements=None):
        """
        Prepare ordered tabulated output

        Args:
            elements (:obj:`list` of :obj:`str`, optional): List of keys which
                shall be included in the table

        Returns:
            :class:`~collections.OrderedDict`: Specified data entries
        """
        d = OrderedDict()
        for k in self._tabkeys if not elements else elements:
            d[k] = getattr(self, k)
        return d


class BaseSearchModel(BaseModel):
    """
    Base class for all classes that are loaded from a :class:`BaseSearchSchema`
    """
    _tabkeys = ['id', 'descriptor']

    def __repr__(self):
        return f'<{self.type}({self.descriptor}, Id: {self.id})>'

    def __str__(self):
        return f'{self.descriptor}'

    @property
    def type(self):
        """str: |NAMI| class without the hierarchy"""
        return self.representedClass.split(".")[-1]


class BaseSchema(Schema):
    """
    Base class for all Schemas in this module

    It handles the formatting of dates so that the fields in the derived
    classes can be standard :class:`~marshmallow.fields.DateTime` field.

    Note:
        This class can not be used on its own but only as a derived class.
    """
    __model__ = BaseModel
    """:std:term:`class`: Main class which this Schema is modelling. Each
    derived class must define this attribute."""

    class Meta:
        """
        This Base Meta class defines the default date and time format.
        """
        datetimeformat = '%Y-%m-%d %H:%M:%S'
        """str: Default |NAMI| datetime format"""
        dateformat = '%Y-%m-%d %H:%M:%S'
        """str: Default |NAMI| date format. Note that in most cases the time
        part is only zeroes. However it can happen that the incoming value has
        time information as well."""

    @pre_load
    def correctEmptySTrings(self, data, **kwargs):
        """
        Replace empty strings with :data:`None`

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
                          (fields.DateTime, fields.Date, fields.Email)):
                if data[key] == '':
                    data[key] = None
        return data

    @post_load
    def make_object(self, data, **kwargs):
        """
        Create the object associated with this Schema by making use of the
        :meth:`~marshmallow.decorators.post_load` decorator.

        Args:
            data (dict): Data dictionary containing all keywords and their
                values
            **kwargs: Possible keyword arguments passed through to this method
                during the loading procedure.

        Returns:
            :std:term:`class`: Main class correspoding to this Schema
        """
        return self.__model__(**data)


class BaseSearchSchema(BaseSchema):
    """
    Base class for all schemas that describe search results.

    All search results share the same three attributes.
    """
    __model__ = BaseSearchModel

    id = fields.Raw()
    """:obj:`int` ore :obj:`str`: Internal id of the object This is an integer
    in most cases."""
    descriptor = fields.String()
    """str: Object description. In some cases the same as
    :attr:`representedClass`."""
    representedClass = fields.String()
    """str: |NAMI| class structure"""
