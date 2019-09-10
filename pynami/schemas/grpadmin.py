# -*- coding: utf-8 -*-
"""
This module contains classes for group admin (`Gruppierungsverwaltung`) stuff
"""
from marshmallow import fields, pre_load

from .base import BaseSchema, BaseModel
from ..util import extract_url


class SearchInvoice(BaseModel):
    """
    Repesents an invoice that came up as a search result

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<SearchInvoice({self.entries_displayName})>'

    def __str__(self):
        return f'{self.entries_displayName}'


class SearchInvoiceSchema(BaseSchema):
    """
    Schema class for the :class:`SearchInvoice` class
    """
    __model__ = SearchInvoice

    entries_rechnungsLauf = fields.Integer()
    descriptor = fields.String()
    entries_reCreated = fields.DateTime()
    representedClass = fields.String()
    entries_kontoOwnerId = fields.Integer()
    id = fields.Integer()
    entries_debitorType = fields.String()
    entries_reNr = fields.String()
    entries_freigabeDatum = fields.DateTime()
    entries_rechnungsEmpfaenger = fields.String()
    entries_fibuErloesKonto = fields.String()
    entries_status = fields.String()
    entries_debitorName = fields.String()
    entries_debitor = fields.String()
    entries_kontoOwnerTyp = fields.String()
    entries_kontoverbindung = fields.String()
    entries_debitorId = fields.Integer()
    entries_zahlungsEmpfaenger = fields.String()
    entries_reNetto = fields.String()
    entries_kreditor = fields.String()
    entries_reDatum = fields.DateTime()
    entries_einzugsDatum = fields.DateTime(allow_none=True)
    entries_displayName = fields.String()
    entries_erloesKtoName = fields.String()
    entries_debitor_document_id = fields.Integer()
    entries_reMwst = fields.String()
    entries_fibuDebitorKonto = fields.String()


class Invoice(BaseModel):
    """
    Repesents an invoice

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<Invoice({self.displayName})>'

    def __str__(self):
        return f'{self.displayName}'


class InvoiceSchema(BaseSchema):
    """
    Schema class for the :class:`Invoice` class
    """
    __model__ = Invoice

    id = fields.Integer()
    reDatum = fields.DateTime()
    reCreated = fields.DateTime()
    reNr = fields.String()
    status = fields.String()
    debitor = fields.String()
    freigabeDatum = fields.DateTime()
    debitor_document_id = fields.Integer()
    rechnungsLauf = fields.Integer()
    displayName = fields.String()
    debitorName = fields.String()
    einzugsDatum = fields.DateTime()
    zahlungsweise = fields.String()
    zahlungsweiseId = fields.String()
    pdf = fields.Url(relative=True)
    debitorKonto = fields.String()
    erloesKtoName = fields.String(allow_none=True)
    total = fields.String()
    currency = fields.String()

    @pre_load
    def get_download_url(self, data, **kwargs):
        """
        Extract the |HTML| enclosed |URL| string from the pdf download field

        Args:
            data (dict): Data dictionary

        Returns:
            dict: The updated data dictionary
        """
        data['pdf'] = extract_url(data['pdf'])
        return data

