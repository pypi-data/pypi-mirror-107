#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
#  pip install pandas openpyxl
import pandas as pd
import re

TOTAL_BOARDS=8 # later can be 12
BOARD_ABORT="ABORT"
SCORE_ABORT=-50000

def split_contract(contract):
    """
    split the handwriting quick notes into complete info
      S5Cxx+2 => 5CXX, S, +2, 13
      1. remove space
      2. change to uppercase
      3. auto append = if no +-=
      4  return tricks as well for each score later
    """
    upper=contract.upper().replace(" ", "")
    if len(upper) == 0: # abort
        contract = BOARD_ABORT
        return "",contract,"",0
    # check whether there is +-= result
    if not re.search(re.compile(r'\+|=|-'), upper):
        upper=upper+"="
    declarer = upper[0]

    # parse to get segments
    contract, sign, result = re.split("(\+|-|=)", upper[1:])
    if sign == "=":
        tricks = int(contract[0]) + 6 
    elif sign == "-":
        tricks = int(contract[0]) + 6 - int(result)
    else: # +
        tricks = int(contract[0]) + 6 + int(result)
    return declarer, contract, sign + result, tricks

def read_excel(xls_file):
    # read raw data from xls, see sample record.xlsx

    # https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html
    pd.set_option("display.unicode.east_asian_width", True)

    # check sheet first
    xl = pd.ExcelFile(xls_file)
    print("all sheets: ", xl.sheet_names)
    teams = []
    players = []
    currentdate = xl.sheet_names[0]
    if "team" not in xl.sheet_names:
        print("`team` sheet is needed inside excel")
    else:
        df = xl.parse("team")
        print("=== Read teams from team sheet:")
        for index, row in df.iterrows():
            teams.append([row["host"],row["guest"]])
    for team in teams:
        a,b = team
        print("> %s : %s" % (a,b))
        if a not in players:
            players.append(a)
        if b not in players:
            players.append(b)
    print("players:", players)
    
    # read current sheet for record
    df = pd.read_excel (xls_file).dropna(how="all").fillna("")
    all_players = {}
    print("=== All boards: \n", df.head(len(players)))
    for index, row in df.iterrows():
        if row["id"] == "url":
            urls = row.tolist()[1:TOTAL_BOARDS+1]
            #print("url: ", urls)
        all_players[row["id"]] =  row.tolist()[1:TOTAL_BOARDS+1]

    boards = []
    for i in range(TOTAL_BOARDS):
        all_results = []
        for player in players:
            declarer, contract, result, tricks = split_contract(all_players[player][i])
            record = {
                "id": player, 
                "declarer": declarer, 
                "contract": contract, 
                "result" : result, 
                "tricks": tricks
            }
            all_results.append(record)
        board = {
            "all": all_results,
            "url": urls[i]
        }
        boards.append(board)
    return teams, players, boards, currentdate
