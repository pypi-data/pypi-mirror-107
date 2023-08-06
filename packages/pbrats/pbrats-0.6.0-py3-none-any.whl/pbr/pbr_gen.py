#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
#  pip install pandas openpyxl
import pandas as pd
import numpy as np
import re
import sys

# https://stackoverflow.com/questions/25127673/how-to-print-utf-8-to-console-with-python-3-4-windows-8
sys.stdout.reconfigure(encoding='utf-8')

# https://pbpython.com/pandas-excel-range.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
"""
excel: E:H and J:M

参赛队伍1	中山大学队		
领队	林航宇	新睿ID	lhylllll
	姓名	新睿ID	新睿大师分
老师/嘉宾	/	沈刚	/
队员2	邵千芊	SqQ	771,53
队员3	马炜俊	超级肥马	153,2
队员4	林航宇	lhylllll	131,54
队员5	吴傲	wuao	23,12
队员6	郑永杰	桥牌哥王	9,85
"""
MAX_MEMBERS=6
MAX_ROUNDS=8

def get_number(str):
    return int(re.findall("\d+", str)[0])

def is_valid(team):
    members = team["members"]
    for member in members:
        # print(member)
        if str(member[0]) == "nan":
            return False
    return True

def parse_teams(df):
    members = [None] * MAX_MEMBERS
    teams=[]
    for index, row in df.iterrows():
        firstcol = row.array[0]
        if str(firstcol)=='nan': # == np.nan:
            pass
        elif "参赛队伍" in firstcol:
            team = {}
            team["index"] = get_number(firstcol)
            team["name"] = row.array[1]
            members = [None] * MAX_MEMBERS
        elif "领队" in firstcol:
            team["leader"] = (row.array[3], row.array[1], None)
        elif "老师" in firstcol:
            members = [None] * MAX_MEMBERS
            members[0] = (row.array[2], row.array[1], row.array[3])
        elif "队员" in firstcol:
            no = get_number(firstcol)
            if no in range(2,MAX_MEMBERS+1):
                members[no-1] = (row.array[2],row.array[1], row.array[3])
            if no == MAX_MEMBERS:
                team["members"] = members
                if is_valid(team):
                    print("====== %2d team: %s / leader: %s" %(team["index"],team["name"],team["leader"][0]))
                    teams.append(team)
    return teams

def get_teams(excel, all_cols=['E:H','J:M']):
    teams = []
    for cols in all_cols:
        df = pd.read_excel(excel, header=0,usecols=cols)
        teams.extend(parse_teams(df))
    return teams

def generate_excel(teams):
    print(teams)
    #for i in range(MAX_MEMBERS):
    groups = [[]*MAX_ROUNDS]*MAX_MEMBERS
    print(groups)
    team_names = []
    for team in teams:
        print(team)
        for i in range(MAX_MEMBERS):
            #print(team["members"][i][0])
            # use copy !!
            group = groups[i].copy()
            group.append(team["members"][i][0])
            groups[i] = group
            #print(groups)
        team_names.append(team["name"])
    for idx, group in enumerate(groups):
        print("group: ", idx+1, group)
        df = pd.DataFrame([[''] * MAX_ROUNDS ] * len(teams),
                    index=[team_names,group],
                    columns=list(range(1, MAX_ROUNDS+1)))
        print(idx, type(idx))
        excel = "202106-record-group%d.xlsx" % (idx+1)
        df.to_excel( excel, sheet_name='0601',  index_label=["team","id"])

def generate(excel):
    print("parsing ...", excel)
    teams = get_teams(excel)
    # print(teams)
    generate_excel(teams)

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('excel', help='excel file contains team information, see sample')
    args = parser.parse_args()
    generate(args.excel)

if __name__ == '__main__':
    main()