Search Mitglieder
=================
.. currentmodule:: pynami.schemas.search

For validation of the search parameters the following class is used:

.. autoclass:: SearchSchema

Search Keys
-----------

.. autoinstanceattribute:: SearchSchema.vorname
    :annotation:
.. autoinstanceattribute:: SearchSchema.funktion
    :annotation:
.. autoinstanceattribute:: SearchSchema.organisation
    :annotation:
.. autoinstanceattribute:: SearchSchema.nachname
    :annotation:
.. autoinstanceattribute:: SearchSchema.alterVon
    :annotation:
.. autoinstanceattribute:: SearchSchema.alterBis
    :annotation:
.. autoinstanceattribute:: SearchSchema.mglWohnort
    :annotation:
.. autoinstanceattribute:: SearchSchema.mitgliedsNummer
    :annotation:
.. autoinstanceattribute:: SearchSchema.mglStatusId
    :annotation:
.. autoinstanceattribute:: SearchSchema.mglTypeId
    :annotation:
.. autoinstanceattribute:: SearchSchema.tagId
    :annotation:
.. autoinstanceattribute:: SearchSchema.bausteinIncludeId
    :annotation:
.. autoinstanceattribute:: SearchSchema.spitzname
    :annotation:
.. autoinstanceattribute:: SearchSchema.zeitschriftenversand
    :annotation:
.. autoinstanceattribute:: SearchSchema.untergliederungId
    :annotation:
.. autoinstanceattribute:: SearchSchema.taetigkeitId
    :annotation:
.. autoinstanceattribute:: SearchSchema.mitAllenTaetigkeiten
    :annotation:
.. autoinstanceattribute:: SearchSchema.withEndedTaetigkeiten
    :annotation:

Restrict search to some group or level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are two way to search only in a specified group or level which are mutually exclusive:

1. Choose the level and specify the group id and/or the group name
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

   .. autoinstanceattribute:: SearchSchema.ebeneId
       :annotation:
   .. autoinstanceattribute:: SearchSchema.grpNummer
       :annotation:
   .. autoinstanceattribute:: SearchSchema.grpName
       :annotation:

2. Choose group ids from different levels from a automated list
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

   .. autoinstanceattribute:: SearchSchema.gruppierung1Id
       :annotation:
   .. autoinstanceattribute:: SearchSchema.gruppierung2Id
       :annotation:
   .. autoinstanceattribute:: SearchSchema.gruppierung3Id
       :annotation:
   .. autoinstanceattribute:: SearchSchema.inGrp
       :annotation:
   .. autoinstanceattribute:: SearchSchema.unterhalbGrp
       :annotation:

Unused search keys
^^^^^^^^^^^^^^^^^^
.. autoinstanceattribute:: SearchSchema.gruppierung4Id
    :annotation:
.. autoinstanceattribute:: SearchSchema.gruppierung5Id
    :annotation:
.. autoinstanceattribute:: SearchSchema.gruppierung6Id
    :annotation:
.. autoinstanceattribute:: SearchSchema.privacy
    :annotation:
.. autoinstanceattribute:: SearchSchema.searchName
    :annotation:
.. autoinstanceattribute:: SearchSchema.searchType
    :annotation: = 'MITGLIEDER'
