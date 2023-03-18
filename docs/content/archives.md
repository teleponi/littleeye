---
title: Archives 
date: 20221223
author: realcaptainsolaris 
---

# Tar 

## Packen

Unkomprimiert:

    tar -cf archive.tar file1 file2

Gzip-Komprimiert und Verbose (z)

    tar -cvzf tarball.tar file file

Bzip2-Komprimiert und Verbose (j)

    tar -cvzf tarball.tar file file

Alle Dateien eines Verzeichnisses hinzufügen

    tar -cvzf tarball.tar ./*

## Datei zu Tarball hinzufügen

    tar -rf tarball.tar newfile

## Tar Datei untersuchen

    tar -tf tarball.tar

## Tar Datei entpacken

    tar -xf archive.tar

## gzip komprimiertes Tar-Archiv entpacken
  
    tar -xvzf tarball.tar

# GZIP
Mit Gzip lassen sich nur einzelne Dateien komprimieren,
deshalb wird immer erst mit tar gepakt und dann komprimiert.

    gzip file1

Um die Datei nach dem Komprimieren nicht zu löschen, 

    gzip -k file1

Entpacken und Behalten

    gzip -dk file1


## GUNZIP

    gunzip datei2.gz
    gunzip -d datei2.gz

## BZIP2

    bzip1 file2.bz
    bzip2 -d file2.bz
