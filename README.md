<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![Pull Requst][pr-shield]][pr-url]
[![Activity][activity-shield]][activity-url]
[![Stargazers][stars-shield]][stars-url]

<!-- ABOUT THE PROJECT -->
## About
<div align="center">
    <a href="https://github.com/LabConnect-RCOS/LabConnect-Backend">
        <img src="misc/LabConnect_Logo-removebg-preview.png" alt="LabConnect Logo" width="360">
    </a>
    <br/><br/>
    <p align="center">A centralized website to connect RPI undergraduate students with research or lab positions<br>
posted by professors, graduate students, or lab staff.</p>
</div>


### Built With

[![Python][Python]][Python-url]
[![Flask][Flask]][Flask-url]
[![PostgreSQL][PostgreSQL]][PostgreSQL-url]
[![SQLAlchemy][SQLAlchemy]][SQLAlchemy-url]


<!-- Getting Started -->
## Prerequisites
 * Clone
    * Clone repo through CLI
        ```bash
        $ git clone https://github.com/LabConnect-RCOS/LabConnect-Backend.git
        ```
    * or through [Github Desktop](https://desktop.github.com/)
 * Install Python 3.12.4
    * Mac
        ```
        brew install python@3.14
        ```
    * Windows: [here](https://www.python.org/downloads/release/python-3124/)
    * Linux:
        ```
        $ sudo apt install python3
        ```
 * Install PostgreSQL
    * The application is built and tested with postgresql 17
    * Mac: [UI here](https://postgresapp.com/) or
    ```
    brew install postgresql@17
    ```
    * Windows: [here](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) 
    * Linux:
        ```
        $ sudo apt install postgresql
        ```
 * Install Libraries 
    ```
    $ python3 -m pip install -r requirements.txt
    ```
* Setup user and initialize database
    * Windows:
        ```bash
        $ psql -U postgres -d postgres
        CREATE DATABASE labconnect;
        ALTER USER postgres WITH PASSWORD 'root';
        \q
        ```
    * macOS (Homebrew):
        ```bash
        # start postgres if not running
        $ brew services start postgresql
        $ psql -U postgres -d postgres
        CREATE DATABASE labconnect;
        ALTER USER postgres WITH PASSWORD 'root';
        \q
        ```
    * macOS (Postgres.app):
        ```bash
        # open Postgres.app, then in a terminal (Postgres.app adds psql to PATH)
        $ psql -d postgres
        CREATE DATABASE labconnect;
        ALTER USER postgres WITH PASSWORD 'root';
        \q
        ```
    * Linux:
        ```bash
        $ sudo -i -u postgres
        $ psql
        ALTER USER postgres WITH PASSWORD 'root';
        \q
        $ exit
        $ sudo -u postgres createdb labconnect
        ```
    
    * Final step
      * Run the db initialization with test/dummy data `make create`

## Testing
 * Run pytest
   * Run all the test files and generate a coverage report. Coverage reports are set up to output to the terminal and provide an HTML file that can be viewed to show what branches or statements are not covered. It is in the project's best interest to have high coverage to ensure all statements and branches work as expected.
   ```bash
   $ make test
   ```
   or manually
   ```bash
   $ python3 -m pytest
   ```
   or manually with a coverage report generated
   ```bash
   $ python3 -m pytest --cov
   ```

## Development
 * Run flask with python directly
   * Run all the test files
   ```bash
   $ make develop
   ```
   or
   ```bash
   $ python run.py
   ```

## Deployment
Create PRs to the main branch. Upon merging, a new Docker container will be created and pushed to the [packages for this repo](https://github.com/LabConnect-RCOS/LabConnect-Backend/pkgs/container/labconnect-backend).

## Production
Use the Docker container in the [packages tab](https://github.com/LabConnect-RCOS/LabConnect-Backend/pkgs/container/labconnect-backend). You can set these environment variables:

### Environment Variables

| Variable Name          | Default Value | Description                                                   |
|------------------------|---------------|---------------------------------------------------------------|
| `SECRET_KEY` | `main-secret` | Secret Key for Flask |
| `JWT_SECRET_KEY` | `jwt-secret` | Secret Key for JWT |
| `FRONTEND_URL` | None | URL to the frontend server |
| `DB` | None | URI for postgres database eg. `postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres/labconnect` |
| `CONFIG` | `config.TestingConfig` | URL to the backend server |

 * Run gunicorn to test how the service runs in production
   ```bash
   $ make run
   ```
   or with Makefile
    ```bash
   $ gunicorn run:app -w 6 --preload --max-requests-jitter 300 --bind 0.0.0.0:8000
   ```

## Contact Us
[![Discord](https://img.shields.io/badge/Discord-5865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/tsaxCKjYHT)
[![Jira](https://img.shields.io/badge/Jira-0052CC.svg?style=for-the-badge&logo=jira&logoColor=white)](https://rcoslabconnect.atlassian.net/jira/software/projects/CCS/list)


## License

Distributed under the Apache License. See [LICENSE](https://github.com/LabConnect-RCOS/LabConnect-Backend/blob/main/LICENSE) for more information.

<!-- https://home.aveek.io/GitHub-Profile-Badges/ -->

<!-- LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/LabConnect-RCOS/LabConnect-Backend.svg?style=for-the-badge
[contributors-url]: https://github.com/LabConnect-RCOS/LabConnect-Backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/LabConnect-RCOS/LabConnect-Backend.svg?style=for-the-badge
[forks-url]: https://github.com/LabConnect-RCOS/LabConnect-Backend/network/members
[stars-shield]: https://img.shields.io/github/stars/LabConnect-RCOS/LabConnect-Backend.svg?style=for-the-badge
[stars-url]: https://github.com/LabConnect-RCOS/LabConnect-Backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/LabConnect-RCOS/LabConnect-Backend.svg?style=for-the-badge
[issues-url]: https://github.com/LabConnect-RCOS/LabConnect-Backend/issues
[pr-shield]: https://img.shields.io/github/issues-pr/LabConnect-RCOS/LabConnect-Backend.svg?style=for-the-badge
[pr-url]: https://github.com/LabConnect-RCOS/LabConnect-Backend/pulls

[activity-shield]: https://img.shields.io/github/last-commit/LabConnect-RCOS/LabConnect-Backend?style=for-the-badge
[activity-url]: https://github.com/LabConnect-RCOS/LabConnect-Backend/activity

[Python]: https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white
[Python-url]: https://www.python.org/
[Flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[SQLAlchemy]: https://img.shields.io/badge/SQLAlchemy-000000?style=for-the-badge&logo=sqlalchemy&logoColor=white
[SQLAlchemy-url]: https://www.sqlalchemy.org/