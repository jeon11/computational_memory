import os
import csv
import pandas as pd
from collections import Counter
import sys
import math
from __future__ import division

root = os.getcwd()
dataDir = os.path.join(root, '../data_for_cdcatmr/')
os.chdir(dataDir)
os.getcwd()

# pandas dataframe
col_names = ['subj','period','slash','nan','stim_total', 'period %','total response %','average rt','cond1 resp','cond1 total','cond1 %','cond2 resp','cond2 total','cond2 accuracy']
results = pd.DataFrame(columns=col_names)

if sys.version_info[0] < 3:
    pilots = os.listdir('.')
else:
    pilots = os.listdir()
pilots.sort()
pilots
a = pilots[3]
a
os.chdir(os.path.join(dataDir, a))
pwd = os.getcwd()
pwd = pwd + '/events/'
pwd
os.chdir(pwd)
ls = os.listdir('.')
ls.sort()
ls

if ls[0][-4:] == '.csv':
    dat = pd.read_csv(ls[0])
len(dat)
dat
stim_pres_index = []
for i in range(0,len(dat)):
    if dat.iloc[i]['type'] == 'stim_pres':
        stim_pres_index.append(i)

math_ans = []
for i in range(0,len(dat)):
    if dat.iloc[i]['type'] == 'math_ans':
        math_ans.append(i)
len(math_ans)
# math_ans

resp = []
rt = []
for i in range(0, len(stim_pres_index)):
    resp.append(dat.iloc[stim_pres_index[i]]['resp'])
    rt.append(dat.iloc[stim_pres_index[i]]['rt'])
len(resp)
resp

# count number of responses for each
period = []
slash = []
nan = []
for i in range(0, len(resp)):
    if resp[i] == 'period':
        period.append(stim_pres_index[i])
    elif resp[i] == 'slash':
        slash.append(stim_pres_index[i])
    elif resp[i] is not 'period' and resp[i] is not 'slash':
        nan.append(stim_pres_index[i])

# double check resp is sum of all possible responses
if len(resp) != len(period) + len(slash) + len(nan):
    print('resp sum error. double check')

ratio = (len(period)/(len(period)+len(slash))) * 100
ratio = round(ratio, 2)
ratio_response = ((len(period)+len(slash))/len(resp)) * 100
ratio_response = round(ratio_response, 2)

# get average rt for responses
positive_rt = []
for i in range(0,len(rt)):
    try:
        temp = float(rt[i][:4])
        positive_rt.append(temp)
    except (ValueError, TypeError):
        pass
average_rt = sum(positive_rt)/len(positive_rt)
average_rt = round(average_rt, 2)

results_subj = list([a[-1:]])
results_period = list([len(period)])
results_slash = list([len(slash)])
results_nan = list([len(nan)])
results_stim_total = list([len(resp)])
results_periodr = list([ratio])
results_response = list([ratio_response])
results_rt = list([average_rt])


#### MATH STUFF
stimDir = '/Users/Jin/Documents/MATLAB/research/cdcatmr/stimuli/export_stim/'
os.chdir(stimDir)
os.getcwd()

if sys.version_info[0] < 3:
    stimFiles = os.listdir('.')
else:
    stimFiles = os.listdir()
stimFiles.sort()
stimFiles
for i in range(0, len(stimFiles)):
    if a in stimFiles[i]:
            stim = pd.read_csv(stimFiles[i])

cond0_trials = [-2]
cond1_trials = [-1]
cond2_trials = [0]

for i in range(0, len(dat)):
    if dat.iloc[i]['trialN'] not in cond0_trials and dat.iloc[i]['trialN'] not in cond1_trials and dat.iloc[i]['trialN'] not in cond2_trials:
        temp = dat.iloc[i]['trialN'] - 1
        dex = 20 + temp * 27
        temp_cond = stim.iloc[dex]['cond']
        if temp_cond == 0:
            cond0_trials.append(dat.iloc[i]['trialN'])
        if temp_cond == 1:
            cond1_trials.append(dat.iloc[i]['trialN'])
        if temp_cond == 2:
            cond2_trials.append(dat.iloc[i]['trialN'])

# cond0_trials
# cond1_trials
# cond2_trials

# response rate for condition 1: light distraction
cond1_resp = []
cond1_resp_nan = []
cond1_byTrial = {}
for i in range(0, len(math_ans)):
    if dat.iloc[math_ans[i]]['trialN'] in cond1_trials:
        temp_resp = dat.iloc[math_ans[i]]['resp']
        cond1_byTrial["cond1_corrT{0}".format(dat.iloc[math_ans[i]]['trialN'])] = []
        cond1_byTrial["cond1_errT{0}".format(dat.iloc[math_ans[i]]['trialN'])] = []
        if temp_resp == 'period' or temp_resp == 'slash':
            cond1_resp.append(i)
            cond1_byTrial["cond1_corrT{0}".format(dat.iloc[math_ans[i]]['trialN'])].append(i)
        else:
            cond1_resp_nan.append(i)
            cond1_byTrial["cond1_errT{0}".format(dat.iloc[math_ans[i]]['trialN'])].append(i)
len(cond1_resp)
len(cond1_resp_nan)
cond1_byTrial
cond1_byTrial['cond1_corrT-1']
ratio_cond1_resp = (len(cond1_resp) / (len(cond1_resp) + len(cond1_resp_nan))) * 100
ratio_cond1_resp = round(ratio_cond1_resp, 2)
ratio_cond1_resp
cond1_total = len(cond1_resp) + len(cond1_resp_nan)

# response rate for condition 2: heavy distraction
cond2_resp = []
cond2_resp_nan = []
for i in range(0, len(math_ans)):
    if dat.iloc[math_ans[i]]['trialN'] in cond2_trials:
        temp_resp = dat.iloc[math_ans[i]]['resp']
        if temp_resp == 'period' or temp_resp == 'slash':
            cond2_resp.append(i)
        else:
            cond2_resp_nan.append(i)
len(cond2_resp)
len(cond2_resp_nan)
ratio_cond2_resp = len(cond2_resp) / (len(cond2_resp) + len(cond2_resp_nan))
ratio_cond2_resp = round(ratio_cond2_resp, 2)
ratio_cond2_resp
cond2_total = len(cond2_resp) + len(cond2_resp_nan)

# get correct rate for condition 2: heavy distration
temp = []
cond2_resp_corr = []
cond2_resp_err = []
for i in range(0, len(dat)):
    if dat.iloc[i]['trialN'] in cond2_trials and dat.iloc[i]['type'] == 'math_dist':
        temp.append(int(dat.iloc[i]['item']))
    if dat.iloc[i]['trialN'] in cond2_trials and dat.iloc[i]['type'] == 'math_ans':
        if sum(temp) == int((dat.iloc[i]['item'][:-1])):
            cond2_resp_corr.append(i)
            temp = []
        else:
            cond2_resp_err.append(i)
            temp = []
len(cond2_resp_corr)
len(cond2_resp_err)
ratio_cond2_corr = len(cond2_resp_corr) / cond2_total * 100
ratio_cond2_corr = round(ratio_cond2_corr, 2)

# col_names = ['subj','period','slash','nan','stim_total', 'period %','total response %','average rt','cond1 resp','cond1 total','cond1 %','cond2 resp','cond2 total','cond2 accuracy']
# add to csv
temp_df = pd.DataFrame()
temp_df['subj'] = results_subj
temp_df['period'] = results_period
temp_df['slash'] = results_slash
temp_df['nan'] = results_nan
temp_df['stim_total'] = results_stim_total
temp_df['period %'] = results_periodr
temp_df['total response %'] = results_response
temp_df['average rt'] = results_rt
temp_df['cond1 resp'] = len(cond1_resp)
temp_df['cond1 total'] = cond1_total
temp_df['cond1 %'] = ratio_cond1_resp
temp_df['cond2 resp'] = len(cond2_resp)
temp_df['cond2 total'] = cond2_total
temp_df['cond2 accuracy'] = ratio_cond2_corr

# append to events dataframe
results = results.append(temp_df)

# save to machine (if scripts crashes we would lose 1 item max)
results.to_csv(pwd + '../../responseSummary.csv', sep=',', index=False)
