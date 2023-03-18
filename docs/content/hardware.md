---
title: Hardware 
date: 20230126
author: realcaptainsolaris 
---

# Geräte auflisten 

## PCI Geräte auflisten
mit dem Argument `-vv` erhalten wir eine Verbose Ansicht.

    lspci -vv

mit dem Argument `-k` kann man sehen, welche Module das Gerät verwenden:

    lspci -k 


## USB Geräte
    
    lsusb -vv
    lsusb
