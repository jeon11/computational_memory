# -*- coding: utf-8 -*-
"""
¯\_(ツ)_/¯
1. First decodes the wav file to Python pickle using quail
2. Unpickle files to clean out text and save to csv

speech decoding for all wav files in a given subject folder
ideal file directory:
cdcatmr > data (pwd) > subj_folder names
        > stimuli    > export_stim

and ideally only trial wav files should be within the record folder
"""
import pickle
import os
import sys
import quail
import csv
import pandas as pd
from collections import Counter

if sys.version_info[0] < 3:
    ls = os.listdir('.')
else:
    ls = os.listdir()
ls.sort()
print('Subject data file in pwd: \n ' + str(ls))
print("TYPE: decode('subj name in strings')")

dataDir = os.getcwd()
stimDir = os.path.join(dataDir, '../stimuli')
os.chdir(stimDir)

# call in cdcatmr stim pool
with open('cel_names.txt', 'r') as f:
    cel_list = f.read().splitlines()
with open('loc_names.txt', 'r') as f:
    loc_list = f.read().splitlines()
with open('obj_names.txt', 'r') as f:
    obj_list = f.read().splitlines()

total_list = cel_list + loc_list + obj_list

# create flatten version of total list
total_temp = total_list
for i in range(0, len(total_temp)):
    total_temp[i] = total_temp[i].split(" ")
total_breakdown = []
for sublist in total_temp:
    for item in sublist:
        total_breakdown.append(item)

# create two lists for filtering
uniqueWords = []
stopWords = []
a = Counter(total_breakdown)
for i in range(0,len(a)):
    if a.values()[i] >= 2:
        stopWords.append(a.keys()[i].lower())
    else:
        uniqueWords.append(a.keys()[i].lower())

os.chdir(dataDir)

def decode(subj):
    """
    Help: type decode('subj name in strings')
    decode_all_wav.py needs to be inside data folder
    decoding wav to pickle is based on quail's decode_speech.py
    You need Google Cloud account setup with key.json file + quail setup on your computer to run this
    """
    col_order = ['trialN','index','item','category','intrusion','onset','offset']
    df = pd.DataFrame(columns=col_order)

    subj = subj.lower()

    # get export_stim
    dataDir = os.getcwd()
    stimDir = os.path.join(dataDir, '../stimuli')
    export_stimDir = stimDir + '/export_stim/' + str(subj)
    print('identifying subject trial data at: ' + str(export_stimDir))
    export_stim = pd.read_csv(export_stimDir + 'stimuli.csv')
    stim_temp = export_stim.stimName

    # remove random spaces in text if so
    stim = [0] * len(stim_temp)
    for i in range(0,len(stim_temp)):
        stim[i] = ' '.join(stim_temp[i].split())

    # correct trial set
    stim_trial1 = stim[18:45]
    stim_trial2 = stim[45:72]
    stim_trial3 = stim[72:99]
    stim_trial4 = stim[99:126]
    stim_trial5 = stim[126:153]
    stim_trial6 = stim[153:180]
    stim_trial7 = stim[180:207]
    stim_trial8 = stim[207:234]
    stim_trial9 = stim[234:261]

    # need flatten list for accurate comparison
    def flatten_list(trial_list):
        temp_flat = [0] * len(trial_list)
        for i in range(0,len(trial_list)):
            temp_flat[i] = trial_list[i].split(' ')
        stim_flat = []
        for sub in temp_flat:
            for item in sub:
                stim_flat.append(item)
        for k in range(0,len(stim_flat)):
            stim_flat[k] = stim_flat[k].lower()
        return stim_flat

    stim_trial_flat1 = flatten_list(stim_trial1)
    stim_trial_flat2 = flatten_list(stim_trial2)
    stim_trial_flat3 = flatten_list(stim_trial3)
    stim_trial_flat4 = flatten_list(stim_trial4)
    stim_trial_flat5 = flatten_list(stim_trial5)
    stim_trial_flat6 = flatten_list(stim_trial6)
    stim_trial_flat7 = flatten_list(stim_trial7)
    stim_trial_flat8 = flatten_list(stim_trial8)
    stim_trial_flat9 = flatten_list(stim_trial9)

    # cd to subj/record path
    pwdDir = os.getcwd()
    filename = os.path.join(pwdDir, '' + str(subj))
    if not os.path.isdir(filename):
        print('No such subject name/data file')
    os.chdir(filename)
    pwdDir = os.getcwd()
    filename = os.path.join(pwdDir + '/record')
    os.chdir(filename)

    # check if python 2 or 3
    if sys.version_info[0] < 3:
        ls = os.listdir('.')
    else:
        ls = os.listdir()
    print(len(ls))

    # use quail to decode wav to pickle
    for i in range(0,len(ls)):
    # set trial_stim specific to that trial for speech_context
        try:
            trial_stim = eval('stim_trial%d'% (i+1))
        except NameError:
            pass

        #double check if wav file
        if ls[i][-4:] == '.wav':
            recall_data = quail.decode_speech(ls[i], save=True,speech_context=trial_stim,keypath='/Users/Jin/documents/matlab/research/recall-0fa1a5e0555b.json')
            # recall_data = quail.decode_speech(ls[i], save=True,speech_context=total_list,keypath='/Users/Jin/documents/matlab/research/recall-0fa1a5e0555b.json')
            print(recall_data)
            print('end of wav file ' + str(i+1))

#######################################################
### Let's unpickle
#######################################################
    # reinstate ls for newly created files
    if sys.version_info[0] < 3:
        ls = os.listdir('.')
    else:
        ls = os.listdir()

    pickle_files = []
    for i in range(0,len(ls)):
    # pickle_files = lsit of all the pickle file names in str
        if ls[i][-2:] == '.p':
            pickle_files.append(str(ls[i]))
    pickle_files.sort()
    print('all that pickles! ~_@' + str(pickle_files))

    # now main loop part... going through each pickle
    for p in range(0,len(pickle_files)):
        objects = []
        pickleFile = pickle_files[p]
        with (open(pickleFile, 'rb')) as openfile:
            while True:
                try:
                    objects.append(pickle.load(openfile))
                except EOFError:
                    break
        print(len(pickle_files))
        trial_stim = eval('stim_trial%d'% (p+1))
        trial_stim_flat = eval('stim_trial_flat%d'% (p+1))

    # save a text file with all the unpickle for backup
        temp_text = pickleFile[:-6]
        unpickled = temp_text + '_T' + str(p+1) + '[FULL-TEXT].txt'
        f=open(unpickled,'w')
        f.write(str(objects))
        f.close()
        with open(unpickled, 'r') as f:
            unpickled_text = f.read().splitlines()
            # unpickled_text = f.read().split(" ")

    # initial filtering: extract out lines with 'transcript'
        recalled_words = []
        seconds = []
        nanos = []
        start_time = []
        end_time = []
        count = False
        for i in range(0, len(unpickled_text)):
            if 'transcript' in unpickled_text[i]:
                recalled_words.append(unpickled_text[i])
        # parse out timing
            if 'start_time' in unpickled_text[i]:
                if ('seconds' in unpickled_text[i+1]) or ('nanos' in unpickled_text[i+1]):
                    start_time.append(unpickled_text[i+1])
                if 'nanos' in unpickled_text[i+2]:
                    start_time.append(unpickled_text[i+2])
            if 'end_time' in unpickled_text[i]:
                if ('seconds' in unpickled_text[i+1]) or ('nanos' in unpickled_text[i+1]):
                    end_time.append(unpickled_text[i+1])
                if 'nanos' in unpickled_text[i+2]:
                    end_time.append(unpickled_text[i+2])

#### Onset / Offset cleaning
        # for extracting onset/offset time
        # remove random spaces
        for i in range(0,len(start_time)):
            start_time[i] = ' '.join(start_time[i].split())
        for i in range(0,len(end_time)):
            end_time[i] = ' '.join(end_time[i].split())

        # check if seconds/nanos are alternating and find missing spots
        for i in range(0, len(start_time)):
            try:
                # set the starting
                if 'nanos' in start_time[0]:
                    start_time[0:0] = ['seconds: 0']
                # if nanos is missing
                if 'seconds' in start_time[i] and 'nanos' not in start_time[i+1]:
                    start_time[i+1:i+1] = ['nanos: 0000']
                # if seconds is missing
                if 'nanos' in start_time[i] and 'seconds' not in start_time[i+1]:
                    start_time[i+1:i+1] = ['seconds: 0']
            except IndexError:
                pass

        # check the same for end_time
        for i in range(0, len(end_time)):
            try:
                # set the starting
                if 'nanos' in start_time[0]:
                    end_time[0:0] = ['seconds: 0']
                # if nanos is missing
                if 'seconds' in end_time[i] and 'nanos' not in end_time[i+1]:
                    end_time[i+1:i+1] = ['nanos: 0000']
                # if seconds is missing
                if 'nanos' in end_time[i] and 'seconds' not in end_time[i+1]:
                    end_time[i+1:i+1] = ['seconds: 0']
            except IndexError:
                pass

        # extract only the digits for start_time
        for i in range(0,len(start_time)):
            a = start_time[i].split()
            start_time[i]=[str(s) for s in a if s.isdigit()]
        # extract only the digits for end_time
        for i in range(0,len(end_time)):
            a = end_time[i].split()
            end_time[i]=[str(s) for s in a if s.isdigit()]

        # shorten the numbers if len exceeds 2
        for i in range(0,len(start_time)):
            if len(start_time[i][0]) >= 2:
                start_time[i][0] = start_time[i][0][:2]
        for i in range(0,len(end_time)):
            if len(end_time[i][0]) >= 2:
                end_time[i][0] = end_time[i][0][:2]

        # merge seconds and nanos into one time format
        flat_start = []
        flat_end = []
        numbers = range(0, len(start_time)+1)
        evens = [n for n in numbers if n % 2 == 0]
        for i in range(0,len(start_time)):
            if i in evens:
                try:
                    temp= start_time[i][0] + '.' + start_time[i+1][0]
                    flat_start.append(temp)
                except IndexError:
                    pass

        numbers = range(0, len(end_time)+1)
        evens = [n for n in numbers if n % 2 == 0]
        for i in range(0,len(end_time)):
            if i in evens:
                try:
                    temp= end_time[i][0] + '.' + end_time[i+1][0]
                    flat_end.append(temp)
                except IndexError:
                    pass


#### back to cleaning text file
        for i in range(0, len(recalled_words)):
            recalled_words[i] = recalled_words[i].split(" ")
            recalled_words[i] = recalled_words[i][5:]

    # flattens out the list to individual item index
        flat_list = []
        for sublist in recalled_words:
            for item in sublist:
                flat_list.append(item)

    # cleaning text file
    # remove '"' in front and end of items
        while '"' in flat_list:
            try:
                for i in range(0, len(flat_list)):
                    if flat_list[i] == '"':
                        flat_list.remove(flat_list[i])
            except IndexError:
                pass
        for i in range(0, len(flat_list)):
            if flat_list[i][0] == '"':
                flat_list[i] = flat_list[i][1:]
        for i in range(0, len(flat_list)):
            if flat_list[i][-1] == '"':
                flat_list[i] = flat_list[i][:-1]

    # zip the words to corresponding onset/offset timing
        timing = list(zip(flat_list,flat_start,flat_end))

        # check for repeats & mark them
        uniq = []
        reps = []
        for i in range(0, len(flat_list)):
            if flat_list[i] in uniq:
                reps.append(flat_list[i])
                flat_list[i] = flat_list[i] + '_repeat'
            if flat_list[i] not in uniq:
                uniq.append(flat_list[i])

    # compare recalled items to actual wordpool
        final_list = []
        intrusion_list = []

        for j in range(0, len(flat_list)):
            for k in range(0, len(trial_stim)):

            # ADD EXCEPTION CASES ---------------------------------------------
            # 'white' and 'house' are both common words
                if (flat_list[j].lower() == 'white') and (flat_list[j+1].lower() == 'house') and ('White House' in trial_stim):
                    final_list.append('White House')
                    intrusion_list.append(0)
                    break

            # ######################---------------------------------------------
            # compare list to stim trial and check if it's correct
                if flat_list[j].lower() in uniqueWords:
                    if (flat_list[j].lower() in trial_stim[k].lower()) and (trial_stim[k] not in final_list):
                        final_list.append(trial_stim[k])
                        intrusion_list.append(0)
                        break

            # checks for intrusion/unidentified words
                if flat_list[j].lower() not in trial_stim_flat:
                    final_list.append(flat_list[j])
                    intrusion_list.append(1)
                    break

    # get category list array
        category_list = [0] * len(final_list)

        for i in range(0,len(final_list)):
            if final_list[i] in cel_list:
                category_list[i] = 1
            if final_list[i] in loc_list:
                category_list[i] = 2
            if final_list[i] in obj_list:
                category_list[i] = 3

    # pairing start/end time of each word
        onset = [0] * len(final_list)
        offset = [0] * len(final_list)

        for i in range(0,len(final_list)):
            # if length of final list item is exactly 1 word
            if len(final_list[i].split()) == 1:
                for j in range(0, len(timing)):
                    if timing[j][0].lower() == final_list[i].split()[0].lower():
                        onset[i] = timing[j][1]
                        offset[i] = timing[j][2]
            # if length of final list item is more than 1 word
            if len(final_list[i].split()) >= 2:
                for j in range(0, len(timing)):
                    if timing[j][0].lower() == final_list[i].split()[0].lower():
                        onset[i] = timing[j][1]
                    if timing[j][0].lower() == final_list[i].split()[-1].lower():
                        offset[i] = timing[j][2]

        # remove '_repeat' tags
        for i in range(0,len(final_list)):
            if '_repeat' in final_list[i]:
                final_list[i] = final_list[i][:-7]
                intrusion_list[i] = -1

    # save to pandas dataframe & save as csv
        index = range(1,len(final_list)+1)
        recall_data = {'trialN': p+1, 'index': index, 'item': final_list, 'category': category_list, 'intrusion': intrusion_list, 'onset':onset, 'offset':offset}

        temp_df = pd.DataFrame(data=recall_data)
        temp_df = temp_df.reindex(columns=col_order)
        df = df.append(temp_df)

    # delete the erroroneous .txt file created from quail
        temp_text = pickleFile[:-2]
        os.remove(temp_text + '.txt')

    # create easy-to-read textfile
        temp_text = pickleFile[:-6]
        timingTxt = temp_text + '_T' + str(p+1) + '[EASY-READ].txt'
        with open(timingTxt, 'w') as f:
            for item in timing:
                f.write("%s\n" % (item,))

    # print summary of trial recalled items
        print('TRIAL ' + str(p+1) ,final_list)

    df = df.reindex(columns=col_order)

    df.to_csv(subj + '[ANNOTATION].csv', sep=',',index = False)

## go back to original file
    filename = os.path.join(pwdDir + '/..')
    os.chdir(filename)
