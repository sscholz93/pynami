Usage
=====

The package should be quite comfortable to use without loosing flexibility.

Authentification
----------------

.. code-block:: python
    :caption: Make use of :std:ref:`the with statement <with>` for automatic login and logout

    from pynami.nami import NaMi

    with NaMi(username='MITGLIEDSNUMMER', password='PASSWORD') as nami:
        pass
    
.. code-block:: python
    :caption: Authentificate manually

    from pynami.nami import NaMi

    nami = NaMi()
    nami.auth(username='MITGLIEDSNUMMER', password='PASSWORD')
    # do stuff
    nami.logout()

Access default values
---------------------

.. code-block:: python
    :caption: Get gender names and their internal ids

    from pynami.tools import tabulate2x

    print(tabulate2x(nami.geschlechter()))

Get a specific mitglied
-----------------------

.. code-block:: python
    :caption: Get a mitglied and view its Mitgliedsnummer

    id_ = nami.search(vorname='Max', nachname='Mustermann')[0].id
    mgl = nami.mitglied(id_)
    print(mgl.mitgliedsNummer)