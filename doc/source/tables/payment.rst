Payment details
===============

Member management
-----------------

.. csv-table:: Payment method
	:header: "Beschreibung", "ID"

	"Std Lastschrift",1
	"Std Überweisung",2

.. csv-table:: Fee type
	:header: "Beschreibung", "ID"

	"DPSG Bundesverband 000000 (Familienermäßigt - Stiftungseuro - VERBANDSBEITRAG)",5
	"DPSG Bundesverband 000000 (Familienermäßigt - VERBANDSBEITRAG)",2
	"DPSG Bundesverband 000000 (Sozialermäßigt - Stiftungseuro - VERBANDSBEITRAG)",6
	"DPSG Bundesverband 000000 (Sozialermäßigt - VERBANDSBEITRAG)",3
	"DPSG Bundesverband 000000 (Übernahme - VERBANDSBEITRAG)",7
	"DPSG Bundesverband 000000 (Voller Beitrag - Stiftungseuro - VERBANDSBEITRAG)",4
	"DPSG Bundesverband 000000 (Voller Beitrag - VERBANDSBEITRAG)",1

.. seealso::

	:ref:`urls:Default values`
		How to get these values

Ids for searching
-----------------

.. http:get:: //tagging/getTagList
	
	Get default values and their ids.

	:query int page: The page number of result display
	:query int start: Show search results form this index
	:query int limit: Show only up to this many entries
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json int totalEntries: Number of returned entries
	:>json list data: The search results. Each returned tag is a list entry in the form of a json array.

		.. csv-table:: Tag list of fee types
			:header: "Beschreibung", "ID"

			"Familienbeitrag - 30",1158
			"Förderbeitrag - 20",1159
			"Halbjahr - 30",1161
			"Jahresbeitrag - 60",1157
			"Rechnung - 30",1223
			"Rechnung - 60",1162
			"Sonderbeitrag",1160

		.. seealso::

			:class:`~pynami.schemas.default.BaseadminSchema`
				|JSON| schema of the returned data

	:status 200: No error

