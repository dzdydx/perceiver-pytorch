# -*- coding: utf-8 -*-
# @Time    : 2021/11/10 11:17 AM
# @Author  : dzdydx
# @Affiliation  : 
# @Email   : 
# @File    : eval_set_reshape.py

# rename eval set files to [ytid].flac

import pandas as pd
import os, shutil, json
from tqdm import trange

def write_log(ytid, info):
    with open('log.json', 'r', encoding='utf8') as fp:
        log = json.load(fp)

    with open('log.json', 'w', encoding='utf8') as f:
        log[ytid] = info
        json.dump(log, f)

os.chdir('../dataset')
eval_csv = pd.read_excel('eval-labels.xlsx')
ytids = eval_csv.iloc[:,0].tolist()

eval_dir = os.listdir('audioset-eval')
ids = [int(i.split('_')[0][7:]) for i in eval_dir]

log = {}
for i in trange(len(ytids)):
    if i in ids:
        orig_file = f'audioset-eval/{eval_dir[ids.index(i)]}'
        targ_file = f'eval/{ytids[i]}.flac'
        os.system(f"ffmpeg -i {orig_file} \
            -ac 1 -ar 16000 -c:a flac -loglevel quiet \
            {targ_file}")
    else:
        log[ytids[i]] = 'miss'

with open('log.json', 'w', encoding='utf8') as f:
    json.dump(log, f)
