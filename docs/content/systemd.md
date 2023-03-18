---
title: systemd 
date: 20221223
author: realcaptainsolaris 
---

# systemd 

Ist ein System- und Sitzungs-Manager (Init-System), der für die Verwaltung aller auf dem System laufenden Dienste über die gesamte Betriebszeit des Rechners, vom Startvorgang bis zum Herunterfahren, zuständig ist. Prozesse werden dabei immer (soweit möglich) parallel gestartet, um den Bootvorgang möglichst kurz zu halten.

## Units

systemd holt alle seine Vorgaben und Einstellungen zur Verwaltung aus Dateien, in der Terminologie von systemd sind dies "Units". Dabei wird zwischen systemweit geltenden Units und solchen, die nur für den jeweiligen Benutzer-Bereich gelten User Units unterschieden. Es gibt diverse Arten von Units wie z.B. Service Units zum Starten von Diensten oder Timer Units zum (wiederholten) Ausführen einer Aktion zu einem bestimmten Zeitpunkt.

Dateien finden sich in zwei Dateien

Unter `/etc/systemd/system` finden sich die Units, dh. Dateien
die gestartet werden.

Weitere Dateien: `/lib/systemd/system`

## systemctl

Manager für das system.d

Alle Units auflisten:

    systemctl list-units

Status eines Diestes erfragen

    systemctl status docker

