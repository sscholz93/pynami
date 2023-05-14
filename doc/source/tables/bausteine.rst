DPSG Bausteine
==============

.. http:get:: /module/baustein
	
	Get default values and their ids.

	:query int gruppierung: A chosen group id (usually your Stammesnummer) (optional)
	:query int mitglied: Member id (not the |DPSG| Mitgliedsnummer) (optional)
	:query int page: The page number of result display
	:query int start: Show search results form this index
	:query int limit: Show only up to this many entries
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json int totalEntries: Number of returned entries
	:>json list data: The search results. Each returned baustein is a list entry in the form of a json array.

		.. csv-table:: Baustein tags (latest search results)
			:file: bausteine.csv
			:header-rows: 1

		.. seealso::
			:attr:`~pynami.nami.NaMi.bausteine`
		.. seealso::
			:class:`~pynami.schemas.default.BaseadminSchema`
				|JSON| schema of the returned data

	:>json json metaData: Additional information about the data fields but not on the data itself.
	:status 200: No error


