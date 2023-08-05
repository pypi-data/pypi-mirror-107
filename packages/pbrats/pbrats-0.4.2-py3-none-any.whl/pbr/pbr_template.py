#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import Template
import pkgutil

# below are html template
id_template="""
    <td align='center'  class='td_nowrap td_leftSolid td_topSolid' >$declarer</td>
    <td align='center'  class='td_nowrap td_leftDotted td_topSolid' >$contract</td>
    <td align='center'  class='td_nowrap td_leftDotted td_topSolid' >$result</td>
    <td  colspan='2' align='right' class='td_nowrap td_leftSolid td_topSolid' ><font color='$scorecolor'>$score</font></td>
"""

# below are html template
board_id_template="""
    <td align='center'  class='td_nowrap td_leftSolid td_topSolid'><font color='#A0A080'>$vul</font></td>
    <td align='center'  class='td_nowrap td_leftSolid td_topSolid'>$declarer</td>
    <td align='center'  class='td_nowrap td_leftDotted td_topSolid'>$contract</td>
    <td align='center'  class='td_nowrap td_leftDotted td_topSolid'>$result</td>
    <td  colspan='2' align='right' class='td_nowrap td_leftSolid td_topSolid' ><font color='$scorecolor'>$score</font></td>
"""

onerow_template="""
<tr  bgcolor='#FAFAFA'>
    <td align='center' rowspan='2' class='td_top'><small>$boardno</small></td>
    <td align='center' rowspan='2' class='d_lt'><font color='#A0A080'>$vul</font></td>
    $host
    <td align='center' rowspan='2' class='d_lt'>$diff</td>
    <td align='center' rowspan='2' class='d_lt'>$hostimp</td>
    <td align='center' rowspan='2' class='d_lt'>$guestimp</td>
</tr>
<tr bgcolor="#F0F4F4">
    $guest
</tr>
"""

oneboardrow_template="""
<tr  bgcolor='#FAFAFA'>
    <td align='center' class='td_top'>$id</td>
    $host
</tr>
"""

board_template="""
<h3>第 $boardno 副</h3>
$pbn
<table class='TableFrame_blank1px' align='center' cellspacing='0px' cellpadding='6px'>
    <tr  bgcolor='#D5E0FF'>
        <td align='center'>ID</td>
        <td align='center' class='td_left'>局况</td>
        <td align='center' class='td_left'>做庄</td>
        <td align='center' class='td_left'>定约</td>
        <td align='center' class='td_left'>结果</td>
        <td align='center' class='td_left'>基本分</td>
    </tr>
    $board
</table>
"""

summary_template="""
<table class='TableFrame_blank1px' align='center' cellspacing='0px' cellpadding='6px'>
    <tr  bgcolor='#D5E0FF'>
        <td align='center'>主队</td>
        <td align='center'>vs</td>
        <td align='center'>客队</td>
        <td align='center' colspan='3' class='td_left'>IMP</td>
        <td align='center' colspan='3' class='td_left'>比赛胜利分</td>
    </tr>
    $teamsummary
</table>
"""

def read_template(template_file):
    # read local first (debug), then module
    try:
        template = open(template_file, "r",encoding="utf-8").read()
        src = Template(template)
    except FileNotFoundError:
        if __name__ == "__main__":
            raise IOError("can't find file, debug?")
        else:
            template = pkgutil.get_data(__name__,template_file)
            src = Template(template.decode('utf-8'))
    return src

def html_suit(contract):
    suit_css = {
        'S':  "<font color=black>&spades;</font>",
        "H":  "<font color=red>&hearts;</font>",
        "D":  "<font color=red>&diams;</font>",
        "C":  "<font color=black>&clubs;</font>"
    }
    for k,v in suit_css.items():
        contract = contract.replace(k, v)
    return contract
