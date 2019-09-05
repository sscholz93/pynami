# -*- coding: utf-8 -*-
"""
Some utility functions for convenience
"""
import webbrowser


def send_emails(to, mitglieder, method='bcc', email1=True, email2=True):
    """
    Send emails to several members.

    Args:
        to (str): Must be a valid email address for the primary recipient
        mitglieder (list): The List contents can be either
            :class:`~pynami.schemas.SearchMitglied` or
            :class:`~pynami.schemas.Mitglied`
        method (:obj:`str`, optional): If you want to send your mails as bcc
            or something else. Currently only bcc is supported.
        email1 (:obj:`bool`, optional): If emails should be send to the
            primary address of the members.
        email2 (:obj:`bool`, optional): If emails should be send to the email
            account of the member's parent.

    Returns:
        str: The mailto link
    """
    recipients = []
    if email1:
        recipients.append([mgl.email for mgl in mitglieder])
    if email2:
        recipients.append([mgl.emailVertretungsberechtigter
                           for mgl in mitglieder])
    bcc = ','.join(recipients)
    url = 'mailto:' + to + '?bcc=' + bcc
    webbrowser.open(url, new=1)
    return url
