Subdivision
===========

.. http:get:: /orgadmin/untergliederung
	
	Get default values and their ids.

	:query int gruppierung: A chosen group id (usually your Stammesnummer)
	:query int mitglied: Member id (not the |DPSG| Mitgliedsnummer)
	:query int page: The page number of result display
	:query int start: Show search results form this index
	:query int limit: Show only up to this many entries
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json int totalEntries: Number of returned entries
	:>json list data: The search results. Each returned subdivision is a list entry in the form of a json array.

		.. csv-table:: Subdivision types for searching (latest search results)
			:header: "Beschreibung", "ID"

			"AG Ausbildung",24
			"AG DPSG App",50
			"AG Freiwilligendienst",51
			"AG Friedenslicht",52
			"AG Geschlechtergerechtigkeit",53
			"AG Jahresaktion 2018 - Lebendig. Kraftvoll. Schärfer. Glaubste?",55
			"AG Jahresaktion 2019 - vollKostbar",54
			"AG Jahresaktion 2020 - No waste - ohne Wenn und Abfall",69
			"AG Jahresaktion 2021 - Pfadfinderinnen/Pfadfinder sind MITTENdrin",70
			"AG NaMi Community Management NCM",57
			"AG Netzwerk DPSG",56
			"AG Öffentlichkeitsarbeit",22
			"AG Ordnung",62
			"AG Pfingsten in Westernohe PIW",58
			"AG Politische Bildung",59
			"AG Satzungsfragen",31
			"AG Spiritualität",42
			"AG Transparente Finanzen",60
			"AG WBK-Rahmenkonzept",61
			"Archivbeirat",64
			"BDKJ",17
			"Biber",49
			"Bundesamt",38
			"Bundesebene",39
			"Elternbeirat",14
			"Entwicklungsfragen",6
			"Freunde und Förderer",35
			"Hauptausschuss",29
			"Inklusion",8
			"Interkulturelles Lernen",7
			"Internationale Gerechtigkeit",41
			"Internationales",21
			"Jugendhilfeausschuss",20
			"Jugendring",18
			"Jungpfadfinder",2
			"Kuratorium Westernohe",65
			"Landesstelle",37
			"MoViS - Beauftragte/Beauftragter für ehrenamtliches Engagement",71
			"Ökologie",26
			"Pfadfinder",3
			"PGR",19
			"RdP",16
			"Rechnungsprüfungsausschuss RPA",66
			"Rechtsträger",15
			"Rover",4
			"SG internationale Ausbildung",68
			"SG Nahost",67
			"Sonstige",48
			"Sonstige Mitarbeitende (mit Versicherungsschutz)",13
			"Sonstige Mitarbeitende (ohne Versicherungsschutz)",47
			"StG Deutsch-Französisch",40
			"Stiftung",36
			"Vorstand",5
			"Wahlausschuss",30
			"Westernohe",34
			"Wölfling",1

		.. seealso::

			:class:`~pynami.schemas.default.BaseadminSchema`
				|JSON| schema of the returned data

	:>json json metaData: Additional information about the data fields but not on the activities themselves.
	:status 200: No error
