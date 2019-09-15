# Equitable preprints API

Django-based REST API serving data from rxivist database enhanced with the low visibility shadow index.

## /categories

A list of categories. No parameters acceptes.

A category has the following fields: `key`, `name` and `total` (total number of preprints).

    [
        {
            "key": "neuroscience",
            "name": "Neuroscience",
            "total": 10267
        },
        {
            "key": "bioinformatics",
            "name": "Bioinformatics",
            "total": 5914
        },
        ...
    ]

## /articles

A list of articles. Accepts the following parameters:

  * `category`: category key
  * `query`: search terms (against article title or abstract)
  * `posted_since`: filters the articles posted on or after given date (format: `yyyy-mm-dd`, e.g. `2019-05-01`)

An article has the following fields: `id`, `title`, `category`, `url`, `doi`, `authors`, `shadow_index`.

    {
        "total": 180,
        "articles": [
            {
                "id": 17793,
                "title": "The mandibular gland in Nasonia vitripennis (Hymenoptera: Pteromalidae)",
                "category": "zoology",
                "url": "https://www.biorxiv.org/content/10.1101/006569v1",
                "doi": "10.1101/006569",
                "shadow_index": 100.0,
                "authors": "Andrew Deans, Istvan Miko"
            },
            {
                "id": 17794,
                "title": "Mitochondrial DNA variation and structure among North American populations of Megaselia scalaris",
                "category": "zoology",
                "url": "https://www.biorxiv.org/content/10.1101/006288v1",
                "doi": "10.1101/006288",
                "shadow_index": 50.0,
                "authors": "Bret S Lesavoy, Mohamed A.F. Noor, Suzanne E McGaugh"
            },
            {
                "id": 31811,
                "title": "Evaluation of rearing parameters of a self-limiting strain of the Mediterranean fruit fly, Ceratitis capitata (Diptera: Tephritidae)",
                "category": "zoology",
                "url": "https://www.biorxiv.org/content/10.1101/404749v1",
                "doi": "10.1101/404749",
                "shadow_index": 33.333,
                "authors": "Ahmed Mazih, Martha Koukidou, Neil Naish, Rachid Elaini, Romisa Asadi"
            },
            ...
        ]
    }
