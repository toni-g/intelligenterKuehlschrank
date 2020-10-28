# intelligenterKuehlschrank
Eine Anwendung, die nach Eingabe vorhandener Lebensmittel kochbare Rezepte ausgibt

### Datenbank

Die Datenbank besteht aus 6 Tabellen
1. rezept<br>
  Die Tabelle rezept enthält alle Rezepte, die von der Anwendung ausgegeben werden können. Hier sind Rezeptname, Zubereitung, Dauer und die Bilddatei gespeichert. Jedes Rezept besitzt eine ID, die der Hautschlüssel ist.<br>
  Sollte der Nutzer ein Rezept ohne Bild hochgeladen haben, ist die Bilddatei der Platzhalter "noimage.png".
2. zutaten<br>
  In der Tabelle zutaten sind alle Zutaten und ihre zugehörigen Kategorien zu finden. Die Zuaten sind durch den Hauptschlüssen ZutatenID eindeutig zuzuordnen.
3. lebensmittelkategorie<br>
  In der Tabelle lebensmittelkategorien sind 11 verschiedene Kategorien aufgelistet. Diese Tabelle wird nicht verändert.
4. menge<br>
  Die Tabelle menge ist eine Schnittstelle der Tabellen rezept und zutaten. Diese Tabelle gibt an, welche Lebensmittel und welche Mengen für die Rezepte aus der Tabelle rezept benötigt werden. So kommt es also vor, dass es mehrere Einträge mit dem gleichen Wert des Fremdschlüssels RezeptID gibt, denn ein Rezept bestehlt üblicherweise aus mehr als nur einer Zutat.
5. kuehlschrank<br>
  In der Tabelle kuehlschrank sind alle Lebensmittel verzeichnet, die sich momentan im Kühlschrank befinden, oder bereits verbraucht wurden.<br>
  Die Tabelle besitzt 3 Spalten: ZutatenID, da_seit und weg_seit.<br>
  Öffnet man die Anwendung zum ersten Mal, gibt es keinen Eintag in dieser Tabelle. Sobald der Nutzer auf der Seite "dein_kuehlschrank" Lebensmittel ausgewählt und das Formular abgeschickt hat, wird für jedes ausgewählte Lebensmittel ein Eintag in dieser Tabelle erstellt.<br>
  Dabei entspricht der Wert in der Spalte ZutatenID der ZutatenID der ausgewählen Zutat und der Wert in der Spalte da_seit der aktuellen Uhrzeit. Der Wert der Spalte weg_seit ist NULL, weil sich das Lebensmittel noch im Kühlschrank befindet.<br>
  Sobald das Lebensmittel wieder nicht ausgewählt ist, wird der Eintag in der Datenbank durch das aktuelle Datum in der Spalte weg_seit ergänzt.
6. log_vorschlaege<br>
