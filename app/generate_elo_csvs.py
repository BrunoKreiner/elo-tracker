# The goal of this file is to make an externally runnable command
# that will take Matches.csv, and generate the appropriate 
# ELOHistory.csv and ParticipatesIn.csv files.

# Matches is of the form
# activity,matchID,user1_ID,user2_ID,user1_score,user2_score,date_time,accepted

# ELOHistory is of the form
# id,user_id,activity,elo,matchID

# ParticipatesIn is of the form
# user_ID,activity,elo

##################################################################################################
##################################################################################################
##################################################################################################
#################################### RUN THIS IN THE TERMINAL ####################################
#################### EXECUTE python3 generate_elo_csvs.py in /elo-tracker/app ####################
##################################################################################################
##################################################################################################
##################################################################################################

import numpy as np
import math as m
import time as t
import random as r
import pandas as pd
import os

d = 15

'''

Things to further implement
Mitigate the effect of new players on existing ELOs (log graph-ish?)

'''

participates_in = {}    # user_id -> activity -> elo
elo_history = {}        # user_id -> activity -> elo, matchID
game_time = {}          # match_id -> date_time
matches = []            # activity,matchID,user1_ID,user2_ID,user1_score,user2_score,date_time,accepted

def get_current(id, activity):
    if id in participates_in.keys():
        if activity in participates_in[id].keys():
            return participates_in[id][activity]
        else:
            participates_in[id][activity] = 1000
            return participates_in[id][activity]
    else:
        participates_in[id] = {}
        participates_in[id][activity] = 1000
        return participates_in[id][activity]

def amount_won(winner_ELO, loser_ELO):
    return win_multiplier(winner_ELO) * base_amount_changed(winner_ELO, loser_ELO)
    
def amount_lost(winner_ELO, loser_ELO):
    return loss_multiplier(loser_ELO) * base_amount_changed(winner_ELO, loser_ELO)
    
def base_amount_changed(winner_ELO, loser_ELO):
    diff = winner_ELO - loser_ELO
    c = 6
    return 200 + (200/c) * np.log((1 / (diff * (np.exp(c) - 1) / (4000 * (1 + np.exp(c))) + 0.5)) - 1)
    
def win_multiplier(winner_ELO):
    return np.log(1 / (((np.exp(d) - 1) / (2 * (1 + np.exp(d)))) * (winner_ELO / 1000 - 1) + 0.5) - 1) / d + 1
    
    
def loss_multiplier(loser_ELO):
    return -1 * np.log(1 / (((np.exp(d) - 1) / (2 * (1 + np.exp(d)))) * (loser_ELO / 1000 - 1) + 0.5) - 1) / d + 1
    
def calculate_diff(activity, p1_id, p1_score, p2_id, p2_score):
    p1_score = int(p1_score)
    p2_score = int(p2_score)
    if p1_score == p2_score:
        return 0,0
    did_p1_win = p1_score > p2_score
    
    p1_diff = amount_won(get_current(p1_id, activity), get_current(p2_id, activity)) if did_p1_win else -1 * amount_lost(get_current(p2_id, activity), get_current(p1_id, activity))
    p2_diff = amount_won(get_current(p2_id, activity), get_current(p1_id, activity)) if not did_p1_win else -1 * amount_lost(get_current(p1_id, activity), get_current(p2_id, activity))
    
    p1_diff = round(p1_diff)
    p2_diff = round(p2_diff)
    
    return (p1_diff, p2_diff)

def game(activity, p1_id, p1_score, p2_id, p2_score):
    p1_elo = get_current(p1_id, activity)
    p2_elo = get_current(p2_id, activity)

    p1_diff, p2_diff = calculate_diff(activity, p1_id, p1_score, p2_id, p2_score)
    
    # report_game(p1_id, p1_score, p1_diff, p2_id, p2_score, p2_diff)
        
    p1_elo += p1_diff
    p2_elo += p2_diff
    
    p1_elo = keep_in_bounds(p1_elo)
    p2_elo = keep_in_bounds(p2_elo)
    participates_in[p1_id][activity] = p1_elo
    participates_in[p2_id][activity] = p2_elo
    return (p1_elo, p2_elo)
    
def keep_in_bounds(elo):
    elo = max(0, elo)
    elo = min(2000, elo)
    return elo

if __name__ == "__main__":
    # Activity, match_ID, user1_id, user2_id, user1_score, user2_score, date_time, approved
    df = pd.read_csv('../db/data/Matches.csv', header = None)

    for ind in df.index:
        # print("Playing game of {:} between {:} and {:} with a score of {:}:{:}".format(df.iloc[ind, 0], df.iloc[ind, 2], df.iloc[ind, 3], df.iloc[ind, 4], df.iloc[ind, 5]))
        if np.isnan(df.iloc[ind, 4]) or np.isnan(df.iloc[ind, 4]):
            # print("Skipping game {:}".format(df.iloc[ind, 1]))
            continue
        p1_elo, p2_elo = game(df.iloc[ind, 0], df.iloc[ind, 2], df.iloc[ind, 4], df.iloc[ind, 3], df.iloc[ind, 5])
        # print("Player {:} now has an ELO of {:} | Player {:} now has an ELO of {:}".format(df.iloc[ind, 2], p1_elo, df.iloc[ind, 3], p2_elo))
        if df.iloc[ind, 2] not in elo_history:
            elo_history[df.iloc[ind, 2]] = {}
        if df.iloc[ind, 0] not in elo_history[df.iloc[ind, 2]]:
            elo_history[df.iloc[ind, 2]][df.iloc[ind, 0]] = []
        elo_history[df.iloc[ind, 2]][df.iloc[ind, 0]] += [[p1_elo, df.iloc[ind, 1]]]
        # print("Player {:} achieved an ELO of {:} in {:} in match {:}".format(df.iloc[ind, 2], p1_elo, df.iloc[ind, 0], df.iloc[ind, 1]))
        if df.iloc[ind, 3] not in elo_history:
            elo_history[df.iloc[ind, 3]] = {}
        if df.iloc[ind, 0] not in elo_history[df.iloc[ind, 3]]:
            elo_history[df.iloc[ind, 3]][df.iloc[ind, 0]] = []
        elo_history[df.iloc[ind, 3]][df.iloc[ind, 0]] += [[p2_elo, df.iloc[ind, 1]]]
        # print("Player {:} achieved an ELO of {:} in {:} in match {:}".format(df.iloc[ind, 3], p2_elo, df.iloc[ind, 0], df.iloc[ind, 1]))
    elo_data = []
    count = 0
    for u in elo_history:
        for a in elo_history[u]:
            for m in elo_history[u][a]:
                elo_data += [[count, u, a, m[0], m[1]]]
                count += 1

    prt_data = []
    for u in participates_in:
        for a in participates_in[u]:
            prt_data += [[u, a, participates_in[u][a]]]

    df_elo = pd.DataFrame(elo_data, columns = ['id', 'user_id', 'activity', 'elo', 'match_id'])
    df_prt = pd.DataFrame(prt_data, columns = ['user_id', 'activity', 'elo'])

    df_elo.to_csv("ELOHistory_gen.csv", index = False, header = None)
    df_prt.to_csv("ParticipatesIn_gen.csv", index = False, header = None)