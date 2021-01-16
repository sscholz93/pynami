# -*- coding: utf-8 -*-
"""
Some utility functions that are used by other classes and methods from this #
package but not directly connected to the |NAMI|.
"""
import os
import time
import tempfile as tf
import subprocess as sp
from html.parser import HTMLParser
from tkinter.filedialog import asksaveasfilename
from tkinter import Tk
from marshmallow import ValidationError
from schwifty import IBAN


def validate_iban(value):
    """
    Validate an |IBAN|

    Args:
        value (str): Value to check. Spaces are allowed.

    Raises:
        ValidationError: In case of invalid |IBAN|.

    Returns:
        str: The |IBAN| in compact form.

    """
    try:
        if value != '':
            return IBAN(value).compact
        return value
    except ValueError as e:
        raise ValidationError(str(e))


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


def open_download_pdf(content, open_file=True, save_file=False, timeout=10,
                      filename=''):
    """
    Open and/or save a downloaded |PDF| file.

    When you only want to open the file: To avoid having to deal with graphical
    save-the-file dialogues a temporary file inside a temporary directory is
    created which is deleted after a timeout that is used to open the file.
    During this timeout the program is blocked.

    Args:
        content (bytes): Content of the downloaded file
        open_file (:obj:`bool`, optional): Wether to directly open the
            downloaded file. Defaults to :data:`True`.
        save_file (:obj:`bool`, optional): Wether to save the downloaded file
            to disc. Defaults to :data:`False`.
        timeout (:obj:`float`, optional): Time the system has for opening the
            file. Defaults to 10 seconds.
        filename (:obj:`str`, optional): Full path to save file
    """
    if save_file:
        if not filename:
            Tk().withdraw()
            filename = asksaveasfilename(filetypes=[('pdf files', '*.pdf')],
                                         initialdir = os.getcwd(),
                                         defaultextension=".pdf")
        if filename:
            with open(filename, 'wb') as f:
                f.write(content)
    if open_file:
        if save_file and filename:
            sp.Popen([filename], shell=True)
        else:
            with tf.TemporaryDirectory() as tmpdir:
                with tf.NamedTemporaryFile(suffix='.pdf', delete=False,
                                           dir=tmpdir) as tmpfile:
                    tmpfile.write(content)
                sp.Popen([tmpfile.name], shell=True)
                time.sleep(timeout)
