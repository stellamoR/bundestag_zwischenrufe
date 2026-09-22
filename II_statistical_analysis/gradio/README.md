# Bundestag dashboard

Interactive plots for the generated speech and interruption datasets.

## Local launch

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r II_statistical_analysis\gradio\requirements.txt
.\.venv\Scripts\python.exe II_statistical_analysis\gradio\app.py
```

Then open <http://127.0.0.1:7860>.

The app reads `_data/speeches.csv`, `_data/interruptions.csv`, and
`_data/bt_period_data.json`. Paths are resolved relative to the repository, so
the launch command also works from another current directory.

## Lizenz und Datenquellen

Dieses Projekt (Code, aufbereitete Daten und Auswertungen) steht unter der
[Creative Commons Namensnennung – Weitergabe unter gleichen Bedingungen 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.de).
Der vollständige Lizenztext liegt in [`LICENSE`](../../LICENSE).

**Quelle der Rohdaten:** Plenarprotokolle und Stammdaten der Abgeordneten des
Deutschen Bundestages, bezogen über das
[DIP](https://dip.bundestag.de) und das [Open-Data-Angebot des Bundestages](https://www.bundestag.de/services/opendata).
Die Protokolle sind amtliche Werke (§ 5 Abs. 2 UrhG) und selbst urheberrechtsfrei;
die CC-BY-SA-Lizenz gilt nur für die Beiträge dieses Projekts.

**Veränderungshinweis:** Die Daten in `_data/` (vom Dashboard gelesen) wurden maschinell aus den
Originalprotokollen extrahiert und verändert (Zerlegung in Reden und
Zwischenrufe, Zuordnung von Personen und Parteien, Aggregationen). Sie sind keine
amtliche Fassung; maßgeblich sind die Originalprotokolle des Bundestages.
