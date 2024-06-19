# Project Sheet: "Bühne Bundestag: Die Tonlage der Debatte"

Team-Mitglieder:

* Linh Tran Quang tranquangli88949@th-nuernberg.de 
* Edward Simonjan simonjaned87761@th-nuernberg.de
* Robin Sternberg sternbergro87782@th-nuernberg.de

## Motivation / Szenario

>"Pöbelein und Hetze erleben wir inzwischen einfach in jeder Sitzung" (Simone Strohmayr) 

Im Bayerischen Landtag wurde erst kürzlich eine Änderung im Abgeordnetengesetz verabschiedet, welche beleidigende Zwischenrufe mit einem Bußgeld von bis zu 4000€ belegt. Das Gesetz wurde über Koalitionsgrenzen hinweg von allen Parteien mit Ausnahme der AfD beschlossen. Störungen im parlamentarischen Betrieb sind also allgegenwärtig und behindern im schlimmsten Fall den demokratischen Prozess.  
Durch die offensichtlichen Probleme in Bayern stellt sich die Frage, wie es denn im Bundestag aussieht. Wird hier oft beleidigt? Welche Parteien und Politiker tendieren dazu, häufiger Zwischenrufe bei den Debatten zu machen? Wer unterbricht wen am öftesten? Gibt es klare Unterschiede zwischen Opposition und Regierung? Ist das Sentiment eher kritisch oder unterstützend? 

Diese Unterbrechungen lassen sich auch gut mit weiteren Informationen anreichern. Welche Themen (z.B. Bildung, Verteidigung etc.) sind besonders brisant, haben also besonders viele Zwischenrufe? Überhaupt, welche Themen nehmen wie viel Zeit im Bundestag ein?


## Daten

Zu all diesen Fragen gibt es zum Glück die überaus umfassenden Protokolle der Bundestagssitzungen. Neben der Mitschrift von Redebeiträgen und Tagesordnungspunkte, werden auch Zurufe und Beifallsbekundungen sorgfältig festgehalten. Und das seit 1949.
Dieser enorme Wissensschatz ist auf der [Website des Bundestags](https://www.bundestag.de/services/opendata) verfügbar.  

## Vorgehen

### Statistische Analyse
- Zählen der Zwischenrufe
  -  Aufschlüsselung nach Zeitpunkt, Partei, Redner etc.
  -  "Wer ruft wem am öftesten hinein?", "Gibt es Unterschiede zwischen Opposition und Regierung"
- Auszählen von Wörtern. Beispielsweise Schimpfwörter, "Inflation" etc. Beispielartikel der Zeit zu Schimpfwörtern [hier](https://www.zeit.de/kultur/2019-09/beleidigungen-bundestagsreden-arsch-arschloch-bundeswoerter)
- Klassische Wordcloud-Analysen.

### ML-Task 1: Sentimentanalyse
- Sentimentanalyse auf den Zwischenrufen
- Einige Daten selbst labeln und dann ein Modell trainieren. Dieses Modell dann auf die ungelabelten Zwischenrufe anwenden.
- Passt gut zur statistischen Analyse -> Danach kann man nicht nur beantworten: "Wer ruft wem hinein?", sondern "Ist der Einwurf untersützend, oder kritisch?"

### ML-Task 2: Prediction und Generation von Einwürfen
#### Teil 1
- Wann wird unterbrochen?
- Textinput -> Vorhersage, an welcher Stelle es wahrscheinlich ist, dass jemand reinruft.
- Dabei soll auch vorhergesagt werden, welcher Partei der Kommentator angehört.
#### Teil 2
- Was wird reingerufen?
- Modell erhält Informationen über aktuellen Redner, den Text der bisherigen Rede und die Parteizugehörigkeit des Störers. Jetzt soll ein Zwischenruf formuliert werden. 

#### Zusammenspiel von Teil 1 und Teil 2
- Eingabe einer Demo-Rede -> Das Modell fügt eigens formulierte Unterbrechungen an passenden Stellen ein.

