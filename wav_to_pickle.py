# -*- coding: utf-8 -*-
"""
¯\_(ツ)_/¯
speech decoding for all wav files in a given subject folder
"""
import os
import sys
import quail

if sys.version_info[0] < 3:
    ls = os.listdir('.')
else:
    ls = os.listdir()
print('Subject data file in pwd: \n ' + str(ls))
print("TYPE: decode_all_wav('subj name in strings')")

dataDir = os.getcwd()
stimDir = os.path.join(dataDir, '../stimuli')
os.chdir(stimDir)

with open('cel_names.txt', 'r') as f:
    cel_list = f.read().splitlines()
with open('loc_names.txt', 'r') as f:
    loc_list = f.read().splitlines()
with open('obj_names.txt', 'r') as f:
    obj_list = f.read().splitlines()

total_list = cel_list + loc_list + obj_list

os.chdir(dataDir)

def decode_all_wav(subj):
    """
    Help: type decode_all_wav('subj name in strings')
    decode_all_wav.py needs to be inside data folder
    Code is based on quail's decode_speech.py
    You need Google Cloud account setup with key.json file + quail setup on your computer to run this
    """
    subj = subj.lower()
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

    for i in range(0,len(ls)):
        #double check if wav file
        if ls[i][-3:] == 'wav':
            recall_data = quail.decode_speech(ls[i], save=True,speech_context=total_list,keypath='/Users/Jin/documents/matlab/research/recall-0fa1a5e0555b.json')
            print(recall_data)
            print('end of wav file ' + str(i+1))
    filename = os.path.join(pwdDir + '/..')
    os.chdir(filename)



"""
https://github.com/ContextLab/quail/blob/master/quail/decode_speech.py
Parameters for quail.decode_speech:
    ----------
    path : str
        Path to a wav file, or a folder of wav files.
    keypath : str
        Google Cloud Speech API key filepath. This is a JSON file containing
        credentials that was generated when creating a service account key.
        If None, assumes you have a local key that is set with an environmental
        variable. See the speech decoding tutorial for details.
    save : boolean
        False by default, but if set to true, will save a pickle with the results
        object from google speech, and a text file with the decoded words.
    speech_context : list of str
        This allows you to give some context to the speech decoding algorithm.
        For example, this could be the words studied on a given list, or all
        words in an experiment.
    sample_rate : float
        The sample rate of your audio files (default is 44100).
    max_alternatives : int
        You can specify the speech decoding to return multiple guesses to the
        decoding.  This will be saved in the results object (default is 1).
    language_code : str
        Decoding language code.  Default is en-US. See  here for more details:
        https://cloud.google.com/speech/docs/languages
    enable_word_time_offsets : bool
        Returns timing information s(onsets/offsets) for each word (default is
        True).
    return_raw : boolean
        Intead of returning the parsed results objects (i.e. the words), you can
        return the raw reponse object.  This has more details about the decoding,
        such as confidence.
    Returns
    ----------
    words : list of str, or list of lists of str
        The results of the speech decoding. This will be a list if only one file
        is input, or a list of lists if more than one file is decoded.
    raw : google speech object, or list of objects
        You can optionally return the google speech object instead of the parsed
        results by using the return_raw flag.
"""
