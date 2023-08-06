#import libraries
import requests
import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

#read basic data
try:
    data = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
except:
    raise ConnectionError('Unable to reach FPL')
data = json.loads(data.content)

#Dictionarys for conversion
code2pos={}
for item in data['element_types']:
    code2pos.update({item['id']:item['singular_name_short']})

code2team={}
team2code={}
temp2team={}
for item in data['teams']:
    code2team.update({item['code']:item['short_name']})
    team2code.update({item['short_name']:item['code']})
    temp2team.update({item['id']:item['short_name']})

#list of teams
teams_list=list(team2code.keys())


#Function to return list of valid team names
def team():
    """
    This function will return all valid team names
    """
    return(teams_list)

#Function to return the list of valid positions
def pos():
    """
    This function will retun all valid positions
    """
    return list(code2pos.values())

#Read final stats
df=pd.json_normalize(data['elements'])

#Preprocess
df.team=df.team_code.apply(lambda x: code2team[x])
df.element_type=df.element_type.apply(lambda x:code2pos[x])
df['full_name']=''
for i in range(df.shape[0]):
    if df.first_name[i] in df.web_name[i]:
        df.full_name[i]=df.web_name[i]
    else:
        df.full_name[i]=df.first_name[i]+' '+df.web_name[i]
df.rename(columns={'full_name':'name'}, inplace=True)
df.rename(columns={'element_type':'pos'}, inplace=True)

#Select and order required colums
fin_cols=['code', 'id','name','team', 'pos', 'total_points','cost_change_start','dreamteam_count', 'form', 'in_dreamteam','now_cost', 'points_per_game', 'selected_by_percent', 'transfers_in', 'transfers_out', 'value_form', 'value_season', 'minutes', 'goals_scored','assists', 'clean_sheets', 'goals_conceded', 'own_goals','penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards','saves', 'bonus', 'bps', 'influence', 'creativity', 'threat', 'ict_index', 'influence_rank',  'creativity_rank', 'threat_rank','ict_index_rank', 'corners_and_indirect_freekicks_order', 'direct_freekicks_order', 'penalties_order']
df=df[fin_cols]

#Dictionaries to convert element data
element2name={e:n for e,n in zip(df.id, df.name)}
element2team={e:t for e,t in zip(df.id, df.team)}
element2pos={e:p for e,p in zip(df.id, df.pos)}

#Function to validate team entry
def validate_team(teams):
    if (len(teams)==0):
        return code2team.values()
    i_list=[]
    #print('Inside val_teams')
    #print(teams, type(teams), len(teams))
    for i in teams:
        #print(i)
        i=str(i).upper()
        if i=='ALL':
            return code2team.values()
        if i in code2team.values():
            i_list.append(i)
        else:
            raise KeyError(f'{i} :Team name not available')
    return i_list

#Function to validate position entry
def validate_poss(pos):
    if (len(pos)==0):
        return code2pos.values()
    i_list=[]
    #print('inside val_pos')
    #print(pos, type(pos), len(pos))
    for i in pos:
        #print(i)
        i=str(i).upper()
        if i=='ALL':
            return code2pos.values()
        if i in code2pos.values():
            i_list.append(i)
        else:
            raise KeyError(f'{i} :Position not available')
    return i_list

#basic info for player list
basic_cols=['id','name','team','pos']    

#Function returns player info
def players_list(team='all', pos='all'):
    """
    Parameters:
    team : list of team names 
    eg: ['ARS', 'MUN']
    use team() to get all valid inputs
    
    pos  : list of positions 
    eg: ['GKP', 'MID']
    use pos() to get all valid positions
    
    Example:
    Get all defenders of Manchester City and Liverpool
    team=['LIV','MCI']
    pos=['DEF']
    player_list(team=team, pos=pos)
    """
    if type(team)==str:
        team=team.upper()
        
    if type(pos)==str:
        pos=pos.upper()
        
    if team=='ALL':
        teams=code2team.values()
    else:
        team=list(team)
        teams= validate_team(team)
        
    if pos=='ALL':
        poss=code2pos.values()
    else:
        poss=validate_poss(pos)
    return df[df.team.isin(teams)==True][df.pos.isin(poss)==True][basic_cols].reset_index(drop=True)

#Function returns GW data
def player_gw_stats(player_id):
    """
    Parameters:
    player_id  : int
    Use player_list() to get player id
    
    Returns
    DataFrame containing player stats for every gameweek
    
    Example: 
    player_gw_stats(player_id=302)
    Returns gameweek wise statistics of Bruno Fernandez
    """
    try:
        url=f'https://fantasy.premierleague.com/api/element-summary/{player_id}/'
        try:
            pl_stats = requests.get(url, timeout=2)
        except:
            raise ConnectionError('Unable to reach FPL')
        pl_stats = json.loads(pl_stats.content)
        df=pd.json_normalize(pl_stats['history'])
        cols=list(df.columns)
        df['name']=df.element.apply(lambda x:element2name[x])
        df['team']=df.element.apply(lambda x:element2team[x])
        new_cols=['name','team']
        new_cols.extend(cols)
        df=df[new_cols]
        #df=df.drop(['element'], axis=1)
        df.opponent_team=df.opponent_team.apply(lambda x:temp2team[x])
        return df
    except ValueError:
        raise ValueError("Player Id not Found")

#Function to validate player id
def validate_pid(pid):
    i_list=[]
    for i in pid:
        if i in np.arange(1,714):
            i_list.append(i)
        else:
            pass
    if len(i_list)==0:
        raise ValueError('ID not Found')
    return list(set(i_list))

#Function to get player summary
def player_summary(player_id=[], team=[], pos=[], full=False):
    """
    Parameters:
    player_id: list of integer values 
    Use player_list() to get player id
    
    team: List of team names
    eg: ['ARS', 'MUN']
    use team() to get all valid inputs
    
    pos : List of Positions
    eg: ['GKP', 'MID']
    use pos() to get all valid positions
    
    full : type Boolean
    if True return stats of all players
    default False
    """
    if full==True:
        return df.drop('code', axis=1)
    if len(player_id)>0:
        player_id=validate_pid(player_id)
        return df[df.id.isin(player_id)==True]
    elif(len(team)+len(pos)==0):
        raise ValueError('No parameters found')
    else:
        team=validate_team(team)
        pos=validate_poss(pos)
        return df[df.team.isin(team)==True][df.pos.isin(pos)==True].drop('code', axis=1)


