import sys
import ipdb
import pandas as pd
import datetime as dt
from Levenshtein import distance as dist
from os.path import expanduser
pd.set_option('display.max_colwidth',80)

FILTER_TERMS = ['ls','install','dt hist', 'git diff', 'dt -v',
                'ipython','htop','git push','git pull','git stash']

def dt_conv(l: str):
    try:
        # TODO: correct timezone? why does midnight show up as 4 pm?
        pd_dt_repr = pd.to_datetime(dt.datetime.fromtimestamp(int(l[1].strip())))
        return  '_'.join(str(pd_dt_repr).split(' ')[::-1])
    except ValueError as e:
        # TODO: why does this occur
        # print(e)
        pass


def filter_term(term: tuple):
    # TODO: does not seem to work properly
    # Logic: all filter terms need to _not_ match
    return all([term[0] not in ft for ft in FILTER_TERMS])

def hist_print(n_lines=20):
    home = expanduser("~")
    # TODO: check if 'rb' does not break linux implementation
    f = open(f'{home}/.zsh_history', 'rb').read()
    split_f = str(f).split(':')

    # TODO: \n -> \\n for Mac, check if this is an issue on Linux
    parsed_commands = [ ''.join(l.replace('\\n','').strip().split(';')[-1:]) for l in split_f if '\\n' in l]
    parsed_dt = [ t for t in split_f if '\\n' not in t]

    parsed = list(zip(parsed_commands, parsed_dt))

    cmds = [ t for t in parsed if filter_term(t) ]

    # dist(l[-1],l[-2])
    lev_dist = [ dist(cmds[i][0],cmds[i+1][0]) for i in range(len(cmds)-1) ]

    # TODO: make more efficent
    # Lev dist with previous terms (1 approx to catch typos)
    ld = lev_dist + [9999]
    # dist_dict = { k:v for k,v in zip(cmds,ld) }
    dist_dict = { k:v for k,v in zip(cmds,ld) if v>4 }
    # TODO check if ordered before
    last_list = list(dist_dict.keys())[-n_lines:]

    # constructs DF with one line per command
    last_cmds = [ l[0].replace('\\','') for l in last_list ]
    # TODO: the time seems to be wrong still
    last_dt = [ dt_conv(l) for l in last_list]
    df = pd.DataFrame([last_cmds,last_dt]).T
    df.columns = ['Command', 'Time']

    return df