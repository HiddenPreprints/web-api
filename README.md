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

## Development

To run the Equitable Preprints API, first make sure Docker is installed.

Databases credentials are taken from `vars.env` file. It can be created by copying from `vars.env.example` and replacing question marks with appropriate values. `BIORXIV_*` variables should point to an existing database, from which the data will be imported. `SECRET_KEY` and `MYSQL_*` variables are related to the local Django and MySQL and should be set before the first deployment and not changed afterwards.

To start all Docker services, in the project directory run:

```
docker-compose up -d
```

You may see errors resulting from the fact that the services start at the same time and not in the preferred order. Eventually, all services should start and connections between them should be established.

The API's backend is MySQL database. Use these commands to create tables in the database, import bioRxiv data and calculate Shadow Index (all this will take several minutes):

```
docker-compose exec api python manage.py create_tables
docker-compose exec api python manage.py import_biorxiv
docker-compose exec api python manage.py calculate_shadow_index
```

The backend database stores all data in `<REPO DIR>/mysql_data` directory. As long as this directory is not deleted, restarting and rebuilding Docker containers does not affect the data in the database.

The API can be accessed at `http://localhost:8000`.
