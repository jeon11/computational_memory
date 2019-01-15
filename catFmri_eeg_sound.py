################################################################################
# PsychoPy code to run catFmri - blocked category design
# behavioural version
# Rebecca Cutler September 2018

# saves detailed .log recorded by system and
# events.csv contains:
#   type:       event label (e.g. stim_pres, math_dist)
#   item:       name of stimuli
#   duration:   how long item was on the screen (in ms, but defined by frameNs)
#   resp:       keyboard response to item if relevant
#   rt:         response time of resp
#   trialtime:  time of event within each trial (trial = list of items)
#   runtime:    time dictated by scanner from first trigger launch
################################################################################

from __future__ import absolute_import, division, print_function
import os
import random
import pandas as pd
from builtins import range
from psychopy import visual, event, gui, core, logging, microphone, sound

##########################################
#         Experiment Parameters          #
##########################################

netstation = True
recording  = True

#-------------------------------------------------------------------------#
# vars        | values     | default     | description                    #
#-------------------------------------------------------------------------#

n_trials      = 9             # 9       | n trials (func runs)
n_trains      = 9             # 9        | trains (block cats) per run
n_per_train   = 3             # 3        | items per train

# durations (in seconds)
dur_stim      = 2.5           # 2.5      | stimuli presentatation time
dur_FR        = 90            # 90       | free recall time recorded
dur_digit     = 0.7           # 0.7      | math digit presentation time
dur_blank     = 0.2           # 0.2      | interval time between each math digit
dur_question  = 2             # 2        | math questions wait response time
dur_finalmath = 10            # 10       | duration of final mathQ round

isi_low       = 5             # 5        | lowest isi range
isi_high      = 8             # 8        | highest isi range
isi_mean      = 7             # 7        | n_items of isi created around mean
instrWaitTime = 2             # 2        | wait time for prep instructions

# stim size (keep ratio) && stim text distance
stim_width    = 5.08*2                   # actual image width  = 5.08cm
stim_height   = 6.35*2                   # actual image height = 6.35cm
stimTxt_height= 7                        # 7 - 6.35 = 0.65cm above the image

# miscellenious
i             = 0             # 0        | set to 0 for full runthrough
mouse_visible = False         # False    | false = mouse invisible
fixation_size = 0.7           # 0.7      | units in cm
fullscreen    = True          # True     |
n_items       = n_trains * n_per_train   # total items per trial


#########################################
#               Pre Setup               #
#########################################

# GUI to enter subj & experiment details
gui = gui.Dlg()
# subject and experiment specific information
gui.addField("SubjID:")
# gui.addField("Session:") # e.g. 0 = pilot (beh), 1 = pilot (scan) 2 = familiarity (beh) 3 = scan
# gui.addField("Date:") #
gui.show()
# record subj/exp specific information
subj_id = gui.data[0]
# sess = gui.data[1]
# date = gui.data[2]

# NetStation setup
if netstation:
    import egi.simple as egi
    ms_localtime = egi.ms_localtime
    ns = egi.Netstation()
    print("Imported PyNetstation")

# create window
win = visual.Window([800, 800], fullscr=fullscreen, monitor='testMonitor2')
# win = visual.Window([800,800], fullscr=False, winType='pygame', monitor='0')

# get relative path
stimDir = os.getcwd() + '/../'  # location of cdcatmr

# get current directory and create data file in /data > events, log, record
filename = os.path.join(stimDir, 'data/' + subj_id)
evtDirName = filename+'/events'
logDirName = filename+'/log'
wavDirName = filename+'/record'
if os.path.isdir(filename):
    print('DATA ALREADY EXISTS WITH SAME NAME!!! QUITTING...')
    core.quit()
if not os.path.isdir(filename):
    os.makedirs(filename)
    os.makedirs(evtDirName)
    os.makedirs(logDirName)
    os.makedirs(wavDirName)

# enable sound input/output:
microphone.switchOn()
mic = microphone.AdvAudioCapture(name=subj_id, saveDir=wavDirName, stereo=False)

# read in condition and stimuli data
fn1 = stimDir + 'stimuli/export_stim/' + subj_id + 'stimuli.csv'
stim_file = pd.read_csv(fn1, None, engine='python')
# stim_file = pd.read_csv(fn1,None, engine='python',skiprows=[19,20,21,22,23,24,25,26,27])

# read in sound data
soundDir = stimDir + 'stimuli/stimSound/'

# read in math distraction data
fn2 = stimDir + 'stimuli/math_dist.csv'
math_csv = pd.read_csv(fn2, None, engine='python')

# read text files
genIntroText1="Thank you for participating in this study! We are interested in understanding how people judge and subsequently remember items from different categories. \n\nDuring the course of the study, you will see a list of images on the computer screen. Each image will come from one of three categories: \n\n1) Famous People \n2) Locations \n3) Objects \n\nWhen an image comes up, please press a button to indicate whether you \"like\" or \"dislike\" the person, location, or object. \n\nPress TRUE to indicate \"like\" \nPress FALSE to indicate \"dislike\" \nAt the end of the list, you will asked to recall these images. \n\n       * Press SPACE to continue *"

genIntroText2="Between images you will perform a task lasting a few seconds. You will be told the type of task with brief instructions at the start of each list. Tasks will remain consistent for the list. The 3 possible tasks are: \n\nTask 1: Keeping your eyes focused on the fixation cross at the center of the screen \n\nTask 2: Pressing TRUE button whenever you see a number with a question mark \n\nTask 3: Solving a series of true or false math addition problems \n\nPlease note that both tasks 2 and 3 show numbers on the screen, but you will only solve math problems in task 3. \n\n\t\t* Press SPACE to continue *"

genIntroText3="In both tasks 2 and 3, a number will be presented on the screen one at a time. After either 2 or 3 numbers are presented, a number with a question mark will appear. \n\nFor task 2, simply press TRUE button whenever you see the number with a question mark. \n\n\t\t* Press SPACE to continue *"

genIntroText4="Task 3 is solving math problems. You need to press TRUE or FALSE button to indicate whether the last number with a question mark is the correct sum of the previous 2 or 3 numbers. \nFor example: \n\n'3' + '2' + '4' = '9?'\n\nIn this case, you should answer TRUE because 9 is the sum of three numbers. As you are solving the problems, the math period may time out and the next image will be presented. In such case, just focus on remembering the new image.\n\n\t\t* Press SPACE to continue *"

genIntroText5="After the final image in each list, you will perform Task 3 (Solving math problems) for several seconds again. \n\n\t\t* Press SPACE to continue *"

genIntroText6="After the final set of math problems, you will be asked to remember the images from the most recent list. \n\nOnce you see a set of stars (*******) on the screen, say as many names as you can remember from the list, in whatever order they come to mind. \n\nTry to make sure that the name you recall is as close as possible to the name presented with each image.\n\n\t\t* Press SPACE to continue *"

genIntroText7="You will have fixed amount of time to say the list. Please keep trying throughout the given time, as you may remember some words even after you feel like you have exhausted your memory. \n\nPlease avoid saying other things, such as \"um\" or \"uh...\". Speak loudly and clearly into the microphone. \n\n\t\t* Press SPACE to continue *"
genIntroText8="Before we begin the study, the experimenter will check in with you briefly. \n\n\t\t* Press SPACE to begin practice *"

text_cond_0="Task 1: \nKeep your eyes focused on the fixation cross at the center of the screen. \n\n\t\t* Press '1' to continue *"
text_cond_1="Task 2: \nPress TRUE whenever a question mark appears next to a number (e.g. '5?') \n\n\t\t* Press '2' to continue *"
text_cond_2="Task 3: \nSolve math addition problems. \ne.g. Press TRUE if the number with question mark is the correct sum. \n\n\t\t* Press '3' to continue *"

practiceText = "You are done with practice trials. \n\nExperimenter will check in  with you. Please ask any questions before you begin the experiment."
finalMathText = "Final task: Solve math addition problems"
breakText = "That concludes the list. \n\nPlease take a break if you need to and feel free to ask the experimenter if you have any questions. \n\n* Press SPACE to continue onto the next list *"
prepfrText = "Prepare to recall the list"
recordingText = "*******"
endingText = "You are done with the experiment. Thank you!"

# randomize math distractions to iterate
# (n numbers in problem and correct: incorrect ratio will be random)
math_file = math_csv.sample(frac=1).reset_index(drop=True)
math_head = list(math_file)

# read in stimuli variables
cond = stim_file['cond']
cat = stim_file['cat']
stimImg = stim_file['stimImg']
stimName = stim_file['stimName']

# for pandas dataframe
col_names = ['type', 'item', 'resp', 'rt', 'trialtime', 'duration', 'runtime', 'isi']

# create pandas dataframe
events = pd.DataFrame(columns=col_names)

# text/visual component properties
genIntText = visual.TextStim(
win=win,text='use for detailed instructions at beginning',
color="white", height=0.6, pos=(0,0),units='cm',
alignHoriz='center',alignVert='center'
)

instrText = visual.TextStim(
win=win,text= 'use for short instructions at each trial',
color="white",height=0.7, pos=(0,0),units='cm',
alignHoriz='center',alignVert='center'
)

fixation = visual.ShapeStim(
win=win,
vertices=((0, -fixation_size), (0, fixation_size), (0,0), (-fixation_size,0), (fixation_size, 0)),
lineWidth=6,
closeShape=False,
lineColor="white",units='cm'
)

img = visual.ImageStim(
win=win,
image=stimImg[0],
size = ([stim_width, stim_height]),units='cm'
)

stimText = visual.TextStim(
win=win,
text=stimName[0],
pos = ([0, stimTxt_height]),
color="white",units='cm'
)

mathText = visual.TextStim(
win=win,
text=math_file['num1'][0],
color="white",
)


# helper funcs
def pseudo_randomISI(low, high, k, n_items):
    """
    Creates n_items number of isi with range low and high with resulted numbers
    averaging around mean k
    """
    assert k < high
    rand_isi = [low] * n_items
    to_add = (k - low) * n_items
    for _ in range(to_add):
        i = random.randint(0, n_items-1)
        while rand_isi[i] == high:
            i = random.randint(0, n_items-1)
        rand_isi[i] += 1
    return rand_isi


def if_esc_quit():
    if event.getKeys(keyList=["escape"]):
        win.close()
        core.quit()


def blank_screen(dur_blank):
    instrText.text = ' '
    instrText.draw()
    win.flip()
    core.wait(dur_blank)


practiceTrial = True
def send_to_NS(code, trialnum, item, cond, category):
    """
    helper function to send signals with desired event tags, labels, cond for segmentation

    code = trial info ie. t1, t2, t3 ...
    label = 4 letter code sent to NS
    trialnum = t
    item = s                | item index number (1-27)
    cond = [1, 2, 3]        | fixation, light, heavy distraction
    category = [1, 2, 3]    | 1 = celeb, 2 = location, 3 = objects
    """
    if not practiceTrial and netstation:
        temp = 't' + str(trialnum)
        ns.sync()
        logging.data('trial ' + str(trialnum) + ' | ' + str(code) + ' | cond: ' + str(cond) + ' | cat: ' + str(category))
        ns.send_event(key=temp, label=str(code), timestamp=None, table={'item': item, 'cond': cond, 'catg': category}, pad=False)


# mouse cursor visibility
win.mouseVisible = mouse_visible

math_cnt = 0  # keep track of overall math problems
total_event_cnt = 0  # all events over all trials # n.b this might suck

# set up log to keep track of all events across trials
globalClock = core.Clock()  # if this isn't provided the log times will reflect secs since python started
trial_timer = core.Clock()  # start trial time

#########################################
#         General Instructions          #
#########################################
g = 1
while g in range(1, 9):
    genInt_timer = core.Clock()
    genIntText.text = eval('genIntroText%d' % (g))
    genIntText.draw()
    win.flip()
    inst_key = event.getKeys(keyList=['space'], timeStamped=genInt_timer)
    if_esc_quit()
    if inst_key:
        g += 1

# starts logging
logging.setDefaultClock(globalClock)
logging.console.setLevel(logging.DEBUG)  # receive nearly all messages; change for exp
logDat = logging.LogFile(stimDir + 'data/' + str(subj_id) + '/log/' + 'pilot_' + str(subj_id) + '.log',
    filemode='w',  # if you set this to 'a' it will append instead of overwriting
    level=logging.DEBUG)  # errors, data and warnings will be sent to this logfile

# NetStation
if netstation:
    ns.connect('10.0.0.42', 55513)
    ns.BeginSession()
    print("Connected to Netstation")
    if recording:
        ns.StartRecording()
        print("Recording ...")

actualTrial = False
#########################################
#           Experiment Code             #
#########################################
for t in range(0, n_trials+3):  # n_trials+4 b/c 3 is used for 3 practice trials
    trial_timer.reset()
    if t <= 2:
        practiceTrial = True
        n_items = 6  # practice round is fixed to 6 stim each
    if t > 2:
        practiceTrial = False
        actualTrial = True
        n_items = n_trains * n_per_train
    isi_list = pseudo_randomISI(isi_low, isi_high, isi_mean, n_items)

    if cond[i] == 0:  # fixation condition
        i11 = trial_timer.getTime()
        instrText.text = text_cond_0
        instrText.draw()
        win.logOnFlip('first instrText frame', level=logging.EXP)
        win.flip()
        instr_key = event.waitKeys(keyList=['1'], timeStamped=True, clearEvents=True)

        type = list(['instruction'])
        item = list(['instrText0'])
        trialtime = list([i11])
        duration = list([instr_key[0][1]])
        resp = list(['NaN'])
        rt = list(['NaN'])
        runtime = list(['NaN'])
        isi = list(['NaN'])

    if cond[i] == 1:  # light distraction
        i21 = trial_timer.getTime()
        instr1_timer = core.Clock()
        instrText.text = text_cond_1
        instrText.draw()
        win.logOnFlip('first instrText frame', level=logging.EXP)
        win.flip()
        instr_key = event.waitKeys(keyList=['2'], timeStamped=instr1_timer, clearEvents=True)
        if_esc_quit()

        type = list(['instruction'])
        item = list(['instrText1'])
        trialtime = list([i21])
        duration = list([instr_key[0][1]])
        resp = list(['NaN'])
        rt = list(['NaN'])
        runtime = list(['NaN'])
        isi = list(['NaN'])

    if cond[i] == 2:  # heavy distraction (solve math problems)
        i31 = trial_timer.getTime()
        instr2_timer = core.Clock()
        instrText.text = text_cond_2
        instrText.draw()
        win.logOnFlip('first instrText frame', level=logging.EXP)
        win.flip()
        instr_key = event.waitKeys(keyList=['3'], timeStamped=instr2_timer, clearEvents=True)
        if_esc_quit()

        type = list(['instruction'])
        item = list(['instrText2'])
        trialtime = list([i31])
        duration = list([instr_key[0][1]])
        resp = list(['NaN'])
        rt = list(['NaN'])
        runtime = list(['NaN'])
        isi = list(['NaN'])

    for s in range(0, n_items):
        item_isi = isi_list[s]
        print('item ' + str(s+1) + ' of trial ' + str(t-2) + ' (isi:' + str(item_isi) + ' | task:' + str(cond[i]+1) + ' | img:' + str(stimName[i]) + ')')

        # NetStation
        send_to_NS(code='bgin', trialnum=t, item=s+1, cond=cond[i]+1, category=None)

        if s >= 1:  # if this isn't the first item in the trial, then init all lists
            type = []
            item = []
            resp = []
            rt = []
            trialtime = []
            duration = []
            runtime = []

        event_cnt = 0  # keep track of n events to save per item pres
        mathTimeOut = False

        if cond[i] == 0:  # keep flipping fixation
            t11 = trial_timer.getTime()
            for frameN in range(int(item_isi*60)):
                fixation.draw()

                if frameN == 0:
                    win.logOnFlip('first fixation frame', level=logging.EXP)
                    # NetStation
                    send_to_NS(code='disS', trialnum=t, item=s+1, cond=cond[i]+1, category=cat[i])

                elif frameN == ((item_isi*60)-1):
                    win.logOnFlip('last fixation frame', level=logging.EXP)
                win.flip()
                if_esc_quit()

            t12 = trial_timer.getTime()
            t1_duration = t12 - t11

            # log fixation event
            type.append('fix_dist')
            item.append('+')
            trialtime.append(t11)
            duration.append(t1_duration)
            resp.append([])
            rt.append([])
            runtime.append([])
            isi = list([])
            event_cnt = event_cnt + 1

        else:  # light and heavy distraction = same number presentation, but diff keyboard commands
            math_timer = core.Clock()  # start timer to limit math distraction
            # NetStation
            send_to_NS(code='disS', trialnum=t, item=s+1, cond=cond[i]+1, category=cat[i])
            while math_timer.getTime() < item_isi:
                # grab random row from math dist file
                if math_cnt >= 90:
                    math_cnt = 0
                    math_file = math_csv.sample(frac=1).reset_index(drop=True)  # check
                # iterate through pre-randomized file
                cur_math = math_file.loc[[math_cnt]]

                # check if 2 or 3 numbers being presented
                if cur_math.iloc[0, 2] == 0:
                    n_math = 2
                else:
                    n_math = 3

                # math number loop
                for m in range(n_math):

                    # present numbers
                    cur_num = cur_math.iloc[0, m]
                    mathText.text = str(cur_num)

                    t21 = trial_timer.getTime()
                    for frameN in range(int(dur_digit*60)):
                        mathText.draw()

                        if frameN == 0:
                            win.logOnFlip('mathOnset, item %i' % m, level=logging.EXP)
                        win.flip()
                        if_esc_quit()

                        if math_timer.getTime() > item_isi:
                            mathTimeOut = True
                            blank_screen(dur_blank)
                            break
                        event.clearEvents('keyboard')
                    blank_screen(dur_blank)
                    # if mathTimeOut or (math_timer.getTime() > item_isi):
                    if math_timer.getTime() > item_isi:
                        mathTimeOut = True
                        blank_screen(dur_blank)
                        break

                    t22 = trial_timer.getTime()
                    t2_duration = t22-t21

                    # math_cnt = math_cnt + 1
                    type.append('math_dist')
                    item.append(cur_math.iloc[0, m])
                    trialtime.append(t21)
                    duration.append(t2_duration)
                    resp.append([])
                    rt.append([])
                    runtime.append([])
                    isi.append(item_isi)
                    event_cnt = event_cnt + 1
                event.clearEvents('keyboard')
                if_esc_quit()
                # final math number w/ question mark
                # randomly selects correct or incorrect answer to present
                if not mathTimeOut:
                    ans = random.randint(3, 4)
                    mathText.text = str(cur_math.iloc[0, ans]) + '?'
                    mathText.draw()
                if math_timer.getTime() > item_isi:
                    mathTimeOut = True
                    blank_screen(dur_blank)
                    break

                event.clearEvents('keyboard')
                if cond[i] == 2 and not mathTimeOut:  # heavy math distraction
                    t31 = trial_timer.getTime()
                    questionClock = core.Clock()
                    for frameN in range(dur_question*60):
                        mathText.draw()
                        if frameN == 0:
                            win.logOnFlip('mathQOnset', level=logging.EXP)
                        qDurClock = core.Clock()
                        win.flip()
                        if_esc_quit()
                        math_keys = event.getKeys(keyList=['period','slash'],  modifiers=False, timeStamped=questionClock)
                        if math_keys:
                            blank_screen(dur_blank)
                            break
                        if not math_keys and qDurClock.getTime() > dur_question:
                            blank_screen(dur_blank)
                            break
                        if math_timer.getTime() > item_isi:
                            blank_screen(dur_blank)
                            break

                    t32 = trial_timer.getTime()
                    t3_duration = t32-t31

                if cond[i] == 1 and mathTimeOut == False:
                    t31 = trial_timer.getTime()
                    questionClock = core.Clock()
                    for frameN in range(dur_question*60):
                        mathText.draw()
                        if frameN == 0:
                            win.logOnFlip('first mathQ frame', level=logging.EXP)
                        qDurClock = core.Clock()
                        win.flip()
                        if_esc_quit()
                        math_keys = event.getKeys(keyList=['period'], modifiers=False, timeStamped=questionClock)

                        if math_keys:
                            blank_screen(dur_blank)
                            break
                        if not math_keys and qDurClock.getTime() > dur_question:
                            blank_screen(dur_blank)
                            break
                        if math_timer.getTime() > item_isi:
                            blank_screen(dur_blank)
                            break


                    t32 = trial_timer.getTime()
                    t3_duration = t32-t31

                type.append('math_ans')
                item.append(str(cur_math.iloc[0, ans]) + '?')
                trialtime.append(t31)
                duration.append(t3_duration)
                if math_keys:
                    resp.append(math_keys[0][0])
                    rt.append(math_keys[0][1])
                else:
                    resp.append('NaN')
                    rt.append('NaN')
                runtime.append([])
                isi.append(item_isi)
                math_cnt = math_cnt + 1
                event_cnt = event_cnt + 1
            # NetStation
            send_to_NS(code='disE', trialnum=t, item=s+1, cond=cond[i]+1, category=cat[i])

        # stimulus image + text presentation and record keypress
        img.image = stimImg[i]
        stimText.text = stimName[i]

        # set sound
        stimSound = os.path.basename(stimImg[i])[:-4] # get just the stim name and {} ie. acorn{}
        stimSound = soundDir + stimSound + '.wav'
        vocal = sound.Sound(stimSound)
        vocal.setVolume(1)

        t41 = trial_timer.getTime()
        stimClock = core.Clock() # incase we care about RT of stim resp

        temp_stim_keys=[]

        soundDur = vocal.getDuration()
        for frameN in range(int(dur_stim*60)):
            img.draw()
            # stimText.draw()
            if frameN == 0:
                # vocal.play() # play immediately with image shown
                # NetStation
                send_to_NS(code='imgS', trialnum=t, item=s+1, cond=cond[i]+1, category=cat[i])
                keyResp = event.getKeys(keyList=['period','slash'], modifiers=False, timeStamped=stimClock)
                win.logOnFlip('stimOnset', level=logging.EXP)
            win.flip()
            if_esc_quit()
            if frameN == int((dur_stim/2 * 60)-(soundDur/2 * 60)):  # center align sound
                vocal.play()
                # NetStation
                send_to_NS(code='sndS', trialnum=t, item=s+1, cond=cond[i]+1, category=cat[i])
            if frameN == int((dur_stim/2 * 60)-(soundDur/2 * 60)+(soundDur * 60)):
                # NetStation
                send_to_NS(code='sndE', trialnum=t, item=s+1, cond=cond[i]+1, category=cat[i])
            if keyResp:
                stim_keys = keyResp
            else:
                stim_keys = []
            if stim_keys:
                # NetStation
                send_to_NS(code='imgK', trialnum=t, item=s+1, cond=cond[i]+1, category=cat[i])
                resp.append(stim_keys[0][0])
                rt.append(stim_keys[0][1])
                t42 = trial_timer.getTime()
                t4_duration = t42-t41
                type.append('stim_pres')
                item.append(stimName[i])
                trialtime.append(t41)
                duration.append(t4_duration)
                runtime.append([])
                temp_stim_keys=True
            if frameN >= ((dur_stim*60)-1) and not temp_stim_keys:
                # NetStation
                send_to_NS(code='imgE', trialnum=t, item=s+1, cond=cond[i]+1, category=cat[i])
                resp.append('NaN')
                rt.append('NaN')
                t42 = trial_timer.getTime()
                t4_duration = t42-t41
                type.append('stim_pres')
                item.append(stimName[i])
                trialtime.append(t41)
                duration.append(t4_duration)
                runtime.append([])

        # checks when to end practice trial
        if (practiceTrial == True) and (t == 2) and (s == n_items-1):
            instrText.text = practiceText
            instrText.draw()
            win.flip()
            practiceKeypress = event.waitKeys(keyList=['return','escape'], timeStamped=False, clearEvents=True)
            if practiceKeypress == 'return':
                practiceTrial = False
            if practiceKeypress == 'escape':
                core.quit()
        event_cnt = event_cnt + 1
        i = i+1  # update item count after each stimulus presentation

        temp_df = pd.DataFrame()
        temp_df['type'] = type; temp_df['item'] = item; temp_df['trialtime'] = trialtime; temp_df['duration'] = duration;
        temp_df['resp'] = resp; temp_df['rt'] = rt; temp_df['runtime'] = runtime;
        temp_df['isi'] = item_isi
        # append to events dataframe
        events = events.append(temp_df)

        # save to machine (if scripts crashes we would lose 1 item max)
        events.to_csv(stimDir + 'data/' + str(subj_id) + '/events/' + subj_id + '_events.csv', sep=',', index=False)
        logging.flush()  # force flush of .log messages at end of each stim pres

    #########################################
    #        Final Math Distraction         #
    #########################################
    finalMathTimeOut = False
    if actualTrial and not practiceTrial:
        type= []
        item = []
        resp = []
        rt = []
        trialtime = []
        duration = []
        runtime = []

        win.logOnFlip('final math instr', level=logging.EXP)
        instrText.text = finalMathText
        instrText.draw()
        win.flip()
        core.wait(instrWaitTime)

        math_timer_final = core.Clock()  # start timer to limit math distraction

        # NetStation
        send_to_NS(code='finS', trialnum=t, item=None, cond=None, category=None)
        while math_timer_final.getTime() < dur_finalmath:

            if math_cnt >= 90:  # catch end of math stim and reset
                math_cnt = 0
                math_file = math_csv.sample(frac=1).reset_index(drop=True)

            # iterate through pre-randomized file
            cur_math = math_file.loc[[math_cnt]]
            # check if 2 or 3 numbers being presented
            if cur_math.iloc[0, 2] == 0:
                n_math = 2
            else:
                n_math = 3

                # math number loop
            for m in range(n_math):

                # present numbers
                cur_num = cur_math.iloc[0, m]
                mathText.text = str(cur_num)

                m11 = trial_timer.getTime()
                for frameN in range(int(dur_digit*60)):
                    mathText.draw()
                    if frameN == 0:
                        win.logOnFlip('first mathF frame, item %i' % m, level=logging.EXP)
                        # NetStation
                        # send_to_NS(code='mthS', trialnum=t, item=None, cond=None, category=None)
                    win.flip()
                    if_esc_quit()
                    if math_timer_final.getTime() > dur_finalmath:
                        finalMathTimeOut = True
                        blank_screen(dur_blank)
                        break
                    event.clearEvents('keyboard')
                blank_screen(dur_blank)
                if math_timer_final.getTime() > dur_finalmath:
                    finalMathTimeOut = True
                    blank_screen(dur_blank)
                    break

                m12 = trial_timer.getTime()
                m1_duration = m12-m11

                math_cnt = math_cnt + 1
                type.append('math_dist')
                item.append(cur_math.iloc[0, m])
                trialtime.append(m11)
                duration.append(m1_duration)
                resp.append([])
                rt.append([])
                runtime.append([])
                isi.append([])
                event_cnt = event_cnt + 1
            event.clearEvents('keyboard')
            # final math number w/ question mark
            # randomly select correct or incorrect answer to present
            if not finalMathTimeOut:
                ans = random.randint(3, 4)
                mathText.text = str(cur_math.iloc[0, ans]) + '?'
                mathText.draw()
            if math_timer_final.getTime() > dur_finalmath:
                finalMathTimeOut = True
                blank_screen(dur_blank)
                break
            event.clearEvents('keyboard')

            m21 = trial_timer.getTime()
            questionFinalClock = core.Clock()

            if not finalMathTimeOut:
                for frameN in range(dur_question*60):
                    mathText.draw()
                    if frameN == 0:
                        win.logOnFlip('first mathQF frame', level=logging.EXP)
                    qDurClock = core.Clock()
                    win.flip()
                    if_esc_quit()
                    math_keysF = event.getKeys(keyList=['period','slash'], modifiers=False, timeStamped=questionFinalClock)

                    if math_keysF:
                        # NetStation
                        send_to_NS(code='finK', trialnum=t, item=None, cond=None, category=None)
                        blank_screen(dur_blank)
                        break
                    if not math_keysF and qDurClock.getTime() > dur_question:
                        blank_screen(dur_blank)
                        break
                    if math_timer_final.getTime() > dur_finalmath:
                        blank_screen(dur_blank)
                        break

            m22 = trial_timer.getTime()
            m2_duration = m22-m21

            type.append('math_ans')
            item.append(str(cur_math.iloc[0, ans]) + '?')
            trialtime.append(m21)
            duration.append(m2_duration)
            if math_keysF:
                resp.append(math_keysF[0][0])
                rt.append(math_keysF[0][1])
            else:
                resp.append('NaN')
                rt.append('NaN')
            runtime.append([])
            isi.append([])
            event_cnt = event_cnt + 1

    # NetStation
    send_to_NS(code='finE', trialnum=t, item=None, cond=None, category=None)
    #########################################
    #         Free Recall & Break           #
    #########################################
    if actualTrial and not practiceTrial:
        i31 = trial_timer.getTime()
        instrFR_timer = core.Clock()
        instrText.text = prepfrText
        instrText.draw()
        win.logOnFlip('first instrFRText frame', level=logging.EXP)
        win.flip()
        core.wait(instrWaitTime)

        # recording
        instrText.text = recordingText
        instrText.draw()
        win.logOnFlip('first recordtext frame', level=logging.EXP)
        win.flip()
        if_esc_quit()

        type.append('rec_start')
        item.append('audio')
        fr11 = trial_timer.getTime()
        trialtime.append(fr11)
        duration.append(dur_FR)
        resp.append([])
        rt.append([])
        runtime.append([])
        isi.append([])

        event_cnt = event_cnt + 1
        # NetStation
        send_to_NS(code='recS', trialnum=t, item=None, cond=None, category=None)

        mic.record(sec=dur_FR, block=True)
        win.logOnFlip('last recordtext frame', level=logging.EXP)

        # NetStation
        send_to_NS(code='recE', trialnum=t, item=None, cond=None, category=None)
        win.flip()

        # finish if all trials
        if t == (n_trials + 2):
            instrText.text = endingText
            instrText.draw()
            win.logOnFlip('end', level=logging.EXP)
            win.flip()
            core.wait(instrWaitTime)
            core.quit()

        # give break after each trial
        instrText.text = breakText
        instrText.draw()
        win.logOnFlip('break', level=logging.EXP)
        win.flip()
        breakKey = event.waitKeys(keyList=['space','escape'],  timeStamped=False, clearEvents=True)
        if breakKey == 'escape':
            core.quit()

        # record end of trial data
        # both manual and system logs
        temp_df = pd.DataFrame()
        temp_df['type'] = type; temp_df['item'] = item; temp_df['trialtime'] = trialtime; temp_df['duration'] = duration;
        temp_df['resp'] = resp; temp_df['rt'] = rt; temp_df['runtime'] = runtime;
        temp_df['isi'] = item_isi
        # append to events dataframe
        events = events.append(temp_df)

        # save to machine (if scripts crashes we would lose 1 item max)
        events.to_csv(stimDir + 'data/' + str(subj_id) + '/events/' + subj_id + '_events.csv', sep=',', index=False)
        logging.flush() # force flush of .log messages at end of each stim pres (backup data to disk)
