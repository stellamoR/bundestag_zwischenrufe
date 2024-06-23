import gradio as gr
from math import log
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from gradio_calendar import Calendar
from datetime import datetime
import json




def plot_num_sents_single(start_year, end_year):
    relevant_speeches_grouped = df_speeches_grouped[(df_speeches_grouped['year']>=start_year)&(df_speeches_grouped['year']<=end_year)]

    fig = px.line(relevant_speeches_grouped,
              x='year',
              y='speech_len_sents',
              title='Anzahl der Sätze im Deutschen Bundestag pro Jahr',
              labels={'year': 'Jahr', 'speech_len_sents': 'Anzahl der Sätze'},
              markers=True,)
    fig.update_layout(hovermode='x unified')
    return fig

def plot_num_sents_party(start_year,end_year,norm=False):

    relevant_sent_nums = df_speeches_grouped_parties_years[(df_speeches_grouped_parties_years['year']>=start_year)&(df_speeches_grouped_parties_years['year']<=end_year)]

    fig = px.line(relevant_sent_nums,
              x='year',
              y='speech_len_sents',
              color='speaker_party',
              title='Anzahl der Sätze nach Partei im Deutschen Bundestag pro Jahr',
              labels={'year': 'Jahr', 'speech_len_sents': 'Anzahl der Sätze', 'speaker_party': 'Partei'},
              markers=True,
              color_discrete_map=party_colors)

    fig.update_layout(hovermode='x unified')

    return fig

def plot_interruptions_party_line(start_year, end_year,norm=False):

    relevant_interruptions_per_year = interruptions_per_year[(interruptions_per_year['year']>=start_year)&(interruptions_per_year['year']<=end_year)]
    fig = px.line(relevant_interruptions_per_year,
                x='year',
                y='interruptions',
                color='comment_party',
                title='Zwischenrufe nach Partei pro Jahr',
                labels={'year': 'Jahr', 'interruptions': 'Anzahl der Zwischenrufe', 'comment_party': 'Partei'},
                markers=True,
                color_discrete_map=party_colors)

    fig.update_layout(hovermode='x unified')

    return fig



def plot_interruptions_by_party(start_date, end_date, norm_seats, bt_period, choose_date_with_bt_period):

    if norm_seats or choose_date_with_bt_period:
        start_date = bt_periods[str(bt_period)]['start_date'] # use bt_period start + end dates
        end_date = bt_periods[str(bt_period)]['end_date']

    df_interruptions_num = get_interruption_count_for_timespan(start_date, end_date)
    # party names + interrupt counts
    parties_pd = df_interruptions_num.index
    comments_per_party = df_interruptions_num['num_of_interruptions']

    if norm_seats:
        num_seats_dict_sorted =  dict(sorted(bt_periods[str(bt_period)]['num_seats'].items(), key = lambda x: parties.index(x[0])))
        abgeordnete_absolute_nums = [seats for party, seats in num_seats_dict_sorted.items()]
        abgeordnete_absolute_nums = abgeordnete_absolute_nums[:-1] # without fraktionslos
        df_interruptions_num_norm_seats = df_interruptions_num.drop(index='fraktionslos').div(abgeordnete_absolute_nums, axis=0)
        df_interruptions_num_norm_seats['num_of_interruptions'] = df_interruptions_num_norm_seats['num_of_interruptions'].round(2)
        comments_per_party = df_interruptions_num_norm_seats['num_of_interruptions']
    
    party_colors = { # AfD and LINKE have different colors (compared to the line plots). These look nicer in Block form.
        'CDU/CSU': 'black',
        'SPD': 'red',
        'GRÜNE': 'green',
        'FDP': 'yellow',
        'AfD': 'blue',
        'DIE LINKE': 'red',
        'fraktionslos': 'gray'
    }


    yaxis = dict(autorange=True)
    title = 'Anzahl der Zwischenrufe nach Partei'

    if not norm_seats:
        fig = go.Figure(data=[go.Bar(x=parties_pd, y=comments_per_party, marker_color=[party_colors[party] for party in parties_pd])])
        yaxis['title'] = 'Anzahl der Zwischenrufe'
    else:
        fig = go.Figure(data=[go.Bar(x=parties_pd, y=comments_per_party, marker_color=[party_colors[party] for party in parties_pd])])
        title = 'Anzahl der Zwischenrufe normalisiert nach Sitzanzahl'
        yaxis['title'] = 'Zwischenrufe pro Abgeordneten'

    fig.update_layout(title=title,
                    xaxis_title="Partei",
                    xaxis=dict(tickangle=-45),
                    yaxis=yaxis
                    )

    return fig

def plot_interruption_matrix(start_date, end_date, norm_seats, bt_period, norm_sents, choose_date_with_bt_period):
    if norm_seats or choose_date_with_bt_period :
        start_date = bt_periods[str(bt_period)]['start_date'] # use bt_period start + end dates
        end_date = bt_periods[str(bt_period)]['end_date']

    interruption_matrix, sentence_counts = get_interrupt_matrix_for_timespan(start_date, end_date)

    if norm_seats:
        num_seats_dict_sorted =  dict(sorted(bt_periods[str(bt_period)]['num_seats'].items(), key = lambda x: parties.index(x[0])))
        print(num_seats_dict_sorted)
        abgeordnete_absolute_nums = [seats for party, seats in num_seats_dict_sorted.items()]
        abgeordnete_absolute_nums = abgeordnete_absolute_nums[:-1] # without fraktionslos
        print(abgeordnete_absolute_nums)
        interruption_matrix = interruption_matrix.drop(labels='fraktionslos').drop(columns='fraktionslos') # get rid of fraktionslos as the low number of people distorts the normed_output
        interruption_matrix = interruption_matrix.div(np.array(abgeordnete_absolute_nums), axis=1)
        print(f"interruption_matrix norm-seats: {interruption_matrix}")

    if norm_sents:
        if 'fraktionslos' in interruption_matrix.columns:
            interruption_matrix = interruption_matrix.drop(labels='fraktionslos').drop(columns='fraktionslos')
        print(sentence_counts[:-1])
        interruption_matrix = interruption_matrix.div(np.array(sentence_counts)[:-1])
    


    plt.figure(figsize=(8,6))
    sns.set_style("whitegrid")

    ax = sns.heatmap(interruption_matrix, cmap="Blues", annot=False, cbar=True, square=True, cbar_kws={'shrink': 0.8})

    # Rotate x-axis labels
    if len(interruption_matrix.columns) < len(parties): # ohne Fraktionslose Abgeordnete
        ax.set_xticklabels(parties[:-1], rotation=20)
        # Rotate x-axis labels
        ax.set_yticklabels(parties[:-1], rotation=0)
    else:
        ax.set_xticklabels(parties, rotation=20)
        ax.set_yticklabels(parties, rotation=0)

    # Set y-axis labels to the top
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')

    ax.set_xlabel('Partei des Zwischenrufenden', labelpad=5)
    ax.set_ylabel('Partei des Redners', labelpad=5)

    plt.title('Zwischenrufe im Deutschen Bundestag', pad=20)

    return plt


    
################################
# Utils
################################

def get_interruption_count_for_timespan(start_date, end_date):
    relevant_comments = df_interruptions[ (df_interruptions['date'] >=start_date) & (df_interruptions['date']  <= end_date)]
    
    custom_order = parties

    num_interruptions = relevant_comments.groupby('comment_party').size().reset_index(name='num_of_interruptions')

    # reorder rows
    num_interruptions = num_interruptions.set_index('comment_party').reindex(custom_order)

    return num_interruptions

def get_interrupt_matrix_for_timespan(start_date, end_date):
    relevant_comments = df_interruptions[ (df_interruptions['date'] >=start_date) & (df_interruptions['date']  <= end_date)]

    df_unique_speeches = relevant_comments.drop_duplicates(subset=['interrupted_speaker_party', 'speech_id'])
    df_sum_speech_len_sents = df_unique_speeches.groupby('interrupted_speaker_party')['speech_len_sents'].sum().reset_index()
    df_sum_speech_len_sents.columns = ['Party', 'Total_Speech_Length_Sents']
    df_sum_speech_len_sents = df_sum_speech_len_sents.set_index('Party').reindex(parties)

    interruption_matrix = pd.crosstab(relevant_comments['comment_party'], relevant_comments['interrupted_speaker_party']) # pretty handy function...

    interruption_matrix = interruption_matrix.reindex(parties, axis=1)
    interruption_matrix = interruption_matrix.reindex(parties, axis=0)

    return interruption_matrix.T, df_sum_speech_len_sents



#################################
# Data loading + preprocessing
#################################

parties = ['CDU/CSU', 'SPD','GRÜNE', 'FDP', 'AfD', 'DIE LINKE', 'fraktionslos']

party_colors = {
    'CDU/CSU': 'black',
    'AfD': 'lightblue',
    'DIE LINKE': 'darkred',
    'SPD': 'red',
    'GRÜNE': 'green',
    'FDP': 'yellow',
    'fraktionslos': 'grey'
    }

#------- df_interruptions ---------
df_interruptions =  pd.read_csv('../../_data/interruptions.csv')
df_interruptions['date'] = pd.to_datetime(df_interruptions['date'])
df_interruptions['year'] = df_interruptions['date'].dt.year

# group by year and party and calculate the size
interruptions_per_year = df_interruptions.groupby(['year', 'comment_party']).size().unstack(fill_value=0)
# format for plotly
interruptions_per_year = interruptions_per_year.reset_index().melt(id_vars='year', var_name='comment_party', value_name='interruptions')


#------- df speeches ------------
df_speeches = pd.read_csv('../../_data/speeches.csv', encoding='utf-8').drop(columns = 'Unnamed: 0').set_index('speech_id')

def clear_title(name):
    if name.startswith('Dr.'):
        return name[4:] 
    return name
df_speeches['speaker'] = df_speeches['speaker'].apply(clear_title)


df_speeches['date'] = pd.to_datetime(df_speeches['date'])
df_speeches['year'] = df_speeches['date'].dt.year

df_speeches_grouped = df_speeches.groupby('year')['speech_len_sents'].sum().reset_index()
df_speeches_grouped['number_protocols'] = df_speeches.groupby('year')['date'].nunique().to_list()

# group by year and calculate the total speech length
df_speeches_grouped_parties_years = df_speeches.groupby(['year', 'speaker_party'])['speech_len_sents'].sum().reset_index()
for year in range(1991, 2025):
    for party in parties:
        if not ((df_speeches_grouped_parties_years['year'] == year) & (df_speeches_grouped_parties_years['speaker_party'] == party)).any():
            df_speeches_grouped_parties_years = pd.concat([df_speeches_grouped_parties_years, pd.DataFrame([{'year': year, 'speaker_party': party, 'speech_len_sents': 0}])])
df_speeches_grouped_parties_years = df_speeches_grouped_parties_years.sort_values(by = 'year', ascending=True)

# ----------- Number of seats + start- &enddate ---------
with open('../../_data/bt_period_data.json', 'r', encoding='utf-8') as f:
    bt_periods = json.load(f)


#########################################
# Gradio Stuff
########################################

def line_plots_xdate(plot_type, start_year, end_year):
    if plot_type == 'Gesamtanzahl Sätze':
        return plot_num_sents_single(start_year, end_year)
    if plot_type =='Anzahl der Zwischenrufe nach Partei':
        return plot_interruptions_party_line(start_year, end_year)
    if plot_type =='Anzahl Sätze nach Partei':
        return plot_num_sents_party(start_year, end_year)
    
def plots_start_end(plot_type, norm_seats, norm_sents,bt_period, start_date, end_date, choose_date_with_bt_period):
    if plot_type == 'Anzahl der Zwischenrufe nach Partei':
        return plot_interruptions_by_party(start_date, end_date, norm_seats, bt_period, choose_date_with_bt_period)
    if plot_type =='Zwischenruf-Matrix':
        return plot_interruption_matrix(start_date, end_date, norm_seats, bt_period, norm_sents, choose_date_with_bt_period)
    

def handle_norm_sents_checkbox_change(norm, input_bt_period):
    if not input_bt_period:
        return {
            bundestagsperiode: gr.update(visible=norm),
            info_text: gr.update(visible=norm),
            start_date: gr.update(visible=not norm),
            end_date: gr.update(visible=not norm),
            choose_date_with_bt_period: gr.update(visible =not norm)
        }
    return {
            bundestagsperiode: gr.update(visible=input_bt_period),
            info_text: gr.update(visible=norm or input_bt_period),
            choose_date_with_bt_period: gr.update(visible =not norm)
        }

def handle_plot_type_change1(plot_type):
    return {
        norm_sents: gr.update(visible = plot_type == 'Zwischenruf-Matrix'),
        norm_seats: gr.update(visible = True)
    }


def handle_bt_period_change(bt_period):
    start_date = bt_periods[str(bt_period)]['start_date']
    end_date = bt_periods[str(bt_period)]['end_date']
    return f"Startdatum: {start_date} \nEnddatum: {end_date}"
    
def handle_input_fav(choose_date_with_bt_period,norm_seats):
    return {
        start_date: gr.update(visible= not choose_date_with_bt_period),
        end_date: gr.update(visible= not choose_date_with_bt_period),
        bundestagsperiode: gr.update(visible= choose_date_with_bt_period),
        info_text: gr.update(visible = choose_date_with_bt_period or norm_seats)
    }

with gr.Blocks() as tab1:

    plot = gr.Plot()
    refresh = gr.Button('Refresh')
    display = [
        gr.Dropdown(['Anzahl der Zwischenrufe nach Partei','Gesamtanzahl Sätze','Anzahl Sätze nach Partei' ], value = 'Anzahl der Zwischenrufe nach Partei', label="plot_type"),
        gr.Slider(1991, 2024, 1991, label='start_year', step=1),
        gr.Slider(1991, 2024, 2024, label='end_year', step=1)
    ]
    
    #display.change(line_plots_xdate, inputs=display, outputs=plot)
    refresh.click(line_plots_xdate, inputs=display, outputs=plot)
    tab1.load(fn=line_plots_xdate, inputs=display, outputs=plot)



with gr.Blocks() as tab2:
    with gr.Row():
        with gr.Column(scale=4):
            plot_type = gr.Dropdown(['Zwischenruf-Matrix', 'Anzahl der Zwischenrufe nach Partei'], value='Zwischenruf-Matrix', label="plot_type")
            norm_seats = gr.Checkbox(value=False, label='Grafiken nach Anzahl der Sitze der Unterbrecher-Partei normalisieren')
            norm_sents = gr.Checkbox(value=False, label='Grafiken nach Anzahl der gesprochenen Sätze der Redner-Partei im Zeitraum normalisieren')
            choose_date_with_bt_period = gr.Checkbox(value=False, label='Zeitraum per Bundestagsperiode bestimmen')
            bundestagsperiode = gr.Dropdown(range(12, 21), value=20, label='Bundestagsperiode', visible=False)
            start_date = Calendar(type="datetime", label="start_date", value=datetime(2017, 9, 1))
            end_date = Calendar(type="datetime", label="end_date", value=datetime(2024, 6, 20))
            info_text = gr.Textbox(value =  "Startdatum: 2021-10-26\nEnddatum: 2025-09-01",
                                   label= 'info_text', visible = False)

            # Connect the checkbox change to the handler
            norm_seats.change(fn=handle_norm_sents_checkbox_change, inputs=[norm_seats, choose_date_with_bt_period], outputs=[bundestagsperiode, info_text, start_date, end_date, choose_date_with_bt_period])
            plot_type.change(fn= handle_plot_type_change1, inputs = plot_type, outputs = [norm_sents, norm_seats])
            bundestagsperiode.change(fn=handle_bt_period_change, inputs=bundestagsperiode, outputs=info_text)
            choose_date_with_bt_period.change(fn = handle_input_fav, inputs= [choose_date_with_bt_period,norm_seats], outputs=[start_date, end_date, bundestagsperiode, info_text])

        with gr.Column(scale=12):
            plot = gr.Plot()
            refresh = gr.Button('Refresh')

    refresh.click(fn=plots_start_end, inputs=[plot_type, norm_seats, norm_sents, bundestagsperiode, start_date, end_date, choose_date_with_bt_period], outputs=plot)
    tab2.load(fn=plots_start_end, inputs=[plot_type, norm_seats, norm_sents,bundestagsperiode, start_date, end_date, choose_date_with_bt_period], outputs=plot)



demo = gr.TabbedInterface(
    [tab1, tab2], 
    ['Linien Plots', 'Unterbrechungen in anderen Darstellungsformen']
)

demo.launch()

