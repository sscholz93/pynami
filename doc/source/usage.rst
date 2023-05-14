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

Search for a group of members
-----------------------------

.. code-block:: python
    :caption: Search for all Jungpfadfinder and Pfadfinder

    search = {
        'mglStatusId': 'AKTIV',
        'mglTypeId': 'MITGLIED',
        'untergliederungId': [2, 3],
        'taetigkeitId': 1
    }
    result = nami.search(**search)
    print(tabulate2x(result))

Send emails
-----------

.. code-block:: python
    :caption: Send emails to the members of the search result

    from pynami.tools import send_emails

    send_emails(result)

Export data
-----------

There are two functions for exporting data. The first is to export the data as a |CSV| formatted string and save that as a file using the method :meth:`~pynami.tools.make_csv`.

.. code-block:: python
    :caption: Export basic member data to a csv file

    from pynami.tools import make_csv

    keys = ['mitgliedsNummer', 'vorname', 'nachname', 'geschlecht', 'geburtsDatum']
    with open('data.csv', 'w', newline='', encoding='utf-8-sig') as f:
        f.writelines(make_csv(result, keys, delimiter=';'))

Another option is to export the data as an Excel file using the function :meth:`~pynami.tools.export_xlsx` which comes already with a possible write to file functionality.

.. code-block:: python
    :caption: Export basic member data to an Excel file

    from pynami.tools import export_xlsx

    export_xlsx(result, keys, write_to_file=True, filepath='data.xlsx')
