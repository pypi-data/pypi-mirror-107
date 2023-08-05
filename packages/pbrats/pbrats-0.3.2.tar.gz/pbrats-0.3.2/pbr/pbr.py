#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
import sys
import pkgutil
import pkg_resources  # part of setuptools
version = pkg_resources.require("pbrats")[0].version

import repackage
repackage.up()

from string import Template

from pbr.bridge_score import Contract, matchpoints, imps, vul_table, board_vul, vp_scale_8boards, vul_maptable
from pbr.pbr_template import *
from pbr.pbr_excel import *

def get_dealside(board_no):
    # return EW/NS for scoring
    if (board_no%2) == 0:
        dealside="NS"
    else:
        dealside="EW"
    return dealside

# fill one id for each board
def process_onedeal(deal,vuls, dealside):
    html, score = process_oneid(deal,vuls, dealside)
    return html

# fill one id for each board
def process_oneid(board,vuls, dealside):
    src = Template(id_template)
    contract = board["contract"]
    declarer = board["declarer"]
    if declarer in vul_maptable[vuls]:
        vul=True
    else:
        vul=False
    if contract == BOARD_ABORT:
        score=SCORE_ABORT
    else:
        score = Contract.from_str(contract, vul).score(board["tricks"])
    if declarer in "EW":
        score = -score
    # need vul 
    # print(score)
    if score > 0:
        scorecolor="red"
    else:
        scorecolor="green"
    if score==abs(SCORE_ABORT):
        show_score = ""
    else:
        show_score = score
    all = { "contract": html_suit(contract), "result": board["result"],
            "declarer" : board["declarer"], "score": show_score, "scorecolor": scorecolor}
    return src.safe_substitute(all), score

def get_teammatch_onerow(idx, board, team):
    # for one row for each board with host/guest id
    src = Template(onerow_template)
    host_id, guest_id = team
    # TODO
    host = [d for d in board if d['id'] == host_id][0]
    guest = [d for d in board if d['id'] == guest_id][0]
    # need IMP, VP
    vul = vul_table[board_vul[idx]]
    dealside = get_dealside(idx)
    host_html, host_score = process_oneid(host, board_vul[idx], dealside)
    guest_html, guest_score = process_oneid(guest, board_vul[idx], dealside)
    score_diff = host_score - guest_score
    imp = imps(host_score,guest_score)

    host_imp=guest_imp=""
    if abs(score_diff) > abs(SCORE_ABORT) - 10000: # abort
        score_diff = ""
        if guest_score == SCORE_ABORT:
            host_imp, guest_imp = (3,-3)
        else:
            host_imp, guest_imp = (-3,3)
    else:
        if imp > 0:
            host_imp=str(imp)
        elif imp <0:
            guest_imp=str(-imp)
    all = { "boardno": idx+1, "vul": vul, "host": host_html, "guest" : guest_html, "diff" : score_diff, "hostimp": host_imp, "guestimp": guest_imp }
    return src.safe_substitute(all), host_imp, guest_imp

def get_board_onerow(idx, deal):
    # for one row for each board with host/guest id
    src = Template(oneboardrow_template)
    #print(deal)
    # need IMP, VP
    dealside = get_dealside(idx)
    vul = board_vul[idx]
    host_html = process_onedeal(deal, vul, dealside)
    all = { "boardno": idx+1, "vul": vul, "host": host_html, "id": deal["id"] }
    return src.safe_substitute(all)

def get_match(boards, teamno, team):
    """
    calculate one match
    """
    rows = ""
    total_hostimp = 0
    total_guestimp = 0
    for idx, board in enumerate(boards):
        row,host_imp,guest_imp = get_teammatch_onerow(idx, board["all"], team)
        rows += row
        total_hostimp += int(host_imp) if host_imp else 0
        total_guestimp+= int(guest_imp) if guest_imp else 0

    # calculate VP from IMPs, it depends on board number
    diff_imp = total_hostimp - total_guestimp
    if abs(diff_imp) > len(vp_scale_8boards)-1:
        vp = vp_scale_8boards[-1] # 20.00
    else:
        vp = vp_scale_8boards[abs(diff_imp)]
    if diff_imp > 0:
        host_vp=vp
        guest_vp=20-vp
    else:
        guest_vp=vp
        host_vp=20-vp

    result = {
        "rows" : rows,
        "teamno": teamno,
        "teamhost" : team[0],
        "teamguest" : team[1],
        "hostimp" : total_hostimp,
        "guestimp": total_guestimp,
        "hostvp": format(host_vp,".2f"),
        "guestvp": format(guest_vp,".2f")
    }
    src = read_template("match-temp.html")
    contents = src.safe_substitute(result)
    return contents,(total_hostimp,total_guestimp), (host_vp,guest_vp)

def get_team_summary(summary):
    teams_html = ""
    print("\n>> Summary of team score:")
    print("==============")
    for idx, scores in enumerate(summary):
        teams, imp, vp = scores
        print("> %d: %2d : %-2d, %.2f : %.2f / %s" % \
            (idx+1,imp[0],imp[1],vp[0],vp[1],"%s vs %s" % (teams[0], teams[1]) ))
        html =  "<tr><td  class='td_top'><a href='#match-%d'>%s<a></td><td class='td_top'>vs</td><td class='td_top'><a href='#match-%d'>%s</a></td>" % (idx+1, teams[0], idx+1, teams[1])
        html += "<td align='right' class='d_lt'>%2d</td><td class='d_top''>:</td><td align='left' class='td_top'>%2d</td>" %  (imp[0],imp[1])
        html += "<td align='right' class='d_lt'>%.2f</td><td class='d_top' padding='1px'>:</td><td align='left' class='td_top'>%.2f</td></tr>" %  (vp[0],vp[1])

        teams_html += html
    
    src = Template(summary_template)
    result={ "teamsummary" :teams_html } 
    contents = src.safe_substitute(result)
    return contents

def get_boards_summary(boards):
    """
    calculate one match
    """
    boards_html = ""
    for idx, board in enumerate(boards):
        # for each board
        src = Template(board_template)
        board_html = ""
        for result in board["all"]:
            row = get_board_onerow(idx, result)
            board_html += row
        result={ "board" : board_html, "boardno": idx+1 } 
        contents = src.safe_substitute(result)
        boards_html += contents
    #src = Template(boards_template)
    #result={ "boards" :teams_html } 
    return boards_html

def pbr(record_xls):
    """
    read xls file and generate related html
    """
    base_file = record_xls[:-len("xlsx")]
    output = base_file + "html"
 
    teams,players,boards,currentdate = read_excel(record_xls)

    teams_html =""
    summary=[]
    for idx, team in enumerate(teams):
        html, imp, vp = get_match(boards, idx+1, team)
        teams_html += html
        summary.append([team,imp, vp])
    summary_html=get_team_summary(summary)

    boards_html=get_boards_summary(boards)

    result = {  "teams" : teams_html, 
                "summary" : summary_html, 
                "boards" : boards_html,
                "version" : version,
                "date": currentdate}
    src = read_template("index-temp.html")
    contents = src.safe_substitute(result)

    with io.open(output, "w", encoding="utf-8") as text_file:
        print("write to file %s" % output)
        text_file.write(contents)

def usage():
    usage = """
    $ pbr sample # download sample record.xlsx
    $ pbr <record.xlsx> # check result.html
    see more for README
    """
    print(usage)

def download_sample():
    if __name__ == '__main__':
        print("dear contributor, do this in package mode")
        return
    sample_files=['record.xlsx']
    for sample_file in sample_files:
        if os.path.exists(sample_file):
            print("%s already exists, ingore (or remove it first)" % sample_file)
        else:
            print("download sample file -> [%s]" % sample_file)
            shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)),sample_file),".")

def main():
    # print(sys.argv)
    if len(sys.argv) > 1:
        params = sys.argv[1:]
        if params[0] == "sample":
            download_sample()
        elif params[0] == "help":
            usage()
        else:
            record_xls=params[0]
            if record_xls.endswith(".xlsx"):
                pbr(record_xls)
            else:
                usage()
    else:
        usage()

if __name__ == '__main__':
    main()

