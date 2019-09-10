# -*- coding: utf-8 -*-
"""
This module contains classes to handle stuff with the certificates of good
conduct.
"""
from marshmallow import fields, pre_load

from .base import BaseSchema, BaseSearchSchema, BaseModel
from ..util import extract_url


class SearchBescheinigung(BaseModel):
    """
    Base data class for a certificate about the inspection of a certificate of
    goos conduct that came up as a search result.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<{self.representedClass.split(".")[-1]}' + \
               f'({self.descriptor}, Id: {self.id})>'

    def __str__(self):
        return f'{self.descriptor}'


class SearchBescheinigungSchema(BaseSearchSchema):
    """
    Schema class for the :class:`SearchBescheinigung` class
    """
    __model__ = SearchBescheinigung

    entries_erstelltAm = fields.DateTime()
    """:class:`~datetime.datetime`: Entry creation date"""
    entries_fzNummer = fields.String()
    """str: Number of the |CGC|"""
    entries_empfaenger = fields.String()
    """str: Receiver"""
    entries_empfNachname = fields.String()
    """str: Surname"""
    entries_empfVorname = fields.String()
    """str: First name"""
    entries_empfGebDatum = fields.DateTime()
    """:class:`~datetime.datetime`: Birth date"""
    entries_datumEinsicht = fields.DateTime(allow_none=True)
    """:class:`~datetime.datetime`: Inspection date. May be empty."""
    entries_fzDatum = fields.DateTime()
    """:class:`~datetime.datetime`: Date of the |CGC|"""
    entries_autor = fields.String()
    """str: Person who did the inspection"""


class Bescheinigung(BaseModel):
    """
    Base data class for a certificate about the inspection of a certificate of
    goos conduct.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<Bescheinigung(FZ-Nr.: {self.fzNummer}, Id: {self.id})>'

    def __str__(self):
        return f'{self.fzNummer}'


class BescheinigungSchema(BaseSchema):
    """
    Schema class for the :class:`Bescheinigung` class
    """
    __model__ = Bescheinigung

    id = fields.Integer()
    """int: Id of this certificate"""
    fzDatum = fields.DateTime()
    """:class:`~datetime.datetime`: Date of the |CGC|"""
    fzNummer = fields.String()
    """str: Number of the |CGC|"""
    empfaenger = fields.String()
    """str: Receiver"""
    erstelltAm = fields.DateTime()
    """:class:`~datetime.datetime`: Entry creation date"""
    autor = fields.String()
    """str: Person who did the inspection"""
    download = fields.Url(relative=True)
    """str: Relative download |URL|"""
    datumEinsicht = fields.DateTime(allow_none=True)
    """:class:`~datetime.datetime`: Inspection date. May be empty."""

    @pre_load
    def get_download_url(self, data, **kwargs):
        """
        Extract the |HTML| enclosed |URL| string from the pdf download field

        Args:
            data (dict): Data dictionary

        Returns:
            dict: The updated data dictionary
        """
        data['download'] = extract_url(data['download'])
        return data

