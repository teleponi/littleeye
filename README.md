# LittleEye - Korrekturmanagementsystem

## 1. Programm ohne Docker starten 

    cd littleye_project/app

### Environment anlegen 
Falls noch kein virtuelles Environment auf dem lokalen Rechner für 
dieses Projekt angelegt wurde, muss das jetzt gemacht werden.

    python -m venv env

Es sollte jetzt ein Verzeichnis unter `littleeye_project/app/env` exisitieren.

### Enviroment starten
für Mac / Linux / Unix

    source env/bin/activate

für Windows

    .\env\Scripts\activate
    
### für dieses Environment pip-tools installieren

    (env) pip install pip-tools

### Dependencies kompilieren und installieren

    (env) pip-compile requirements.in
    (env) pip-compile requirements-dev.in
    (env) pip-sync requirements.txt requirements-dev.txt 

### .env-Datei anlegen
Falls noch nicht getan, muss eine .env-Datei angelegt werden, in der die
lokalen Settings liegen. Dazu einfach die env.example kopieren.



### Testuser anlegen

    (env) python manage.py create_user n=10  
    

http://127.0.0.1:1337

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
