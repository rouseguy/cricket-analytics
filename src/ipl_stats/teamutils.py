import streamlit as st
from streamlit_folium import folium_static
import folium
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dask.dataframe as dd
import datashader as ds
from matplotlib.cm import hot, viridis, Blues, plasma, magma, Greens
import datashader.transfer_functions as tf
import plotly.express as px
sns.set()
import chart_studio.plotly as py
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
cf.go_offline()
import plotly.express as px
import plotly.graph_objs as go

matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')
matches.replace({'Sunrisers Hyderabad':'Hyderabad Sunriser','Deccan Chargers':'Hyderabad Sunriser',\
'Rising Pune Supergiants':'Pune Supergiant','Delhi Daredevils':'Delhi Capitals',\
'Pune Warriors':'Pune Warriors','Punjab Kings':'Kings XI Punjab',
'Rising Pune Supergiant':'Pune Supergiant'}, inplace= True)

@st.cache(hash_funcs={dict: lambda _: None})
def make_fig():
    some_fig = Achart().graph1()
    cached_dict = {'f1': some_fig}    
    return cached_dict



def get_team1_name():
    return np.unique(matches['team1'].values) 
def get_team2_name():
    return np.unique(matches['team2'].values) 
def get_city_name():
    return np.unique(matches['country'].values)
    

def comparison(team1,team2):
    compare = matches[((matches['team1']==team1) | (matches['team2']==team1)) & ((matches['team1']==team2) | (matches['team2']==team2))]
    fig = plt.figure(figsize=(10,5))
    sns.countplot(x='season',hue='winner',data=compare)    
    return st.pyplot(fig)
    


def winper():
    winloss = matches[['team1','team2','winner']]
    winloss.head()
    winloss['loser'] = winloss.apply(lambda x: x['team2'] if x['team1']== x['winner'] else x['team1'], axis = 1)
    teamwins = winloss['winner'].value_counts()
    teamloss = winloss['loser'].value_counts()
    played = (matches['team1'].value_counts() + matches['team2'].value_counts()).reset_index()
    played.columns = ['team','played']
    wins = matches['winner'].value_counts().reset_index()
    wins.columns = ['team','won']
    played = played.merge(wins, left_on='team', right_on='team', how='inner')
    loss = winloss['loser'].value_counts().reset_index()
    loss.columns = ['team','lost']
    played = played.merge(loss, left_on = 'team', right_on = 'team', how='inner')
    played['%win'] = round((played['won'] / played['played'])*100,2)
    played['%loss'] = round((played['lost'] / played['played']) * 100,2)
    played = played.sort_values(by='%win',ascending=False)
    return played
    
def venue(choice):
    json1 = f"states_india.geojson"
    m = folium.Map(location=[23.47,77.94], tiles='CartoDB Dark Matter', name="Light Map",
               zoom_start=5, attr="iplnani.com")
    win_venue = f"winner.csv"
    win_venue_data = pd.read_csv(win_venue)
    choice_selected=choice
    folium.Choropleth(
        geo_data=json1,
        name="choropleth",
        data=win_venue_data,
        columns=["state_code",choice_selected],
        key_on="feature.properties.state_code",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name=choice_selected
    ).add_to(m)
    folium.features.GeoJson('states_india.geojson',name="States", popup=folium.features.GeoJsonPopup(fields=["st_nm"])).add_to(m)

    folium_static(m, width=700, height=500)