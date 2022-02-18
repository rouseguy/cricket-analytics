import streamlit as st
from teamutils import *
from teammodules import *
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import chart_studio.plotly as py
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()
import plotly.express as px
import plotly.graph_objs as go

select=st.sidebar.selectbox('Cricket Analysis',['Team Stats', 'Player Stats'])

if select=='Team Stats':
    select = st.sidebar.selectbox('Team Analysis', ['Toss Wins','Lucky Venues','Comparison between Teams','Total Runs', 'Win Count' ])
    if select == 'Comparison between Teams':
        compare()
    elif select == 'Lucky Venues':
        luckvenue()
    elif select == 'Total Runs':
        totalruns()
    elif select == 'Toss Wins':
        tosswins()
    elif select == 'Win Count':
        wincount()


    


# runs   = pd.concat([season_runs(player, ipl_ball, ipl_match, 'IPL'), season_runs(player, bbl_ball, bbl_match, 'BBL')], ignore_index=True)
# wicket = pd.concat([season_wickets(player, ipl_ball, ipl_match, 'IPL'), season_wickets(player, bbl_ball, bbl_match, 'BBL')], ignore_index=True)


# c  =  alt.Chart(runs).mark_bar().properties(width=350).encode(
#         x='year',
#         y='batsman_runs',
#         color='Game',
#         column='Game'
#     )
# st.subheader('Batting Carrier')
# st.altair_chart(c)
# col1, col2 = st.columns(2)

# c  =  alt.Chart(wicket).mark_bar().properties(width=350).encode(
#         x='year',
#         y='batsman',
#         color='Game',
#         column='Game'
#     )

# st.subheader('Bowling Carrier')
# st.altair_chart(c)

# st.subheader('Head-Head')
# convert_dict = {'Dots': int ,'1':int,'2': int,'4': int,'6': int ,'runs':int,'balls': int,'Strike Rate':int}  

# if player_type == 'bowler':
#     batsman = st.selectbox('Player', get_player(ipl_ball,'batsman'))
#     st.subheader(player+' Vs '+batsman)

#     stat  = pd.concat([one_vs_one(batsman,get_data(player,ipl_ball,'bowler') , ipl_match, 'IPL'), 
#                        one_vs_one(batsman, get_data(batsman,bbl_ball,'bowler'), bbl_match, 'BBL')], 
#                        ignore_index=True)

# else:
#     bowler  = st.selectbox('Player', get_player(ipl_ball,'bowler'))
#     st.subheader(player+' Vs '+ bowler)

#     stat  = pd.concat([one_vs_one(player,get_data(bowler,ipl_ball,'bowler') , ipl_match, 'IPL'), 
#                        one_vs_one(player, get_data(bowler,bbl_ball,'bowler'), bbl_match, 'BBL')], 
#                        ignore_index=True)


# stat = stat[['year','Dots','1','2','4','6','runs','balls','wicket','Strike Rate','Game']]
# stat = stat.set_index('year')
# st.dataframe(stat.astype(convert_dict)  )
