# Der intelligente Kühlschrank
Eine Anwendung, die nach Eingabe vorhandener Lebensmittel kochbare Rezepte ausgibt

## Anleitung zum Öffnen
1. alle Dateien herunterladen
2. xampp installieren und ggf. Ports anpassen
3. Module Apache und MySQL auf xampp starten
4. localhost/phpmyadmin/ im Browser öffnen
5. links auf "Neu" klicken und so eine neue Datenbank erstellen (der Name der Datebank muss "codecompetition" heißen)
6. die erstellte Datenbank auswählen und in der Menüleiste auf "Importieren" klicken
7. im Absatz "Zu importierende Datei:" auf den Button "Datei auswählen" klicken und die heruntergeladene Datei "codecompetition.sql" öffnen

8. die Kommandozeile öffnen und folgende Befehle ausfühen:<br>
pip install flask<br>
pip install mysql.connector
9. in der Kommandozeile zum Ordner wechseln, der die Datei app.py enthält
10. den Befehl "python app.py" ausführen (im Fenster der Kommandozeile sollten 6 Zeilen erscheinen mit einer url in der letzten Zeile, z.B. http://127.0.0.1:5000/)
11. die url in einem Browser öffnen

## Anleitung zum Benutzen
Nach dem Öffnen landen Sie auf der Startseite, wo zu sehen ist, welche Lebensmittel sich im Kühlschrank befinden und welche Gerichte daraus gekocht werden können.
Sollten Sie die Anwendung zum ersten Mal öffnen, sehen Sie noch kein Rezept, weil Sie noch keine Lebensmittel ausgewählt haben. <br>
Klicken Sie daher auf den Button "<- Zum Kühlschrank", wo Sie alle Lebensmittel sehen, die für alle Rezepte benötigt werden. Die Lebensmittel sind nach Kategorien sortiert. Viele Lebensmittel sehen Sie nicht, da sich bisher nur sechs Rezepte in der Datenbank befinden.<br>
Ziel der Anwendung ist es, möglichst viele Rezepte zu speichern, damit eine große Zutatenvielfalt entsteht.<br>
Neue Rezepte können Sie jederzeit selber hinzufügen, indem sie die Eingabefelder auf der Seite "/neues_rezept" ausfüllen und abschicken. Falls Sie eine Zutat eingeben, die bereits in der Datenbank zu finden ist, wird das Feld für die Kategorie ausgeraut und zeigt die zugehörige Kategorie an.<br>
Sie können auch ein Bild des Gerichtes hochladen.

## Datenbank

Die Datenbank besteht aus 6 Tabellen
1. rezept<br>
  Die Tabelle _rezept_ enthält alle Rezepte, die von der Anwendung ausgegeben werden können. Hier sind Rezeptname, Zubereitung, Dauer und die Bilddatei gespeichert. Jedes Rezept besitzt eine ID, die der Hauptschlüssel ist.<br>
  Sollte der Nutzer ein Rezept ohne Bild hochgeladen haben, ist die Bilddatei der Platzhalter "noimage.png".
2. zutaten<br>
  In der Tabelle _zutaten_ sind alle Zutaten und ihre zugehörigen Kategorien zu finden. Die Zuaten sind durch den Hauptschlüssen ZutatenID eindeutig zuzuordnen.
3. lebensmittelkategorie<br>
  In der Tabelle _lebensmittelkategorie_ sind 11 verschiedene Kategorien aufgelistet. Diese Tabelle wird nicht verändert.
4. menge<br>
  Die Tabelle _menge_ ist eine Schnittstelle der Tabellen _rezept_ und _zutaten_. Diese Tabelle gibt an, welche Lebensmittel und welche Mengen für die Rezepte aus der Tabelle rezept benötigt werden. So kommt es also vor, dass es mehrere Einträge mit dem gleichen Wert des Fremdschlüssels _RezeptID_ gibt, denn ein Rezept bestehlt üblicherweise aus mehr als nur einer Zutat.
5. kuehlschrank<br>
  In der Tabelle _kuehlschrank_ sind alle Lebensmittel verzeichnet, die sich momentan im Kühlschrank befinden, oder bereits verbraucht wurden.<br>
  Die Tabelle besitzt 3 Spalten: _ZutatenID_, _da_seit_ und _weg_seit_.<br>
  Öffnet man die Anwendung zum ersten Mal, gibt es keinen Eintrag in dieser Tabelle. Sobald der Nutzer auf der Seite "dein_kuehlschrank" Lebensmittel ausgewählt und das Formular abgeschickt hat, wird für jedes ausgewählte Lebensmittel ein Eintrag in dieser Tabelle erstellt.<br>
  Dabei entspricht der Wert in der Spalte _ZutatenID_ der ZutatenID der ausgewählen Zutat und der Wert in der Spalte _da_seit_ der aktuellen Uhrzeit. Der Wert der Spalte _weg_seit_ ist NULL, weil sich das Lebensmittel noch im Kühlschrank befindet.<br>
  Sobald das Lebensmittel wieder nicht ausgewählt ist, wird der Eintrag in der Datenbank durch das aktuelle Datum in der Spalte _weg_seit_ ergänzt.
6. log_vorschlaege<br>
  Jedes Mal, wenn der Nutzer wieder auf die Startseite kommt, werden die Rezepte, die ihm vorgeschlagen werden, in dieser Tabelle dokumentiert. Auch die aktuelle Zeit wird hier eingetragen.<br>

![Datenbankstruktur](/static/Datenbank_Struktur.png)
