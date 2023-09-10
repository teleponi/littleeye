# LittleEye - Korrekturmanagementsystem

Ein Studienprojekt von A. Duman, T. Bartholome und B. Fischer

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


