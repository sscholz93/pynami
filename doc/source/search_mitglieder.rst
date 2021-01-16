Search Mitglieder
=================
.. currentmodule:: pynami.schemas.search

For validation of the search parameters the following class is used:

.. autoclass:: SearchSchema

Search Keys
-----------

.. autoattribute:: SearchSchema.vorname
    :annotation:
.. autoattribute:: SearchSchema.funktion
    :annotation:
.. autoattribute:: SearchSchema.organisation
    :annotation:
.. autoattribute:: SearchSchema.nachname
    :annotation:
.. autoattribute:: SearchSchema.alterVon
    :annotation:
.. autoattribute:: SearchSchema.alterBis
    :annotation:
.. autoattribute:: SearchSchema.mglWohnort
    :annotation:
.. autoattribute:: SearchSchema.mitgliedsNummer
    :annotation:
.. autoattribute:: SearchSchema.mglStatusId
    :annotation:
.. autoattribute:: SearchSchema.mglTypeId
    :annotation:
.. autoattribute:: SearchSchema.tagId
    :annotation:
.. autoattribute:: SearchSchema.bausteinIncludeId
    :annotation:
.. autoattribute:: SearchSchema.spitzname
    :annotation:
.. autoattribute:: SearchSchema.zeitschriftenversand
    :annotation:
.. autoattribute:: SearchSchema.untergliederungId
    :annotation:
.. autoattribute:: SearchSchema.taetigkeitId
    :annotation:
.. autoattribute:: SearchSchema.mitAllenTaetigkeiten
    :annotation:
.. autoattribute:: SearchSchema.withEndedTaetigkeiten
    :annotation:

Restrict search to some group or level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are two way to search only in a specified group or level which are mutually exclusive:

1. Choose the level and specify the group id and/or the group name
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

   .. autoattribute:: SearchSchema.ebeneId
       :annotation:
   .. autoattribute:: SearchSchema.grpNummer
       :annotation:
   .. autoattribute:: SearchSchema.grpName
       :annotation:

2. Choose group ids from different levels from a automated list
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

   .. autoattribute:: SearchSchema.gruppierung1Id
       :annotation:
   .. autoattribute:: SearchSchema.gruppierung2Id
       :annotation:
   .. autoattribute:: SearchSchema.gruppierung3Id
       :annotation:
   .. autoattribute:: SearchSchema.inGrp
       :annotation:
   .. autoattribute:: SearchSchema.unterhalbGrp
       :annotation:

Unused search keys
^^^^^^^^^^^^^^^^^^
.. autoattribute:: SearchSchema.gruppierung4Id
    :annotation:
.. autoattribute:: SearchSchema.gruppierung5Id
    :annotation:
.. autoattribute:: SearchSchema.gruppierung6Id
    :annotation:
.. autoattribute:: SearchSchema.privacy
    :annotation:
.. autoattribute:: SearchSchema.searchName
    :annotation:
.. autoattribute:: SearchSchema.searchType
    :annotation: = 'MITGLIEDER'
