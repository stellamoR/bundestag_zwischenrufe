"""Interactive dashboard for the Bundestag speech and interruption data."""

from __future__ import annotations

import json
import inspect
import html
import re
from urllib.parse import quote
import warnings
from dataclasses import dataclass
from pathlib import Path

import gradio as gr
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity


APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parents[1]
DATA_DIR = REPO_ROOT / "_data"
LABELED_INTERRUPTION_PATH = DATA_DIR / "interruptions_labeled.parquet"

PARTIES = ["CDU/CSU", "SPD", "GRÜNE", "FDP", "AfD", "DIE LINKE", "BSW", "fraktionslos"]
PARTY_COLORS = {
    "CDU/CSU": "#232323", "SPD": "#e3000f", "GRÜNE": "#46962b",
    "FDP": "#ffed00", "AfD": "#009ee0", "DIE LINKE": "#be3075",
    "BSW": "#7d254f", "fraktionslos": "#7a7a7a",
}
COALITION_PARTY_ORDER = [
    "CDU/CSU", "SPD", "FDP", "GRÜNE", "DIE LINKE", "AfD", "BSW",
    "fraktionslos",
]
PLOT_TEMPLATE = "plotly_white"
HEATMAP = "Beziehungen zwischen Parteien"
# Gradio forces Plotly to fill its container, so the heatmap's square shape is
# fixed by these pixel sizes plus the matching max-width in CSS below.
HEATMAP_GRID_PX = 470
HEATMAP_MARGIN = {"l": 110, "r": 120, "t": 140, "b": 30}
HEATMAP_WIDTH_PX = HEATMAP_MARGIN["l"] + HEATMAP_GRID_PX + HEATMAP_MARGIN["r"]

# Gradio 5.50 warns that these options are moving to launch(), although its
# launch() method does not accept them yet. Support both the 5.x and 6.x APIs.
LAUNCH_ACCEPTS_PAGE_ASSETS = "css" in inspect.signature(gr.Blocks.launch).parameters


@dataclass(frozen=True)
class DashboardData:
    speeches: pd.DataFrame
    interruptions: pd.DataFrame
    periods: dict[str, dict]
    min_date: pd.Timestamp
    max_date: pd.Timestamp


def seat_weights(
    frame: pd.DataFrame, periods: dict[str, dict], party_column: str,
) -> pd.Series:
    """Return 1 / party seats for each row on the date of that Bundestag sitting.

    Parties without seats get NaN and are left out of normalized aggregates.
    """
    ordered = sorted(periods, key=lambda period: periods[period]["start_date"])
    starts = pd.to_datetime([periods[period]["start_date"] for period in ordered])
    # Each day belongs to the most recent period that had started by then.
    positions = starts.searchsorted(frame["date"], side="right") - 1
    seats = pd.DataFrame(
        {period: pd.Series(periods[period]["num_seats"], dtype="float64") for period in ordered}
    ).replace(0, np.nan)
    weights = pd.Series(np.nan, index=frame.index)
    for position, period in enumerate(ordered):
        in_period = positions == position
        weights[in_period] = 1 / frame.loc[in_period, party_column].map(seats[period])
    return weights


def load_data() -> DashboardData:
    """Load generated files independently of the current working directory."""
    speeches = pd.read_parquet(DATA_DIR / "speeches.parquet")
    interruptions = pd.read_parquet(DATA_DIR / "interruptions.parquet")
    speeches["date"] = pd.to_datetime(speeches["date"], errors="coerce")
    interruptions["date"] = pd.to_datetime(interruptions["date"], errors="coerce")
    speeches = speeches.dropna(subset=["date"])
    interruptions = interruptions.dropna(subset=["date"])
    speeches["year"] = speeches["date"].dt.year
    interruptions["year"] = interruptions["date"].dt.year

    with (DATA_DIR / "bt_period_data.json").open("r", encoding="utf-8") as input_file:
        periods = json.load(input_file)
    interruptions["seat_weight"] = seat_weights(interruptions, periods, "comment_party")
    speeches["seat_weight"] = seat_weights(speeches, periods, "speaker_party")
    speeches["sentences_per_seat"] = speeches["speech_len_sents"] * speeches["seat_weight"]
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
    for period in sorted(DATA.periods, key=int, reverse=True)
]
DEFAULT_PERIOD = PERIOD_CHOICES[0][1]


def train_negative_sentiment_model() -> tuple[TfidfVectorizer, LogisticRegression]:
    """Train a small CPU-only classifier from the project's manual labels."""
    labeled = pd.read_parquet(LABELED_INTERRUPTION_PATH)
    labeled = labeled.dropna(subset=["comment_text", "sentiment"])
    texts = labeled["comment_text"].astype(str)
    negative = labeled["sentiment"].astype(int).eq(1).astype(int)
    vectorizer = TfidfVectorizer(
        analyzer="char_wb", ngram_range=(3, 5), min_df=2,
        max_features=30_000, sublinear_tf=True,
    )
    features = vectorizer.fit_transform(texts)
    model = LogisticRegression(
        class_weight="balanced", max_iter=1_000, random_state=42,
    )
    model.fit(features, negative)
    return vectorizer, model


SENTIMENT_VECTORIZER, NEGATIVE_SENTIMENT_MODEL = train_negative_sentiment_model()


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


def fractional_year(value: str) -> float:
    date = pd.Timestamp(value)
    return date.year + (date.dayofyear - 1) / (366 if date.is_leap_year else 365)


def add_coalition_band(
    figure: go.Figure, start_year: int, end_year: int,
) -> go.Figure:
    """Add a hoverable, fixed-height coalition strip below a numeric year axis."""
    visible_start = start_year - 0.25
    visible_end = end_year + 0.25
    coalition_phases = []
    for period in DATA.periods.values():
        for coalition in period.get("coalitions", []):
            left = max(fractional_year(coalition["start_date"]), visible_start)
            right = min(fractional_year(coalition["end_date"]), visible_end)
            parties = sorted(
                coalition.get("parties", []),
                key=lambda party: COALITION_PARTY_ORDER.index(party),
            )
            if right <= left or not parties:
                continue
            coalition_phases.append((left, right, coalition, parties))
            party_height = 1 / len(parties)
            hover = (
                "<b>Koalition</b><br>"
                + " · ".join(parties)
                + f"<br>{pd.Timestamp(coalition['start_date']):%d.%m.%Y}–"
                + f"{pd.Timestamp(coalition['end_date']):%d.%m.%Y}"
            )
            for index, party in enumerate(parties):
                figure.add_trace(go.Bar(
                    x=[(left + right) / 2], y=[party_height],
                    width=[right - left], base=[1 - (index + 1) * party_height],
                    yaxis="y2", marker={
                        "color": PARTY_COLORS.get(party, "#7a7a7a"),
                        "line": {"width": 0},
                    },
                    opacity=0.9, showlegend=False,
                    customdata=[[hover]],
                    hovertemplate="%{customdata[0]}<extra></extra>",
                ))

    # Coalition changes get a vertical separator; parties within one coalition
    # deliberately have no horizontal white separators.
    boundaries = sorted({right for _left, right, _coalition, _parties in coalition_phases})
    for boundary in boundaries[:-1]:
        if visible_start < boundary < visible_end:
            figure.add_shape(
                type="line", xref="x", yref="paper", x0=boundary, x1=boundary,
                y0=0, y1=0.055, line={"color": "white", "width": 1.2},
            )
    figure.add_annotation(
        xref="paper", yref="paper", x=0, y=0.0275,
        text="KOALITION", showarrow=False, xanchor="right", yanchor="middle",
        xshift=-8, font={"size": 9, "color": "#6b7280"},
    )
    figure.update_layout(
        margin={"l": 75, "r": 25, "t": 75, "b": 55},
        yaxis={"domain": [0.16, 1]},
        yaxis2={
            "domain": [0, 0.055], "range": [0, 1], "fixedrange": True,
            "visible": False, "anchor": "x",
        },
        barmode="overlay",
        hovermode="closest",
    )
    figure.update_xaxes(
        range=[visible_start, visible_end], title_standoff=10, automargin=True,
    )
    return figure


def finish_party_year_figure(
    figure: go.Figure, y_title: str, start_year: int, end_year: int,
) -> go.Figure:
    return add_coalition_band(
        finish_figure(figure, y_title), start_year, end_year,
    )


SENTENCES_TOTAL = "Gesprochene Sätze insgesamt"
SENTENCES_BY_PARTY = "Gesprochene Sätze nach Partei"
INTERRUPTIONS_TOTAL = "Zwischenrufe insgesamt"
INTERRUPTIONS_BY_PARTY = "Zwischenrufe nach Partei"
INTERRUPTIONS_STACKED = "Zwischenrufe nach Partei, gestapelt"
INTERRUPTIONS_SHARE = "Parteianteile an den Zwischenrufen"
YEAR_PLOT_CHOICES = [
    SENTENCES_TOTAL, SENTENCES_BY_PARTY,
    INTERRUPTIONS_TOTAL, INTERRUPTIONS_BY_PARTY,
    INTERRUPTIONS_STACKED, INTERRUPTIONS_SHARE,
]
SEAT_NORMALIZABLE_YEAR_PLOTS = {
    SENTENCES_BY_PARTY,
    INTERRUPTIONS_BY_PARTY,
    INTERRUPTIONS_STACKED,
    INTERRUPTIONS_SHARE,
}

CUSTOM_YEAR_RANGE = "Benutzerdefiniert"
ALL_YEAR_RANGE = "Gesamter Zeitraum"
LAST_TEN_YEARS = "Letzte 10 Jahre"
YEAR_RANGE_PRESETS = {
    ALL_YEAR_RANGE: (MIN_YEAR, MAX_YEAR),
    LAST_TEN_YEARS: (max(MIN_YEAR, MAX_YEAR - 9), MAX_YEAR),
}
for period in sorted(DATA.periods, key=int, reverse=True):
    configured = DATA.periods[period]
    start = max(MIN_YEAR, int(configured["start_date"][:4]))
    end = min(MAX_YEAR, int(configured["end_date"][:4]))
    if start <= end:
        YEAR_RANGE_PRESETS[f"{period}. Bundestag ({start}–{end})"] = (start, end)


def apply_year_preset(preset: str, start_year: int, end_year: int) -> tuple[int, int]:
    if preset == CUSTOM_YEAR_RANGE:
        return int(start_year), int(end_year)
    return YEAR_RANGE_PRESETS.get(preset, (MIN_YEAR, MAX_YEAR))


def mark_custom_year_range(_start: int, _end: int):
    return gr.update(value=CUSTOM_YEAR_RANGE)


def update_year_seat_toggle(plot_type: str):
    supported = plot_type in SEAT_NORMALIZABLE_YEAR_PLOTS
    if supported:
        return gr.update(visible=True)
    return gr.update(visible=False, value=False)


def interruptions_per_party_year(
    start_year: int, end_year: int, normalize_seats: bool,
) -> pd.DataFrame:
    """Aggregate interruptions per year/party, with explicit zeros for area charts."""
    selected = DATA.interruptions.loc[
        DATA.interruptions["year"].between(start_year, end_year)
    ]
    if normalize_seats:
        counts = selected.groupby(["year", "comment_party"])["seat_weight"].sum(min_count=1)
    else:
        counts = selected.groupby(["year", "comment_party"]).size()
    parties = [party for party in PARTIES if party in counts.index.get_level_values("comment_party")]
    years = sorted(counts.index.get_level_values("year").unique())
    full_index = pd.MultiIndex.from_product([years, parties], names=["year", "comment_party"])
    return counts.reindex(full_index, fill_value=0).rename("interruptions").reset_index()


def render_year_plot(
    plot_type: str, start_year: int, end_year: int, normalize_seats: bool,
) -> go.Figure:
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
        value_column = "sentences_per_seat" if normalize_seats else "speech_len_sents"
        frame = (
            DATA.speeches.loc[DATA.speeches["year"].between(start_year, end_year)]
            .groupby(["year", "speaker_party"], as_index=False)[value_column]
            .sum(min_count=1)
        )
        unit = "Sätze je Sitz" if normalize_seats else "Sätze"
        title = ("Gesprochene Sätze je Sitz nach Partei und Jahr"
                 if normalize_seats else "Gesprochene Sätze nach Partei und Jahr")
        figure = px.line(
            frame, x="year", y=value_column, color="speaker_party", markers=True,
            category_orders={"speaker_party": PARTIES}, color_discrete_map=PARTY_COLORS,
            title=title,
            labels={"year": "Jahr", value_column: unit, "speaker_party": "Partei"},
        )
        figure.update_traces(
            hovertemplate=("%{y:,.1f} Sätze je Sitz" if normalize_seats
                           else "%{y:,.0f} Sätze") + "<extra>%{fullData.name}</extra>"
        )
        return finish_party_year_figure(figure, unit, start_year, end_year)
    if plot_type == INTERRUPTIONS_TOTAL:
        frame = (DATA.interruptions.loc[DATA.interruptions["year"].between(start_year, end_year)]
                 .groupby("year").size().rename("interruptions").reset_index())
        figure = px.line(frame, x="year", y="interruptions", markers=True,
                         title="Zwischenrufe pro Jahr",
                         labels={"year": "Jahr", "interruptions": "Zwischenrufe"})
        return finish_figure(figure, "Zwischenrufe")

    frame = interruptions_per_party_year(start_year, end_year, normalize_seats)
    if frame.empty:
        return empty_figure("Für diesen Zeitraum liegen keine Zwischenrufe vor.")
    unit = "Zwischenrufe je Sitz" if normalize_seats else "Zwischenrufe"
    labels = {"year": "Jahr", "interruptions": unit, "comment_party": "Partei"}
    plot_style = {"x": "year", "y": "interruptions", "color": "comment_party", "labels": labels,
                  "category_orders": {"comment_party": PARTIES},
                  "color_discrete_map": PARTY_COLORS}
    if plot_type == INTERRUPTIONS_STACKED:
        title = "Zwischenrufe nach Partei und Jahr (gestapelt)"
        if normalize_seats:
            title = "Zwischenrufe je Sitz nach Partei und Jahr (gestapelt)"
        figure = px.area(frame, title=title, **plot_style)
        figure.update_traces(
            hovertemplate=("%{y:.3f} Zwischenrufe je Sitz" if normalize_seats
                           else "%{y:,.0f} Zwischenrufe") + "<extra>%{fullData.name}</extra>"
        )
        return finish_party_year_figure(figure, unit, start_year, end_year)
    if plot_type == INTERRUPTIONS_SHARE:
        title = "Anteil der Parteien an allen Zwischenrufen pro Jahr"
        if normalize_seats:
            title = "Anteil der Parteien an den sitznormalisierten Zwischenrufraten"
        figure = px.area(frame, groupnorm="percent",
                         title=title, **plot_style)
        figure.update_traces(hovertemplate="%{y:.1f} %<extra>%{fullData.name}</extra>")
        share_unit = ("Anteil der sitznormalisierten Zwischenrufraten (%)"
                      if normalize_seats else "Anteil der Zwischenrufe (%)")
        figure = finish_party_year_figure(
            figure, share_unit, start_year, end_year)
        # Only the main percentage axis uses 0–100. Applying this through
        # update_yaxes() would also squash the coalition strip's 0–1 axis.
        figure.update_layout(
            yaxis={"range": [0, 100], "ticksuffix": " %"},
            hovermode="x unified",
        )
        figure.update_xaxes(
            showspikes=True, spikemode="across", spikesnap="cursor",
            spikedash="dot", spikecolor="#5f6570", spikethickness=1,
        )
        return figure

    title = ("Zwischenrufe je Sitz nach Partei und Jahr"
             if normalize_seats else "Zwischenrufe nach Partei und Jahr")
    figure = px.line(frame, markers=True, title=title, **plot_style)
    figure.update_traces(
        hovertemplate=("%{y:.3f} Zwischenrufe je Sitz" if normalize_seats
                       else "%{y:,.0f} Zwischenrufe") + "<extra>%{fullData.name}</extra>"
    )
    return finish_party_year_figure(figure, unit, start_year, end_year)


def normalized_callout(value: str) -> str:
    """Normalize a callout for exact-duplicate detection without changing its display."""
    return re.sub(r"\W+", " ", value.casefold(), flags=re.UNICODE).strip()


def rank_mixed_unique_callouts(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    """Select a diverse mix of roughly 80% negative and 20% positive callouts."""
    candidates = frame.copy()
    candidates["comment_text"] = candidates["comment_text"].fillna("").astype(str).str.strip()
    candidates = candidates.loc[candidates["comment_text"].str.len().ge(4)].copy()
    if "quote_complete" in candidates.columns:
        # Skip quotes whose end is missing in the source protocol text.
        candidates = candidates.loc[candidates["quote_complete"].fillna(True).astype(bool)].copy()
    candidates = candidates.loc[
        candidates["comment_name"].fillna("").astype(str).str.strip().ne("<unknown>")
    ].copy()
    candidates["normalized_text"] = candidates["comment_text"].map(normalized_callout)
    candidates = candidates.drop_duplicates("normalized_text", keep="last")
    if candidates.empty:
        return candidates

    sentiment_features = SENTIMENT_VECTORIZER.transform(candidates["comment_text"])
    candidates["negative_probability"] = NEGATIVE_SENTIMENT_MODEL.predict_proba(
        sentiment_features
    )[:, 1]

    # Character n-grams handle German compounds, spelling variants, and the
    # occasional OCR artifact better than word-level token matching.
    uniqueness_vectorizer = TfidfVectorizer(
        analyzer="char_wb", ngram_range=(3, 5), min_df=1,
        max_features=30_000, sublinear_tf=True,
    )
    uniqueness_features = uniqueness_vectorizer.fit_transform(candidates["comment_text"])
    similarities = cosine_similarity(uniqueness_features, dense_output=False)
    similarities.setdiag(0)
    candidates["uniqueness"] = 1 - similarities.max(axis=1).toarray().ravel()

    diversity = 0.35 + 0.65 * candidates["uniqueness"]
    candidates["negative_score"] = candidates["negative_probability"] * diversity
    candidates["positive_score"] = (1 - candidates["negative_probability"]) * diversity

    positive_count = min(max(1, round(limit * 0.2)), limit)
    negative_count = limit - positive_count
    negative = candidates.loc[candidates["negative_probability"].ge(0.5)].nlargest(
        negative_count, "negative_score")
    positive = candidates.loc[candidates["negative_probability"].lt(0.5)].nlargest(
        positive_count, "positive_score")

    # Put a positive example roughly after every four negative ones rather than
    # collecting both groups in visibly separate blocks.
    selected_rows = []
    negative_rows = list(negative.iterrows())
    positive_rows = list(positive.iterrows())
    while negative_rows or positive_rows:
        selected_rows.extend(negative_rows[:4])
        negative_rows = negative_rows[4:]
        if positive_rows:
            selected_rows.append(positive_rows.pop(0))
    selected = candidates.loc[[index for index, _row in selected_rows]]
    if len(selected) < limit:
        remaining = candidates.drop(index=selected.index)
        fallback_score = remaining[["negative_score", "positive_score"]].max(axis=1)
        selected = pd.concat([selected, remaining.loc[fallback_score.nlargest(limit - len(selected)).index]])
    return selected.head(limit)


def latest_window() -> tuple[pd.Timestamp, pd.Timestamp, pd.DataFrame]:
    """Return the latest protocol day and the 30 preceding calendar days."""
    end = DATA.max_date.normalize()
    start = end - pd.Timedelta(days=30)
    frame = DATA.interruptions.loc[DATA.interruptions["date"].between(start, end)].copy()
    return start, end, frame


def latest_party_pie(frame: pd.DataFrame) -> go.Figure:
    counts = (
        frame.groupby("comment_party").size().rename("interruptions").reset_index()
    )
    counts["party_order"] = counts["comment_party"].map(
        {party: index for index, party in enumerate(PARTIES)}
    )
    counts = counts.sort_values("party_order")
    figure = px.pie(
        counts,
        names="comment_party",
        values="interruptions",
        color="comment_party",
        color_discrete_map=PARTY_COLORS,
        category_orders={"comment_party": PARTIES},
        title="Anteil der Zwischenrufe nach Partei",
        hole=0.35,
    )
    figure.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="%{label}<br>%{value:,} Zwischenrufe<br>%{percent}<extra></extra>",
    )
    figure.update_layout(
        template=PLOT_TEMPLATE,
        width=500,
        height=400,
        autosize=False,
        legend_title_text="Partei der Zwischenrufenden",
        margin={"l": 25, "r": 25, "t": 75, "b": 25},
    )
    return figure


LATEST_PARTY_SHARE = "Parteianteile"
LATEST_DAILY_STACK = "Tagesverlauf"
LATEST_VIEW_CHOICES = [LATEST_DAILY_STACK, LATEST_PARTY_SHARE]
INITIAL_CALLOUT_COUNT = 8
CALLOUT_PAGE_SIZE = 5


def latest_daily_stacked_bars(
    frame: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp,
) -> go.Figure:
    counts = (
        frame.groupby(["date", "comment_party"])
        .size()
        .rename("interruptions")
        .reset_index()
    )
    figure = px.bar(
        counts,
        x="date",
        y="interruptions",
        color="comment_party",
        category_orders={"comment_party": PARTIES},
        color_discrete_map=PARTY_COLORS,
        labels={
            "date": "Datum",
            "interruptions": "Zwischenrufe",
            "comment_party": "Partei",
        },
        title="Zwischenrufe pro Protokolltag und Partei",
    )
    figure.update_traces(
        hovertemplate=(
            "%{x|%d.%m.%Y}<br>%{y:,.0f} Zwischenrufe"
            "<extra>%{fullData.name}</extra>"
        )
    )
    figure.update_layout(
        template=PLOT_TEMPLATE,
        height=400,
        barmode="stack",
        hovermode="x unified",
        legend_title_text="Partei der Zwischenrufenden",
        margin={"l": 55, "r": 25, "t": 75, "b": 55},
    )
    # A continuous date axis preserves gaps between sittings. Limit labels to
    # roughly weekly ticks; the exact date remains available in the hover.
    figure.update_xaxes(
        range=[start - pd.Timedelta(days=1), end + pd.Timedelta(days=1)],
        tickformat="%d.%m.",
        dtick=7 * 24 * 60 * 60 * 1_000,
        tickangle=0,
    )
    figure.update_yaxes(title="Zwischenrufe", rangemode="tozero")

    # Mark a parliamentary summer recess when two consecutive protocol days
    # leave a substantial gap that overlaps July or August.
    protocol_dates = DATA.speeches["date"].drop_duplicates().sort_values().tolist()
    for previous, following in zip(protocol_dates, protocol_dates[1:]):
        gap_days = (following - previous).days - 1
        gap_start = previous + pd.Timedelta(days=1)
        gap_end = following - pd.Timedelta(days=1)
        overlaps_window = gap_start <= end and gap_end >= start
        summer_overlap = any(
            month in {7, 8}
            for month in pd.date_range(gap_start, gap_end).month
        )
        if gap_days >= 14 and overlaps_window and summer_overlap:
            figure.add_vrect(
                x0=max(gap_start, start),
                x1=min(gap_end, end),
                fillcolor="#8b95a5",
                opacity=0.12,
                line_width=0,
                annotation_text="Sommerpause",
                annotation_position="top",
            )
    return figure


def latest_figure(
    frame: pd.DataFrame, view: str, start: pd.Timestamp, end: pd.Timestamp,
) -> go.Figure:
    if view == LATEST_DAILY_STACK:
        return latest_daily_stacked_bars(frame, start, end)
    return latest_party_pie(frame)


def callouts_markdown(callouts: pd.DataFrame) -> str:
    if callouts.empty:
        return "*Keine geeigneten Zwischenrufe gefunden.*"
    entries = []
    for _, row in callouts.iterrows():
        text = html.escape(row["comment_text"])
        caller = html.escape(str(row["comment_name"]))
        party = html.escape(str(row["comment_party"]))
        interrupted = html.escape(str(row["interrupted_speaker"]))
        # Interruptions during a chair turn have no interrupted party.
        interrupted_party = (f" ({html.escape(str(row['interrupted_speaker_party']))})"
                             if pd.notna(row["interrupted_speaker_party"]) else "")
        date = row["date"].date().strftime("%d.%m.%Y")
        if "protocol_id" in row and pd.notna(row["protocol_id"]):
            period, sitting = str(row["protocol_id"]).split("/", maxsplit=1)
            source_label = f"BT-PlPr. {int(period)}/{int(sitting)}"
            source_url = (
                f"https://dserver.bundestag.de/btp/{int(period)}/"
                f"{int(period):02d}{int(sitting):03d}.pdf"
            )
        else:
            source_label = "Quelle: Deutscher Bundestag"
            source_url = "https://www.bundestag.de/services/opendata"
        entries.append(
            f"> **„{text}“**\n>\n"
            f"> {date} · **{caller} ({party})** während der Rede von "
            f"**{interrupted}**{interrupted_party} · "
            f"[{source_label}]({source_url})"
        )
    return "\n\n".join(entries)


def render_latest_board(view: str, callout_count: int) -> tuple[str, go.Figure, str]:
    start, end, frame = latest_window()
    if frame.empty:
        return "Keine Daten im jüngsten Zeitraum.", empty_figure("Keine Daten."), ""
    callouts = rank_mixed_unique_callouts(frame, int(callout_count))
    summary = (
        f"### Bundestag Aktuell\n"
        f"Neuester verfügbarer Protokolltag: **{end:%d.%m.%Y}** · "
        f"Zeitraum: **{start:%d.%m.%Y}–{end:%d.%m.%Y}** · "
        f"**{len(frame):,}** Zwischenrufe"
    ).replace(",", ".")
    return summary, latest_figure(frame, view, start, end), callouts_markdown(callouts)


def load_more_latest_callouts(callout_count: int) -> tuple[int, str]:
    new_count = int(callout_count) + CALLOUT_PAGE_SIZE
    _, _, frame = latest_window()
    callouts = rank_mixed_unique_callouts(frame, new_count)
    return new_count, callouts_markdown(callouts)


def correction_issue_link(category: str, reference: str, description: str) -> str:
    if not description or not description.strip():
        raise gr.Error("Bitte die vorgeschlagene Korrektur kurz beschreiben.")
    title = f"Datenkorrektur: {category}"
    body = (
        "## Art der Korrektur\n"
        f"{category}\n\n"
        "## Fundstelle\n"
        f"{reference.strip() or 'Nicht angegeben'}\n\n"
        "## Beschreibung\n"
        f"{description.strip()}\n\n"
        "---\n"
        "Diese Meldung wurde über das Korrekturformular des Dashboards erstellt."
    )
    url = (
        "https://github.com/stellamoR/bundestag_zwischenrufe/issues/new"
        f"?title={quote(title)}&body={quote(body)}&labels=data-correction"
    )
    return (
        "Die Angaben wurden noch nicht versendet. Bitte den vorausgefüllten Eintrag prüfen und "
        f"anschließend **[Korrektur auf GitHub absenden]({url})**."
    )


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


def coalition_cards(
    start: pd.Timestamp, end: pd.Timestamp, exclude_carryover: bool,
) -> str:
    """Render equal-size coalition cards for phases intersecting a date range."""
    phases = []
    for period in DATA.periods.values():
        for coalition in period.get("coalitions", []):
            phase_start = pd.Timestamp(coalition["start_date"])
            phase_end = pd.Timestamp(coalition["end_date"])
            if phase_end >= start and phase_start <= end:
                parties = sorted(
                    coalition.get("parties", []),
                    key=lambda party: COALITION_PARTY_ORDER.index(party),
                )
                if parties:
                    phases.append((phase_start, phase_end, parties))

    # At the beginning of a new Bundestag, the previous cabinet may remain in
    # office in a caretaker capacity. If a new coalition starts in the selected
    # parliamentary period, show that political formation rather than the
    # carryover from the preceding Bundestag.
    if exclude_carryover and any(start <= phase_start <= end for phase_start, _, _ in phases):
        phases = [phase for phase in phases if phase[0] >= start]

    if not phases:
        return '<div class="coalition-empty">Keine Koalitionsdaten im gewählten Zeitraum.</div>'

    latest_period = max(DATA.periods, key=int)
    provisional_end = pd.Timestamp(DATA.periods[latest_period]["end_date"])
    cards = []
    for phase_start, phase_end, parties in phases:
        swatches = "".join(
            f'<span style="background:{PARTY_COLORS.get(party, "#7a7a7a")}"></span>'
            for party in parties
        )
        end_label = f"{phase_end:%d.%m.%Y}"
        end_caption = "Bis"
        if phase_end == provisional_end:
            end_caption = "Bis · Voraussichtlich"
        cards.append(
            '<div class="coalition-card">'
            f'<div class="coalition-swatches">{swatches}</div>'
            '<div class="coalition-dates">'
            f'<span><small>Von</small>{phase_start:%d.%m.%Y}</span>'
            f'<span><small>{end_caption}</small>{end_label}</span>'
            '</div></div>'
        )
    return '<div class="coalition-card-list">' + "".join(cards) + "</div>"


def interruption_matrix(frame: pd.DataFrame, normalize_seats: bool,
                        normalize_sentences: bool,
                        selected_parties: list[str], show_values: bool) -> go.Figure:
    if normalize_seats:
        matrix = frame.pivot_table(index="comment_party", columns="interrupted_speaker_party",
                                   values="seat_weight", aggfunc="sum")
        matrix = matrix.reindex(index=selected_parties, columns=selected_parties)
    else:
        matrix = pd.crosstab(frame["comment_party"], frame["interrupted_speaker_party"])
        matrix = matrix.reindex(index=selected_parties, columns=selected_parties, fill_value=0).astype(float)
    if normalize_sentences:
        sentence_counts = (frame.drop_duplicates("speech_id")
                           .groupby("interrupted_speaker_party")["speech_len_sents"].sum()
                           .reindex(selected_parties).replace(0, np.nan))
        matrix = matrix.div(sentence_counts, axis="columns") * 1_000

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
        labels={"x": "Rede von …", "y": "Zwischenruf von …", "color": units},
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
                       show_values: bool) -> tuple[go.Figure, str, str]:
    start, end = selected_range(not custom_dates, period, start_value, end_value)
    coalition_list = coalition_cards(start, end, exclude_carryover=not custom_dates)
    frame = DATA.interruptions.loc[DATA.interruptions["date"].between(start, end)].copy()
    selected_parties = [party for party in PARTIES if party in (selected_parties or [])]
    if not selected_parties:
        return (empty_figure("Bitte mindestens eine Partei auswählen."),
                "Keine Partei ausgewählt.", coalition_list)
    if plot_type == "Zwischenrufe nach Partei":
        frame = frame.loc[frame["comment_party"].isin(selected_parties)]
    else:
        frame = frame.loc[
            frame["comment_party"].isin(selected_parties)
            & frame["interrupted_speaker_party"].isin(selected_parties)
        ]
    if frame.empty:
        return (empty_figure("Für diesen Zeitraum liegen keine Zwischenrufe vor."),
                "Keine Daten im gewählten Zeitraum.", coalition_list)
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
    return figure, summary, coalition_list


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

INFO_CONTENT = f"""
## Über dieses Dashboard

Das Dashboard wertet **{len(DATA.speeches)} Reden** und
**{len(DATA.interruptions)} Zwischenrufe** aus veröffentlichten
Plenarprotokollen des Deutschen Bundestages aus. Der derzeitige Datenstand reicht
vom **{DATA.min_date.date():%d.%m.%Y}** bis zum **{DATA.max_date.date():%d.%m.%Y}**.

### Herkunft und Aktualisierung

Grundlage sind die amtlichen Plenarprotokolle und Abgeordneten-Stammdaten aus dem
[DIP](https://dip.bundestag.de) und dem
[Open-Data-Angebot des Bundestages](https://www.bundestag.de/services/opendata).
Ein automatischer Prozess sucht einmal täglich nach neuen oder korrigierten
Protokollen. Das Dashboard ist deshalb nicht live: Eine Sitzung erscheint erst,
nachdem das Protokoll veröffentlicht und die Verarbeitung
erfolgreich abgeschlossen ist.

### Aufbereitung und mögliche Fehler

Reden, Zwischenrufe, Personen und Parteien werden maschinell aus den
Protokolltexten extrahiert. Die Extraktion erfolgt durch Text-Matching und nicht durch XML-parsing, da die Protokolle erst seit der 19. BT-Periode mit dem \<kommentar\>-Feld veröffentlicht werden. Dies ermöglicht eine Auswertung von älteren Protokollen. Historische Schreibweisen, Protokoll- oder OCR-Fehler, uneindeutige
Namensnennungen und Änderungen der Protokollstruktur können zu Fehlzuordnungen
oder fehlenden Treffern führen. Maßgeblich bleibt immer das amtliche
Originalprotokoll.

### So sind die Kennzahlen zu lesen

- **Je Sitz:** Jeder Zwischenruf wird mit `1 / Sitzzahl der zwischenrufenden
  Partei` im zum Datum gehörenden Bundestag gewichtet.
- **Je 1.000 Sätze:** Zwischenrufe werden durch die Zahl der gesprochenen Sätze
  der unterbrochenen Partei geteilt und auf 1.000 Sätze hochgerechnet.
- **Heatmap:** Die Zeile „Zwischenruf von …“ bezeichnet die unterbrechende
  Partei; die Spalte „Rede von …“ bezeichnet die Partei der redenden Person.
- **Letzte 30 Tage:** Der Zeitraum endet am neuesten verfügbaren Protokolltag,
  nicht am heutigen Datum, und umfasst die 30 davorliegenden Kalendertage.

### Interessante Zurufe

Die Auswahl verwendet kein großes Sprachmodell. Ein klassisches
TF-IDF-/Logistic-Regression-Modell wurde mit **4.500 manuell annotierten
Zwischenrufen** trainiert. Die Liste enthält ungefähr **80 % negativ und 20 %
positiv** eingeordnete Zurufe. Ähnliche Texte im 30-Tage-Fenster werden per
TF-IDF-Cosinus-Ähnlichkeit erkannt, damit sich Formulierungen möglichst wenig
wiederholen. Die Modellwerte werden nicht angezeigt. Ironie, Zitate und
fehlender Kontext können zu falschen Einstufungen führen.

### Lizenz

Die maschinell aufbereiteten Daten, Auswertungen und Visualisierungen dieses
Projekts stehen unter [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de).
Für die amtlichen Ausgangsdokumente gelten die Hinweise des Deutschen
Bundestages.
"""

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
.gradio-container {{width: calc(100% - 48px) !important; max-width: 1680px !important; min-width: 0 !important; margin: 0 auto !important;}}
.title-row {{align-items: center !important;}}
.dashboard-title {{margin-bottom: 0 !important;}}
.dashboard-subtitle {{color: #5f6570; margin-top: 0 !important;}}
.info-button {{
  margin-left: auto !important;
  max-width: 110px !important;
  background: #ffffff !important;
  color: #202124 !important;
  border: 1px solid #c9ced6 !important;
  box-shadow: none !important;
}}
.info-button:hover {{background: #f7f8fa !important; border-color: #9ca3ad !important;}}
.info-panel {{border: 1px solid #d9dde3; border-radius: 14px; padding: 18px 22px; margin: 8px 0 18px !important; background: #f8f9fb;}}
.source-notice {{color: #5f6570; font-size: 0.85em; margin-top: 12px !important;}}
.control-section {{margin: 8px 0 -4px !important;}}
.control-section h3 {{font-size: 0.9rem !important; letter-spacing: 0.02em; color: #5f6570;}}
.year-input-row {{flex-wrap: nowrap !important;}}
.year-input-row > * {{min-width: 0 !important;}}
.tab-nav {{overflow-x: auto !important; flex-wrap: nowrap !important; scrollbar-width: thin;}}
.tab-nav button {{flex: 0 0 auto !important; white-space: nowrap !important;}}
.desktop-row {{display: flex !important; flex-wrap: nowrap !important; gap: 24px !important; align-items: flex-start !important;}}
.control-panel {{flex: 0 0 350px !important; min-width: 350px !important; max-width: 350px !important; border: 1px solid #e4e7eb; border-radius: 14px; padding: 16px;}}
.plot-panel {{flex: 1 1 auto !important; min-width: 680px !important;}}
.plot-panel .plot-container {{min-height: 600px !important;}}
.latest-plot .plot-container {{min-height: 400px !important;}}
.heatmap-plot {{max-width: {HEATMAP_WIDTH_PX}px !important; margin-left: 0 !important; margin-right: auto !important; overflow-x: auto !important;}}
.heatmap-plot .plot-container {{min-height: 0 !important;}}
.coalition-card-list {{display: flex; flex-wrap: wrap; gap: 10px; margin: 2px 0 8px;}}
.coalition-card {{flex: 0 0 220px; height: 82px; overflow: hidden; background: #f4f5f7; border: 1px solid #dfe3e8; border-radius: 12px; box-shadow: 0 1px 2px rgba(20, 30, 45, 0.05);}}
.coalition-swatches {{display: flex; width: 100%; height: 9px;}}
.coalition-swatches span {{flex: 1 1 0;}}
.coalition-dates {{display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 11px 13px; color: #202124; font-size: 0.86rem;}}
.coalition-dates span {{display: flex; flex-direction: column; white-space: nowrap;}}
.coalition-dates small {{color: #707782; font-size: 0.68rem; line-height: 1.2; margin-bottom: 3px; text-transform: uppercase; letter-spacing: 0.04em;}}
.coalition-empty {{padding: 14px 16px; background: #f4f5f7; border: 1px solid #dfe3e8; border-radius: 12px; color: #707782;}}
.callout-list blockquote {{border-left: 4px solid #c9ced6; margin: 14px 0; padding: 10px 14px; background: #f7f8fa;}}
@media (max-width: 900px) {{
  .gradio-container {{width: calc(100% - 24px) !important;}}
  .desktop-row {{flex-direction: column !important; gap: 12px !important;}}
  .control-panel {{flex: 1 1 auto !important; min-width: 0 !important; max-width: none !important; width: 100% !important; box-sizing: border-box;}}
  .plot-panel {{min-width: 0 !important; width: 100% !important;}}
  .plot-panel .plot-container {{min-height: 420px !important;}}
  .latest-plot .plot-container {{min-height: 400px !important;}}
  .heatmap-plot {{max-width: 100% !important; width: 100% !important;}}
  .heatmap-plot .plot-container {{min-width: {HEATMAP_WIDTH_PX}px !important; min-height: 0 !important;}}
  .title-row {{flex-wrap: nowrap !important;}}
  .dashboard-title {{min-width: 0 !important;}}
  .dashboard-title h1 {{font-size: 1.65rem !important;}}
  .info-button {{flex: 0 0 auto !important;}}
}}
@media (max-width: 600px) {{
  .gradio-container {{width: calc(100% - 16px) !important;}}
  .control-panel {{padding: 12px;}}
  .plot-panel .plot-container {{min-height: 360px !important;}}
  .latest-plot .plot-container {{min-height: 350px !important;}}
  .coalition-card {{flex-basis: min(220px, 100%);}}
  .info-panel {{padding: 14px 16px;}}
  .dashboard-title h1 {{font-size: 1.35rem !important; line-height: 1.2 !important;}}
}}
"""


def build_app() -> gr.Blocks:
    blocks_kwargs = {
        "title": "Bundestag · Reden und Zwischenrufe",
        "fill_width": True,
    }
    if not LAUNCH_ACCEPTS_PAGE_ASSETS:
        blocks_kwargs.update(css=CSS, js=FORCE_LIGHT_MODE_JS)

    with warnings.catch_warnings():
        if not LAUNCH_ACCEPTS_PAGE_ASSETS:
            warnings.filterwarnings(
                "ignore",
                message="The '(css|js)' parameter in the Blocks constructor will be removed",
                category=DeprecationWarning,
            )
        dashboard = gr.Blocks(**blocks_kwargs)

    with dashboard:
        info_open = gr.State(value=False)
        with gr.Row(elem_classes="title-row"):
            gr.Markdown("# Bundestag: Reden und Zwischenrufe", elem_classes="dashboard-title")
            info_button = gr.Button("ⓘ Info", min_width=100, elem_classes="info-button")
        gr.Markdown(
            f"Interaktive Auswertung der Plenarprotokolle von **{DATA.min_date.date():%d.%m.%Y}** "
            f"bis **{DATA.max_date.date():%d.%m.%Y}**.", elem_classes="dashboard-subtitle",
        )
        with gr.Group(visible=False, elem_classes="info-panel") as info_panel:
            gr.Markdown(INFO_CONTENT)
            close_info = gr.Button("Info schließen", min_width=130)
        with gr.Tabs():
            with gr.Tab("Entwicklung über Zeit"):
                with gr.Row(elem_classes="desktop-row"):
                    with gr.Column(scale=1, elem_classes="control-panel"):
                        gr.Markdown("### Darstellung", elem_classes="control-section")
                        year_plot_type = gr.Dropdown(
                            YEAR_PLOT_CHOICES, value=INTERRUPTIONS_BY_PARTY,
                            show_label=False, allow_custom_value=False, filterable=False,
                        )
                        gr.Markdown("### Zeitraum", elem_classes="control-section")
                        year_range_preset = gr.Dropdown(
                            choices=[CUSTOM_YEAR_RANGE, *YEAR_RANGE_PRESETS],
                            value=ALL_YEAR_RANGE, show_label=False,
                            allow_custom_value=False, filterable=False,
                        )
                        with gr.Row(elem_classes="year-input-row"):
                            start_year = gr.Number(
                                value=MIN_YEAR, label="Von", precision=0, step=1,
                                minimum=MIN_YEAR, maximum=MAX_YEAR, min_width=0,
                            )
                            end_year = gr.Number(
                                value=MAX_YEAR, label="Bis", precision=0, step=1,
                                minimum=MIN_YEAR, maximum=MAX_YEAR, min_width=0,
                            )
                        gr.Markdown("### Normalisierung", elem_classes="control-section")
                        year_normalize_seats = gr.Checkbox(
                            value=False,
                            label="Nach Sitzen der jeweiligen Partei normalisieren",
                            info="Gleicht unterschiedlich große Fraktionen aus.",
                        )
                        refresh_year = gr.Button("Diagramm aktualisieren", variant="primary")
                    with gr.Column(elem_classes="plot-panel"):
                        year_plot = gr.Plot(show_label=False)
            with gr.Tab("Wer unterbricht wen?"):
                with gr.Row(elem_classes="desktop-row"):
                    with gr.Column(scale=1, elem_classes="control-panel"):
                        gr.Markdown("### Darstellung", elem_classes="control-section")
                        detail_plot_type = gr.Dropdown(
                            [HEATMAP, "Zwischenrufe nach Partei"],
                            value=HEATMAP, show_label=False,
                            allow_custom_value=False, filterable=False)
                        show_values = gr.Checkbox(value=False, label="Werte in der Heatmap anzeigen")
                        gr.Markdown("### Zeitraum", elem_classes="control-section")
                        period = gr.Dropdown(
                            PERIOD_CHOICES, value=DEFAULT_PERIOD, show_label=False,
                            allow_custom_value=False, filterable=False)
                        custom_dates = gr.Checkbox(
                            value=False, label="Benutzerdefiniertes Start- und Enddatum")
                        start_date = gr.Textbox(value=str(DATA.min_date.date()), label="Startdatum",
                                                info="JJJJ-MM-TT", visible=False)
                        end_date = gr.Textbox(value=str(DATA.max_date.date()), label="Enddatum",
                                              info="JJJJ-MM-TT", visible=False)
                        period_info = gr.Markdown(
                            update_period_info(DEFAULT_PERIOD), visible=False)
                        gr.Markdown("### Parteien", elem_classes="control-section")
                        selected_parties = gr.CheckboxGroup(
                            choices=PARTIES,
                            value=default_parties(DEFAULT_PERIOD),
                            show_label=False,
                            info="Standard: Parteien mit Sitzen; fraktionslos abgewählt",
                        )
                        gr.Markdown("### Normalisierung", elem_classes="control-section")
                        normalize_seats = gr.Checkbox(value=False, label="Nach Sitzen der unterbrechenden Partei normalisieren")
                        normalize_sentences = gr.Checkbox(value=False, label="Nach gesprochenen Sätzen der unterbrochenen Partei normalisieren")
                        refresh_detail = gr.Button("Diagramm aktualisieren", variant="primary")
                    with gr.Column(elem_classes="plot-panel"):
                        detail_summary = gr.Markdown()
                        detail_plot = gr.Plot(show_label=False, elem_classes=["heatmap-plot"])
                        gr.Markdown("### Regierungskoalitionen", elem_classes="control-section")
                        detail_coalitions = gr.HTML()
            with gr.Tab("Bundestag Aktuell"):
                latest_callout_count = gr.State(value=INITIAL_CALLOUT_COUNT)
                latest_summary = gr.Markdown()
                with gr.Row(elem_classes="desktop-row"):
                    with gr.Column(scale=1, elem_classes="control-panel"):
                        gr.Markdown("### Darstellung", elem_classes="control-section")
                        latest_view = gr.Radio(
                            choices=LATEST_VIEW_CHOICES,
                            value=LATEST_DAILY_STACK,
                            show_label=False,
                        )
                        gr.Markdown("### Zeitraum", elem_classes="control-section")
                        gr.Markdown(
                            "Die Auswahl endet am neuesten verfügbaren Protokolltag und umfasst "
                            "die 30 vorhergehenden Kalendertage."
                        )
                        refresh_latest = gr.Button("Ansicht aktualisieren", variant="primary")
                    with gr.Column(scale=2, elem_classes="plot-panel"):
                        latest_plot = gr.Plot(show_label=False, elem_classes="latest-plot")
                gr.Markdown("## Interessante Zurufe")
                gr.Markdown(
                    "Automatisch ausgewählt: ungefähr 80 % negativ und 20 % positiv "
                    "eingeordnete, möglichst unterschiedliche Zurufe. Ironie oder fehlender "
                    "Kontext können übersehen werden.",
                    elem_classes="dashboard-subtitle",
                )
                latest_callouts = gr.Markdown(elem_classes="callout-list")
                load_more_callouts = gr.Button("Mehr Zwischenrufe laden")

        with gr.Accordion("Fehler melden oder Korrektur vorschlagen", open=False):
            gr.Markdown(
                "Bitte möglichst Datum, Person und – falls vorhanden – das Originalprotokoll "
                "angeben. Die Meldung kann vor dem Absenden auf GitHub geprüft werden."
            )
            correction_category = gr.Dropdown(
                choices=[
                    "Falsche Person", "Falsche Partei", "Falscher Wortlaut",
                    "Fehlender Zwischenruf", "Doppelter Eintrag", "Sonstiges",
                ],
                value="Falsche Person",
                label="Art der Korrektur",
                allow_custom_value=False,
                filterable=False,
            )
            correction_reference = gr.Textbox(
                label="Fundstelle",
                placeholder="z. B. 14.06.2024, Name, BT-PlPr. 20/176 oder URL",
            )
            correction_description = gr.Textbox(
                label="Beschreibung",
                placeholder="Was ist falsch und wie sollte der Eintrag lauten?",
                lines=4,
            )
            correction_submit = gr.Button("Korrektur vorbereiten", variant="primary")
            correction_result = gr.Markdown()

        gr.Markdown(SOURCE_NOTICE, elem_classes="source-notice")

        year_inputs = [year_plot_type, start_year, end_year, year_normalize_seats]
        detail_inputs = [detail_plot_type, custom_dates, period, start_date, end_date,
                         normalize_seats, normalize_sentences, selected_parties, show_values]
        latest_inputs = [latest_view, latest_callout_count]
        latest_outputs = [latest_summary, latest_plot, latest_callouts]
        info_button.click(
            lambda is_open: (gr.update(visible=not is_open), not is_open),
            inputs=info_open,
            outputs=[info_panel, info_open],
        )
        close_info.click(
            lambda: (gr.update(visible=False), False),
            outputs=[info_panel, info_open],
        )
        correction_submit.click(
            correction_issue_link,
            inputs=[correction_category, correction_reference, correction_description],
            outputs=correction_result,
        )
        refresh_latest.click(
            render_latest_board,
            inputs=latest_inputs,
            outputs=latest_outputs,
        )
        latest_view.change(
            render_latest_board,
            inputs=latest_inputs,
            outputs=latest_outputs,
        )
        load_more_callouts.click(
            load_more_latest_callouts,
            inputs=latest_callout_count,
            outputs=[latest_callout_count, latest_callouts],
        )
        refresh_year.click(render_year_plot, inputs=year_inputs, outputs=year_plot)
        refresh_detail.click(
            render_detail_plot, inputs=detail_inputs,
            outputs=[detail_plot, detail_summary, detail_coalitions],
        )
        dashboard.load(render_year_plot, inputs=year_inputs, outputs=year_plot)
        dashboard.load(
            render_detail_plot, inputs=detail_inputs,
            outputs=[detail_plot, detail_summary, detail_coalitions],
        )
        dashboard.load(render_latest_board, inputs=latest_inputs, outputs=latest_outputs)

        year_plot_type.change(
            update_year_seat_toggle,
            inputs=year_plot_type,
            outputs=year_normalize_seats,
        ).then(
            render_year_plot,
            inputs=year_inputs,
            outputs=year_plot,
        )
        year_range_preset.change(
            apply_year_preset,
            inputs=[year_range_preset, start_year, end_year],
            outputs=[start_year, end_year],
        ).then(
            render_year_plot,
            inputs=year_inputs,
            outputs=year_plot,
        )
        for year_input in [start_year, end_year]:
            year_input.change(
                mark_custom_year_range,
                inputs=[start_year, end_year],
                outputs=year_range_preset,
            ).then(
                render_year_plot,
                inputs=year_inputs,
                outputs=year_plot,
            )
        year_normalize_seats.change(render_year_plot, inputs=year_inputs, outputs=year_plot)

        for control in [detail_plot_type, custom_dates]:
            control.change(
                update_detail_controls,
                inputs=[detail_plot_type, custom_dates],
                outputs=[period, period_info, custom_dates, start_date, end_date, normalize_sentences, show_values, detail_plot],
            ).then(
                render_detail_plot,
                inputs=detail_inputs,
                outputs=[detail_plot, detail_summary, detail_coalitions],
            )
        period.change(
            update_period,
            inputs=period,
            outputs=[period_info, selected_parties],
        ).then(
            render_detail_plot,
            inputs=detail_inputs,
            outputs=[detail_plot, detail_summary, detail_coalitions],
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
                outputs=[detail_plot, detail_summary, detail_coalitions],
            )
    return dashboard


demo = build_app()

if __name__ == "__main__":
    launch_kwargs = {}
    if LAUNCH_ACCEPTS_PAGE_ASSETS:
        launch_kwargs.update(css=CSS, js=FORCE_LIGHT_MODE_JS)
    demo.launch(**launch_kwargs)
