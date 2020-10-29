from flask import Flask,render_template, request, url_for
import mysql.connector
from itertools import chain
from collections import Counter
import datetime
from werkzeug.utils import secure_filename
import os

#hier wird der Ordner definiert, in dem die Bilder der Rezepte gespeichert werden
UPLOAD_FOLDER = os.getcwd()+'\static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verbindung zur Datenbank
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="codecompetition"
)

mycursor = mydb.cursor()


#es wird ein Array mit allen schon vorhandenen Lebensmittel erstellt
def vorhandenaktualisieren():
	vorhanden = []
	#in der Tabelle "kuehlschrank" sind alle Lebensmittel dokumentiert, die auf der Seite "dein_kuehlschrank.html" ausgewählt wurden. Wurden diese nicht wieder rausgenommen, ist der Wert in der Spalte "weg_seit" leer (NULL)
	mycursor.execute("SELECT zutaten.Zutat FROM zutaten INNER JOIN kuehlschrank ON zutaten.ZutatenID = kuehlschrank.ZutatenID WHERE weg_seit IS NULL")
	myresult = mycursor.fetchall()
	c = chain.from_iterable(myresult)
	for row in c:
		vorhanden.append(row)
	vorhanden.sort()
	return vorhanden

#es wird ein Array mit allen Rezepten und den jeweiligen Zutaten erstellt
#das Array hat folgende Form: [[rezept1,dauer1,zubereitung1],[zutat1,zutat2,...],[rezept2,dauer2,zubereitung2],[zutat1,zutat5,...]]
#die Einträge des Arrays an gerader Stelle sind die Rezepte, die Rezeptdauer und die Zubereitung, die Einträge an ungerader Stelle sind die Zutaten des Rezeptes von der Stelle davor
def allerezepteaktualisieren():
	allerezepte = []
	mycursor.execute("SELECT Rezeptname,Dauer,Zubereitung,Bilddatei FROM rezept")
	myresult = mycursor.fetchall()
	for i in myresult:
		allerezepte.append(list(i)) #aus den ausgelesenen Werten wird ein Array erstellt und im Array "allerezepte" gespeichtert
		zut = []
		mycursor.execute("SELECT zutaten.Zutat FROM menge INNER JOIN rezept ON rezept.RezeptID = menge.RezeptID INNER JOIN zutaten ON zutaten.ZutatenID = menge.ZutatenID WHERE Rezeptname=%s",(i[0],))
		myresult = mycursor.fetchall()
		c = chain.from_iterable(myresult)
		for eintrag in c:
			zut.append(eintrag)
		allerezepte.append(zut) #dem Array "allerezepte" wird ein Array mit den Zutaten angehängt, die für das Rezept benötigt werden
	return allerezepte #der Rückgabewert dieser Funktion ist das Array "allerezepte"

#es wird ein Array mit allen Rezepten erstellt, die mit den vorhandenen Lebensmitteln gekocht werden können
def kochbare_rezepte_aktualisieren():
	kochbare_rezepte=[]
	allerezepte = allerezepteaktualisieren()
	vorhanden = vorhandenaktualisieren()
	datum = datetime.datetime.now()
	for i in range(0,len(allerezepte)):
		if i%2 == 0:
			#falls die Länge der Liste, die aus der Überschneidung von den vorhanden und den benötigten Lebensmitteln entsteht, die gleiche Länge hat wie die Liste der benötigten Lebensmitteln,
			#dann ist das Rezept kochbar
			if (len(set(vorhanden).intersection(allerezepte[i+1]))) == len(allerezepte[i+1]):
 				kochbare_rezepte.append(allerezepte[i])
	
	#alle Rezepte, die kochbar sind, werden in der Datenbanktabelle "log_vorschlaege" dokumentiert
	for i in kochbare_rezepte:
		mycursor.execute("INSERT INTO log_vorschlaege (`RezeptID`, `Vorgeschlagen`) VALUES ((SELECT RezeptID FROM rezept WHERE Rezeptname = %s),%s)",(i[0],datum))
		mydb.commit()
		
	return kochbare_rezepte #der Rückgabewert dieser Funktion ist das Array "kochbare_rezepte"


#es wird ein Array mit allen Kategorien und den enthaltenen Zutaten erstellt
#das Array "kategorien" hat folgende Form: [kategorie1,[zutat1, zutat3, zutat4],kategorie2,[zutat2, zutat5],...]
def kategorien_aktualisieren():
	kategorien = []
	mycursor.execute("SELECT Kategorie FROM lebensmittelkategorie ORDER BY Kategorie ASC") #alle Kategorien werden in alphabetischer Reihenfolge ausgelesen
	myresult = mycursor.fetchall()
	for row in chain.from_iterable(myresult):
		kategorien.append(row) #die Kategorie wird dem Array "kategorien" angehängt

		#es wird ein Array "zutat" erstellt, das alle Zutaten enthält, die der jeweiligen Kategorie zugeordnet wurden. Die Zutaten werden in alphabetische Reihenfolge gebracht
		zutat = []
		mycursor.execute("SELECT zutaten.Zutat FROM zutaten INNER JOIN lebensmittelkategorie ON lebensmittelkategorie.Kategorie_ID = zutaten.Kategorie_ID WHERE Kategorie = %s ORDER BY zutaten.Zutat ASC",(row,))
		res = mycursor.fetchall()
		for row in chain.from_iterable(res):
			zutat.append(row)
		kategorien.append(zutat) #das Array "zutat" wird dem Array "kategorien" angehängt
	return kategorien #der Rückgabewert dieser Funktion ist das Array "kategorien"


#Startseite
@app.route("/",methods=["GET","POST"])
def home():
	datum = datetime.datetime.now()
	vorhanden = vorhandenaktualisieren()
	kategorien = kategorien_aktualisieren()

	if request.method != "POST":
		kochbare_rezepte= kochbare_rezepte_aktualisieren()
	
	if request.method == 'POST':
		if request.headers.get("Referer").endswith("/dein_kuehlschrank") == True: #falls der Nutzer von der Seite "/dein_kuehlschrank" kommt, sollen folgende Schritte ausgeführt werden

			checked=request.form.getlist('lebensmittel') #in dem Array "checked" sind alle ausgewählten Zutaten aus dem Kühlschrank aufgelistet

			daseit = list(set(checked) - set(vorhanden)) #das Array "daseit" enthält alle Lebensmittel, die nur in dem Array "checked" vorhanden sind, aber nicht im Array "vorhanden". 
			#(das sind alle Lebensmittel, die der Nutzer soeben hinzugefügt hat)
			
			#falls es Lebensmittel gibt, die der Nutzer gerade hinzugefügt hat, wird die Tabelle "kuehlschrank" der Datenbank um einen neuen Eintag ergänzt
			if len(daseit) > 0:
				for lebensmittel in daseit:
					mycursor.execute("INSERT INTO kuehlschrank (`ZutatenID`, `da_seit`, `weg_seit`) VALUES ((SELECT ZutatenID FROM zutaten WHERE Zutat = %s),%s,NULL)",(lebensmittel,datum))
					mydb.commit()

			wegseit = list(set(vorhanden) - set(checked)) #das Array "wegseit" enthält alle Lebensmittel, die nun nicht mehr ausgewählt sind
			#falls das Array Lebensmittel enthält, wird der Eintrag in der Tabelle "kuehlschrank" um das aktuelle Datum in der Spalte "weg_seit" ergänzt
			if len(wegseit) > 0:
				for lebensmittel in wegseit:
					mycursor.execute("UPDATE `kuehlschrank` INNER JOIN zutaten ON kuehlschrank.ZutatenID = zutaten.ZutatenID SET weg_seit = %s WHERE Zutat = %s",(datum,lebensmittel)) 
					mydb.commit()
			
			kochbare_rezepte = kochbare_rezepte_aktualisieren()

		if request.headers.get("Referer").endswith("/neues_rezept") == True: #falls der Nutzer von der Seite "/neues_rezept" kommt, sollen folgende Schritte ausgeführt werden

			formular = request.form #das Array "formular" enthällt alle übermittelten Eingaben des Nutzers
			mengen = formular.getlist('menge') #alle Eingaben aus den Feldern mit dem Namen "menge" werden in dem Array "mengen" gespeichert
			lmittel = formular.getlist('lmittel') #alle Eingaben aus den Feldern mit dem Namen "lmittel" werden in dem Array "lmittel" gespeichert
			
			zu = formular['zubereitung'].replace("\r\n", "<>") #da es nur ein Eingabefeld für die Zubereitung gibt, muss kein Array erstellt werden. 
			#Falls der Nutzer mehrere Absätze geschrieben hat, werden diese durch die Zeichenfolge "<>" getrennt

			print(request.files['img'].filename)
			if "img" in request.files: #falls der Nutzer ein Bild hinzugefügt hat, sollen folgende Schritte ausgeführt werden
				file = request.files['img']
				if file.filename != "":
					if file and allowed_file(file.filename):
						# print("Bild")
						filename = secure_filename(file.filename)
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #das Bild wird im Order gespeichert, der am Anfange dieser Datei definiert wurde
						#das neue Rezept wird in die Datenbank eingetragen
						mycursor.execute("INSERT INTO rezept (`Rezeptname`,`Zubereitung`,`Dauer`,`Bilddatei`) VALUES (%s,%s,%s,%s)",(formular['rezeptname'],zu,formular['dauer'],file.filename))
						mydb.commit()
				else: #ansonsten wird das Rezept mit der Bilddatei "noimage.png" (Platzhalter) in die Datenbank eingetragen
					# print("Kein Bild")
					mycursor.execute("INSERT INTO rezept (`Rezeptname`,`Zubereitung`,`Dauer`,`Bilddatei`) VALUES (%s,%s,%s,'noimage.png')",(formular['rezeptname'],zu,formular['dauer']))
					mydb.commit()

			#da die bereits vorhandenen Zutaten ihre jeweilige Kategorie nicht mit abschickt, weil das Kategorie-Feld ausgegraut wird, kann es vorkommen, dass gar kein Feld mit dem Namen "kat" übermittelt wird
			if ('kat' in formular): #wenn es ein Element mit dem Namen "kat" im abgeschickten Formular gibt, wurde eine neue Zutat eingegeben
				for zutat in lmittel:
					men = mengen[lmittel.index(zutat)] #die zugehörige Menge, die für eine Zutat eingegeben wurde, befindet sich an der gleichen Stelle des Arrays "mengen", wie die Zutat im Array "lmittel"
					if zutat in (item for sublist in kategorien for item in sublist): #falls die eingegebe Zutat schon existiert
						mycursor.execute("INSERT INTO menge (`RezeptID`,`ZutatenID`,`Menge`) VALUES ((SELECT RezeptID FROM rezept WHERE Rezeptname = %s),(SELECT ZutatenID FROM zutaten WHERE Zutat = %s),%s)",(formular['rezeptname'],zutat,men))
						mydb.commit()
					else:
						#falls die Zutat noch nicht in der Datenbank existiert
						mycursor.execute("INSERT INTO zutaten (`Zutat`,`Kategorie_ID`) VALUES (%s,(SELECT Kategorie_ID FROM lebensmittelkategorie WHERE Kategorie = %s))",(zutat,formular.getlist('kat')[0]))
						mydb.commit()
						formular.getlist('kat').pop(0) #das erste Element der Liste wird gelöscht
						mycursor.execute("INSERT INTO menge (`RezeptID`,`ZutatenID`,`Menge`) VALUES ((SELECT RezeptID FROM rezept WHERE Rezeptname = %s),(SELECT ZutatenID FROM zutaten WHERE Zutat = %s),%s)",(formular['rezeptname'],zutat,men))
						mydb.commit()
						print(zutat +"gibt es noch nicht")

			else: #falls alle Zutaten des neues Rezeptes schon in der Datenbank existieren
				for zutat in lmittel:
					men = mengen[lmittel.index(zutat)]
					mycursor.execute("INSERT INTO menge (`RezeptID`,`ZutatenID`,`Menge`) VALUES ((SELECT RezeptID FROM rezept WHERE Rezeptname = %s),(SELECT ZutatenID FROM zutaten WHERE Zutat = %s),%s)",(formular['rezeptname'],zutat,men))
					mydb.commit()
			

			kochbare_rezepte= kochbare_rezepte_aktualisieren()
	
	#der Benutzer wird auf die Datei index.html weitergeleitet. Dabei werden die Parameter vorhanden und kochbare_rezepte mitgegeben
	return render_template("index.html",vorhanden=vorhandenaktualisieren(), rez = kochbare_rezepte)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Dein Kühlschrank
@app.route("/dein_kuehlschrank", methods=["GET","POST"])
def dein_kuehlschrank():
	vorhanden = vorhandenaktualisieren()
	allerezepte = allerezepteaktualisieren()
	kategorien = kategorien_aktualisieren()
	return render_template("dein_kuehlschrank.html",zutaten=kategorien,vorhanden=vorhanden)


#Rezept
@app.route("/rezept", methods=["GET","POST"])
def rezept():

	if request.method =="POST":
		#der Text des angeklickten Rezeptes (also der Rezeptname) wird ausgelesen
		name=request.form["rezept"]
		
		#alle Zutaten und Mengen, die für das Rezept benötigt werden, werden im Array menge gespeichert
		#dieses Array hat folgende Form: menge=[(menge,Zutat1),(menge,Zutat2),...]
		menge=[]
		mycursor.execute("SELECT menge.Menge,zutaten.Zutat FROM menge INNER JOIN zutaten ON menge.ZutatenID = zutaten.ZutatenID INNER JOIN rezept ON menge.RezeptID = rezept.RezeptID WHERE Rezeptname=%s",(name,))
		menge = mycursor.fetchall()

		#die Variablen "dauer" und "zubereitung" werden definiert
		allerezepte = allerezepteaktualisieren()
		for ind in range(0,len(allerezepte),2): #nur jeder zweiter Eintrag des Arrays "allerezepte" wird iteriert
			if name in allerezepte[ind]: #falls der Rezeptname im Array zu finden ist, befindet sich die Dauer an zweiter und die Zubereitung an dritter Stelle 
				dauer = allerezepte[ind][1]
				zubereitung=allerezepte[ind][2].split("<>")
				bilddatei = allerezepte[ind][3]
	# der Benutzer wird auf die Datei rezept.html weitergeleitet. Dabei werden die Parameter rezeptname, zubereitung, menge und dauer mitgegeben
	return render_template("rezept.html",name=name,zubereitung=zubereitung,menge=menge,dauer=dauer,datei=bilddatei)


#Neues Rezept hinzufügen
@app.route("/neues_rezept", methods=["GET","POST"])
def neues_rezept():
	kategorien = kategorien_aktualisieren()
	allezutaten = []
	for i in range(len(kategorien)):
		if (i%2 != 0):
			for leb in kategorien[i]:
				allezutaten.append(leb)
	allezutaten.sort()
		
	return render_template("neues_rezept.html",kategorien=kategorien,allezutaten=allezutaten)

if __name__ == "__main__":
	app.run()