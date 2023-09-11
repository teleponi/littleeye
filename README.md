# LittleEye - Korrekturmanagementsystem

Ein Studienprojekt von A. Duman, T. Bartholmé und B. Fischer

## 1. Programm ohne Docker starten 

    cd littleye_project/app

### Environment anlegen 
Falls noch kein virtuelles Environment auf dem lokalen Rechner für 
dieses Projekt angelegt wurde, muss das jetzt gemacht werden.

    python -m venv env

Es sollte jetzt ein Verzeichnis unter `littleeye_project/app/env` exisitieren.
Das Verzeichnis wird nicht in der Versionskontrolle versioniert, da es bei
gitignore eingetragen ist.

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
    (env) pip-compile requirements-doc.in
    (env) pip-sync requirements.txt requirements-dev.txt requirements-doc.txt

### .env-Datei anlegen
Falls noch nicht getan, muss eine .env-Datei angelegt werden, in der die
lokalen Settings liegen. Dazu einfach die env.example kopieren und umbenennen
in .env.
Gleiches für env_db_example => .env.db 

## Handbuch publizieren

beim Installieren der requirements-doc.txt wurde mkdocs installiert. Dort das
Helferprogramm gh-deploy ausführen
    
    (env) mkdocs gh-deploy

Der ensprechende Branch auf github wird aktualisiert

## Die Entwicklungsumgebung mit dem Django-Entwicklungserver starten
Das Image builden:

    (env) docker-compose up --build -d

Die Datenbank migrieren

    (env) docker-compose exec app ./manage.py migrate

Die statischen Dateien sammeln

    (env) docker-compose exec app ./manage.py collectstatic

einen Superuser anlegen (hier dann alles ausfüllen, username, password etc)

    (env) docker-compose exec app ./manage.py createsuperuser 


(sicherheitshalber den container jetzt runterfahren, damit die statischen dateien auch gefunden werden)

    (env) docker-compose down


jetzt nochmal starten

    (env) docker-compose up --build -d

Seite aufrufen unter http://127.0.0.1:8000/admin

und Mediatypes (zb. Skript), Tags (zb. falscher Fehler), Benutzer (zb. sarah) und Course (Mathe1) anlegen
dann mit einem Studenten-Account (zb. tom) auf http://127.0.0.1:8000 einloggen
und ein Ticket erstellen

Falls die Seite nicht aufgerufen werden kann, die Logs angucken

    (env) docker-compose logs --follow
