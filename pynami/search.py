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
    """
    vorname = fields.String()
    """str: First Name"""
    funktion = fields.String()
    """str: Unused tag"""
    organisation = fields.String()
    """str"""
    nachname = fields.String()
    """str"""
    alterVon = fields.String()
    """str"""
    alterBis = fields.String()
    """str"""
    mglWohnort = fields.String()
    """str"""
    mitgliedsNummer = fields.String(data_key='mitgliedsNummber')
    """str"""
    mglStatusId = fields.String(allow_none=True, default=None)
    """str"""
    mglTypeId = fields.List(fields.String)
    """:obj:`list` of :obj:`str`"""
    tagId = fields.List(fields.Integer)
    """:obj:`list` of :obj:`int`"""
    bausteinIncludeId = fields.List(fields.Integer)
    """:obj:`list` of :obj:`int`"""
    spitzname = fields.String()
    """str"""
    zeitschriftenversand = fields.Boolean()
    """bool"""
    gruppierung4Id = fields.Integer(allow_none=True, default=None)
    """int"""
    gruppierung5Id = fields.Integer(allow_none=True, default=None)
    """int"""
    gruppierung6Id = fields.Integer(allow_none=True, default=None)
    """int"""
    privacy = fields.String()
    """str"""
    searchName = fields.String()
    """str"""
    untergliederungId = fields.List(fields.Integer)
    """int"""
    taetigkeitId = fields.List(fields.Integer)
    """:obj:`list` of :obj:`int`"""
    mitAllenTaetigkeiten = fields.Boolean(default=False)
    """bool"""
    withEndedTaetigkeiten = fields.Boolean(default=False)
    """bool"""

    # This group and the following are mutually exclusive
    ebeneId = fields.Integer(allow_none=True, default=None)
    """int"""
    grpNummer = fields.String()
    """str"""
    grpName = fields.String()
    """str"""

    gruppierung1Id = fields.Integer(allow_none=True, default=None)
    """int"""
    gruppierung2Id = fields.Integer(allow_none=True, default=None)
    """int"""
    gruppierung3Id = fields.Integer(allow_none=True, default=None)
    """int"""
    inGrp = fields.Boolean(default=False)
    """bool"""
    unterhalbGrp = fields.Boolean(default=False)
    """bool"""

    searchType = fields.String(default='MITGLIEDER')
    """str"""

    class Meta(BaseSchema.Meta):
        ordered = True
        """bool: All attributes shall be dumped in code order"""

    @pre_dump
    def get_missing(self, data):
        """
        Check for missspelled or incorrect data

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
            clsdict[key]
        return data