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
    entries_fzNummer = fields.String()
    entries_empfaenger = fields.String()
    entries_empfNachname = fields.String()
    entries_empfVorname = fields.String()
    entries_empfGebDatum = fields.DateTime()
    entries_datumEinsicht = fields.DateTime(allow_none=True)
    entries_fzDatum = fields.DateTime()
    entries_autor = fields.String()


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
    fzDatum = fields.DateTime()
    fzNummer = fields.String()
    empfaenger = fields.String()
    erstelltAm = fields.DateTime()
    autor = fields.String()
    download = fields.Url(relative=True)
    datumEinsicht = fields.DateTime(allow_none=True)

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

