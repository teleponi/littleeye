---
title: Modules 
date: 20230126
author: realcaptainsolaris 
---

# Kernelmodule

Welche Module hat der Kernel aktuell geladen?

    lsmod

4-spaltige Übersicht aller Module (Modulname, Modulgröße, benutzt von
wievielen, benutzt von wem).

## Beispiel:

    lsmod
    [...]
    lpc_ich                28672  0
    sdhci                  81920  1 sdhci_pci
    libahci                45056  1 ahci
    crc_itu_t              16384  1 firewire_core
    wmi                    32768  2 wmi_bmof,think_lmi
    video                  57344  2 thinkpad_acpi,i915

## Kernelmodule Informationen
Um mehr Informationen über ein Modul zu erhalten, gibt es `modinfo`
   
    modinfo libahci 

    ❯ modinfo libahci
    filename:       /lib/modules/5.15.0-58-generic/kernel/drivers/ata/libahci.ko
    license:        GPL
    description:    Common AHCI SATA low-level routines
    author:         Jeff Garzik
    srcversion:     D5902F34F56CD0E9B29D99F
    depends:        
    retpoline:      Y
    intree:         Y
    name:           libahci
    vermagic:       5.15.0-58-generic SMP mod_unload modversions 
    sig_id:         PKCS#7
    ..

## Kernelmodule laden und entladen mit modprobe
Um zur Laufzeit Module entladen:
    
    sudo modprobe -r ip_tables
    
Prüfen, ob Module noch läuft:

    lsmod | grep ip_tables

Modul wieder laden:

    sudo modprobe ip_tables
