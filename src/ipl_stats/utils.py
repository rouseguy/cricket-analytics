import pandas as pd
import numpy as np

def get_start_end(player, ball, match):
    temp   =  match[['id','date']]
    flag   =  ball[['id','bowler']]
    player =  bbl_ball[bbl_ball['bowler'] == bowler ]
    final  =  pd.merge(temp,flag,how='inner',left_on=['id'],right_on=['id'])
    return final['date'].min(),final['date'].max()

def get_player_name(ball):
    return np.unique(ball[['batsman', 'bowler','non_striker']].values) 

def get_wicket(ball,bowler = None, flag = 'Wickets', innings = None, wickets = None, choice = None, limit = 3,  asc = False):
    
    player                  = ball[ball['bowler'].isin(bowler)] if bowler else ball
    wicket                  = len(player[(player['is_wicket'] == 1) & (player['dismissal_kind'].isin(['caught','bowled','lbw','stumped','caught and bowled','hit wicket']))])

    temp_wicket             = player[(player['is_wicket'] == 1) & (player['dismissal_kind'].isin(['caught','bowled','lbw','stumped','caught and bowled','hit wicket']))].groupby(['bowler']).agg({'is_wicket':'sum'}).astype(int)
    
    if len(temp_wicket) == 0:
        tt = pd.DataFrame(columns = [ 'bowler','Innings','Wickets','Balls','Runs','BBI','Avg','SR','Eco','5W' ] )
        tt = tt[choice] if choice else tt[['Innings','Wickets','Balls','Runs','BBI','Avg','SR','Eco','5W']]
        tt['bowler'] = bowler
        tt['BBI'] = '-'
        return tt.fillna(0) 
    
    temp_wicket['Innings']  = player.groupby(['bowler']).agg({'id':'nunique'})
    temp_wicket['Balls']    = player[~player['extras_type'].isin(['wides','noballs','penalty'])].groupby(['bowler']).agg({'id':'count'})
    temp_wicket['Runs']     = player[ ~ player['extras_type'].isin(['legbyes','byes','penalty'])].groupby(['bowler']).agg({'total_runs':'sum'})
    
    flag1                   = player[player['dismissal_kind'].isin(['caught','bowled','lbw','stumped','caught and bowled','hit wicket'])].groupby(['id','bowler']).agg({'is_wicket':'sum'})
    flag2                   = player[ ~ player['extras_type'].isin(['legbyes','byes','penalty'])].groupby(['id','bowler']).agg({'total_runs':'sum'})
    
    final                   = pd.merge(flag1, flag2, how = 'inner', left_on= ['bowler','id'],right_on = ['bowler','id'] ).sort_values(['is_wicket','total_runs'], ascending = [False, True]).groupby(['bowler']).head(1).reset_index()
    final['bbi']            = final['is_wicket'].astype(int).astype(str) + '/' + final['total_runs'].astype(str)
    fin                     = final.copy()
    final                   = final[['bowler','bbi']].set_index('bowler')
    temp_wicket['BBI']      = final
    temp_wicket['Avg']      = round(temp_wicket['Runs']  / temp_wicket['is_wicket'],2)
    temp_wicket['SR']       = round(temp_wicket['Balls'] / temp_wicket['is_wicket'],2)
    temp_wicket['Eco']      = round( temp_wicket['Runs'] / (temp_wicket['Balls'] / 6 ),2)
    temp_wicket['5W']       = flag1[flag1['is_wicket'] == 5].groupby(['bowler']).agg({'is_wicket':'count'}).astype(int)
    
    temp_wicket             = temp_wicket.rename(columns = {'is_wicket':'Wickets'})
    temp_wicket             = temp_wicket.fillna(0) 
    temp_wicket             = temp_wicket.astype({'5W':int})
    temp_wicket             = temp_wicket[temp_wicket['Innings'] >= innings] if innings else temp_wicket 
    temp_wicket             = temp_wicket[temp_wicket['Wickets'] >= wickets ] if wickets else temp_wicket 
    temp_wicket             = temp_wicket[choice] if choice else temp_wicket[['Innings','Wickets','Balls','Runs','BBI','Avg','SR','Eco','5W']]
    

    if flag == 'BBI':
        fin                 = fin[['bowler','is_wicket','total_runs']].set_index('bowler')
        temp_wicket[['X','Y']]  = fin
        temp_wicket = temp_wicket.sort_values(['X','Y'], ascending = [False, True]).head(limit).reset_index() 
        return temp_wicket.drop(['X','Y'], axis = 1).head(limit)
        
    return temp_wicket.sort_values(flag, ascending = asc ).head(limit).reset_index()





def get_run(ball, batsman = None, flag = 'Runs', innings = None, runs = None, choice = None, limit = 3, asc = False ):
    
    player                = ball[ball['batsman'].isin(batsman) ] if batsman else ball   
    temp_runs             = player.groupby(['batsman']).agg({'batsman_runs': 'sum'})
    
    runs_match            = player.groupby(['id']).agg({'batsman_runs':'sum'}).sort_values('batsman_runs',ascending = False)
    if len(temp_runs) == 0:
        tt = pd.DataFrame(columns = [ 'batsman','Innings','Not Out','Runs','Dots','HS','Avg','BF','SR','Hundered','Fifty','Four','Six' ] )
        tt = tt[choice] if choice else tt[['Innings','Not Out','Runs','Dots','HS','Avg','BF','SR','Hundered','Fifty','Four','Six']]
        tt['batsman'] = batsman
        return tt.fillna(0) 
    temp_runs['HS']       = player.groupby(['id','batsman']).agg({'batsman_runs':'sum'}).reset_index().groupby(['batsman']).agg({'batsman_runs':'max'})
    
    temp_runs_match       = player.groupby(['id','batsman']).agg({'batsman_runs':'sum'}).reset_index()
    temp_runs['Hundered'] = temp_runs_match[temp_runs_match['batsman_runs'] >= 100 ].groupby(['batsman']).agg({'batsman_runs':'count'})
    temp_runs['Fifty']    = temp_runs_match[ (temp_runs_match['batsman_runs'] < 100) & (temp_runs_match['batsman_runs'] >= 50) ].groupby(['batsman']).agg({'batsman_runs':'count'})
    temp_runs['Innings']  = temp_runs_match.groupby(['batsman']).agg({'id':'count'})
    
    temp_runs['No']       = ball[ball['player_dismissed'].isin(batsman)].groupby(['player_dismissed']).agg({'id':'count'}) if batsman else ball.groupby(['player_dismissed']).agg({'id':'count'})
         
    temp_runs['Not Out']  = temp_runs['Innings'] - temp_runs['No']
    temp_runs['Six']      = player[ (player['batsman_runs'] == 6) & (player['non_boundary'] == 0) ].groupby(['batsman']).agg({'batsman_runs':'count'})
    temp_runs['Four']     = player[ (player['batsman_runs'] == 4) & (player['non_boundary'] == 0) ].groupby(['batsman']).agg({'batsman_runs':'count'})
    temp_runs['Dots']     = player[player['batsman_runs'] == 0 ].groupby(['batsman']).agg({'batsman_runs':'count'})
    temp_runs['BF']       = player[~ player['extras_type'].isin(['wides'])].groupby(['batsman']).agg({'id':'count'})
    temp_runs['Avg']      = round(temp_runs['batsman_runs'] /(temp_runs['No'] ),2)
    temp_runs['SR']       = round((temp_runs['batsman_runs']/temp_runs['BF'])*100,2)
    temp_runs             = temp_runs.rename(columns = {'batsman_runs':'Runs'})

    temp_runs             = temp_runs.fillna(0) 
    temp_runs             = temp_runs.astype({'Six':int,'Four':int,'Hundered':int,'Fifty':int})
    temp_runs             = temp_runs[temp_runs['Innings'] >= innings] if innings else temp_runs    
    temp_runs             = temp_runs[temp_runs['Runs'] >= runs] if runs else temp_runs
    temp_runs             = temp_runs[choice] if choice else temp_runs[['Innings','Not Out','Runs','Dots','HS','Avg','BF','SR','Hundered','Fifty','Four','Six']]
    
    
    return temp_runs.sort_values(flag, ascending = asc ).head(limit).reset_index()
    



def get_player_data(player, ball,flag = 'bowler'):
    return ball[ball[flag].isin(player) ]

def get_team_data( team, ball, player_type = 'batsman'):
    flag = 'bowling_team' if player_type == 'batsman' else 'batting_team'
    return  ball[ball[flag].isin(team) ]



def seasonal_wickets(bowler,ball, match, game):
    player = ball[ball['bowler'] == bowler ]
    match  =   match[['id','date']]
    
    player = player[(player['is_wicket'] == 1) & (player['dismissal_kind'].isin(['caught','bowled','lbw','stumped','caught and bowled','hit wicket']))]
    final  = pd.merge(player,match , how = 'inner',left_on=['id'],right_on=['id'])
    
    final  = final[['id','date','batsman']]
    final['year'] = pd.to_datetime(final['date']).dt.strftime('%Y')
    result = final.groupby(['year']).agg({'batsman' : 'count'})

    result['Game'] = game
    
    result.reset_index(inplace=True)
    result = result.rename(columns = {'index':'Year'})
    
    return result.to_dict()




def one_vs_one(batsman,ball,match, game):
    player         = ball[ball['batsman'] == batsman ]
    match          = match[['id','date']]
    final          = pd.merge(player,match , how = 'inner',left_on=['id'],right_on=['id'])
    final          = final[['id','date','batsman_runs']]
    final['wicket']= np.where((player['is_wicket'] == 1) & (player['dismissal_kind'].isin(['caught','bowled','lbw','stumped','caught and bowled','hit wicket'])),1,0)

    final          = final[['id','date','batsman_runs','wicket']]
    final['year']  = pd.to_datetime(final['date']).dt.strftime('%Y')
    result         = final.groupby(['year','batsman_runs']).agg({'batsman_runs' : 'count','wicket':'sum'})
    wicket         = final.groupby(['year']).agg({'wicket':'sum'})
    result         = result.rename({'batsman_runs':'cnt'},axis='columns')

    result.reset_index(inplace=True)
    result = result.rename(columns = {'index':'Year'})

    wicket.reset_index(inplace=True)
    wicket = wicket.rename(columns = {'index':'Year'})
    
    result = result[['year','cnt','batsman_runs']]
    
    result = result.groupby(['year','batsman_runs']).mean().squeeze().unstack().add_suffix('')
    result = result.fillna(0)
    
    result['runs'] = 0
    result['balls'] = 0
    
    for i in ['0','1','2','3','4','5','6','7','8']:
        if i not in result.columns:
            result[i] = 0
        else:
            result['balls'] += result[i]
            result['runs'] += int(i)*result[i]
    
    result.reset_index(inplace=True)  
    result = result[['year','0','1','2','4','6','runs','balls']]
    
    result = result.rename(columns= {'0':'Dots'})
    result['Strike Rate'] = (result['runs'] / result['balls'])*100
            
    result['Game'] = game
    result = pd.merge(result,wicket,how='inner',left_on='year',right_on='year')
    
    return result, result['runs'].sum()




def decide_batsman( ball, match,team ,player = None, runs = None, opp = None, venue = None, thres = None):
     win_percent = 0
    if player:
        ball = ball[ball['batsman'] == player]    
    else:
         ball = ball[ball['batting_team'].isin(team) ]
        
    if opp != [None]:
        ball = ball[ball['bowling_team'].isin(opp) ]
        
    match_runs = ball.groupby(['id','batsman']).agg({'batsman_runs':'sum'})
    match_runs.reset_index(inplace = True)
    
    if venue:
        match = match[match['venue'] == venue]
        
    match = match[['id','winner']]
    
    final = pd.merge(match_runs, match, how= 'inner', left_on = 'id',right_on = 'id')
        
    final = final [final['batsman_runs'] >= runs]
        
    wins  = final[final['winner'].isin(team)] 
    if len(wins):
        win_percent = len(wins)/ len(final)
    
    final['result'] = np.where((final['winner'].isin(team) ),1,0)

    final = final.groupby(['batsman']).agg({'result':'sum','id':'count'})
    final['Win Percent'] = final['result'] / final['id']

    if thres:
        final = final[final['id'] >= thres]

    final = final.rename(columns = {'result':'Wins','id':'Total'})
    final = final.sort_values('Win Percent', ascending = False)

    return win_percent,final




def decide_bowler( ball, match,team ,player = None, wickets = 1, opp = None, venue = None, thres = None):
    
    win_percent = 0
    if player:
        ball = ball[ball['bowler'] == player]    
    else:
         ball = ball[ball['bowling_team'].isin(team) ]
        
    if opp != [None]:
        ball = ball[ball['batting_team'].isin(opp) ]
        
    
    ball['wicket']= np.where((ball['is_wicket'] == 1) & (ball['dismissal_kind'].isin(['caught','bowled','lbw','stumped','caught and bowled','hit wicket'])),1,0)
        
    match_runs = ball.groupby(['id','bowler']).agg({'wicket':'sum'})
    match_runs.reset_index(inplace = True)
    
    if venue:
        match = match[match['venue'] == venue]
        
    match = match[['id','winner']]
    
    final = pd.merge(match_runs, match, how= 'inner', left_on = 'id',right_on = 'id')
        
    final = final [final['wicket'] >= wickets ]
        
    wins  = final[final['winner'].isin(team)] 
    
    if len(wins):
        win_percent = len(wins)/ len(final)
    
    final['result'] = np.where((final['winner'].isin(team)),1,0)

    final = final.groupby(['bowler']).agg({'result':'sum','id':'count'})
    final['Win Percent'] = final['result'] / final['id']

    if thres:
        final = final[final['id'] >= thres]

    final = final.rename(columns = {'result':'Wins','id':'Total'})
    final = final.sort_values('Win Percent', ascending = False)

    return win_percent,final




def best_in_over(ball,decider_main, balls = 5 ):
    if decider_main in ['Runs','Wickets']:
        player_type = 'batsman' if decider_main == 'Runs' else 'bowler'
        decider = 'batsman_runs' if player_type == 'batsman' else 'is_wicket'

        if decider == 'is_wicket':
            ball = ball[(ball['is_wicket'] == 1) & (ball['dismissal_kind'].isin(['caught','bowled','lbw','stumped','caught and bowled','hit wicket']))]

        final  =  ball.groupby(['over',player_type]).agg({decider:'sum'}).reset_index()
        result = final.groupby(['over']).agg({decider:'max'}).reset_index()

        data = pd.merge(final, result, how = 'inner', left_on = ['over',decider],right_on = ['over',decider])
        
        if decider == 'is_wicket':
            data  = data.rename(columns = {'is_wicket':'Wickets'})
            data  = data.astype({'Wickets':'int'})
            
        else:
            data  = data.rename(columns = {'batsman_runs':'Runs'})
        
    elif decider_main in ['Six','Four'] :
        decider = 6 if decider_main == 'Six' else 4
        
        ball = ball.loc[ (ball['batsman_runs'] == decider ) & (ball['non_boundary'] == 0) ]
        
        final  =  ball.groupby(['over','batsman']).agg({'id':'count'}).reset_index()
        result = final.groupby(['over']).agg({'id':'max'}).reset_index()

        data = pd.merge(final, result, how = 'inner', left_on = ['over','id'],right_on = ['over','id'])
        data = data.rename(columns = {'id':decider_main})
        
    elif decider_main in ['SR'] :
        
        flag1  =  ball.groupby(['over','batsman']).agg({'batsman_runs':'sum'}).reset_index()
        flag2  =  ball[~ ball['extras_type'].isin(['wides'])].groupby(['batsman','over']).agg({'id':'count'})
        final  =  pd.merge(flag1, flag2, how = 'inner', left_on = ['over','batsman'], right_on = ['over','batsman'] )
        
        final['SR'] = round((final['batsman_runs'] / final['id']) * 100,2)
        
        final = final[final['id'] >= balls ]
        
        result = final.groupby(['over']).agg({'SR':'max'}).reset_index()
        data = pd.merge(final, result, how = 'inner', left_on = ['over','SR'],right_on = ['over','SR'])
        data = data.rename(columns = {'batsman_runs':'Runs', 'id': 'BF' })
    data = data.set_index('over')
    return data