-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 28. Okt 2020 um 11:07
-- Server-Version: 10.1.31-MariaDB
-- PHP-Version: 7.2.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `codecompetition`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `kuehlschrank`
--

CREATE TABLE `kuehlschrank` (
  `ZutatenID` int(4) NOT NULL,
  `da_seit` varchar(32) NOT NULL,
  `weg_seit` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `lebensmittelkategorie`
--

CREATE TABLE `lebensmittelkategorie` (
  `Kategorie_ID` int(4) NOT NULL,
  `Kategorie` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Daten für Tabelle `lebensmittelkategorie`
--

INSERT INTO `lebensmittelkategorie` (`Kategorie_ID`, `Kategorie`) VALUES
(0, 'Sonstiges'),
(1, 'Obst und Gemüse'),
(2, 'Getreideprodukte'),
(3, 'Fleisch und Fisch'),
(4, 'Milchprodukte'),
(5, 'Teigwaren'),
(6, 'Gewürze und Kräuter'),
(7, 'Öl und Fette'),
(8, 'Süßwaren'),
(9, 'Hülsenfrüchte, Nüsse und Samen'),
(10, 'Früchte');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `log_vorschlaege`
--

CREATE TABLE `log_vorschlaege` (
  `RezeptID` int(4) NOT NULL,
  `Vorgeschlagen` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `menge`
--

CREATE TABLE `menge` (
  `RezeptID` int(4) NOT NULL,
  `ZutatenID` int(4) NOT NULL,
  `Menge` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Daten für Tabelle `menge`
--

INSERT INTO `menge` (`RezeptID`, `ZutatenID`, `Menge`) VALUES
(1, 1, '1,25 kg'),
(1, 2, '2 EL'),
(1, 3, '250 g'),
(1, 4, '150 g'),
(1, 5, '150 g'),
(1, 6, '2 TL'),
(1, 7, '2 EL'),
(1, 8, '2 EL'),
(2, 11, '250 g'),
(2, 12, '1/2'),
(2, 13, '180 g'),
(2, 14, '1'),
(2, 15, '1 Msp'),
(2, 16, '2 EL'),
(2, 17, '2 EL'),
(2, 18, '500 g'),
(3, 12, '2'),
(4, 28, '1 kg'),
(4, 21, '1 kleine'),
(4, 22, '1 Zehe'),
(4, 23, '1 TL'),
(4, 24, '1 TL'),
(4, 25, '100 ml'),
(4, 26, '100 ml'),
(4, 27, '100 g'),
(4, 20, '120 g'),
(4, 10, 'etwas'),
(3, 9, 'etwas'),
(1, 9, 'etwas'),
(2, 9, 'etwas'),
(4, 9, 'etwas'),
(10, 31, '500 g'),
(10, 32, '1 Pck'),
(10, 3, '50 g'),
(10, 33, '200 g'),
(10, 9, 'etwas'),
(12, 34, '1'),
(12, 11, '500 g'),
(12, 35, '400 g'),
(12, 23, '50 g'),
(12, 9, 'etwas'),
(12, 36, '2 TL');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `rezept`
--

CREATE TABLE `rezept` (
  `RezeptID` int(4) NOT NULL,
  `Rezeptname` varchar(32) NOT NULL,
  `Zubereitung` varchar(1000) NOT NULL,
  `Dauer` varchar(10) NOT NULL,
  `Bilddatei` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Daten für Tabelle `rezept`
--

INSERT INTO `rezept` (`RezeptID`, `Rezeptname`, `Zubereitung`, `Dauer`, `Bilddatei`) VALUES
(1, 'Kürbisgratin', 'Den Backofen auf 200 Grad (Umluft 180 Grad) vorheizen. Kürbis waschen, halbieren, das Fruchtfleisch mitsamt den Kernen herauslösen und den Kürbis in 2,5 cm breite Spalten schneiden. Kürbisspalten in einer weiten Auflaufform verteilen, mit Öl beträufeln, salzen und pfeffern. Im Ofen ca. 15 Minuten garen, bis der Kürbis leicht gebräunt ist. <> Inzwischen die Tomaten abspülen, trocken tupfen und auf dem Kürbis verteilen. Halb getrocknete Tomaten etwas abtropfen lassen, Feta in Scheiben schneiden, etwas kleiner brechen und beides auf dem Kürbis verteilen. Fenchelsamen im Mörser grob zerstoßen, Kürbiskerne und Haselnusskerne grob hacken, mit Fenchel mischen und über den Kürbis streuen. 4 EL Öl von den halb getrockneten Tomaten darüberträufeln. Im Ofen weitere 10–15 Minuten backen.', '45 min', 'kuerbisgratin.jpg'),
(2, 'Pastinaken-Reibekuchen', 'Kartoffeln schälen, Apfel entkernen und alles zusammen mit den Pastinaken grob raspeln. Schalotte fein schneiden.<>\r\nMit den übrigen Zutaten bis auf das Öl vermischen und gegebenenfalls austretende Flüssigkeit wegschütten.<>\r\nDie Hälfte des Öls in einer großen Pfanne erhitzen und die Kartoffelmischung in Portionen teilen. Jede Portion von jeder Seite bei mittlerer Hitze 4 Minuten goldbraun braten. Die gebratenen Reibekuchen bei 80 Grad Umluft im Backofen warm halten.<>\r\nServieren Sie dazu Rollmöpse.', '35 min', 'pastinaken-reibekuchen.jpg'),
(3, 'Salzapfel süß', 'blabla', '2 h', 'salzapfel.jpg'),
(4, 'Rosenkohl-Gratin', 'Den Rosenkohl putzen, am Strunk einschneiden und die äußeren Blätter entfernen. Die Zwiebeln pellen und in kleine Würfel schneiden. Den Knoblauch pellen und eben-falls fein hacken.<>\r\nDie Butter in einem Topf bei geringer Hitze zerlassen und die Zwiebelwürfel sowie den Knoblauch darin anschwitzen.<>\r\nMit Sahne und Milch ablöschen und kurz aufkochen. Den Rosenkohl sowie den Kümmel in die kochende Flüssigkeit geben. Für 5-7 Minuten unter ständigem Rühren köcheln lassen. Den Rosenkohl anschließend mitsamt Soße in eine große Auflaufform geben.<>\r\nDen Bacon in feine Streifen schneiden und in einer beschichteten Pfanne ohne Zugabe von Fett knusprig braten. Den Bacon unter den Rosenkohl heben, den Pecorino reiben und über dem Kohl verteilen.<>\r\nDas Gratin bei 180°C Ober-/Unterhitze für 15 Minuten goldbraun backen und mit frischem Schnittlauchröllchen vor dem Servieren garnieren.', '30 min', 'rosenkohl-gratin.jpg'),
(10, 'Nudelauflauf', 'Die Nudeln kochen.<>Nudeln, Schinken und halbierte Tomaten in eine Form geben und mit Käse bestreuen.<>Nach Belieben würzen.<>Im Ofen bei 200° Heißluft für 30 Minuten backen.', '1h', 'nudelauflauf.jpg'),
(12, 'Steckrübeneintopf', 'Steckrübe in ca. 2-3 cm große Würfel schneiden. Karotten und Kartoffeln ebenfalls in Würfel schneiden.<>Butter in einem großen Topf glasig schmelzen und nach und nach Kartoffeln, Karotten und Rüben hinzugeben.<>Wenn alles leicht angebraten ist, 750ml Wasser hinzugeben.<>Mit Salz, Pfeffer und Majoran nach Belieben würzen.<>30 Minuten kochen lassen und mit etwas Petersilie anrichten.<>Dazu schmecken Gänsekeulen oder Kochwürste.', '45 min', 'Steckruebe.jpg');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `zutaten`
--

CREATE TABLE `zutaten` (
  `ZutatenID` int(4) NOT NULL,
  `Zutat` varchar(32) NOT NULL,
  `Kategorie_ID` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Daten für Tabelle `zutaten`
--

INSERT INTO `zutaten` (`ZutatenID`, `Zutat`, `Kategorie_ID`) VALUES
(1, 'Kürbis', 1),
(2, 'Olivenöl', 7),
(3, 'Rispentomate', 10),
(4, 'Tomaten, getrocknet, eingelegt', 10),
(5, 'Feta', 4),
(6, 'Fenchelsamen', 6),
(7, 'Kürbiskerne', 9),
(8, 'Haselnusskerne', 9),
(9, 'Salz und Pfeffer', 6),
(10, 'Schnittlauch', 6),
(11, 'Kartoffel', 0),
(12, 'Apfel', 1),
(13, 'Pastinake', 1),
(14, 'Schalotte', 1),
(15, 'Muskatnuss', 6),
(16, 'Weizenmehl', 2),
(17, 'Rapsöl', 7),
(18, 'Rollmops', 3),
(19, 'Tomaten, passiert', 10),
(20, 'Pecorino', 4),
(21, 'Zwiebel', 0),
(22, 'Knoblauch', 0),
(23, 'Butter', 7),
(24, 'Kümmel', 6),
(25, 'Sahne', 4),
(26, 'Milch', 4),
(27, 'Bacon', 3),
(28, 'Rosenkohl', 1),
(31, 'Nudeln', 5),
(32, 'Schinken', 3),
(33, 'geriebener Käse', 4),
(34, 'Steckrübe', 1),
(35, 'Karotten', 1),
(36, 'Majoran', 1);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `kuehlschrank`
--
ALTER TABLE `kuehlschrank`
  ADD KEY `zutid` (`ZutatenID`);

--
-- Indizes für die Tabelle `lebensmittelkategorie`
--
ALTER TABLE `lebensmittelkategorie`
  ADD PRIMARY KEY (`Kategorie_ID`);

--
-- Indizes für die Tabelle `log_vorschlaege`
--
ALTER TABLE `log_vorschlaege`
  ADD KEY `rez` (`RezeptID`) USING BTREE;

--
-- Indizes für die Tabelle `menge`
--
ALTER TABLE `menge`
  ADD KEY `rezeptid` (`RezeptID`),
  ADD KEY `zu` (`ZutatenID`);

--
-- Indizes für die Tabelle `rezept`
--
ALTER TABLE `rezept`
  ADD PRIMARY KEY (`RezeptID`);

--
-- Indizes für die Tabelle `zutaten`
--
ALTER TABLE `zutaten`
  ADD PRIMARY KEY (`ZutatenID`),
  ADD KEY `kategorie` (`Kategorie_ID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `rezept`
--
ALTER TABLE `rezept`
  MODIFY `RezeptID` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT für Tabelle `zutaten`
--
ALTER TABLE `zutaten`
  MODIFY `ZutatenID` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `kuehlschrank`
--
ALTER TABLE `kuehlschrank`
  ADD CONSTRAINT `zutid` FOREIGN KEY (`ZutatenID`) REFERENCES `zutaten` (`ZutatenID`);

--
-- Constraints der Tabelle `log_vorschlaege`
--
ALTER TABLE `log_vorschlaege`
  ADD CONSTRAINT `rez` FOREIGN KEY (`RezeptID`) REFERENCES `rezept` (`RezeptID`);

--
-- Constraints der Tabelle `menge`
--
ALTER TABLE `menge`
  ADD CONSTRAINT `rezeptid` FOREIGN KEY (`RezeptID`) REFERENCES `rezept` (`RezeptID`),
  ADD CONSTRAINT `zu` FOREIGN KEY (`ZutatenID`) REFERENCES `zutaten` (`ZutatenID`);

--
-- Constraints der Tabelle `zutaten`
--
ALTER TABLE `zutaten`
  ADD CONSTRAINT `katid` FOREIGN KEY (`Kategorie_ID`) REFERENCES `lebensmittelkategorie` (`Kategorie_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
