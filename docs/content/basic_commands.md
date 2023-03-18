---
title: Basic Linux Commands 
date: 20221223
author: realcaptainsolaris 
---

# Basic Commands 

## HISTORY

Die History Datei liegt unter

    echo $HISTFILE

angucken mit
  
    cat $HISTFILE

oder 
    
    history


## ECHO
Mit echo kann man Variablen ausgeben

    ochse=1
    echo $x
    echo "alles ausgeben \n bricht nicht um"
    echo -e "test \n test mit -e wird Zeilenumbruch ausgeführt"
    man echo

## Umgebugnsvariablen

Alle Umgebungsvariablen anzeigen

    env

die Path-Varialbe anziegen:

    echo $PATH

## CAT
Datei(en) öffnen

      cat datei
      cat datei1 datei2 > datei3

## LESS
seitenweise große Dateien anzeigen
      
      less datei1

mit q verlassen

## HEAD
ersten 10 zeilen anzeigen

    head /etc/passwd
    head /etc/passwd -n 10 

## TAIL
wie head, nur von hinten

Live überwachen
    
    tail -f /var/log/dpkg.log

## NL

gibt die Anzahl aller Zeilen aus

    nl /etc/passwd

Leerzeilen haben keine Zeilennummer!

## WC

Wordcount

    wc /etc/passwd

die erte Zahl Zeilenanzhl
die zweite zahl: anzal wrörter
die dirtte zhtl: bytes

## OD
od - dump files in octal and other formats

    od -c /etc/passwd
    od /etc/passwd


## SORT

table.csv
1,Hans
23,Axenmensch
24,peter
2,kanter

    sort -n table.csv

Sort sagen, dass wir komma als seperator haben
und das wir nach der spalte 2 sortiern wollen (name)


    sort -t "," -k2 table.csv

-t Trenner
-k Key numerisch
Dateiname

## UNIQ
uniq löscht untereinanderstehende gleiche Zeilen.
mit -c kann man sich anzeigen lassen, wie oft die Zeile
vor kam.

    uniq uniq.txt
    uniq -c uniq.txt
    uniq --group uniq.txt

## TR
translate: ersetzt zeichen durch anderes zeichen
ersetze komma durch semikolon:

    echo "one,two" | tr ',' ';'
    one;two

    cat table.csv | tr ',' ';' > table2.csv

    echo "one,two" | tr 'a-z' 'A-Z'
    ONE,TWO


    echo "one,two" | tr 'a-z' 'A-Z' | tr ',' ';'
    ONE;TWO

Große Json-Datei in Zeilen splitten und nach Vorkommen suchen:

    tr "," "\n" < staticfiles.json | grep "filetosearchfor"

## CUT
wie cat, nur mit ausschneiden.
-d Delimiter
-f Field
 
    cut -d ',' -f 2 table2.csv

    Hans
    peter
    kanter
    Axenmensch



❯ cat table2.csv
1,Hans,34
24,peter,22
2,kanter,11
23,Axenmensch,21

man kann auch zwei Fields rausschneiden

    cut -d ',' -f 2,3 table2.csv

    Hans,34
    peter,22
    kanter,11
    Axenmensch,21

## PASTE

Dateien zusammenführen
cat a.txt
1,alfa
2,beute

cat b.txt
apple
bea

paste -d ',' a.txt b.txt
1,alfa,apple
2,beute,bea

## SED

Inhalte erstezen
s = substitute
finden
ersetzen
g global (alles ersetzten)

ändere alle vorkommen von er durch ra in table2.csv

    sed 's/er/ra/g' table2.csv

wenn man die Datei verändern will, muss man kleines i nutzen

    sed 's/er/ra/g' -i table2.csv

Alle Vorkommen in Dateien ersetzen mit ag (Silver Search)
  
    ag SearchString -l0 | xargs -0 sed -i 's/SearchString/Replacement/g'

Alle Vorkommen in Dateien ersetzen mit grep

    grep -rl SearchString . | xargs sed -i 's/SearchString/Replacement/g'

# SPLIT
eine DAtei in kleinere Dateien zerlegen (20 bytes große dateien)

    split -b 20 table2.csv

## SCP
Auf entfernten Server kopieren (mit ssh-key)

    scp -i ~/.ssh/id_rsa.pub FILENAME USER@SERVER:/home/USER/FILENAME

## DD
Bootloader sichern (die ersten 512 Bytes der HD)

    dd if=/dev/sda of=backup_bootloader bs=512 count=1
