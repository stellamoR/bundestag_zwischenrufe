# Aufgabe 2.1: Prediction von Einwürfen

## Ziel
Ein Modell entwickeln, das die Wahrscheinlichkeit von Einwürfen und die Partei des Kommentators vorhersagen kann.

# Aufgabe 2.1: Prediction von Einwürfen

## Ziel
Ein Modell entwickeln, das die Wahrscheinlichkeit von Einwürfen und die Partei des Kommentators vorhersagen kann.

## 1. Modellauswahl (z.B. BERT Kontextwindow von 512 Wörtern)
- Auf Huggingface ein vortrainiertes Modell finden, das
    - einzelne Wörter predicted - schauen, was sich eventuell auf <interruption_[party]> abbilden lässt (schon ähnlich ist)
    - oder Positionstags ausgibt z.B. Satzenden vorhersagt oder Absätze vorhersagt etc.
- Doku: Warum wir das Modell ausgewählt haben und Alternativen verlinken.
    
## 2. Data Preparation
- Daten auf das Modell aus 1. anpassen. Was sind die Inputs? Braucht man bestimmte Tags für das Modell (siehe Foliensatz RAG bei Beispielprompts). 
- Basically alle Kommentare innerhalb der speeches durch Tokens (<interruption_[party]>) ersetzen (RegEx aus parsing notebook benutzen, evtl abändern)

## 3. Modell Finetunen
- Welche Loss-Funktion eignet sich, ist die evtl. im vortrainierten Modell schon enthalten?
- Lohnt es sich die Redner-Partei als eigenen Tag oder als Kontext im Input <inzuzufügen? Wie würde das im Modell gehen?
- Modell und Daten in Google Colab reinladen (vermutlich über transformers library)
- Modell finetunen. Wahrscheinlich Überschneidungen zum Übungsnotebook BERT finetuning.

## (Optional je nach in 1. gewähltem Modell) 4. Vorhersage der Partei des Kommentators
- Multiklassen-Klassifikationsmodell verwenden, um die Partei des Kommentators basierend auf der Position zu bestimmen, bei der ein Einwurf vorhergesagt wurde

## 6. Evaluierung

### Performance Metriken
- Leistung des Modells/der Modelle bewerten.
- Performance Metriken für Wortvorhersage herausfinden und auf 1. Modell anwenden
- (optional, je nach in 1. gewähltem Modell): accuracy, percision, f1-score auf Klassifikationsmodell anwenden
