Activity types
==============

.. http:get:: /nami/search-multi/all-visible-taetigkeiten
	
	Get default values and their ids.

	:query int gruppierung: A chosen group id (usually your Stammesnummer)
	:query int mitglied: Member id (not the |DPSG| Mitgliedsnummer)
	:query int page: The page number of result display
	:query int start: Show search results form this index
	:query int limit: Show only up to this many entries
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json int totalEntries: Number of returned entries
	:>json list data: The search results. Each returned activity is a list entry in the form of a json array.

		.. csv-table:: All activity types for searching
			:file: activities.csv
			:header-rows: 1

		.. seealso::
			:attr:`~pynami.nami.NaMi.activities`
		.. seealso::
			:class:`~pynami.schemas.default.BaseadminSchema`
				|JSON| schema of the returned data

	:>json json metaData: Additional information about the data fields but not on the activities themselves.
	:status 200: No error
