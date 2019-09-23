# -*- coding: utf-8 -*-
"""
This module contains classes for group admin (`Gruppierungsverwaltung`) stuff
"""
from marshmallow import fields, pre_load

from .base import BaseSchema, BaseModel, BaseSearchSchema, BaseSearchModel
from ..util import extract_url


class SearchInvoice(BaseSearchModel):
    """
    Repesents an invoice that came up as a search result

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<SearchInvoice({self.entries_displayName})>'

    def __str__(self):
        return f'{self.entries_displayName}'


class SearchInvoiceSchema(BaseSearchSchema):
    """
    Schema class for the :class:`SearchInvoice` class
    """
    __model__ = SearchInvoice

    entries_rechnungsLauf = fields.Integer()
    """int: Internal invoice number"""
    entries_reCreated = fields.DateTime()
    """:class:`~datetime.datetime`: Creation date of the invoice"""
    entries_kontoOwnerId = fields.Integer()
    """int: Id of the account owner"""
    entries_debitorType = fields.String()
    """str: |NAMI| class"""
    entries_reNr = fields.String()
    """str: Official invoice number"""
    entries_freigabeDatum = fields.DateTime()
    """:class:`~datetime.datetime`: """
    entries_rechnungsEmpfaenger = fields.String()
    """str: Recipient"""
    entries_fibuErloesKonto = fields.String()
    """str: This my be empty"""
    entries_status = fields.String()
    """str: If the invoice has been released"""
    entries_debitorName = fields.String()
    """str: Debitor, e.g. a group"""
    entries_debitor = fields.String()
    """str: Id of the debitor"""
    entries_kontoOwnerTyp = fields.String()
    """str: |NAMI| class"""
    entries_kontoverbindung = fields.String()
    """str: Account details"""
    entries_debitorId = fields.Integer()
    """int: e.g. a group id"""
    entries_zahlungsEmpfaenger = fields.String()
    """str: Recipient of the payment"""
    entries_reNetto = fields.String()
    """str: Netto amount including currency"""
    entries_kreditor = fields.String()
    """str: May be empty"""
    entries_reDatum = fields.DateTime()
    """:class:`~datetime.datetime`: Date of the invoice"""
    entries_einzugsDatum = fields.DateTime(allow_none=True)
    """:class:`~datetime.datetime`: Date of money collection"""
    entries_displayName = fields.String()
    """str: Human-readable string describing the invoice"""
    entries_erloesKtoName = fields.String()
    """str: This may be empty"""
    entries_debitor_document_id = fields.Integer()
    """int: Some other internal id"""
    entries_reMwst = fields.String()
    """str: |VAT| amount including currency"""
    entries_fibuDebitorKonto = fields.String()
    """str: Some account id"""


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
    """int: |NAMI| id"""
    reDatum = fields.DateTime()
    """:class:`~datetime.datetime`: Date of the invoice"""
    reCreated = fields.DateTime()
    """:class:`~datetime.datetime`: Creation date of the invoice"""
    reNr = fields.String()
    """str: Official invoice number"""
    status = fields.String()
    """str: If the invoice has been released"""
    debitor = fields.String()
    """str: Id of the debitor"""
    freigabeDatum = fields.DateTime()
    """:class:`~datetime.datetime`: When the invoice was released"""
    debitor_document_id = fields.Integer()
    """int: Some other internal id"""
    rechnungsLauf = fields.Integer()
    """int: Internal invoice number"""
    displayName = fields.String()
    """str: Human-readable string describing the invoice"""
    debitorName = fields.String()
    """str: Debitor, e.g. a group"""
    einzugsDatum = fields.DateTime()
    """:class:`~datetime.datetime`: Date of money collection"""
    zahlungsweise = fields.String()
    """str: Way of payment (e.g. ``'Lastschrift'``)"""
    zahlungsweiseId = fields.String()
    """str: Id of the way of payment (e.g. ``'LASTSCHRIFT'``)"""
    pdf = fields.Url(relative=True)
    """str: Relative download |URL|"""
    debitorKonto = fields.String()
    """str: Some account id"""
    erloesKtoName = fields.String(allow_none=True)
    """str: This may be empty"""
    total = fields.String()
    """str: Total amount"""
    currency = fields.String()
    """str: Currency (e.g. ``'EUR'``)"""

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

