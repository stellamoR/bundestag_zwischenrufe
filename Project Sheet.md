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
- Einige Daten selbst labeln und dann ein Modell trainieren. Dieses Modell dann auf die ungelabelten Zwischenrufe anwenden. Welches wir wählen, klären wir noch mit den Dozenten
- Passt gut zur statistischen Analyse -> Danach kann man nicht nur beantworten: "Wer ruft wem hinein?", sondern "Ist der Einwurf untersützend, oder kritisch?"

### ML-Task 2: Klassifikation
- Klassifikation von Reden und Tagesordnungspunkten auf Themenbereiche der Politik. z.B. Bildung, Verteidigung, etc.
- Hier kann das labeln dadurch abgekürzt werden, dass nicht der Fließtext der Reden selbst händisch gelabelt werden, sondern nur der dazugehörige Tagesordnungspunkt für das Labeln genutzt wird.
- Auch hier ist die Art des Modells noch nicht geklärt, für lange Reden eignen sich aber vermutlich eher LLMs.
- Fragestellungen:
  - "Womit beschäftigt sich der Bundestag wie viel?"
  - In Zusammenhang mit der statistischen Analyse und ML-Task 1: "Welche Themen sind besonders brisant?"


## Fragen

Welche Modelle eignen sich für die Fragestellungen am besten?
