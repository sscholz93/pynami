# -*- coding: utf-8 -*-
"""
Some utility functions for convenience
"""
import time
import webbrowser
import tempfile as tf
import subprocess as sp
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
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.url = value


def extract_url(htmlstr):
    """
    Extract a |URL| from a |HTML| string
    """
    parser = ExtractHrefParser()
    parser.feed(htmlstr)
    return parser.url

def open_download_pdf(content):
    with tf.TemporaryDirectory() as tmpdir:
        with tf.NamedTemporaryFile(suffix='.pdf', delete=False,
                                   dir=tmpdir) as tmpfile:
            tmpfile.write(content)
        sp.Popen([tmpfile.name], shell=True)
        time.sleep(10)