# -*- coding: utf-8 -*-
"""
Some utility functions for user convenience
"""
# Standard library imports
import io
import csv
import webbrowser

# Third party imports
from tabulate import tabulate


def send_emails(mitglieder, to='', method='bcc', email1=True, email2=True,
                open_browser=True):
    """
    Send emails to several members.

    Args:
        mitglieder (list): The List contents can be either
            :class:`~pynami.schemas.SearchMitglied` or
            :class:`~pynami.schemas.Mitglied`
        to (:obj:`str`, optional): Primary recipient
        method (:obj:`str`, optional): If you want to send your mails as bcc
            or something else. Currently only bcc is supported.
        email1 (:obj:`bool`, optional): If emails should be send to the
            primary address of the members.
        email2 (:obj:`bool`, optional): If emails should be send to the email
            account of the member's parent.
        open_browser (:obj:`bool`, optional): If :data:`True` the link is
            opened directly by the system. On a computer this may open your
            default mail program.

    Returns:
        str: The mailto link
    """
    recipients = []
    if email1:
        recipients += [mgl.email for mgl in mitglieder if mgl.email]
    if email2:
        recipients += [mgl.emailVertretungsberechtigter for mgl in mitglieder
                       if mgl.emailVertretungsberechtigter]
    url = f"mailto:{to}?{method}={','.join(set(recipients))}"
    if open_browser:
        webbrowser.open(url, new=1)
    return url


def tabulate2x(objs, elements=None):
    """
    Tabulate a list of objects by tabulating each object first

    Args:
        obj (list): The list of objects to tabulate. If they are not from the
        same class this may not work.
        elements (:obj:`list` of :obj:`str`, optional): List of keys which
            should be displayed

    Returns:
        str: Nicely formatted tabulated output
    """
    return tabulate([x.tabulate(elements=elements) for x in objs],
                    headers='keys')


def make_csv(data, attrs=None, includeheader=True):
    """
    Makes a |CSV| formatted string from a data set

    Args:
        data (list): Data objects. They should all belong to the same class.
        attrs (:obj:`list`, optional): Attribute names for the |CSV| table. If
            left empty (:data:`None`) the value of the first
            :attr:`.base.BaseModel._tabkeys` attribute in the list is taken.
        includeheader (:obj:`bool`, optional): Whether to include headers in
            the output. Defaults to :data:`True`.

    Returns:
        str: |CSV| formatted data
    """
    if not data:
        return ''
    if not attrs:
        attrs = data[0]._tabkeys
    data = [x.tabulate(attrs) for x in data]
    output = io.StringIO()
    w = csv.DictWriter(output, attrs, quoting=csv.QUOTE_NONNUMERIC)
    if includeheader:
        w.writeheader()
    w.writerows(data)
    return output.getvalue()
