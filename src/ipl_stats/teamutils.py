import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import chart_studio.plotly as py
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
cf.go_offline()
import plotly.express as px
import plotly.graph_objs as go

absolute_path = os.path.abspath(__file__)
path = os.path.dirname(absolute_path)

matches = pd.read_csv(path+'/matches.csv')
deliveries = pd.read_csv(path+'/deliveries.csv')
matches.replace({'Sunrisers Hyderabad':'Hyderabad (Sunriser/Chargers)','Deccan Chargers':'Hyderabad (Sunriser/Chargers)',\
'Rising Pune Supergiants':'Pune (Supergiant/ Warriors)','Delhi Daredevils':'Delhi (Capitals/ Daredevils)',\
'Delhi Capitals':'Delhi (Capitals/ Daredevils)','Pune Warriors':'Pune (Supergiant/ Warriors)','Punjab Kings':'Kings XI Punjab',
'Rising Pune Supergiant':'Pune (Supergiant/ Warriors)'}, inplace= True)

@st.cache(hash_funcs={dict: lambda _: None})
def make_fig():
    some_fig = Achart().graph1()
    cached_dict = {'f1': some_fig}    
    return cached_dict



def get_team1_name():
    return np.unique(matches['team1'].values) 
def get_team2_name():
    return np.unique(matches['team2'].values) 

    

def comparison(team1,team2):
    compare = matches[((matches['team1']==team1) | (matches['team2']==team1)) & ((matches['team1']==team2) | (matches['team2']==team2))]
    fig = plt.figure(figsize=(10,5))
    sns.countplot(x='season',hue='winner',data=compare)    
    return st.pyplot(fig)
    
def lucky(matches,team):
    return matches[matches['winner']==team]['venue'].value_counts()

 
def geth2h(team1,team2):
    teams = [team1,team2]
    if team1 in teams and team2 in teams:
        return True
    else:
        return False

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
    
    

    
    #return h2h
    
    #fig = plt.figure(figsize=(10,5))
    #sns.countplot(x='winner',hue='df',data=h2h) 
    
