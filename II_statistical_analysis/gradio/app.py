"""Interactive dashboard for the Bundestag speech and interruption data."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import gradio as gr
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parents[1]
DATA_DIR = REPO_ROOT / "_data"

PARTIES = ["CDU/CSU", "SPD", "GRÜNE", "FDP", "AfD", "DIE LINKE", "fraktionslos"]
PARTY_COLORS = {
    "CDU/CSU": "#232323", "SPD": "#e3000f", "GRÜNE": "#46962b",
    "FDP": "#ffed00", "AfD": "#009ee0", "DIE LINKE": "#be3075",
    "fraktionslos": "#7a7a7a",
}
PLOT_TEMPLATE = "plotly_white"
HEATMAP = "Heatmap: Wer unterbricht wen?"
# Gradio forces Plotly to fill its container, so the heatmap's square shape is
# fixed by these pixel sizes plus the matching max-width in CSS below.
HEATMAP_GRID_PX = 470
HEATMAP_MARGIN = {"l": 110, "r": 120, "t": 140, "b": 30}
HEATMAP_WIDTH_PX = HEATMAP_MARGIN["l"] + HEATMAP_GRID_PX + HEATMAP_MARGIN["r"]


@dataclass(frozen=True)
class DashboardData:
    speeches: pd.DataFrame
    interruptions: pd.DataFrame
    periods: dict[str, dict]
    min_date: pd.Timestamp
    max_date: pd.Timestamp


def seat_weights(interruptions: pd.DataFrame, periods: dict[str, dict]) -> pd.Series:
    """Weight each interruption by 1 / seats of its party in the Bundestag sitting that day.

    Summing these weights normalizes by seats even across several Bundestag
    periods. Comments from parties without seats get NaN and are left out.
    """
    ordered = sorted(periods, key=lambda period: periods[period]["start_date"])
    starts = pd.to_datetime([periods[period]["start_date"] for period in ordered])
    # Each day belongs to the most recent period that had started by then.
    positions = starts.searchsorted(interruptions["date"], side="right") - 1
    seats = pd.DataFrame(
        {period: pd.Series(periods[period]["num_seats"], dtype="float64") for period in ordered}
    ).replace(0, np.nan)
    weights = pd.Series(np.nan, index=interruptions.index)
    for position, period in enumerate(ordered):
        in_period = positions == position
        weights[in_period] = 1 / interruptions.loc[in_period, "comment_party"].map(seats[period])
    return weights


def load_data() -> DashboardData:
    """Load generated files independently of the current working directory."""
    speeches = pd.read_csv(DATA_DIR / "speeches.csv", encoding="utf-8")
    interruptions = pd.read_csv(DATA_DIR / "interruptions.csv", encoding="utf-8")
    speeches = speeches.drop(columns=["Unnamed: 0"], errors="ignore")
    interruptions = interruptions.drop(columns=["Unnamed: 0"], errors="ignore")
    speeches["date"] = pd.to_datetime(speeches["date"], errors="coerce")
    interruptions["date"] = pd.to_datetime(interruptions["date"], errors="coerce")
    speeches = speeches.dropna(subset=["date"])
    interruptions = interruptions.dropna(subset=["date"])
    speeches["year"] = speeches["date"].dt.year
    interruptions["year"] = interruptions["date"].dt.year

    with (DATA_DIR / "bt_period_data.json").open("r", encoding="utf-8") as input_file:
        periods = json.load(input_file)
    interruptions["seat_weight"] = seat_weights(interruptions, periods)
    return DashboardData(
        speeches=speeches,
        interruptions=interruptions,
        periods=periods,
        min_date=min(speeches["date"].min(), interruptions["date"].min()),
        max_date=max(speeches["date"].max(), interruptions["date"].max()),
    )


DATA = load_data()
MIN_YEAR = int(DATA.min_date.year)
MAX_YEAR = int(DATA.max_date.year)
PERIOD_CHOICES = [
    (f"{DATA.periods[period]['start_date'][:4]}–{DATA.periods[period]['end_date'][:4]} "
     f"({period}. Bundestag)", period)
    for period in sorted(DATA.periods, key=int)
]
DEFAULT_PERIOD = PERIOD_CHOICES[-1][1]


def empty_figure(message: str) -> go.Figure:
    figure = go.Figure()
    figure.add_annotation(text=message, showarrow=False, font={"size": 17})
    figure.update_layout(template=PLOT_TEMPLATE, height=560, margin={"t": 55})
    return figure


def finish_figure(figure: go.Figure, y_title: str | None = None) -> go.Figure:
    figure.update_layout(
        template=PLOT_TEMPLATE, height=560, hovermode="x unified",
        legend_title_text="Partei", margin={"l": 55, "r": 25, "t": 75, "b": 55},
        # Plotly reverses legends of stacked charts by default; keep PARTIES order.
        legend_traceorder="normal",
    )
    if y_title:
        figure.update_yaxes(title=y_title, rangemode="tozero")
    return figure


SENTENCES_TOTAL = "Redeanteil: Gesamtanzahl der gesprochenen Sätze von allen Parteien"
SENTENCES_BY_PARTY = "Redeanteil: Gesamtanzahl der gesprochenen Sätze nach Partei"
INTERRUPTIONS_TOTAL = "Zwischenrufe: Gesamtanzahl der Zwischenrufe"
INTERRUPTIONS_BY_PARTY = "Zwischenrufe: Anzahl der Zwischenrufe nach Partei"
INTERRUPTIONS_STACKED = "Zwischenrufe: Zusammensetzung nach Partei (gestapelt)"
INTERRUPTIONS_SHARE = "Zwischenrufe: Anteil der Parteien an allen Zwischenrufen (%)"
YEAR_PLOT_CHOICES = [
    SENTENCES_TOTAL, SENTENCES_BY_PARTY,
    INTERRUPTIONS_TOTAL, INTERRUPTIONS_BY_PARTY,
    INTERRUPTIONS_STACKED, INTERRUPTIONS_SHARE,
]


def interruptions_per_party_year(start_year: int, end_year: int) -> pd.DataFrame:
    """Count interruptions per year and party, with explicit zeros for area charts."""
    counts = (DATA.interruptions.loc[DATA.interruptions["year"].between(start_year, end_year)]
              .groupby(["year", "comment_party"]).size())
    parties = [party for party in PARTIES if party in counts.index.get_level_values("comment_party")]
    years = sorted(counts.index.get_level_values("year").unique())
    full_index = pd.MultiIndex.from_product([years, parties], names=["year", "comment_party"])
    return counts.reindex(full_index, fill_value=0).rename("interruptions").reset_index()


def render_year_plot(plot_type: str, start_year: int, end_year: int) -> go.Figure:
    start_year, end_year = int(start_year), int(end_year)
    if start_year > end_year:
        return empty_figure("Das Startjahr muss vor dem Endjahr liegen.")
    if plot_type == SENTENCES_TOTAL:
        frame = (DATA.speeches.loc[DATA.speeches["year"].between(start_year, end_year)]
                 .groupby("year", as_index=False)["speech_len_sents"].sum())
        figure = px.line(frame, x="year", y="speech_len_sents", markers=True,
                         title="Gesprochene Sätze pro Jahr",
                         labels={"year": "Jahr", "speech_len_sents": "Sätze"})
        return finish_figure(figure, "Sätze")
    if plot_type == SENTENCES_BY_PARTY:
        frame = (DATA.speeches.loc[DATA.speeches["year"].between(start_year, end_year)]
                 .groupby(["year", "speaker_party"], as_index=False)["speech_len_sents"].sum())
        figure = px.line(
            frame, x="year", y="speech_len_sents", color="speaker_party", markers=True,
            category_orders={"speaker_party": PARTIES}, color_discrete_map=PARTY_COLORS,
            title="Gesprochene Sätze nach Partei und Jahr",
            labels={"year": "Jahr", "speech_len_sents": "Sätze", "speaker_party": "Partei"},
        )
        return finish_figure(figure, "Sätze")
    if plot_type == INTERRUPTIONS_TOTAL:
        frame = (DATA.interruptions.loc[DATA.interruptions["year"].between(start_year, end_year)]
                 .groupby("year").size().rename("interruptions").reset_index())
        figure = px.line(frame, x="year", y="interruptions", markers=True,
                         title="Zwischenrufe pro Jahr",
                         labels={"year": "Jahr", "interruptions": "Zwischenrufe"})
        return finish_figure(figure, "Zwischenrufe")

    frame = interruptions_per_party_year(start_year, end_year)
    if frame.empty:
        return empty_figure("Für diesen Zeitraum liegen keine Zwischenrufe vor.")
    labels = {"year": "Jahr", "interruptions": "Zwischenrufe", "comment_party": "Partei"}
    plot_style = {"x": "year", "y": "interruptions", "color": "comment_party", "labels": labels,
                  "category_orders": {"comment_party": PARTIES},
                  "color_discrete_map": PARTY_COLORS}
    if plot_type == INTERRUPTIONS_STACKED:
        figure = px.area(frame, title="Zwischenrufe nach Partei und Jahr (gestapelt)", **plot_style)
        return finish_figure(figure, "Zwischenrufe")
    if plot_type == INTERRUPTIONS_SHARE:
        figure = px.area(frame, groupnorm="percent",
                         title="Anteil der Parteien an allen Zwischenrufen pro Jahr", **plot_style)
        figure.update_traces(hovertemplate="%{y:.1f} %<extra>%{fullData.name}</extra>")
        figure = finish_figure(figure, "Anteil der Zwischenrufe (%)")
        figure.update_yaxes(range=[0, 100], ticksuffix=" %")
        return figure

    figure = px.line(frame, markers=True, title="Zwischenrufe nach Partei und Jahr", **plot_style)
    return finish_figure(figure, "Zwischenrufe")


def parse_date_range(start_value: str, end_value: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    try:
        start = pd.Timestamp(start_value).normalize()
        end = pd.Timestamp(end_value).normalize()
    except (TypeError, ValueError) as error:
        raise gr.Error("Bitte Daten im Format JJJJ-MM-TT eingeben.") from error
    if start > end:
        raise gr.Error("Das Startdatum muss vor dem Enddatum liegen.")
    return start, end


def selected_range(use_period: bool, period: str, start_value: str,
                   end_value: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    if use_period:
        configured = DATA.periods[str(period)]
        return parse_date_range(configured["start_date"], configured["end_date"])
    return parse_date_range(start_value, end_value)


def seat_counts(period: str) -> pd.Series:
    return pd.Series(DATA.periods[str(period)]["num_seats"], dtype="float64").reindex(PARTIES)


def default_parties(period: str) -> list[str]:
    """Select represented parliamentary groups, but not independents."""
    seats = seat_counts(period)
    return [party for party in PARTIES if party != "fraktionslos" and seats.get(party, 0) > 0]


def party_bar(frame: pd.DataFrame, normalize_seats: bool,
              selected_parties: list[str]) -> go.Figure:
    counts = frame.groupby("comment_party").size().reindex(selected_parties, fill_value=0).astype(float)
    title, y_title = "Zwischenrufe nach Partei", "Zwischenrufe"
    if normalize_seats:
        counts = (frame.groupby("comment_party")["seat_weight"].sum(min_count=1)
                  .reindex(selected_parties))
        title, y_title = "Zwischenrufe pro Sitz", "Zwischenrufe pro Sitz"
    visible = counts.dropna()
    figure = go.Figure(go.Bar(
        x=visible.index, y=visible.values,
        marker_color=[PARTY_COLORS[party] for party in visible.index],
        hovertemplate="%{x}<br>%{y:,.2f}<extra></extra>",
    ))
    figure.update_layout(title=title, xaxis_title="Partei", showlegend=False)
    return finish_figure(figure, y_title)


def interruption_matrix(frame: pd.DataFrame, normalize_seats: bool,
                        normalize_sentences: bool,
                        selected_parties: list[str], show_values: bool) -> go.Figure:
    if normalize_seats:
        matrix = frame.pivot_table(index="interrupted_speaker_party", columns="comment_party",
                                   values="seat_weight", aggfunc="sum")
        matrix = matrix.reindex(index=selected_parties, columns=selected_parties)
    else:
        matrix = pd.crosstab(frame["interrupted_speaker_party"], frame["comment_party"])
        matrix = matrix.reindex(index=selected_parties, columns=selected_parties, fill_value=0).astype(float)
    if normalize_sentences:
        sentence_counts = (frame.drop_duplicates("speech_id")
                           .groupby("interrupted_speaker_party")["speech_len_sents"].sum()
                           .reindex(selected_parties).replace(0, np.nan))
        matrix = matrix.div(sentence_counts, axis="index") * 1_000

    active_rows = matrix.notna().any(axis=1) & matrix.fillna(0).ne(0).any(axis=1)
    active_columns = matrix.notna().any(axis=0) & matrix.fillna(0).ne(0).any(axis=0)
    matrix = matrix.loc[active_rows, active_columns]
    if matrix.empty:
        return empty_figure("Für diesen Zeitraum liegen keine Zwischenrufe vor.")
    units = "Zwischenrufe"
    if normalize_seats and normalize_sentences:
        units = "Zwischenrufe je Sitz und 1.000 Sätze"
    elif normalize_seats:
        units = "Zwischenrufe je Sitz"
    elif normalize_sentences:
        units = "Zwischenrufe je 1.000 Sätze"
    figure = px.imshow(
        matrix, color_continuous_scale="Blues", aspect="equal",
        text_auto=".2f" if show_values else False,
        title=f"Wer unterbricht wen? · {units}",
        labels={"x": "Partei der Zwischenrufenden", "y": "Partei der Redenden", "color": units},
    )
    # The x-axis sits on top, so its title needs room below the figure title.
    figure.update_layout(
        template=PLOT_TEMPLATE, width=HEATMAP_WIDTH_PX,
        height=HEATMAP_MARGIN["t"] + HEATMAP_GRID_PX + HEATMAP_MARGIN["b"],
        title={"y": 0.97, "yanchor": "top"}, margin=HEATMAP_MARGIN,
        coloraxis_colorbar={"x": 1, "xanchor": "left", "xpad": 14, "thickness": 18,
                            "title": {"side": "right"}},
    )
    # Square cells; any leftover space stays on the right/bottom.
    figure.update_xaxes(side="top", constrain="domain", constraintoward="left")
    figure.update_yaxes(constrain="domain", constraintoward="top", ticklabelstandoff=8)
    figure.update_xaxes(ticklabelstandoff=4)
    return figure


def render_detail_plot(plot_type: str, custom_dates: bool, period: str,
                       start_value: str, end_value: str, normalize_seats: bool,
                       normalize_sentences: bool, selected_parties: list[str],
                       show_values: bool) -> tuple[go.Figure, str]:
    start, end = selected_range(not custom_dates, period, start_value, end_value)
    frame = DATA.interruptions.loc[DATA.interruptions["date"].between(start, end)].copy()
    selected_parties = [party for party in PARTIES if party in (selected_parties or [])]
    if not selected_parties:
        return empty_figure("Bitte mindestens eine Partei auswählen."), "Keine Partei ausgewählt."
    if plot_type == "Zwischenrufe nach Partei":
        frame = frame.loc[frame["comment_party"].isin(selected_parties)]
    else:
        frame = frame.loc[
            frame["comment_party"].isin(selected_parties)
            & frame["interrupted_speaker_party"].isin(selected_parties)
        ]
    if frame.empty:
        return empty_figure("Für diesen Zeitraum liegen keine Zwischenrufe vor."), "Keine Daten im gewählten Zeitraum."
    figure = (party_bar(frame, normalize_seats, selected_parties)
              if plot_type == "Zwischenrufe nach Partei"
              else interruption_matrix(
                  frame, normalize_seats, normalize_sentences,
                  selected_parties, show_values,
              ))
    summary = (
        f"**{start.date():%d.%m.%Y}–{end.date():%d.%m.%Y}** · "
        f"**{len(frame):,}** Zwischenrufe"
    ).replace(",", ".")
    return figure, summary


def update_period_info(period: str) -> str:
    configured = DATA.periods[str(period)]
    return f"{period}. Bundestag · {configured['start_date']} bis {configured['end_date']}"


def update_period(period: str):
    return update_period_info(period), gr.update(value=default_parties(period))


SEAT_WEIGHTING_INFO = (
    "Bei Normalisierung nach Sitzen über mehrere Bundestagsperioden hinweg werden die "
    "Zwischenrufe einzeln gewichtet: Jeder Zwischenruf zählt 1 / Sitzzahl seiner Partei "
    "in dem Bundestag, der an diesem Tag getagt hat."
)


def update_detail_controls(plot_type: str, custom_dates: bool):
    return (
        gr.update(visible=not custom_dates),
        gr.update(visible=not custom_dates),
        gr.update(info=SEAT_WEIGHTING_INFO if custom_dates else ""),
        gr.update(visible=custom_dates),
        gr.update(visible=custom_dates),
        gr.update(visible=plot_type == HEATMAP),
        gr.update(visible=plot_type == HEATMAP),
        gr.update(elem_classes=["heatmap-plot"] if plot_type == HEATMAP else []),
    )


# Attribution and change notice required by the Bundestag's terms of use (DIP).
SOURCE_NOTICE = (
    "Datenquelle: Plenarprotokolle und Stammdaten des Deutschen Bundestages "
    "([DIP](https://dip.bundestag.de), [Open Data](https://www.bundestag.de/services/opendata)). "
    "Die Protokolle wurden für dieses Dashboard maschinell aufbereitet und verändert "
    "(Extraktion von Reden und Zwischenrufen, Zuordnung zu Parteien, Aggregation); "
    "maßgeblich sind die Originalprotokolle. "
    "Auswertung und Visualisierungen lizenziert unter "
    "[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de)."
)

# Gradio follows the system's dark mode unless the URL asks for the light theme.
FORCE_LIGHT_MODE_JS = """
() => {
    const url = new URL(window.location.href);
    if (url.searchParams.get("__theme") !== "light") {
        url.searchParams.set("__theme", "light");
        window.location.replace(url.href);
    }
}
"""

CSS = f"""
.gradio-container {{width: calc(100% - 48px) !important; max-width: 1680px !important; min-width: 1080px; margin: 0 auto !important;}}
.dashboard-title {{margin-bottom: 0 !important;}}
.dashboard-subtitle {{color: #5f6570; margin-top: 0 !important;}}
.source-notice {{color: #5f6570; font-size: 0.85em; margin-top: 12px !important;}}
.desktop-row {{display: flex !important; flex-wrap: nowrap !important; gap: 24px !important; align-items: flex-start !important;}}
.control-panel {{flex: 0 0 350px !important; min-width: 350px !important; max-width: 350px !important; border: 1px solid #e4e7eb; border-radius: 14px; padding: 16px;}}
.plot-panel {{flex: 1 1 auto !important; min-width: 680px !important;}}
.plot-panel .plot-container {{min-height: 600px !important;}}
.heatmap-plot {{max-width: {HEATMAP_WIDTH_PX}px !important; margin-left: 0 !important; margin-right: auto !important;}}
.heatmap-plot .plot-container {{min-height: 0 !important;}}
"""


def build_app() -> gr.Blocks:
    with gr.Blocks(css=CSS, js=FORCE_LIGHT_MODE_JS, title="Bundestag · Reden und Zwischenrufe",
                   fill_width=True) as dashboard:
        gr.Markdown("# Bundestag: Reden und Zwischenrufe", elem_classes="dashboard-title")
        gr.Markdown(
            f"Interaktive Auswertung der Plenarprotokolle von **{DATA.min_date.date():%d.%m.%Y}** "
            f"bis **{DATA.max_date.date():%d.%m.%Y}**.", elem_classes="dashboard-subtitle",
        )
        with gr.Tabs():
            with gr.Tab("Zeitverlauf"):
                with gr.Row(elem_classes="desktop-row"):
                    with gr.Column(scale=1, elem_classes="control-panel"):
                        year_plot_type = gr.Dropdown(
                            YEAR_PLOT_CHOICES, value=INTERRUPTIONS_BY_PARTY, label="Darstellung")
                        start_year = gr.Slider(MIN_YEAR, MAX_YEAR, value=MIN_YEAR, step=1, label="Von Jahr")
                        end_year = gr.Slider(MIN_YEAR, MAX_YEAR, value=MAX_YEAR, step=1, label="Bis Jahr")
                        refresh_year = gr.Button("Diagramm aktualisieren", variant="primary")
                    with gr.Column(elem_classes="plot-panel"):
                        year_plot = gr.Plot(show_label=False)
            with gr.Tab("Aggregierte Darstellungen von Zwischenrufen"):
                with gr.Row(elem_classes="desktop-row"):
                    with gr.Column(scale=1, elem_classes="control-panel"):
                        detail_plot_type = gr.Dropdown(
                            [HEATMAP, "Zwischenrufe nach Partei"],
                            value=HEATMAP, label="Darstellung")
                        period = gr.Dropdown(PERIOD_CHOICES, value=DEFAULT_PERIOD, label="Bundestagsperiode")
                        custom_dates = gr.Checkbox(
                            value=False, label="Benutzerdefiniertes Start- und Enddatum eingeben")
                        start_date = gr.Textbox(value=str(DATA.min_date.date()), label="Startdatum",
                                                info="JJJJ-MM-TT", visible=False)
                        end_date = gr.Textbox(value=str(DATA.max_date.date()), label="Enddatum",
                                              info="JJJJ-MM-TT", visible=False)
                        period_info = gr.Markdown(update_period_info(DEFAULT_PERIOD))
                        normalize_seats = gr.Checkbox(value=False, label="Nach Sitzen der unterbrechenden Partei normalisieren")
                        normalize_sentences = gr.Checkbox(value=False, label="Nach gesprochenen Sätzen der unterbrochenen Partei normalisieren")
                        selected_parties = gr.CheckboxGroup(
                            choices=PARTIES,
                            value=default_parties(DEFAULT_PERIOD),
                            label="Parteien",
                            info="Standard: Parteien mit Sitzen; fraktionslos abgewählt",
                        )
                        show_values = gr.Checkbox(value=False, label="Werte in der Heatmap anzeigen")
                        refresh_detail = gr.Button("Diagramm aktualisieren", variant="primary")
                    with gr.Column(elem_classes="plot-panel"):
                        detail_summary = gr.Markdown()
                        detail_plot = gr.Plot(show_label=False, elem_classes=["heatmap-plot"])

        gr.Markdown(SOURCE_NOTICE, elem_classes="source-notice")

        year_inputs = [year_plot_type, start_year, end_year]
        detail_inputs = [detail_plot_type, custom_dates, period, start_date, end_date,
                         normalize_seats, normalize_sentences, selected_parties, show_values]
        refresh_year.click(render_year_plot, inputs=year_inputs, outputs=year_plot)
        refresh_detail.click(render_detail_plot, inputs=detail_inputs, outputs=[detail_plot, detail_summary])
        dashboard.load(render_year_plot, inputs=year_inputs, outputs=year_plot)
        dashboard.load(render_detail_plot, inputs=detail_inputs, outputs=[detail_plot, detail_summary])

        year_plot_type.change(render_year_plot, inputs=year_inputs, outputs=year_plot)
        start_year.release(render_year_plot, inputs=year_inputs, outputs=year_plot)
        end_year.release(render_year_plot, inputs=year_inputs, outputs=year_plot)

        for control in [detail_plot_type, custom_dates]:
            control.change(
                update_detail_controls,
                inputs=[detail_plot_type, custom_dates],
                outputs=[period, period_info, custom_dates, start_date, end_date, normalize_sentences, show_values, detail_plot],
            ).then(
                render_detail_plot,
                inputs=detail_inputs,
                outputs=[detail_plot, detail_summary],
            )
        period.change(
            update_period,
            inputs=period,
            outputs=[period_info, selected_parties],
        ).then(
            render_detail_plot,
            inputs=detail_inputs,
            outputs=[detail_plot, detail_summary],
        )
        for control in [
            normalize_seats,
            start_date,
            end_date,
            normalize_sentences,
            selected_parties,
            show_values,
        ]:
            control.change(
                render_detail_plot,
                inputs=detail_inputs,
                outputs=[detail_plot, detail_summary],
            )
    return dashboard


demo = build_app()

if __name__ == "__main__":
    demo.launch()
