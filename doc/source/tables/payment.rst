Payment details
===============

Member management
-----------------

.. csv-table:: Payment methods
	:file: zahlungskonditionen.csv
	:header-rows: 1

.. seealso:: Here
	:meth:`~pynami.nami.NaMi.zahlungskonditionen`

.. csv-table:: Fee types
	:file: beitragsarten_mgl.csv
	:header-rows: 1

.. seealso::
	:meth:`~pynami.nami.NaMi.beitragsarten_mgl`

The following table can be obtained with a different function and is given here for the sake of completeness.

.. csv-table:: Fee types (Yes, the same ones)
	:file: beitragsarten.csv
	:header-rows: 1

.. seealso::
	:meth:`~pynami.nami.NaMi.beitragsarten`

.. seealso::
	:ref:`urls:Default values`
		How to get these values

Ids for searching
-----------------

.. deprecated:: 0.3.3

	No longer in use. You will just get an empty list.

.. http:get:: //tagging/getTagList
	
	Get default values and their ids.

	:query int page: The page number of result display
	:query int start: Show search results form this index
	:query int limit: Show only up to this many entries
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json int totalEntries: Number of returned entries
	:>json list data: The search results. Each returned tag is a list entry in the form of a json array.

		.. seealso::

			:class:`~pynami.schemas.default.BaseadminSchema`
				|JSON| schema of the returned data

	:status 200: No error

.. seealso::
	:meth:`~pynami.nami.NaMi.tagList`