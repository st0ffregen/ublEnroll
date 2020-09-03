# ublEnroll

Reserviert einen Platz n Tage im Voraus in einer der Bibliotheken der Universität Leipzig.

## Beispielnutzung
Reserviert einen Platz für eine Person mit folgenden Daten  

Kartennummer: 123456-1  
Passwort: password123  
Standort: Bibliotheca Albertina  
Bereich: Mitte 2. OG  
Zweiter Bereich: Keine Spezifizierung  
Uhrzeit: 10:00 bis 15:00 Uhr    
Tage im voraus: 7  

```
python3.7 ublEnroll.py 123456-1 password123 10:00 15:00 'Bibliotheca Albertina' 'Mitte 2. OG' 'no selection' 7
```
