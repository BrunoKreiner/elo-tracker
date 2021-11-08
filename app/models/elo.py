#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 23:39:35 2021

@author: andrewkrier
"""
from flask import current_app as app



#import elo_calc as ec

class elo_ref:
    def get_current(activity, id):
        current = app.db.execute('''
        SELECT elo
        FROM ELOHistory
        WHERE :id = user_ID AND matchID in (
            SELECT matchID, 
            FROM Matches
            WHERE date_time in (
                SELECT MAX(date_time)
                FROM Matches
                WHERE (:id = user1_ID OR :id = user2_ID) AND :activity = activity
            )
        )
                                    ''', id = id, activity = activity)
        return current

    def get_old(id, g_id):
        current = app.db.execute('''
        SELECT elo
        FROM ELOHistory
        WHERE matchID = :g_id AND user_ID = :id
                                    ''', id = id, g_id = g_id)
        return current

    def get_average(id):
        # Implementation tbd
        app.jinja_env.globals.update(globalAverageElo=1200)
        return 1200

    def get_all_current(id):
        return 0

    def get_max(id):
        return 2000

    def get_min(id):
        return 0

    def play_game(activity, p1_id, p2_id, p1_score, p2_score):
        # Returns (p1_elo, p2_elo) from after the game is played
        return ec.game(activity, p1_id, p1_score, p2_id, p2_score)

    def get_last_games(activity, id, n):
        games = app.db.execute('''
        SELECT user1_ID, user2_ID, user1_score, user2_score, date_time
        FROM Matches
        WHERE :activity = activity AND (:id = user1_ID OR :id = user2_ID)
        ORDER BY date_time DESC
                                    ''', id = id, activity = activity)
        return games[:n]

    def get_history(activity, id):
        history = app.db.execute('''
        SELECT 
        FROM ELOHistory LEFT OUTER JOIN Matches ON ELOHistory.matchID = Matches.matchID
        WHERE :id = ELOHistory.user_ID AND :activity = ELOHistory.activity
                                    ''', id = id, activity = activity)
        return history

    # Make a function that returns all the current ELOs for the activity the user plays
    # Function that averages these, and maxes them