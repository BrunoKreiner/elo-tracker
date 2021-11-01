#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 23:39:35 2021

@author: andrewkrier
"""

import numpy as np
import math as m
import time as t
import random as r
import matplotlib.pyplot as plt

# TODO: Convert these dictionaries and lists to SQL queries

playerToELO = {}
games = []
end_elos = []


d = 15


'''

Things to further implement
Mitigate the effect of new players on existing ELOs (log graph-ish?)

'''

def reportELO():
    for p in playerToELO:
        print("Player {:} has an ELO of {:}".format(p, playerToELO[p]))
    print("In a league of {:} players there is a total of {:} ELO".format(len(playerToELO), sum(list(playerToELO.values()))))
        
def report_game_log():
    for g in games:
        print("In game played on {:}".format(t.strftime('%Y-%m-%d %H:%M:%S', t.localtime(g[8]))))
        print("Player {:} scored {:} points, and ELO went from {:} to {:}".format(g[0], g[1], g[2], g[2] + g[3]))
        print("Player {:} scored {:} points, and ELO went from {:} to {:}".format(g[4], g[5], g[6], g[6] + g[7]))
        print("Total ELO diff in this game is {:}".format(g[3] + g[7]))

def amount_won(winner_ELO, loser_ELO):
    return win_multiplier(winner_ELO) * base_amount_changed(winner_ELO, loser_ELO)
    
def amount_lost(winner_ELO, loser_ELO):
    return loss_multiplier(loser_ELO) * base_amount_changed(winner_ELO, loser_ELO)
    
def base_amount_changed(winner_ELO, loser_ELO):
    diff = winner_ELO - loser_ELO
    c = 6
    #return (200 * (2 * ((1 + np.exp(c)) / (np.exp(c) - 1)) * ((1 / (1 + np.exp(c * diff / 2000))) - 0.5) + 1))
    return 200 + (200/c) * np.log((1 / (diff * (np.exp(c) - 1) / (4000 * (1 + np.exp(c))) + 0.5)) - 1)
    
def win_multiplier(winner_ELO):
    return np.log(1 / (((np.exp(d) - 1) / (2 * (1 + np.exp(d)))) * (winner_ELO / 1000 - 1) + 0.5) - 1) / d + 1
    
    
def loss_multiplier(loser_ELO):
    #return 2 * ((1 + np.exp(d)) / (np.exp(d) - 1)) * ((1 / (1 + np.exp(-d * (loser_ELO - 1000) / 1000))) - 0.5) + 1
    return -1 * np.log(1 / (((np.exp(d) - 1) / (2 * (1 + np.exp(d)))) * (loser_ELO / 1000 - 1) + 0.5) - 1) / d + 1
    
def calculate_diff(p1_id, p1_score, p2_id, p2_score):
    if p1_score == p2_score:
        return 0,0
    did_p1_win = p1_score > p2_score
    
    p1_diff = amount_won(playerToELO[p1_id], playerToELO[p2_id]) if did_p1_win else -1 * amount_lost(playerToELO[p2_id], playerToELO[p1_id])
    p2_diff = amount_won(playerToELO[p2_id], playerToELO[p1_id]) if not did_p1_win else -1 * amount_lost(playerToELO[p1_id], playerToELO[p2_id])
    
    p1_diff = round(p1_diff * recent_consecutive_outcome_multiplier(p1_id, p1_score, p2_id, p2_score))
    p2_diff = round(p2_diff * recent_consecutive_outcome_multiplier(p1_id, p1_score, p2_id, p2_score))
    
    return (p1_diff, p2_diff)

def game(p1_id, p1_score, p2_id, p2_score):
    if p1_id not in playerToELO:
        playerToELO[p1_id] = 1000

    if p2_id not in playerToELO:
        playerToELO[p2_id] = 1000

    p1_diff, p2_diff = calculate_diff(p1_id, p1_score, p2_id, p2_score)
    
    report_game(p1_id, p1_score, p1_diff, p2_id, p2_score, p2_diff)
        
    playerToELO[p1_id] += p1_diff
    playerToELO[p2_id] += p2_diff
    
    keep_in_bounds(p1_id)
    keep_in_bounds(p2_id)
    
def keep_in_bounds(p_id):
    playerToELO[p_id] = max(0, playerToELO[p_id])
    playerToELO[p_id] = min(2000, playerToELO[p_id])
        
    
def report_game(p1_id, p1_score, p1_diff, p2_id, p2_score, p2_diff):
    games.append([p1_id, p1_score, playerToELO[p1_id], p1_diff, p2_id, p2_score, playerToELO[p2_id], p2_diff, t.time()])
    
def game_sort(g):
    return -1 * g[-1]
    
def get_last_games(p_id, n):
    games.sort(key=game_sort)
    ret = []
    for g in games:
        if g[0] == p_id or g[4] == p_id:
            ret += [g]
            if len(ret) >= n:
                break
    return ret

def did_win(p_id, g):
    return (p_id == g[0] and g[1] > g[5]) or (p_id == g[4] and g[1] < g[5])

def num_consecutive_times_a_beat_b_in_last_n_games(a_id, b_id, n):
    count = 0
    for g in get_last_games(a_id, n):
        if did_win(a_id, g) and (b_id == g[0] or b_id == g[4]):
            count += 1
        else:
            return count
    return count
        
def recent_consecutive_outcome_multiplier(p1_id, p1_score, p2_id, p2_score):
    n = 10
    did_p1_win = p1_score > p2_score
    p1 = num_consecutive_times_a_beat_b_in_last_n_games(p1_id, p2_id, n)
    p2 = num_consecutive_times_a_beat_b_in_last_n_games(p2_id, p1_id, n)
    if p1 != 0 and p2 != 0:
        print("ERROR: Impossible scenario reached")
        #quit()
    if (did_p1_win and p1 != 0) or (not did_p1_win and p2 != 0):
        # print("returning {:}".format(1.0 * max(int(p1), int(p2)) / n))
        return 1 - 1.0 * max(int(p1), int(p2)) / n
    return 1
    
    
    
if __name__ == "__main__":
    for j in range(100):
        playerToELO = {}
        for i in range(100):
            #game(1, 10, 2, 8)
            p1 = r.randint(1, 10)
            p2 = r.randint(1, 10)
            p1_score = r.randint(0, 10)
            p2_score = r.randint(0, 10)
            while(p1 == p2):
                p2 = r.randint(1, 10)
            #print("Playing a game between {:} and {:} with scores {:} and {:}".format(p1, p2, p1_score, p2_score))
            #if p1 in playerToELO and p2 in playerToELO:
            #    print("Player {:} has an ELO of {:}, Player {:} has an ELO of {:}".format(p1, playerToELO[p1], p2, playerToELO[p2]))
            game(p1, p1_score, p2, p2_score)
            
        for k in playerToELO.keys():
            end_elos += [playerToELO[k]]
        
    # Histogram functions are from the internet
    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})
    plt.hist(end_elos, bins=50)
    plt.gca().set(title='Frequency Histogram', ylabel='Frequency');
    #    prev_p1_elo = 0
    #    while(abs(prev_p1_elo - playerToELO[1]) > 0.1):
    #        prev_p1_elo = playerToELO[1]
    #        playerToELO[2] = 2000
    #        game(1, 10, 2, 8)
    #game(1, 8, 2, 10)
    #report_game_log()
    #reportELO()