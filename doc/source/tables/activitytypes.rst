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
			:header: "Beschreibung", "ID"

			"Mitgliederservice",42
			"Erstelllen von SGBVIII Bescheinigungen",43
			"Datenschutzerklärung EAs abgegeben",45
			"Präventionsschulung EAs",46
			"soz. erm. Beiträge zuweisen",47
			"€ Helfer AK/AG/StG/SG",48
			"€ Mitglied",1
			"€ AdministratorIn",14
			"€ Mitglied AK/AG/StG/SG",18
			"€ passive Mitgliedschaft",39
			"Beitragsabrechnung",36
			"€ BeobachterIn",8
			"€ Delegierte(r)",7
			"\- ElternvertreterIn",4
			"EmpfängerIn Freiexemplar",37
			"Empfänger Freiexemplare",28
			"€ Ersatzdelegierte(r)",31
			"€ GeschäftsführerIn",19
			"\- hauptberufliche Mitarbeiter",22
			"€ KassenprüferIn",21
			"€ KassiererIn",20
			"KontakterIn",32
			"€ KuratIn",11
			"€ LeiterIn",6
			"€ Leitungsteam-SprecherIn",5
			"€ MaterialwartIn",23
			"sonst. MitarbeiterIn",16
			"Ref. Ersatzdelegierte(r)",30
			"Ref.-Delegierte(r)",25
			"€ ReferentIn",10
			"€ SprecherIn",2
			"stellv. Vorsitzende(r)",26
			"stellvertr. Mitglied",34
			"Stufendelegierte(r)",33
			"Versandanschrift",29
			"\- VertreterIn (BDKJ/RDP etc.)",24
			"€ Vorsitzende(r)",13
			"€ sonst. MitarbeiterIn (mit Versicherungsschutz)",40
			"\- sonst. MitarbeiterIn (ohne Versicherungsschutz)",41
			"Stammessuche",44
			"Schnuppermitgliedschaft",35

		.. seealso::

			:class:`~pynami.schemas.default.BaseadminSchema`
				|JSON| schema of the returned data

	:>json json metaData: Additional information about the data fields but not on the activities themselves.
	:status 200: No error
