# -*- coding: utf-8 -*-
"""
Some utility functions that are used by other classes and methods from this #
package but not directly connected to the |NAMI|.
"""
import time
import tempfile as tf
import subprocess as sp
from html.parser import HTMLParser


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
