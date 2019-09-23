# -*- coding: utf-8 -*-
"""
Some utility functions for convenience
"""
import time
import webbrowser
import tempfile as tf
import subprocess as sp
from tabulate import tabulate
from html.parser import HTMLParser


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


class ExtractHrefParser(HTMLParser):
    """
    |HTML| parser for extracting a |URL|
    """
    url = None
    """str: |URL| embedded in |HTML| tags"""

    def handle_starttag(self, tag, attrs):
        """
        Handles a |HTML| tag

        Args:
            tag (str): The |HTML| tag
            attrs (list): Attributes inside the tag as name and value tuples
        """
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.url = value


def extract_url(htmlstr):
    """
    Extract a |URL| from a |HTML| string.

    Args:
        htmlstr (str): The |HTML| string which will be parsed.

    Returns:
        str: The |URL|
    """
    parser = ExtractHrefParser()
    parser.feed(htmlstr)
    return parser.url


def open_download_pdf(content, timeout=10):
    """
    Open a downloaded |PDF| file.

    To avoid having to deal with graphical save-the-file dialogues this creates
    a temporary file inside a temporary directory which is deleted after a
    timeout which is used to open the file. During this timeout the program is
    blocked.

    Args:
        content (bytes): Content of the downloaded file
        timeout (:obj:`float`, optional): Time the system has for opening the
            file. Defaults to 10 seconds.
    """
    with tf.TemporaryDirectory() as tmpdir:
        with tf.NamedTemporaryFile(suffix='.pdf', delete=False,
                                   dir=tmpdir) as tmpfile:
            tmpfile.write(content)
        sp.Popen([tmpfile.name], shell=True)
        time.sleep(timeout)


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
