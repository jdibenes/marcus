
_base_ready = {
    'ready',
    'I\'m ready',
    'I am ready',
    'ready now',
    'I\'m ready now',
    'I am ready now',
    'go',
    'go ahead',
    'proceed',
    'carry on',
    'continue',
    'let\'s go',
    'start',
    'begin',
}

_FIRST = {
    'hello',
}

_START = _base_ready
_SCAN = _base_ready

_FORCE_SCAN = {
    'scan',
    'scan it',
    'yes',
    'ya',
    'yas',
    'yup',
    'yeah',
    'da',
    'sure',
    'OK',
    'okay',
    'of course',
    'do it',
    'why not',
    'whatever',
    'for sure',
    'for real',
    'uh huh',
    'if you want',
    'if you wish',
    'if you must',
    'if you say so',
    'as you see fit',
    'aye',
    'right now',
    'alright',
}

_SOLVE = _base_ready

_TALK_STEP = {
    'help',
    'help me',
    'need help',
    'I need help',
    'I need your help',
    'assist me',
    'need assistance',    
    'I need assistance',
    'I need your assistance',
    'I require assistance',
    'I require your assistance',
    'what next',
    'what now',
    'what do',
    'what do next',
    'what do now',
    'what do I do',
    'what do I do next',
    'what do I do now',
    'what should do',
    'what should do next',
    'what should do now',
    'what should I do',
    'what should I do now',
    'what should I do next',
    'what supposed to do',
    'what supposed to do next',
    'what supposed to do now',
    'what am I supposed to do',
    'what am I supposed to do next',
    'what am I supposed to do now',
    'what you want me to do',
    'what do you want me to do',
    'what would you like me to do',
    'what is next',
    'what is next step',
    'what is the next step',
    'what is current step',
    'what is the current step',
    'what is next task',
    'what is the next task',
    'what is current task',
    'what is the current task',
    'what is next goal',
    'what is the next goal',
    'what is current goal',
    'what is the current goal',
    'what is next objective',
    'what is the next objective',
    'what is current objective',
    'what is the current objective',
    'what should I be doing',
    'tell me',
    'tell me next',
    'tell me the next step',
    'tell me current step',
    'tell me the current step',
    'tell me what is the next step'
    'tell me what do',
    'tell me what to do',
    'tell me what do next',
    'tell me what do now',
    'tell me what to do next',
    'tell me what to do now',
    'tell me what supposed to do',
    'tell me what supposed to do next',
    'tell me what supposed to do now',
    'tell me what I\'m supposed to do',
    'tell me what I\'m supposed to do next',
    'tell me what I\'m supposed to do now',
    'read',
    'read to me',
    'read the next step',
    'read to me the next step',
    'read to me the current step',
}

_TALK_PROCESS = {
    'what are you doing',
    'what are we doing',
    'what is going on',
    'what is current process',
    'what is the current process',
    'why',
    'why we doing this',
    'why are we doing this',
    'why is this necessary',
    'why is this required',
    'why do you want me to do this',
}

_CLEAR = {
    'reset',
    'restart',
    'reboot',
    'start over',
    'start again',
    'go back',
    'go to start',
    'go to beginning',
    'go to the beginning',
    'do over',
    'do again',
    'do it again',
    'try again',
    'try that again',
    'from the beginning',    
    'I want to try again',
    'I want to do it again',
    'I want to try that again',
    'I want to go back',
    'I want to start over',
}

_LAST = {
    'goodbye',
}

MASTER_LIST = list(_FIRST | _START | _SCAN | _FORCE_SCAN | _SOLVE | _TALK_STEP | _TALK_PROCESS | _CLEAR | _LAST)


def _translate(match):
    key_first = match in _FIRST
    key_start = match in _START
    key_scan = match in _SCAN
    key_force_scan = match in _FORCE_SCAN
    key_solve = match in _SOLVE
    key_talk_step = match in _TALK_STEP
    key_talk_process = match in _TALK_PROCESS
    key_clear = match in _CLEAR
    key_last = match in _LAST

    return key_first, key_start, key_scan, key_force_scan, key_solve, key_talk_step, key_talk_process, key_clear, key_last


def process(vi, kb):
    key_first, key_start, key_scan, key_force_scan, key_solve, key_talk_step, key_talk_process, key_clear, key_last = _translate(vi) if (vi is not None) else ((False,)*9)

    key_first = key_first or kb == 9 # tab
    key_start = key_start or kb == 9 # tab
    key_scan = key_scan or kb == 9 # tab
    key_force_scan = key_force_scan or kb == 32 # space
    key_solve = key_solve or kb == 9 # tab
    key_talk_step = key_talk_step or kb == 49 # 1
    key_talk_process = key_talk_process or kb == 50 # 2
    key_clear = key_clear or kb == 8 # backspace
    key_last = key_last or kb == 48 # 0

    return key_first, key_start, key_scan, key_force_scan, key_solve, key_talk_step, key_talk_process, key_clear, key_last

