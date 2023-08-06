#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 18:08:49 2021

@author: nattawoot
"""
import pandas as pd
import os
import copy
from collections import namedtuple
from dataclasses import dataclass
from typing import List

from datetime import datetime
from loguru import logger

from wud.aws import s3bucket_json_get


def convar_dict():
    convar_dict = s3bucket_json_get('wud-cloudhouse','maruball_convar.json')
    return convar_dict


@dataclass
class Match:
    kot: datetime = ''
    team_home: str = ''
    team_away: str = ''
    link: str = ''
    league: str = ''


@dataclass
class MatchBet(Match):
    hdc: float = ''
    hdc_side: str = ''
    odd_home: float = ''
    odd_away: float = ''
    source: str = ''
    
@dataclass    
class PrevMatch(Match):
    score_home: str = ''
    score_away: str = ''
    
@dataclass    
class MatchPreview(Match):
    prev_meets: List[PrevMatch] = None
    latest_matches_home: List[PrevMatch] = None
    latest_matches_away: List[PrevMatch] = None
    
    
@dataclass
class Player:
    name: str = ''
    team: str = ''
    goal: int = None
    assist : int = None


def team_name_revise0(team, source_input, source_output):
    
    epl = copy.deepcopy(convar_dict['team_name']['epl'])
    ucl_erp = copy.deepcopy(convar_dict['team_name']['ucl_erp'])
    tpl = copy.deepcopy(convar_dict['team_name']['tpl'])
    etc = copy.deepcopy(convar_dict['team_name']['etc'])

    Team = namedtuple("Team", ['footballapi', 'livescore', 'short', 'league'])   

    
    
    team_set = []
    for t in epl:
        t.append('epl')
        team_set.append(Team(*t))
    for t in ucl_erp:
        t.append('ucl_erp')
        team_set.append(Team(*t))
        
    for t in tpl:
        t.append('tpl')
        team_set.append(Team(*t))
        
    for t in etc:
        t.append('etc')
        team_set.append(Team(*t))
        
        
    result = team
    
    for i in team_set:
        if getattr(i, source_input) == team:
            result = getattr(i, source_output)
            break
        
    return result

def team_name_revise(team, source_input, source_output):
    
    this_folder = os.path.dirname(os.path.abspath(__file__))

    df = pd.read_csv(os.path.join(this_folder,'football_team_name.csv'))
    try:
        row = df.loc[df[source_input] == team]
        result = row.iloc[0][source_output]
    except (IndexError, KeyError):
        logger.warning(f'wud.football.team_name_revise - no register for {team}')
        result = team
        
        if(source_output=='abbv'):
            result = result[:3]

        
    if(pd.isnull(result))   :
        logger.warning(f'wud.football.team_name_revise - blank cell in csv for {team}')
        
        result = team
        if(source_output=='abbv'):
            result = result[:3]
            
    return result       
