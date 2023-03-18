# Corrector
Beispiel für ein dockerized Django Project mit `gunicorn`, `Postgres` und
`nginx`


## Settings anpassen

### .env
In .env müssen die Enviroment-Variablen gesetzt werden. U.a. die database_url

    DATABASE_URL=postgres://postgres:postgres@db:5432/postgres

Das Schema ist:
    
    postgres://{user}:{password}@{hostname}:{port}/{database-name} 


Ein Beispiel findet sich in `env_example`. Das muss umbenannt werden in
`.env`

### .env.db
In .env.db müssen die Datenbank-Passwörter für docker-compose abgelegt werden
(identisch zu .env)

Ein Beispiel findet sich in `env_db_example`. Das muss umbenannt werden in
`.env.db`

## Projekt live
`DEBUG` muss in `.env` auf `False` gesetzt werden. Dann folgende Befehle
ausführen: 

    docker-compose up --build -d --no-cache
    docker-compose exec app ./manage.py collectstatic
    docker-compose exec app ./manage.py createsuperuser 

Unter `http://127.0.0.1:1337` im Browser aufrufen.


## Installationsanweisungen

Ein virtuelles Environment erstellen und pip-tools installieren

    python -m venv env
    source env/bin/activate
    pip install pip-tools

requirements.txt Dateien mit pit-tools kompilieren:

    pip-compile requirements.txt
    pip-compile requirements-dev.text

Syncen:

    pip-sync requirements.txt requirements-dev.text


## Testdaten erstellen

    docker-compose exec app ./manage.py create_user -n 20
    docker-compose exec app ./manage.py create_events --categories 10 --events 200

## Nutzungshinweise
    docker-compose down -v
    docker-compose up -d --build
    docker-compose exec web python manage.py migrate --noinput
    docker-compose exec web python manage.py collectstatic --no-input --clear
