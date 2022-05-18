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
    _tabkeys = ['id', 'reNr', 'reDatum', 'reNetto']

    def __repr__(self):
        return f'<SearchInvoice({self.displayName})>'

    def __str__(self):
        return f'{self.displayName}'

    def get_invoice(self, nami, grpId=None):
        """
        Create a real :class:`Invoice` form the search result by getting the
        corresponding data set through the training id.

        Args:
            nami (:class:`~pynami.nami.NaMi`): Main |NAMI| class
            grpId (:obj:`str`, optional): |DPSG| Group id. Defaults to group
                id of the user

        Returns:
            Invoice: The invoice object corresponding to this search
            result.
        """
        if not grpId:
            grpId = nami.grpId
        return nami.invoice(grpId, self.id)

    def download(self, nami, **kwargs):
        """
        Download this invoice as |PDF|

        Args:
            nami (:class:`~pynami.nami.NaMi`): Main |NAMI| class
            **kwargs: See :meth:`~pynami.util.open_download_pdf`.

        Returns:
            :data:`None`

        """
        nami.download_invoice(self.id, **kwargs)


class SearchInvoiceSchema(BaseSearchSchema):
    """
    Schema class for the :class:`SearchInvoice` class
    """
    __model__ = SearchInvoice

    entries_rechnungsLauf = fields.Integer(attribute='rechnungsverlauf')
    """int: Internal invoice number"""
    entries_reCreated = fields.DateTime(attribute='reCreated')
    """:class:`~datetime.datetime`: Creation date of the invoice"""
    entries_kontoOwnerId = fields.Integer(attribute='kontoOwnerId')
    """int: Id of the account owner"""
    entries_debitorType = fields.String(attribute='debitorType')
    """str: |NAMI| class"""
    entries_reNr = fields.String(attribute='reNr')
    """str: Official invoice number"""
    entries_freigabeDatum = fields.DateTime(attribute='freigabeDatum')
    """:class:`~datetime.datetime`: """
    entries_rechnungsEmpfaenger = \
        fields.String(attribute='rechnungsEmpfaenger')
    """str: Recipient"""
    entries_fibuErloesKonto = fields.String(attribute='fibuErloesKonto')
    """str: This my be empty"""
    entries_status = fields.String(attribute='status')
    """str: If the invoice has been released"""
    entries_debitorName = fields.String(attribute='debitorName')
    """str: Debitor, e.g. a group"""
    entries_debitor = fields.String(attribute='debitor')
    """str: Id of the debitor"""
    entries_kontoOwnerTyp = fields.String(attribute='kontoOwnerTyp')
    """str: |NAMI| class"""
    entries_kontoverbindung = fields.String(attribute='kontoverbindung')
    """str: Account details"""
    entries_debitorId = fields.Integer(attribute='debitorId')
    """int: e.g. a group id"""
    entries_zahlungsEmpfaenger = fields.String(attribute='zahlungsEmpfaenger')
    """str: Recipient of the payment"""
    entries_reNetto = fields.String(attribute='reNetto')
    """str: Netto amount including currency"""
    entries_kreditor = fields.String(attribute='kreditor')
    """str: May be empty"""
    entries_reDatum = fields.Date(attribute='reDatum')
    """:class:`~datetime.datetime`: Date of the invoice"""
    entries_einzugsDatum = fields.Date(allow_none=True,
                                       attribute='einzugsDatum')
    """:class:`~datetime.datetime`: Date of money collection"""
    entries_displayName = fields.String(attribute='displayName')
    """str: Human-readable string describing the invoice"""
    entries_erloesKtoName = fields.String(attribute='erloesKtoName')
    """str: This may be empty"""
    entries_debitor_document_id = \
        fields.Integer(attribute='debitor_document_id')
    """int: Some other internal id"""
    entries_reMwst = fields.String(attribute='reMwst')
    """str: |VAT| amount including currency"""
    entries_fibuDebitorKonto = fields.String(attribute='fibuDebitorKonto')
    """str: Some account id"""


class Invoice(BaseModel):
    """
    Repesents an invoice

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    _tabkeys = ['id', 'reNr', 'reDatum', 'total']

    def __repr__(self):
        return f'<Invoice({self.displayName})>'

    def __str__(self):
        return f'{self.displayName}'

    def download(self, nami, **kwargs):
        """
        Download this invoice as |PDF|

        Args:
            nami (:class:`~pynami.nami.NaMi`): Main |NAMI| class
            **kwargs: See :meth:`~pynami.util.open_download_pdf`.

        Returns:
            :data:`None`

        """
        nami.download_invoice(self.id, **kwargs)


class InvoiceSchema(BaseSchema):
    """
    Schema class for the :class:`Invoice` class
    """
    __model__ = Invoice

    id = fields.Integer()
    """int: |NAMI| id"""
    reDatum = fields.Date()
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
    einzugsDatum = fields.Date(allow_none=True)
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
