#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Version 1: N400 (100) --> Practice (6) --> Trials (400)

NetStation event logging:
NetStation (NS) event is sent at start of fixation, word change, buffer, and response
S at the end of tag means start of the event
E at the end of tag means end of the event
ie. fixS --> fixE for fixation events
If photocell is set on, it is logged as 'wsqS' in PsychoPY, and DIN3 event in NS
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                     Experiment Parameter                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

netstation  = True       #False to run the file locally without connecting to NetStation
recording   = True       #True starts recording NetStation automatically
photocell   = True        #True allows use of photocell device


# Photocell variables #Default values are based on current lab environment
dur_whitesquare=1 #Minimize duration of photocell square blinking
square_width=0.5      #default: 0.5 cm
square_height=0.5     #default: 0.5 cm
square_pos=(14.9,11.2)#default: (14.9,11.2)
square_opac=0.9       #default: 0.9 (range from 0-1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                    Initialize Components                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# NetStation setup
if netstation:
    import egi.simple as egi
    ms_localtime = egi.ms_localtime
    ns = egi.Netstation()
    print("Imported PyNetstation")

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
stimDir = os.getcwd()

# Store info about the experiment session
expName = 'sfv_eeg1'  # from the Builder filename that created this script
expInfo = {'session': '001', 'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[1280, 800], fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

if photocell:
    whitesquare = visual.Rect(
        win=win, name='whitesquare', units='cm',
        width=(square_width, square_height)[0], height=(square_width, square_height)[1],
        ori=0, pos=square_pos,
        lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
        fillColor=[1,1,1], fillColorSpace='rgb',
        opacity=square_opac, depth=0.0, interpolate=True)

# clocks
introClock = core.Clock()
n400Clock = core.Clock()
practiceClock = core.Clock()
instructionsClock = core.Clock()
feedbackClock = core.Clock()
startClock = core.Clock()
trialClock = core.Clock()
feedback3Clock = core.Clock()
endClock = core.Clock()

# n400 trial components
n400IntroText = visual.TextStim(win=win, name='n400IntroText',
    text='Welcome!\n\nFor the first part of this experiment, you will be reading a series of sentences. Some of them will make sense, and some of them will not. Please keep your eyes on the center of the screen and pay attention as each sentence is presented.',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0,units='cm');

fixation_n400 = visual.TextStim(win=win, name='fixation_n400',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0,units='cm');
sentence_n400 = visual.TextStim(win=win, name='sentence_n400',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0,units='cm');
buffer_n400 = visual.TextStim(win=win, name='buffer_n400',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0,units='cm');

# Initialize components for Routine "practice"
practiceIntroText = visual.TextStim(win=win, name='practiceIntroText',
    text="In this next part of the study, you will be verifying a series of word-feature pairs using the 'TRUE' and 'FALSE' keys. We'll start things off with a practice round.\n\nPress the spacebar to begin. ",
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0,units='cm');
bufferPractice = visual.TextStim(win=win, name='bufferPractice',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0,units='cm');
fixationPractice = visual.TextStim(win=win, name='fixationPractice',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0,units='cm');
targetPractice = visual.TextStim(win=win, name='targetPractice',
    text='default text',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0,units='cm');
splitPractice = visual.TextStim(win=win, name='splitPractice',
    text='.',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-4.0,units='cm');
featurePractice = visual.TextStim(win=win, name='featurePractice',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-5.0,units='cm');
respPractice = visual.TextStim(win=win, name='respPractice',
    text='***',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-6.0,units='cm');

# Initialize components for Routine "feedback"
feedbackText = visual.TextStim(win=win, name='feedbackText',
    text="Oops, too slow!",
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0,units='cm');

# Initialize components for Routine "start"
trialIntroText = visual.TextStim(win=win, name='trialIntroText',
    text='That concludes the practice round!\n\nPlease let your experimenter know if you have any remaining questions.\n\nIf not, press the spacebar to begin the experiment.',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0,units='cm');

# Initialize components for Routine "trial"
bufferTrial = visual.TextStim(win=win, name='bufferTrial',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0,units='cm');
fixationTrial = visual.TextStim(win=win, name='fixationTrial',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0,units='cm');
targetTrial = visual.TextStim(win=win, name='targetTrial',
    text='default text',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0,units='cm');
splitTrial = visual.TextStim(win=win, name='splitTrial',
    text='.',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-4.0,units='cm');
featureTrial = visual.TextStim(win=win, name='featureTrial',
    text='placeholder',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-5.0,units='cm');
respTrial = visual.TextStim(win=win, name='respTrial',
    text='***',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-6.0,units='cm');

# Initialize components for Routine "pause"
pauseClock = core.Clock()
pause1Text = visual.TextStim(win=win, name='pause1Text',
    text='You may now take a short break.\n\nThe experimenter will check on you momentarily.\n\n',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0,units='cm');
pause2Text = visual.TextStim(win=win, name='pause2Text',
    text='Press the spacebar to return to the experiment.',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0,units='cm');

# Initialize components for Routine "end"
thankyouText = visual.TextStim(win=win, name='thankyouText',
    text='That concludes our study! Thank you for your participation.\n\nPress the spacebar to exit.',
    font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0,units='cm');

# helpers
def send_to_NS(tag, type, cond):
    """
    helper function to send signals with desired event tags as 'tag' as argument
    tag: fixS, fixE, senS, etc...
    type: N400, prac, or tral
    sem, validity, distance, val are for prac and tral uses

    dev note. # bufs = codes. label = label, key code= table 'abke' is 1, 2, etc
    """
    if netstation:
        ns.sync()
        logging.data(str(tag) + ' in ' + str(type))
        if str(type) == 'n400':
            ns.send_event(key=str(tag),label=str(type),timestamp=None,pad=False)
        if str(type) == 'prac' or str(type) == 'tral':
            ns.send_event(key=str(tag),label=str(type), timestamp=None,table={'cond':cond},pad=False)

# def send_to_NS(tag): #version 1
#     """
#     helper function to send signals with desired event tags as 'tag' as argument
#     Ex. simply put send_to_NS('tri#')
#     """
#     if netstation:
#         ns.sync()
#         logging.data(str(tag))
#         ns.send_event(key=str(tag),timestamp=None,pad=False)

wsq_drawn = False
def show_photocell():
    """
    helper to display photocell given the photocell condition is on
    """
    if photocell:
        whitesquare.setAutoDraw(True)
        logging.data('wsqS')
        wsq_drawn = True

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# ------Prepare to start Routine "intro"-------
t = 0
introClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
instrN400_keyResp = event.BuilderKeyResponse()
# keep track of which components have finished
introComponents = [n400IntroText, instrN400_keyResp]
for thisComponent in introComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# NetStation
if netstation:
    ns.connect('10.0.0.42', 55513)
    ns.BeginSession()
    print("Connected to Netstation")
    if recording:
        ns.StartRecording()
        print("Recording ...")


# -------Start Routine "intro"-------
send_to_NS('intS','n400',cond=None)

while continueRoutine:
    # get current time
    t = introClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

   # *n400IntroText* updates
    if t >= 0.0 and n400IntroText.status == NOT_STARTED:
        # keep track of start time/frame for later
        n400IntroText.tStart = t
        n400IntroText.frameNStart = frameN  # exact frame index
        n400IntroText.setAutoDraw(True)

   # *instrN400_keyResp* updates
    if t >= 0.0 and instrN400_keyResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrN400_keyResp.tStart = t
        instrN400_keyResp.frameNStart = frameN  # exact frame index
        instrN400_keyResp.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if instrN400_keyResp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

       # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in introComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "intro"-------
for thisComponent in introComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# NetStation
send_to_NS('intE','n400',cond=None)
# the Routine "intro" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
n400_stim = data.TrialHandler(nReps=1, method='random',
   extraInfo=expInfo, originPath=-1,
   trialList=data.importConditions(stimDir + '/n400_stim.xlsx'),
   seed=None, name='n400_stim')
thisExp.addLoop(n400_stim)  # add the loop to the experiment
thisN400_stim = n400_stim.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisN400_stim.rgb)
if thisN400_stim != None:
    for paramName in thisN400_stim:
        exec('{} = thisN400_stim[paramName]'.format(paramName))

for thisN400_stim in n400_stim:
    currentLoop = n400_stim
    # abbreviate parameter names if possible (e.g. rgb = thisN400_stim.rgb)
    if thisN400_stim != None:
        for paramName in thisN400_stim:
            exec('{} = thisN400_stim[paramName]'.format(paramName))

    # ------Prepare to start Routine "n400"-------
    t = 0
    n400Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    # get the feature for this trial and split it into a list of words:

    words = stim.split()
    numWords = len(words)
    i = 0
    frameCounter = 0

    fixationDuration = 120
    totalDuration = numWords * 30 #frames
    bufferStart = fixationDuration + totalDuration

    sentence_n400.setText('')
    # keep track of which components have finished
    n400Components = [fixation_n400, sentence_n400, buffer_n400]
    for thisComponent in n400Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # for netstation event logging
    curr_trial = currentLoop.nTotal - currentLoop.nRemaining
    if curr_trial < 10:
        n400trial = 'n00' + str(curr_trial)
    if curr_trial == currentLoop.nTotal:
        n400trial = 'n' + str(currentLoop.nTotal)
    if (curr_trial >= 10) and (curr_trial < 100):
        n400trial = 'n0' + str(curr_trial)

    send_to_NS(n400trial,'n400',cond=None) # per trial
    # -------Start Routine "n400"-------
    while continueRoutine:
        # get current time
        t = n400Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

        if photocell:
            if (frameN == 0) or (frameN == fixationDuration) or (frameN == bufferStart):
                show_photocell()
            if (frameN == 1) or (frameN == fixationDuration+1) or (frameN == bufferStart+1):
                whitesquare.setAutoDraw(False)
            frameCount = 30
            if frameN > fixationDuration:
                if frameCounter != frameCount:
                    whitesquare.setAutoDraw(False)

       # *fixation_n400* updates
        if frameN >= 0 and fixation_n400.status == NOT_STARTED:
           # keep track of start time/frame for later
            fixation_n400.tStart = t
            fixation_n400.frameNStart = frameN  # exact frame index
            fixation_n400.setAutoDraw(True)
            send_to_NS('fixS','n400',cond=None)

        if fixation_n400.status == STARTED and frameN >= (fixation_n400.frameNStart + fixationDuration):
            fixation_n400.setAutoDraw(False)
            send_to_NS('fixE','n400',cond=None)

       # update/draw components on each frame
        if frameN >= fixationDuration:
            if i<= len(words)-1:
                sentence_n400.setText(words[i])
                frameCount = 30
                frameCounter += 1
                if frameCounter == frameCount:
                    send_to_NS('wd+1','n400',cond=None)
                    show_photocell()
                    i+=1
                    frameCounter = 0

        # *sentence_n400* updates
        if frameN >= fixationDuration and sentence_n400.status == NOT_STARTED:
            # keep track of start time/frame for later
            sentence_n400.tStart = t
            sentence_n400.frameNStart = frameN  # exact frame index
            sentence_n400.setAutoDraw(True)
            send_to_NS('senS','n400',cond=None)

        if sentence_n400.status == STARTED and frameN >= (sentence_n400.frameNStart + totalDuration):
            sentence_n400.setAutoDraw(False)
            send_to_NS('senE','n400',cond=None)

        # *buffer_n400* updates
        if frameN >= bufferStart and buffer_n400.status == NOT_STARTED:
            # keep track of start time/frame for later
            buffer_n400.tStart = t
            buffer_n400.frameNStart = frameN  # exact frame index
            buffer_n400.setAutoDraw(True)
            send_to_NS('bufS','n400',cond=None)

        if buffer_n400.status == STARTED and frameN >= (buffer_n400.frameNStart + 240):
            buffer_n400.setAutoDraw(False)
            send_to_NS('bufE','n400',cond=None)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in n400Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "n400"-------
    for thisComponent in n400Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    send_to_NS('n40E','n400',cond=None)
    # the Routine "n400" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

# # completed 1 repeats of 'n400_stim'


# ------Prepare to start Routine "instructions"-------
t = 0
instructionsClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
instrPractice_keyResp = event.BuilderKeyResponse()
# keep track of which components have finished
instructionsComponents = [practiceIntroText, instrPractice_keyResp]
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

send_to_NS('intS','prac',cond=None)
# -------Start Routine "instructions"-------
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *practiceIntroText* updates
    if t >= 0.0 and practiceIntroText.status == NOT_STARTED:
        # keep track of start time/frame for later
        practiceIntroText.tStart = t
        practiceIntroText.frameNStart = frameN  # exact frame index
        practiceIntroText.setAutoDraw(True)

    # *instrPractice_keyResp* updates
    if t >= 0.0 and instrPractice_keyResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrPractice_keyResp.tStart = t
        instrPractice_keyResp.frameNStart = frameN  # exact frame index
        instrPractice_keyResp.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if instrPractice_keyResp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
send_to_NS('intE','prac',cond=None)
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method='random',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(stimDir + '/sfv_practice.xlsx'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))

    # ------Prepare to start Routine "practice"-------
    t = 0
    practiceClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    # get the feature for this trial and split it into a list of words:

    words = feat.split()
    cond_num = cond
    numWords = len(words)
    i = 0
    frameCounter = 0
    totalDuration = numWords * 30 #frames
    ready_for_resp = totalDuration + 180 # when to start practice_resp

    targetPractice.setText(concept)
    prac_keyResp = event.BuilderKeyResponse()
    # keep track of which components have finished
    practiceComponents = [bufferPractice, fixationPractice, targetPractice, splitPractice, featurePractice, respPractice, prac_keyResp]
    for thisComponent in practiceComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # for netstation event logging
    curr_trial = currentLoop.nTotal - currentLoop.nRemaining
    pracTrial = 'pra' + str(curr_trial)

    send_to_NS(pracTrial,'prac',cond=None)
    # -------Start Routine "practice"-------
    while continueRoutine:
        # get current time
        t = practiceClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

        if photocell:
            if (frameN == 0) or (frameN == 60) or (frameN == 120) or (frameN == 150) or (frameN == 180) or (frameN == ready_for_resp):
                show_photocell()
            if (frameN == 1) or (frameN == 61) or (frameN == 121) or (frameN == 151) or (frameN == 181) or (frameN == ready_for_resp+1):
                whitesquare.setAutoDraw(False)
            frameCount = 30
            if frameN > 180 and frameN < ready_for_resp:
                if frameCounter != frameCount:
                    whitesquare.setAutoDraw(False)

        # *bufferPractice* updates
        if frameN >= 0.0 and bufferPractice.status == NOT_STARTED:
            # keep track of start time/frame for later
            bufferPractice.tStart = t
            bufferPractice.frameNStart = frameN  # exact frame index
            bufferPractice.setAutoDraw(True)
            send_to_NS('bufS','prac',cond=cond_num)
        if bufferPractice.status == STARTED and frameN >= (bufferPractice.frameNStart + 60):
            bufferPractice.setAutoDraw(False)
            send_to_NS('bufE','prac',cond=cond_num)

        # *fixationPractice* updates
        if frameN >= 60 and fixationPractice.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixationPractice.tStart = t
            fixationPractice.frameNStart = frameN  # exact frame index
            fixationPractice.setAutoDraw(True)
            send_to_NS('fixS','prac',cond=cond_num)
        if fixationPractice.status == STARTED and frameN >= (fixationPractice.frameNStart + 60):
            fixationPractice.setAutoDraw(False)
            send_to_NS('fixE','prac',cond=cond_num)

        # *targetPractice* updates
        if frameN >= 120 and targetPractice.status == NOT_STARTED:
            # keep track of start time/frame for later
            targetPractice.tStart = t
            targetPractice.frameNStart = frameN  # exact frame index
            targetPractice.setAutoDraw(True)
            send_to_NS('tarS','prac',cond=cond_num)
        if targetPractice.status == STARTED and frameN >= (targetPractice.frameNStart + 30):
            targetPractice.setAutoDraw(False)
            send_to_NS('tarE','prac',cond=cond_num)

        # *splitPractice* updates
        if frameN >= 150 and splitPractice.status == NOT_STARTED:
            # keep track of start time/frame for later
            splitPractice.tStart = t
            splitPractice.frameNStart = frameN  # exact frame index
            splitPractice.setAutoDraw(True)
            send_to_NS('splS','prac',cond=cond_num)
        if splitPractice.status == STARTED and frameN >= (splitPractice.frameNStart + 30):
            splitPractice.setAutoDraw(False)
            send_to_NS('splE','prac',cond=cond_num)

        # featurePractice text change
        if frameN >= 180: # 3 seconds, 60 frames/sec
            if i<= len(words)-1:
                featurePractice.setText(words[i])
                frameCount = 30
                frameCounter += 1
                if frameCounter == frameCount:
                    send_to_NS('ft+1','prac',cond=cond_num)
                    show_photocell()
                    i+=1
                    frameCounter = 0

        # *featurePractice* updates
        if frameN >= 180 and featurePractice.status == NOT_STARTED:
            # keep track of start time/frame for later
            featurePractice.tStart = t
            featurePractice.frameNStart = frameN  # exact frame index
            featurePractice.setAutoDraw(True)
            send_to_NS('feaS','prac',cond=cond_num)
        if featurePractice.status == STARTED and frameN >= (featurePractice.frameNStart + totalDuration):
            featurePractice.setAutoDraw(False)
            send_to_NS('feaE','prac',cond=cond_num)

        # *respPractice* updates
        if frameN >= ready_for_resp and respPractice.status == NOT_STARTED:
            # keep track of start time/frame for later
            respPractice.tStart = t
            respPractice.frameNStart = frameN  # exact frame index
            respPractice.setAutoDraw(True)
            send_to_NS('resS','prac',cond=cond_num)
        if respPractice.status == STARTED and frameN >= (respPractice.frameNStart + 150):
            respPractice.setAutoDraw(False)
            send_to_NS('resE','prac',cond=cond_num)

        # *prac_keyResp* updates
        if frameN >= ready_for_resp and prac_keyResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            prac_keyResp.tStart = t
            prac_keyResp.frameNStart = frameN  # exact frame index
            prac_keyResp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(prac_keyResp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if prac_keyResp.status == STARTED and t >= (prac_keyResp.tStart + 2.5):
            prac_keyResp.status = STOPPED
        if prac_keyResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['period', 'slash'])
            if theseKeys:
                if theseKeys[0] == 'period':
                    send_to_NS('kyp.','prac',cond=cond_num)
                if theseKeys[0] == 'slash':
                    send_to_NS('kyp/','prac',cond=cond_num)


            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if prac_keyResp.keys == []:  # then this was the first keypress
                    prac_keyResp.keys = theseKeys[0]  # just the first key pressed
                    prac_keyResp.rt = prac_keyResp.clock.getTime()
                    # was this 'correct'?
                    if (prac_keyResp.keys == str(corrAns)) or (prac_keyResp.keys == corrAns):
                        prac_keyResp.corr = 1
                    else:
                        prac_keyResp.corr = 0
                    # a response ends the routine
                    continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in practiceComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "practice"-------
    for thisComponent in practiceComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    send_to_NS('praE','prac',cond=None)

    # check responses
    if prac_keyResp.keys in ['', [], None]:  # No response was made
        prac_keyResp.keys=None
        # was no response the correct answer?!
        if str(corrAns).lower() == 'none':
           prac_keyResp.corr = 1  # correct non-response
        else:
           prac_keyResp.corr = 0  # failed to respond (incorrectly)
    # store data for trials (TrialHandler)
    trials.addData('prac_keyResp.keys',prac_keyResp.keys)
    trials.addData('prac_keyResp.corr', prac_keyResp.corr)
    if prac_keyResp.keys != None:  # we had a response
        trials.addData('prac_keyResp.rt', prac_keyResp.rt)
    # the Routine "practice" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "feedback"-------
    t = 0
    feedbackClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    if prac_keyResp.keys:
         continueRoutine = False

    # keep track of which components have finished
    feedbackComponents = [feedbackText]
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # -------Start Routine "feedback"-------
    while continueRoutine:
        # get current time
        t = feedbackClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

        # *feedbackText* updates
        if t >= 0.0 and feedbackText.status == NOT_STARTED:
            # keep track of start time/frame for later
            feedbackText.tStart = t
            feedbackText.frameNStart = frameN  # exact frame index
            feedbackText.setAutoDraw(True)
            send_to_NS('fbtS','prac',cond=None)
        if feedbackText.status == STARTED and frameN >= (feedbackText.frameNStart + 60):
            feedbackText.setAutoDraw(False)
            send_to_NS('fbtE','prac',cond=None)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "feedback"-------
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "feedback" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

# completed 1 repeats of 'trials' practice


# ------Prepare to start Routine "start"-------
t = 0
startClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_respTrial = event.BuilderKeyResponse()
# keep track of which components have finished
startComponents = [trialIntroText, key_respTrial]
for thisComponent in startComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "start"-------
while continueRoutine:
    # get current time
    t = startClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *trialIntroText* updates
    if t >= 0.0 and trialIntroText.status == NOT_STARTED:
        # keep track of start time/frame for later
        trialIntroText.tStart = t
        trialIntroText.frameNStart = frameN  # exact frame index
        trialIntroText.setAutoDraw(True)
    if t >= 0.0 and trialIntroText.status == NOT_STARTED:
        send_to_NS('intS','tral',cond=None)

    # *key_respTrial* updates
    if t >= 0.0 and key_respTrial.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_respTrial.tStart = t
        key_respTrial.frameNStart = frameN  # exact frame index
        key_respTrial.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if key_respTrial.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in startComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "start"-------
for thisComponent in startComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
send_to_NS('intE','tral',cond=None)
# the Routine "start" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials_3 = data.TrialHandler(nReps=1, method='random',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(stimDir + '/sfv_trials.xlsx'),
    seed=None, name='trials_3')
thisExp.addLoop(trials_3)  # add the loop to the experiment
thisTrial_3 = trials_3.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial_3.rgb)
if thisTrial_3 != None:
    for paramName in thisTrial_3:
        exec('{} = thisTrial_3[paramName]'.format(paramName))

for thisTrial_3 in trials_3:
    currentLoop = trials_3
    # abbreviate parameter names if possible (e.g. rgb = thisTrial_3.rgb)
    if thisTrial_3 != None:
        for paramName in thisTrial_3:
            exec('{} = thisTrial_3[paramName]'.format(paramName))

    # ------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat

    # get the feature for this trial and split it into a list of words:

    words = feat.split()
    cond_num = cond
    numWords = len(words)
    i = 0
    frameCounter = 0

    totalDuration = numWords * 30 #frames
    ready_for_resp = totalDuration + 180 # when to start practice_resp
    # currentWordIndex = -1

    targetTrial.setText(concept)
    trial_keyResp = event.BuilderKeyResponse()
    # keep track of which components have finished
    trialComponents = [bufferTrial, fixationTrial, targetTrial, splitTrial, featureTrial, respTrial, trial_keyResp]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # for netstation event logging
    curr_trial = currentLoop.nTotal - currentLoop.nRemaining
    if curr_trial < 10:
        realTrial = 't00' + str(curr_trial)
    if (curr_trial >= 10) and (curr_trial < 100):
        realTrial = 't0' + str(curr_trial)
    if curr_trial >= 100:
        realTrial = 't' + str(curr_trial)

    send_to_NS(realTrial,'tral',cond=None)
    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

        if photocell:
            if (frameN == 0) or (frameN == 60) or (frameN == 120) or (frameN == 150) or (frameN == 180) or (frameN == ready_for_resp):
                show_photocell()
            if (frameN == 1) or (frameN == 61) or (frameN == 121) or (frameN == 151) or (frameN == 181) or (frameN == ready_for_resp+1):
                whitesquare.setAutoDraw(False)
            frameCount = 30
            if frameN > 180 and frameN < ready_for_resp:
                if frameCounter != frameCount:
                    whitesquare.setAutoDraw(False)

        # *bufferTrial* updates
        if frameN >= 0.0 and bufferTrial.status == NOT_STARTED:
            # keep track of start time/frame for later
            bufferTrial.tStart = t
            bufferTrial.frameNStart = frameN  # exact frame index
            bufferTrial.setAutoDraw(True)
            send_to_NS('bufS','tral',cond=cond_num)
        if bufferTrial.status == STARTED and frameN >= (bufferTrial.frameNStart + 60):
            bufferTrial.setAutoDraw(False)
            send_to_NS('bufE','tral',cond=cond_num)

        # *fixationTrial* updates
        if frameN >= 60 and fixationTrial.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixationTrial.tStart = t
            fixationTrial.frameNStart = frameN  # exact frame index
            fixationTrial.setAutoDraw(True)
            send_to_NS('fixS','tral',cond=cond_num)
        if fixationTrial.status == STARTED and frameN >= (fixationTrial.frameNStart + 60):
            fixationTrial.setAutoDraw(False)
            send_to_NS('fixE','tral',cond=cond_num)

        # *targetTrial* updates
        if frameN >= 120 and targetTrial.status == NOT_STARTED:
            # keep track of start time/frame for later
            targetTrial.tStart = t
            targetTrial.frameNStart = frameN  # exact frame index
            targetTrial.setAutoDraw(True)
            send_to_NS('tarS','tral',cond=cond_num)
        if targetTrial.status == STARTED and frameN >= (targetTrial.frameNStart + 30):
            targetTrial.setAutoDraw(False)
            send_to_NS('tarE','tral',cond=cond_num)

        # *splitTrial* updates
        if frameN >= 150 and splitTrial.status == NOT_STARTED:
            # keep track of start time/frame for later
            splitTrial.tStart = t
            splitTrial.frameNStart = frameN  # exact frame index
            splitTrial.setAutoDraw(True)
            send_to_NS('splS','tral',cond=cond_num)
        if splitTrial.status == STARTED and frameN >= (splitTrial.frameNStart + 30):
            splitTrial.setAutoDraw(False)
            send_to_NS('splE','tral',cond=cond_num)

        # update/draw components on each frame
        if frameN >= 180: # 3 seconds, 60 frames/sec
            if i<= len(words)-1:
                featureTrial.setText(words[i])
                frameCount = 30
                frameCounter += 1
                if frameCounter == frameCount:
                    send_to_NS('ft+1','tral',cond=cond_num)
                    show_photocell()
                    i+=1
                    frameCounter = 0

        # *featureTrial* updates
        if frameN >= 180 and featureTrial.status == NOT_STARTED:
            # keep track of start time/frame for later
            featureTrial.tStart = t
            featureTrial.frameNStart = frameN  # exact frame index
            featureTrial.setAutoDraw(True)
            send_to_NS('feaS','tral',cond=cond_num)
        if featureTrial.status == STARTED and frameN >= (featureTrial.frameNStart + totalDuration):
            featureTrial.setAutoDraw(False)
            send_to_NS('feaE','tral',cond=cond_num)

        # *respTrial* updates
        if frameN >= ready_for_resp and respTrial.status == NOT_STARTED:
            # keep track of start time/frame for later
            respTrial.tStart = t
            respTrial.frameNStart = frameN  # exact frame index
            respTrial.setAutoDraw(True)
            send_to_NS('resS','tral',cond=cond_num)
        if respTrial.status == STARTED and frameN >= (respTrial.frameNStart + 150):
            respTrial.setAutoDraw(False)
            send_to_NS('resE','tral',cond=cond_num)

        # *trial_keyResp* updates
        if frameN >= ready_for_resp and trial_keyResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            trial_keyResp.tStart = t
            trial_keyResp.frameNStart = frameN  # exact frame index
            trial_keyResp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(trial_keyResp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if trial_keyResp.status == STARTED and t >= (trial_keyResp.tStart + 2.5):
            trial_keyResp.status = STOPPED
        if trial_keyResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['period', 'slash'])
            if theseKeys:
                if theseKeys[0] == 'period':
                    send_to_NS('kyp.','tral',cond=cond_num)
                if theseKeys[0] == 'slash':
                    send_to_NS('kyp/','tral',cond=cond_num)

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if trial_keyResp.keys == []:  # then this was the first keypress
                    trial_keyResp.keys = theseKeys[0]  # just the first key pressed
                    trial_keyResp.rt = trial_keyResp.clock.getTime()
                    # was this 'correct'?
                    if (trial_keyResp.keys == str(corrAns)) or (trial_keyResp.keys == corrAns):
                        trial_keyResp.corr = 1
                    else:
                        trial_keyResp.corr = 0
                    # a response ends the routine
                    continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    # check responses
    if trial_keyResp.keys in ['', [], None]:  # No response was made
        trial_keyResp.keys=None
        # was no response the correct answer?!
        if str(corrAns).lower() == 'none':
           trial_keyResp.corr = 1  # correct non-response
        else:
           trial_keyResp.corr = 0  # failed to respond (incorrectly)
    # store data for trials_3 (TrialHandler)
    trials_3.addData('trial_keyResp.keys',trial_keyResp.keys)
    trials_3.addData('trial_keyResp.corr', trial_keyResp.corr)
    if trial_keyResp.keys != None:  # we had a response
        trials_3.addData('trial_keyResp.rt', trial_keyResp.rt)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "feedback3"-------
    t = 0
    feedback3Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    if trial_keyResp.keys:
         continueRoutine = False
    # keep track of which components have finished
    feedback3Components = [feedbackText]
    for thisComponent in feedback3Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "feedback3"-------
    while continueRoutine:
        # get current time
        t = feedback3Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame


        # *feedbackText* updates
        if frameN >= 0.0 and feedbackText.status == NOT_STARTED:
            # keep track of start time/frame for later
            feedbackText.tStart = t
            feedbackText.frameNStart = frameN  # exact frame index
            feedbackText.setAutoDraw(True)
        if frameN == 0.0 and feedbackText.status == NOT_STARTED:
            send_to_NS('fbtS','tral',cond=None)
        if feedbackText.status == STARTED and frameN >= (feedbackText.frameNStart + 60):
            feedbackText.setAutoDraw(False)
            send_to_NS('fbtE','tral',cond=None)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in feedback3Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "feedback3"-------
    for thisComponent in feedback3Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "feedback3" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "pause"-------
    t = 0
    pauseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    instrPause_keyResp = event.BuilderKeyResponse()

    # Conditionally execute this pause routine:
    if not trials_3.thisN in [99, 199, 299]: # on most trials:
        continueRoutine = False # don't even start this routine

    # keep track of which components have finished
    pauseComponents = [pause1Text, pause2Text, instrPause_keyResp]
    for thisComponent in pauseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    send_to_NS('pauS','tral',cond=None)
    # -------Start Routine "pause"-------
    while continueRoutine:
        # get current time
        t = pauseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *pause1Text* updates
        if frameN >= 0.0 and pause1Text.status == NOT_STARTED:
            # keep track of start time/frame for later
            pause1Text.tStart = t
            pause1Text.frameNStart = frameN  # exact frame index
            pause1Text.setAutoDraw(True)
        if pause1Text.status == STARTED and frameN >= (pause1Text.frameNStart + 300):
            pause1Text.setAutoDraw(False)

        # *pause2Text* updates
        if frameN >= 300 and pause2Text.status == NOT_STARTED:
            # keep track of start time/frame for later
            pause2Text.tStart = t
            pause2Text.frameNStart = frameN  # exact frame index
            pause2Text.setAutoDraw(True)

        # *instrPause_keyResp* updates
        if frameN >= 300 and instrPause_keyResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            instrPause_keyResp.tStart = t
            instrPause_keyResp.frameNStart = frameN  # exact frame index
            instrPause_keyResp.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if instrPause_keyResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False


        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in pauseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "pause"-------
    for thisComponent in pauseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    send_to_NS('paeE','tral',cond=None)
    # the Routine "pause" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

# completed 1 repeats of 'trials_3'


# ------Prepare to start Routine "end"-------
t = 0
endClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
instrEnding_keyResp = event.BuilderKeyResponse()
# keep track of which components have finished
endComponents = [thankyouText, instrEnding_keyResp]
for thisComponent in endComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
send_to_NS('endS','tral',cond=None)
# -------Start Routine "end"-------
while continueRoutine:
    # get current time
    t = endClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *thankyouText* updates
    if frameN >= 0.0 and thankyouText.status == NOT_STARTED:
        # keep track of start time/frame for later
        thankyouText.tStart = t
        thankyouText.frameNStart = frameN  # exact frame index
        thankyouText.setAutoDraw(True)

    # *instrEnding_keyResp* updates
    if frameN >= 0.0 and instrEnding_keyResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrEnding_keyResp.tStart = t
        instrEnding_keyResp.frameNStart = frameN  # exact frame index
        instrEnding_keyResp.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if instrEnding_keyResp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
