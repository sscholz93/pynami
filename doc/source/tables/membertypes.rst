Member types and states
=======================

Member types
------------

.. http:get:: /nami/enum/mgltype
	
	Get default values and their ids.

	:query int gruppierung: A chosen group id (usually your Stammesnummer) (optional)
	:query int mitglied: Member id (not the |DPSG| Mitgliedsnummer) (optional)
	:query int page: The page number of result display
	:query int start: Show search results form this index
	:query int limit: Show only up to this many entries
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json int totalEntries: Number of returned entries
	:>json list data: The search results. Each returned member type is a list entry in the form of a json array.

		.. csv-table:: Latest search results
			:file: mgltypes.csv
			:header-rows: 1

		.. seealso::
			:meth:`~pynami.nami.NaMi.mgltypes`
		.. seealso::
			:class:`~pynami.schemas.default.BaseadminSchema`
				|JSON| schema of the returned data

	:status 200: No error


Member states
-------------

.. http:get:: /nami/search-multi/status-list
	
	Get default values and their ids.

	:query int page: The page number of result display
	:query int start: Show search results form this index
	:query int limit: Show only up to this many entries
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json int totalEntries: Number of returned entries
	:>json list data: The search results. Each returned member state is a list entry in the form of a json array.

		.. csv-table:: Latest search results
			:file: status_list.csv
			:header-rows: 1

		.. seealso::
			:attr:`~pynami.nami.NaMi.status_list`
		.. seealso::
			:class:`~pynami.schemas.default.BaseadminSchema`
				|JSON| schema of the returned data

	:status 200: No error
