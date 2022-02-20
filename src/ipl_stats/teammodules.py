import streamlit as st
from teamutils import *
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
season_list = ['2007/08','2009','2009/10','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020/21','2021']
season_dict = {2008:'2007/08',2009:'2009',2010:'2009/10',2011:'2011',2012:'2012',2013:'2013',2014:'2014',2015:'2015',2016:'2016',2017:'2017',2018:'2018',2019:'2019',2020:'2020/21',2021:'2021'}
team_dict   =  { 'Delhi Capitals':'Delhi Daredevils' , 'Punjab Kings':'Kings XI Punjab' }

@st.cache(max_entries=130, ttl=3600)
def make_fig():
    some_fig = Achart().graph1()
    return some_fig
    
def compare():
    st.title("Comparison Between Teams by Wins")
    team1 = st.sidebar.selectbox('Team 1', get_team1_name())
    team2 = st.sidebar.selectbox('Team 2', get_team2_name())
    comparison(team1,team2)
    
def luckvenue():
    st.title("Lucky Venue for the Team")
    team = st.sidebar.selectbox('Team', get_team1_name())
    fig=lucky(matches,team)[:10].figure(kind='bar')
    st.plotly_chart(fig)

def tosswins():
    st.title("Toss winning Decision")
    tossdec = matches.groupby('season')['toss_decision'].value_counts()
    tossdec = pd.DataFrame(tossdec)
    tossdec.columns = ['Count']
    tossdec.reset_index(inplace=True)
    tossdec.set_index('season',inplace=True)
    fig = plt.figure(figsize=(10,5))
    sns.countplot(x='season',hue='toss_decision',data=matches);
    st.pyplot(fig)
    
def wincount():
    st.title("Winning and Losing Percentage between each team")
    st.table(winper())



def totalruns():
    st.title("Total runs scored")
    batting_team_gp = deliveries.groupby(['batting_team']).total_runs.sum()
    #convert grouped data to dataframe
    batting_team_gp_df = pd.DataFrame(batting_team_gp)
    batting_team_gp_df.reset_index(inplace=True) 
    batting_team_gp_df.columns = ['Batting Team', 'Total Runs'] #rename the columns 
    fig = px.bar(batting_team_gp_df, x='Batting Team', y='Total Runs', text='Total Runs', color='Total Runs', height = 550,labels={'Batting Team':'Batting Team', 'Total Runs':'Total Runs'}, title='Total Runs by each Batting Team')
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_xaxes(tickangle=45)
    #figu = fig.show()
    st.plotly_chart(fig)
    
    
    
 
