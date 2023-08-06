#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    print(upper, contract, result)
    if sign == "=":
        tricks = int(contract[0]) + 6 
    elif sign == "-":
        tricks = int(contract[0]) + 6 - int(result)
    else: # +
        tricks = int(contract[0]) + 6 + int(result)
    return declarer, contract, sign + result, tricks

"""
team	id	1	2	3	4	5	6	7	8
中山大学队	沈刚								
成中医一队	aces								
成中医二队	老爷								
龙岩学院一队	网桥								
龙岩学院二队	门道								
西交一队	nyt								
地鼠队	gopher	N2S+1	S2D=	W3NT=	E1NT=	E4D+1	S1NT-2	S2NT=	S4S-1
"""
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
    print(df)
    print("=== All boards: \n", df.head(len(players)))
    urls = [""] * TOTAL_BOARDS
    for index, row in df.iterrows():
        print(index, row)
        if row["id"] == "url":
            urls = row.tolist()[2:TOTAL_BOARDS+2]
            # print("url: ", urls)
        all_players[row["id"]] =  row.tolist()[2:TOTAL_BOARDS+2]

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
