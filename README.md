# intelligenterKuehlschrank
Eine Anwendung, die nach Eingabe vorhandener Lebensmittel kochbare Rezepte ausgibt

### Datenbank

Die Datenbank besteht aus 6 Tabellen
1. kuehlschrank<br>
  In der Tabelle kuehlschrank sind alle Lebensmittel verzeichnet, die sich momentan im Kühlschrank befinden, oder bereits verbraucht wurden.<br>
  Die Tabelle besitzt 3 Spalten: ZutatenID, da_seit und weg_seit.<br>
  Öffnet man die Anwendung zum ersten Mal, gibt es keinen Eintag in dieser Tabelle. Sobald der Nutzer auf der Seite "dein_kuehlschrank" Lebensmittel ausgewählt und das Formular abgeschickt hat, wird für jedes ausgewählte Lebensmittel ein Eintag in dieser Tabelle erstellt.<br>
  Dabei entspricht der Wert in der Spalte ZutatenID der ZutatenID aus der Tabelle zutaten und der Wert in der Spalte da_seit der aktuellen Uhrzeit. Der Wert der Spalte weg_seit ist NULL, weil sich das Lebensmittel noch im Kühlschrank befindet.<br>
  Sobald das Lebensmittel wieder nicht ausgewählt ist, wird der Eintag in der Datenbank durch das aktuelle Datum in der Spalte weg_seit ergänzt.
