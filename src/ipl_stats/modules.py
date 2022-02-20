import streamlit as st
import pandas as pd
from utils import *
from modules import *
import os
import numpy as np
import altair as alt
import plotly.graph_objects as go

absolute_path = os.path.abspath(__file__)
path = os.path.dirname(absolute_path)

ipl_ball    =  pd.read_csv(path+'/2008_2021_updated_ball.csv')
ipl_match   =  pd.read_csv(path+'/2008_2021_data_matches.csv')
season_list = ['2007/08','2009','2009/10','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020/21','2021']
season_dict = {2008:'2007/08',2009:'2009',2010:'2009/10',2011:'2011',2012:'2012',2013:'2013',2014:'2014',2015:'2015',2016:'2016',2017:'2017',2018:'2018',2019:'2019',2020:'2020/21',2021:'2021'}
team_dict   =  { 'Delhi Capitals':'Delhi Daredevils' , 'Punjab Kings':'Kings XI Punjab' }

GRID  = True
WIDTH = 0

def formatt(df):
    temp = []
    for i in df.columns:
        if i in  ['SR', 'Avg', 'Eco','Win Percent']:
            temp.append(i)
    return df.style.format(subset=temp, formatter="{:.2f}")
    

def player_career():
    st.title('Player Career')
    player = st.sidebar.selectbox('Player', get_player_name(ipl_ball))
    bat  = pd.DataFrame(get_run( ipl_ball, [player] ))
    bat  = bat.drop(['batsman'], axis = 1)
    bat['M'] = 'IPL' 
    bat  = bat.set_index('M')
    bowl = pd.DataFrame(get_wicket( ipl_ball, [player]  ))
    bowl = bowl.drop(['bowler'], axis = 1)
    bowl['M'] = 'IPL' 
    bowl  = bowl.set_index('M')

    st.subheader('Batting Career')
    bat['Runs'] = bat.apply(lambda x: "{:,}".format(x['Runs']), axis=1)

    st.table(formatt(bat))

    st.subheader('Bowling Career')
    st.table(formatt(bowl))

    result = pd.DataFrame()
    for i in season_list:
        match = ipl_match[ipl_match['season'] == i]
        id = list(match['id'].unique())
        ball = ipl_ball[ipl_ball['id'].isin(id)]
        temp = get_run(ball, batsman = [player], choice = ['Innings','Runs','HS'])
        temp['year'] = i
        result = pd.concat([result,pd.DataFrame(temp)])
    st.subheader('Yearly Performance')
    result =  result.drop(['batsman'], axis = 1)
    c =  alt.Chart(result).mark_trail().encode(
        x='year:T',
        y='Runs:Q',
        size = 'Runs:Q',
        tooltip=['Runs:Q']
    ).configure_axis(
    grid= GRID
    ).configure_view(
        strokeWidth= WIDTH
    ).interactive()

    st.altair_chart(c, use_container_width=True)
    result_bat = result.set_index('year')

    result = pd.DataFrame()
    for i in season_list:
        match = ipl_match[ipl_match['season'] == i]
        id = list(match['id'].unique())
        ball = ipl_ball[ipl_ball['id'].isin(id)]
        temp = get_wicket(ball, bowler= [player], choice = ['Innings','Wickets','BBI'])
        temp['year'] = i
        result = pd.concat([result,pd.DataFrame(temp)])

    result =  result.drop(['bowler'], axis = 1)
    
    c =  alt.Chart(result).mark_trail().encode(
        x='year:T',
        y='Wickets:Q',
        size = 'Wickets:Q',
        tooltip = ['Wickets:Q'],
        color=alt.value("#FFAA00")
    ).configure_axis(
    grid= GRID
    ).configure_view(
        strokeWidth= WIDTH
    ).interactive()
    st.altair_chart(c, use_container_width=True)
    result_bowl = result.set_index('year')


    result = pd.merge(result_bat, result_bowl, how = 'outer', left_on = ['year'], right_on = ['year'])
    result = result[ ~ ((result['Innings_x'] == 0) & (result['Innings_y'] == 0))]
    result = result.rename(columns = {'Innings_x':'Innings Bat' ,'Innings_y':'Innings Bowl' })
    st.table(formatt(result))


def sesonal_stat():
    st.title('Sesonal Stats')
    result = pd.DataFrame()
    choice = ['Innings']
    player_type  = st.sidebar.selectbox('Player Type', ['Batsman','Bowler'] )
    
    if player_type == 'Batsman':
        option = ['Runs','Six','Four','Hundered','Fifty','BF','Avg','SR']
        flag  = st.sidebar.selectbox('Category', option )
        choice.append('Runs')
        if flag != 'Runs':
           choice.append(flag)
    else:
        option =  ['Wickets','Balls','Runs','BBI','Avg','SR','Eco','5W','BBI']
        flag  = st.sidebar.selectbox('Category', option )
        choice.append('Wickets')
        if flag != 'Wickets':
           choice.append(flag)
        

    limit = st.sidebar.slider('Top', 1, 10)
    start_year, end_year = st.sidebar.select_slider("Year", options = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021] , value = (2008,2021))

    temp = []
    for i in option:
        if i not in choice:
            temp.append(i)
    column = st.sidebar.multiselect('Cloumns',temp)

    for i in column:
        choice.append(i)

    innings = st.sidebar.number_input('Innings', step = 0)
    innings = None if innings == 0 else innings

    if 'Wickets' in choice:
        wickets = st.sidebar.number_input('Wickets', step = 0)
        wickets = None if wickets == 0 else wickets
    else:
        runs    = st.sidebar.number_input('Runs', step = 0)
        runs    = None if runs == 0 else runs

    for i in range(start_year, end_year+1):
        i = season_dict[i]
        match = ipl_match[ipl_match['season'] == i]
        id = list(match['id'].unique())
        ball = ipl_ball[ipl_ball['id'].isin(id)]
        if player_type == 'Batsman' :
            temp = get_run(ball,flag = flag, choice = choice, limit = limit, innings = innings, runs = runs)
        else:
            asc = True if flag in ['SR','Eco','Avg'] else False
            temp = get_wicket(ball,flag = flag, choice = choice, limit = limit, innings = innings, wickets = wickets, asc = asc )
        temp['year'] = i
        result = pd.concat([result,pd.DataFrame(temp)])
    result =  result.reset_index()
    result = result.rename(columns = {'index':'Position'})
    result['Position'] += 1
    if player_type == 'Batsman':
        choice.insert(0,'batsman')
    else:
        if 'BBI' in choice:
            choice.remove('BBI')
        choice.insert(0,'bowler')
        if flag == 'BBI':
            flag = 'Wickets'

    c = alt.Chart(result).mark_bar().encode(
        x=alt.X(flag),
        y='year',
        tooltip = choice,
    color = alt.Color('Position', scale=alt.Scale(scheme='redyellowgreen'))
    ).configure_axis(
        grid=False
    ).configure_view(
            strokeWidth= WIDTH
    )
    st.altair_chart(c,use_container_width=True )
    result = result.set_index('year')
    st.table(formatt(result))


def overall_stat():
    st.title('Overall Stats')
    result = pd.DataFrame()
    choice = ['Innings']
    player_type  = st.sidebar.selectbox('Player Type', ['Batsman','Bowler'] )
    
    if player_type == 'Batsman':
        option = ['Runs','Six','Four','Hundered','Fifty','BF','Avg','SR']
        flag  = st.sidebar.selectbox('Category', option )
        choice.append('Runs')
        if flag != 'Runs':
           choice.append(flag)
    else:
        option =  ['Wickets','Balls','Runs','BBI','Avg','SR','Eco','5W','BBI']
        flag  = st.sidebar.selectbox('Category', option )
        choice.append('Wickets')
        if flag != 'Wickets':
           choice.append(flag)
        

    limit = st.sidebar.slider('Top', 1, 20,10)

    temp = []
    for i in option:
        if i not in choice:
            temp.append(i)
    column = st.sidebar.multiselect('Cloumns',temp)

    for i in column:
        choice.append(i)

    innings = st.sidebar.number_input('Innings', step = 0)
    innings = None if innings == 0 else innings

    if 'Wickets' in choice:
        wickets = st.sidebar.number_input('Wickets', step = 0)
        wickets = None if wickets == 0 else wickets
    else:
        runs    = st.sidebar.number_input('Runs', step = 0)
        runs    = None if runs == 0 else runs

    
    if player_type == 'Batsman' :
        temp = get_run(ipl_ball,flag = flag, choice = choice, limit = limit, innings = innings, runs = runs)
        get_player_runs(temp['batsman'].unique())
    else:
        asc = True if flag in ['SR','Eco','Avg'] else False
        temp = get_wicket(ipl_ball,flag = flag, choice = choice, limit = limit, innings = innings, wickets = wickets, asc = asc )
        get_player_wickets(temp['bowler'].unique())
    result = pd.concat([result,pd.DataFrame(temp)])
    result =  result.reset_index()
    result = result.rename(columns = {'index':'Position'})
    result['Position'] += 1
    result = result.set_index('Position')
    
    st.table(formatt(result))

    if player_type == 'Batsman':
        c = alt.Chart(result).mark_circle( color='#EA484E').encode(
            alt.X('batsman', scale=alt.Scale(zero=False)),
            alt.Y('Innings', scale=alt.Scale(zero=False, padding=1)),
            tooltip = ['Runs']
        ).configure_axis(
        grid=GRID
        ).configure_view(
            strokeWidth= WIDTH
        ).encode(
        size=alt.Size('Runs', scale=alt.Scale(domain=[3000,5000]))
        ).interactive()
        st.altair_chart(c, use_container_width=True)
    else:
        c = alt.Chart(result).mark_circle( color='#EA484E').encode(
            alt.X('bowler', scale=alt.Scale(zero=False)),
            alt.Y('Innings', scale=alt.Scale(zero=False, padding=1)),
            tooltip = ['Wickets']
        ).configure_axis(
        grid=GRID
        ).configure_view(
            strokeWidth= WIDTH
        ).encode(
        size=alt.Size('Wickets', scale=alt.Scale(domain=[100,150]))
        ).interactive()
        st.altair_chart(c, use_container_width=True)


def one_vs_one():
    st.title('One Vs One')
    all_player = get_player_name(ipl_ball)
    player = st.sidebar.selectbox('Player', all_player)
    type_ = st.sidebar.selectbox('Vs', ['Team','Player'])

    if type_ == 'Player':
        player_removed = []
        for i in all_player:
            if i != player:
                player_removed.append(i)
        vs = st.sidebar.selectbox(type_,player_removed)
        vs_data = []
        vs_data.append(vs)

    else:
        team = []
        for i in list(ipl_ball['batting_team'].unique()):
            if i not in team_dict.values():
                team.append(i)

        vs = st.sidebar.selectbox(type_,team)
        vs_data = []
        vs_data.append(vs)
        if vs in team_dict.keys():
            vs_data.append(team_dict[vs])

    if type_ == 'Team':
        df_bat = get_team_data(vs_data, ipl_ball, 'batsman')
        df_bat = pd.DataFrame(get_run(df_bat,[player] ))
        df_bat = df_bat.drop(['batsman'], axis = 1)
        df_bat['M'] = 'IPL' 
        df_bat  = df_bat.set_index('M')
        st.subheader('Batting Stats')
        st.caption(player+' Vs '+vs_data[0])
        st.table(formatt(df_bat))

        df_bowl = get_team_data(vs_data, ipl_ball, 'bowler')
        df_bowl = pd.DataFrame(get_wicket(df_bowl,[player] ))
        df_bowl = df_bowl.drop(['bowler'], axis = 1)
        df_bowl['M'] = 'IPL' 
        df_bowl  = df_bowl.set_index('M')
        st.subheader('Bowling Stats')
        st.caption(player+' Vs '+vs_data[0])
        st.table(formatt(df_bowl))

    else:
        df_bat = get_player_data(vs_data, ipl_ball, 'bowler')
        df_bat = pd.DataFrame(get_run(df_bat,[player] ))
        df_bat = df_bat.drop(['batsman'], axis = 1)
        df_bat['M'] = 'IPL' 
        df_bat  = df_bat.set_index('M')
        st.subheader('Batting Stats')
        st.caption(player+' Vs '+vs_data[0])
        st.table(formatt(df_bat))

        df_bowl = get_player_data([player], ipl_ball, 'batsman')
        df_bowl = pd.DataFrame(get_wicket(df_bowl,vs_data ))
        df_bowl = df_bowl.drop(['bowler'], axis = 1)
        df_bowl['M'] = 'IPL' 
        df_bowl  = df_bowl.set_index('M')
        st.subheader('Bowling Stats')
        st.caption(vs_data[0]+' Vs '+player)
        st.table(formatt(df_bowl))


def over_stats():
    type_ = st.sidebar.selectbox('Type', ['Runs','Wickets','Six','Four','SR'])
    balls = 1
    if type_ in ['SR']:
        balls    = st.sidebar.number_input('BF', step = 0, min_value = 1)

    data  = best_in_over(ipl_ball, type_, balls)
    data  =  data.reset_index()
    data  = data.rename(columns = {'index':'Over'})
    data['over'] += 1 
    st.title('Over Stats')
    hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    choice = []
    choice.append('bowler' if type_ == 'Wickets' else 'batsman')

    choice.append(type_)
    c = alt.Chart(data).mark_area(
            line={'color':'darkgreen'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='darkgreen', offset=1)],
                x1=1,
                x2=1,
                y1=1.2,
                y2=0
            )
        ).encode(
            x = alt.X('over',scale = alt.Scale(zero=False)),
            y = '{0}'.format(type_),
            tooltip = choice
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth= WIDTH
        )
    st.altair_chart(c,use_container_width=True)
    st.table(formatt(data))


def win_predict_player():
    type_  = st.sidebar.selectbox('Type', ['Batting','Bowling'])
    team = []
    for i in list(ipl_ball['batting_team'].unique()):
        if i not in team_dict.values():
            team.append(i)
    team_1 = st.sidebar.selectbox('Team', team)
    team_data = []
    team_data.append(team_1)
    if team_1 in team_dict.keys():
        team_data.append(team_dict[team_1])

    if type_ == 'Batting':
        runs    = st.sidebar.number_input('Runs', step = 0, min_value = 30)
        batsman = list(ipl_ball[ipl_ball['batting_team'].isin(team_data)]['batsman'].unique())
        batsman.insert(0,None)
        player  = st.sidebar.selectbox('Player',batsman)
        opp = []
        for i in list(ipl_ball['batting_team'].unique()):
            if i not in team_dict.values() and i not in team_data:
                opp.append(i)
        opp.insert(0,None)
        opp_inp   =  st.sidebar.selectbox('Opponent',opp)
        opp_team = []
        opp_team.append(opp_inp)
        if opp_inp in team_dict.keys():
            opp_team.append(team_dict[opp_inp])

        venue     = list(ipl_match['venue'].unique())
        venue.insert(0,None)
        venue_inp = st.sidebar.selectbox('Venue',venue)
        innings   = st.sidebar.slider('Minimum Innings',1,10)

        win,result = decide_batsman(ipl_ball, ipl_match, team_data, player = player, runs = runs, opp = opp_team ,venue = venue_inp, thres = innings)
    else:
        wickets    = st.sidebar.number_input('Wickets', step = 0, min_value = 2 )
        bowler = list(ipl_ball[ipl_ball['bowling_team'].isin(team_data)]['bowler'].unique())
        bowler.insert(0,None)
        player  = st.sidebar.selectbox('Player',bowler)
        opp = []
        for i in list(ipl_ball['bowling_team'].unique()):
            if i not in team_dict.values() and i not in team_data:
                opp.append(i)
        opp.insert(0,None)
        opp_inp   =  st.sidebar.selectbox('Opponent',opp)
        opp_team = []
        opp_team.append(opp_inp)
        if opp_inp in team_dict.keys():
            opp_team.append(team_dict[opp_inp])

        venue     = list(ipl_match['venue'].unique())
        venue.insert(0,None)
        venue_inp = st.sidebar.selectbox('Venue',venue)
        innings   = st.sidebar.slider('Minimum Innings',1,10)
   
        win,result = decide_bowler(ipl_ball, ipl_match, team_data, player = player, wickets = wickets, opp = opp_team ,venue = venue_inp, thres = innings)

    source = pd.DataFrame({"category": ['Win', 'Lost'], "value": [win, 1- win]})

    st.title('Win Percent')
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = int(win*100),
    domain = {'x': [0, 0.8], 'y': [0, 1]},
    gauge = {'axis':{'range':[0,100]}, }))
    st.plotly_chart(fig)
    st.table(formatt(result))

    fig.update_layout(xaxis = {'range': [0, 100]})



def get_player_runs(batsman):
    result = pd.DataFrame()
    for i in season_list:
        match = ipl_match[ipl_match['season'] == i]
        id   = list(match['id'].unique())
        ball = ipl_ball[ipl_ball['id'].isin(id)]
        ball = ball[ball['batsman'].isin(batsman)]
        temp = ball.groupby(['batsman']).agg({'batsman_runs':'sum'})
        temp['year'] = i
        temp = temp.rename(columns = {'batsman_runs':'Runs'})
        result = pd.concat([result,pd.DataFrame(temp)])
    result = result.reset_index()
    c = alt.Chart(result).mark_rect().encode(
        x = 'batsman:O',
        y = 'year:O',
        color = alt.Color('Runs:Q', scale=alt.Scale(scheme='reds')),
        tooltip = ['Runs:Q']
    ).configure_axis(
        grid=False
    ).configure_view(
            strokeWidth= WIDTH
    )
    st.altair_chart(c,  use_container_width=True)


def get_player_wickets(bowler):
    result = pd.DataFrame()
    for i in season_list:
        match = ipl_match[ipl_match['season'] == i]
        id   = list(match['id'].unique())
        ball = ipl_ball[ipl_ball['id'].isin(id)]
        ball = ball[(ball['is_wicket'] == 1) & (ball['dismissal_kind'].isin(['caught','bowled','lbw','stumped','caught and bowled','hit wicket']))]
        ball = ball[ball['bowler'].isin(bowler)]
        temp = ball.groupby(['bowler']).agg({'is_wicket':'sum'})
        temp = temp.rename(columns = {'is_wicket':'Wickets'})
        temp['year'] = i
        result = pd.concat([result,pd.DataFrame(temp)])
    result = result.reset_index()
    c = alt.Chart(result).mark_rect().encode(
        x = 'bowler:O',
        y = 'year:O',
        color = alt.Color('Wickets:Q', scale=alt.Scale(scheme='reds')),
        tooltip = ['Wickets:Q']
    ).configure_axis(
        grid=False
    ).configure_view(
            strokeWidth= WIDTH
    )
    st.altair_chart(c,  use_container_width=True)