REST URLs
=========

The default server |URL| for the |NAMI| is

.. centered:: https://nami.dpsg.de/ica/rest

Authentification
----------------

.. http:post:: /nami/auth/manual/sessionStartup

	Login

  	:query string username: The |DPSG| member id
	:query string password: Your password 

.. http:get:: /nami/auth/logout

	Logout. Ends the current session.

Search members
--------------

.. http:get:: /nami/mitglied/filtered-for-navigation/gruppierung/gruppierung/(groupId)/flist
	
	List all group members though filtering by one value is possible

	:arg int groupId: A chosen group id (usually your Stammesnummer)
	:query string filterString: The filter attribute (optional)
	:query string searchString: Search value. If the filter attribute refers to a date the format is ``YYYY-mm-dd HH:MM:SS``.
	:query int page: The page number of result display
	:query int start: Show search results form this index
	:query int limit: Show only up to this many entries
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json int totalEntries: Number of returned members
	:>json list data: The search results. Each returned member is a list entry in the form of a json array.
	:status 200: No error

.. http:get:: /nami/search-multi/result-list

	Search members by multiple keys

	:query string searchedValues: A json formatted string of all search values
	:query int page: The page number of result display
	:query int start: Show search results form this index
	:query int limit: Show only up to this many entries
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json int totalEntries: Number of returned members
	:>json list data: The search results. Each returned member is a list entry in the form of a json array.
	:status 200: No error

.. http:get:: /nami/mitglied/filtered-for-navigation/gruppierung/gruppierung/{groupId}/{mglId}

	Get a member by its id (not the |DPSG| Mitgliedsnummer)

	:arg int groupId: A chosen group id (usually your Stammesnummer)
	:arg int mglId: Member id (not the |DPSG| Mitgliedsnummer)
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json string message: Should be ``null``.
	:>json string title: Should be ``null``.
	:>json json data: Contains all relevant information about the member
	:status 200: No error

Update members
--------------

.. http:put:: /nami/mitglied/filtered-for-navigation/gruppierung/gruppierung/{groupId}/{mglId}

	Update information about a member.

	:arg int groupId: A chosen group id (usually your Stammesnummer)
	:arg int mglId: Member id (not the |DPSG| Mitgliedsnummer)
	:json string beitragsArt: Fee type
	:json id beitragsArtId: Id of the fee type
	:json eintrittsdatum: Begin of association (Format: ``YYYY-mm-dd HH:MM:SS``)
	:json string email: Primary email address
	:json string emailVertretungsberechtigter: Email address of an authorized representative.
	:json string ersteTaetigkeit: First activity. Defaults to ``null``.
	:json string ersteUntergliederung: First tier.
	:json string fixBeitrag: Defaults to ``null``.
	:json string geburtsDatum: Birth date (Format: ``YYYY-mm-dd HH:MM:SS``)
	:json string genericField1: Not sure why these even exist.
	:json string genericField1: Not sure why these even exist.
	:json string geschlecht: Gender
	:json int geschlechtId: Corresponding id to the gender
	:json string gruppierung: Group name including its id
	:json string gruppierungId: Group id as a string
	:json int id: Member id
	:json string jungpfadfinder:
	:json string konfession: Confession
	:json int confessionId: Id corresopnding to the confession
	:json string kontoverbindung: JSON formatted string of the payment details
	:json string land: Country the member lives in
	:json int landId: Id corresponding to the address country
	:json string mglType: Member type
	:json string nachname: Surname
	:json string nameZusatz: Additional name
	:json string ort: Address city
	:json string pfadfinder:
	:json string plz: Postal code
	:json string region: Name of the address state
	:json int regionId: Id of the address state
	:json string rover:
	:json boolean sonst01: Defaults to ``false``.
	:json boolean sonst02: Defaults to ``false``.
	:json string spitzname: Nickname
	:json string staatsangehoerigkeit: Citizenship
	:json string staatsangehoerigkeitId: Id of the citizenship
	:json string status: If the member is active or inactive
	:json string strasse: Address street
	:json string stufe: Current tier of the member
	:json string telefax: Fax number
	:json string telefon1: First telephone number
	:json string telefon2: Second telephone number
	:json string telefon3: Third telephone number
	:json int version: History version number
	:json string vorname: First name
	:json boolean wiederverwendenFlag: If the member data may be used after the membership ends
	:json string woelfing:
	:json boolean zeitschriftenversand: If the member gets the |DPSG| newspaper.
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json string message: Should be ``Update successful``.
	:>json string title: Should be ``null``.
	:>json json data: Contains all information about the updated member
	:status 200: No error

Activities
----------

.. http:get:: /nami/zugeordnete-taetigkeiten/filtered-for-navigation/gruppierung-mitglied/mitglied/{mglId}/flist

	Retrieve all activities of a member. There is also an option for filtering the results.

	:arg int mglId: Member id (not the |DPSG| Mitgliedsnummer)
	:query int page: The page number of result display
	:query int start: Show search results form this index
	:query int limit: Show only up to this many entries
	:query string filterString: The filter attribute (optional)
	:query string searchString: Search value. If the filter attribute refers to a date the format is ``YYYY-mm-dd HH:MM:SS``.
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json int totalEntries: Number of returned members
	:>json list data: The search results. Each returned activity is a list entry in the form of a json array.
	:>json json metaData: Additional information about the data fields but not on the activities themselves.
	:status 200: No error

.. http:get:: /nami/zugeordnete-taetigkeiten/filtered-for-navigation/gruppierung-mitglied/mitglied/{mglId}/{actId}

	Get a single activity by its id.

	:arg int mglId: Member id (not the |DPSG| Mitgliedsnummer)
	:arg int actId: Id of the desired activity
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json string message: Should be ``null``.
	:>json string title: Should be ``null``.
	:>json json data: Contains all relevant information about the activity
	:status 200: No error

.. http:put:: /nami/zugeordnete-taetigkeiten/filtered-for-navigation/gruppierung-mitglied/mitglied/{mglId}/{actId}

	Update an activity

	:arg int mglId: Member id (not the |DPSG| Mitgliedsnummer)
	:arg int actId: Id of the desired activity
	:json string aktivBis: End date of the activity (Format: ``YYYY-mm-dd HH:MM:SS``)
	:json string aktivVon: Start date of the activity (Format: ``YYYY-mm-dd HH:MM:SS``)
	:json int beitragsArtId: Id of the fee type (default: ``null``). It has not been observed to be anything else than ``null``.
	:json string caeaGroup: Access rights for the group.
	:json string caeaGroupForGf: Access rights for the sub group.
	:json int caeaGroupId: Corresponsing id for ``caeaGroup``.
	:json int caeaGroupForGfId: Corresponsing id for ``caeaGroupForGf``.
	:json string gruppierung: Group Name including its id.
	:json int id: Id of the activity.
	:json string taetigkeit: Type of the activity.
	:json string untergliederung: Department or tier the activity is assciated with.
	:>json boolean success: If everything was ok
	:>json string responseType: |NAMI| response type: Can be ``OK``, ``INFO``, ``WARN``, ``ERROR``, ``EXCEPTION`` or ``null``
	:>json string message: Should be ``Update successful``.
	:>json string title: Should be ``null``.
	:>json json data: Contains all information about the updated activity.
	:status 200: No error