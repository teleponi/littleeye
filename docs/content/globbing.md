---
title: Globbing
date: 20221223
author: realcaptainsolaris 
---

# Globbing
Alle Dateien mit Endung txt. Sternchen steht für beliebig viele Zeichen.

    ls *.txt 

Fragezeichen steht für genau ein Zeichen (siehe auch regex)

    ls ?.txt

nach einer CSV-DAtei suchen, die test oder Test am Anfang des namens hat,
und die Endung .csv hat

    ls [tT]est*.csv

Ausschluss von Dateien

    ls test[^1-2].txt

    ls {tisch, stuhl}*


