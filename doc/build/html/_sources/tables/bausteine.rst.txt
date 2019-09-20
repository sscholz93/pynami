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
			:header: "Beschreibung", "ID"

			"Schritt 1 - Motivation und Grundlagen zum Leiten, Ausbildung in der DPSG",21
			"Schritt 2 - Gestaltung und Organisation von Gruppenstunden",22
			"Baustein 1a - Identität und Leitungsstil",3
			"Baustein 1b - Teamarbeit",4
			"Baustein 1c - Gesellschaftliches Engagement",5
			"Baustein 1d (Bis 2016 3d) - Spiritualität",14
			"Baustein 2a - Lebenswelt von Kindern und Jugendlichen, Pädagogik der DPSG",6
			"Baustein 2b - Mädchen und Jungen, Geschlechtsbewusste Gruppenarbeit",7
			"Baustein 2c - Pfadfinderische Grundlagen: Pfadfinderische Methodik",8
			"Baustein 2d - Gewalt gegen Kinder und Jugendliche: Sensibilisierung, Intervention",9
			"Baustein 2e - Gewalt gegen Kinder und Jugendliche: Vertiefung, Prävention",10
			"Baustein 3a - Pfadfinderische Grundlagen: Geschichte und Hintergründe",11
			"Baustein 3b - Erste Hilfe",12
			"Baustein 3c - Finanzen, Haftung und Versicherung",13
			"Baustein 3e - Pfadfindertechniken",1
			"Baustein 3f - Planung und Durchführung von Maßnahmen",2
			"Abgeschlossene Modulausbildung - oder Woodbadge-Kurs I",25
			"Woodbadge-Kurs oder Woodbadge-Kurs II - Wölflinge",17
			"Woodbadge-Kurs oder Woodbadge-Kurs II - Jungpfadfinder",18
			"Woodbadge-Kurs oder Woodbadge-Kurs II - Pfadfinder",19
			"Woodbadge-Kurs oder Woodbadge-Kurs II - Rover",20
			"Woodbadge-Kurs oder Woodbadge-Kurs II - Vorstände",23
			"Modulleitungstraining (MLT) - Modulleitungstraining (MLT)",26
			"Teamer Training I (TT I) - Wölflinge",27
			"Teamer Training I (TT I) - Jungpfadfinder",29
			"Teamer Training I (TT I) - Pfadfinder",30
			"Teamer Training I (TT I) - Rover",31
			"Teamer Training I (TT I) - Vorstände",32
			"Teamer Training II (TT II) - Wölflinge",33
			"Teamer Training II (TT II) - Jungpfadfinder",28
			"Teamer Training II (TT II) - Pfadfinder",34
			"Teamer Training II (TT II) - Rover",35
			"Teamer Training II (TT II) - Vorstände",36
			"Assistant Leadertrainer Training (ALT) - Assistant Leadertrainer Training (ALT)",24
			"Kuratenausbildung - Ausbildung der Kuratinnen und Kuraten",37

		.. seealso::

			:class:`~pynami.schemas.default.BaseadminSchema`
				|JSON| schema of the returned data

	:>json json metaData: Additional information about the data fields but not on the data itself.
	:status 200: No error


