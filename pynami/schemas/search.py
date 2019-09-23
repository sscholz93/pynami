# -*- coding: utf-8 -*-
"""
This module contains the classes for a search for members
"""
from marshmallow import fields, pre_dump

from .base import BaseSchema


class SearchSchema(BaseSchema):
    """
    Base class for search parameters

    You could just use :func:`json.dumps` on a dictionary to create the search
    string but this would bypass all the type and spell checking.

    This also takes care of the miss-spelled search key ``'mitgliedsNummber'``
    so that the user of this |API| can use the correct spelling.

    Example:
        .. code-block:: python
            :caption: Generate the search string

            from pynami.search import SearchSchema

            searchKeys = {'vorname': 'Max',
                          'nachname': 'Mustermann'}
            searchedValues = SearchSchema().dumps(searchKeys,
                                                  separators=(',', ':'))
            print(searchedValues)

        .. code-block:: python
            :caption: Make direct use of the search keys by searching for all
                      Wölflinge and Jungpfadfinder

            from pynami.tools import tabulate2x
            from pynami.nami import NaMi

            with NaMi(username='MITGLIEDSNUMMER', password='PASSWORD') as nami:
                searchResults = nami.search(untergliederungId=[1,2])
                print(tabulate2x(searchResults))

    """
    vorname = fields.String()
    """str: First Name"""
    funktion = fields.String()
    """str: Unused tag"""
    organisation = fields.String()
    """str: Unused tag"""
    nachname = fields.String()
    """str: Surname"""
    alterVon = fields.String()
    """str: Minimal age"""
    alterBis = fields.String()
    """str: Maximal age"""
    mglWohnort = fields.String()
    """str: City"""
    mitgliedsNummer = fields.String(data_key='mitgliedsNummber')
    """str: The |DPSG| id"""
    mglStatusId = fields.String(allow_none=True, default=None)
    """str: If the member is active"""
    mglTypeId = fields.List(fields.String)
    """:obj:`list` of :obj:`str`: Kind of membership"""
    tagId = fields.List(fields.Integer)
    """:obj:`list` of :obj:`int`: Kinds of fees"""
    bausteinIncludeId = fields.List(fields.Integer)
    """:obj:`list` of :obj:`int`: Possible completed trainings"""
    spitzname = fields.String()
    """str: Nickname"""
    zeitschriftenversand = fields.Boolean()
    """bool: If the member gets the |DPSG| newpaper"""
    gruppierung4Id = fields.Integer(allow_none=True, default=None)
    """int: Unused"""
    gruppierung5Id = fields.Integer(allow_none=True, default=None)
    """int: Unused"""
    gruppierung6Id = fields.Integer(allow_none=True, default=None)
    """int: Unused"""
    privacy = fields.String()
    """str: Unused"""
    searchName = fields.String()
    """str: Unused"""
    untergliederungId = fields.List(fields.Integer)
    """int: Tiers in which the members are active"""
    taetigkeitId = fields.List(fields.Integer)
    """:obj:`list` of :obj:`int`: List of activities the mambers are comitted
    to"""
    mitAllenTaetigkeiten = fields.Boolean(default=False)
    """bool: Whether to search in all active activities"""
    withEndedTaetigkeiten = fields.Boolean(default=False)
    """bool: Whether to search also in activities that have already ended"""

    # This group and the following are mutually exclusive
    ebeneId = fields.Integer(allow_none=True, default=None)
    """int: Represents a |DPSG| structural level"""
    grpNummer = fields.String()
    """str: Group id"""
    grpName = fields.String()
    """str: Group name"""

    gruppierung1Id = fields.Integer(allow_none=True, default=None)
    """int: Group id of a Diözese"""
    gruppierung2Id = fields.Integer(allow_none=True, default=None)
    """int: Group id of a Bezirk"""
    gruppierung3Id = fields.Integer(allow_none=True, default=None)
    """int: Group id of a Stamm"""
    inGrp = fields.Boolean(default=False)
    """bool: Whether to search in the group"""
    unterhalbGrp = fields.Boolean(default=False)
    """bool: Whether to search in subgroups"""

    searchType = fields.String(default='MITGLIEDER')
    """str: Default search type. Not even strictly neccessary."""

    class Meta(BaseSchema.Meta):
        """
        Extended :class:`marshmallow.Schema.Meta` class for further
        configuration
        """

        ordered = True
        """bool: All attributes shall be dumped in code order"""

    @pre_dump
    def correct_spelling(self, data, **kwargs):
        """
        Check for missspelled or incorrect data before dumping. Realized by the
        :func:`~marshmallow.decorators.pre_dump` decorator.

        Args:
            data (dict): Data set to be dumped

        Returns:
            dict: Corrected data

        Raises:
            KeyError: When there is a search key that is not an attribute of
                this class
        """
        if 'mitgliedsNummber' in data:
            data['mitgliedsNummer'] = data.pop('mitgliedsNummber')
        clsdict = self.__class__.__dict__['_declared_fields']
        for key in data.keys():
            if isinstance(clsdict[key], fields.List):
                if not isinstance(data[key], list):
                    data[key] = [data[key]]
        return data