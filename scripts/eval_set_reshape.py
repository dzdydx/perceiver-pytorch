# -*- coding: utf-8 -*-
# @Time    : 2021/11/10 11:17 AM
# @Author  : dzdydx
# @Affiliation  : 
# @Email   : 
# @File    : eval_set_reshape.py

# reshape eval set of Audioset to a typical Pytorch dataset.

from pathlib import Path
import shutil, os

os.chdir('/home/liuwuyang/project/AudioSet')

eval_files = os.listdir('audioset-eval')
num = 0
for file in eval_files:
  f = file.split('_')
  labels = f[-1][:-4].split('-')
  name = f[0][7:] + '.wav'

  for label in labels:
    p = Path('eval', label).mkdir(exist_ok=True)
    name = f[0][7:] + '.wav'
    shutil.copyfile(Path('audioset-eval', file), Path('eval', label, name))
  
  num += len(labels)
  if num % 2000 == 0:
    print(f'{num} files copied.')

print(f'{len(eval_files)} eval set files, {num} files copied.')