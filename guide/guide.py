
from cube import palette, cube_integrator, cube_simulator


#------------------------------------------------------------------------------
# Status
#------------------------------------------------------------------------------

class status:
    ACTION_NONE = 0
    ACTION_P    = 1

    ACTION_MOVE_MX = 2
    ACTION_MOVE_MY = 4
    ACTION_MOVE_MZ = 6
    ACTION_TURN_MU = 8
    ACTION_TURN_MR = 10
    ACTION_TURN_MF = 12
    ACTION_TURN_MD = 14
    ACTION_TURN_ML = 16
    ACTION_TURN_MB = 18

    ACTION_WAIT    = ACTION_NONE    | ACTION_P
    ACTION_MOVE_PX = ACTION_MOVE_MX | ACTION_P
    ACTION_MOVE_PY = ACTION_MOVE_MY | ACTION_P
    ACTION_MOVE_PZ = ACTION_MOVE_MZ | ACTION_P
    ACTION_TURN_PU = ACTION_TURN_MU | ACTION_P
    ACTION_TURN_PR = ACTION_TURN_MR | ACTION_P
    ACTION_TURN_PF = ACTION_TURN_MF | ACTION_P
    ACTION_TURN_PD = ACTION_TURN_MD | ACTION_P
    ACTION_TURN_PL = ACTION_TURN_ML | ACTION_P
    ACTION_TURN_PB = ACTION_TURN_MB | ACTION_P

    ACTION_INVALID = 31

    ACTION_ASK_WHITE  = 32
    ACTION_ASK_RED    = 33
    ACTION_ASK_GREEN  = 34
    ACTION_ASK_YELLOW = 35
    ACTION_ASK_ORANGE = 36
    ACTION_ASK_BLUE   = 37

    ACTION_ASK_RESCAN = 63

    ERROR_LOST_STATE         = 64
    ERROR_INCONSISTENT_STATE = 65

    WARN_NONE = 0 << 8
    
    WARN_TOP_WHITE = 1 << 8
    WARN_TOP_BLUE  = 2 << 8
    WARN_TOP_GREEN = 3 << 8

    WARN_MISMATCH_WHITE  = 1 << 10
    WARN_MISMATCH_RED    = 2 << 10
    WARN_MISMATCH_GREEN  = 3 << 10
    WARN_MISMATCH_YELLOW = 4 << 10
    WARN_MISMATCH_ORANGE = 5 << 10
    WARN_MISMATCH_BLUE   = 6 << 10

    WARN_SEEN_WHITE  =  9 << 10
    WARN_SEEN_RED    = 10 << 10
    WARN_SEEN_GREEN  = 11 << 10
    WARN_SEEN_YELLOW = 12 << 10
    WARN_SEEN_ORANGE = 13 << 10
    WARN_SEEN_BLUE   = 14 << 10

    _action_ask_color = {
        'white'  : ACTION_ASK_WHITE,
        'red'    : ACTION_ASK_RED,
        'green'  : ACTION_ASK_GREEN,
        'yellow' : ACTION_ASK_YELLOW,
        'orange' : ACTION_ASK_ORANGE,
        'blue'   : ACTION_ASK_BLUE,
    }

    _warn_top_color = {
        'white'  : WARN_TOP_BLUE,
        'red'    : WARN_TOP_WHITE,
        'green'  : WARN_TOP_WHITE,
        'yellow' : WARN_TOP_GREEN,
        'orange' : WARN_TOP_WHITE,
        'blue'   : WARN_TOP_WHITE,
    }

    _warn_mismatch_color = {
        'white'  : WARN_MISMATCH_WHITE,
        'red'    : WARN_MISMATCH_RED,
        'green'  : WARN_MISMATCH_GREEN,
        'yellow' : WARN_MISMATCH_YELLOW,
        'orange' : WARN_MISMATCH_ORANGE,
        'blue'   : WARN_MISMATCH_BLUE,
    }

    _warn_seen_color = {
        'white'  : WARN_SEEN_WHITE,
        'red'    : WARN_SEEN_RED,
        'green'  : WARN_SEEN_GREEN,
        'yellow' : WARN_SEEN_YELLOW,
        'orange' : WARN_SEEN_ORANGE,
        'blue'   : WARN_SEEN_BLUE,
    }

    @staticmethod
    def is_interactive(code):
        return (code & 32) != 0
    
    @staticmethod
    def is_error(code):
        return (code & 64) != 0
    
    @staticmethod
    def get_action(recommendation):
        return recommendation & 0x00FF
    
    @staticmethod
    def get_warn(recommendation):
        return recommendation & 0xFF00
    
    @staticmethod
    def to_recommendation(action, warn):
        return action | warn


#------------------------------------------------------------------------------
# Scan Guide
#------------------------------------------------------------------------------

class scan_guide(cube_integrator):
    ORDER = ['red', 'blue', 'orange', 'green', 'white', 'yellow']

    def __init__(self, threshold, size, auto):
        super().__init__(threshold, size)
        self._index = 0
        self._auto = auto

    def _current_side(self):
        return scan_guide.ORDER[self._index]
    
    def _build_recommendation(self, warn_match, warn_novel):
        side = self._current_side()
        action = status._action_ask_color[side]
        warn = status._warn_top_color[side]
        return action, warn | (status._warn_mismatch_color[warn_match] if (warn_match is not None) else 0) | (status._warn_seen_color[warn_novel] if (warn_novel is not None) else 0)

    def next(self, colors):
        self.update(self._current_side(), colors)
        self._index += 1
        return self._index < len(scan_guide.ORDER)
    
    def assess(self, colors, trigger):
        if (trigger):
            return (status.ACTION_NONE, status.WARN_NONE)

        observed_side = self.get_name(colors)
        novel = not self.is_registered(colors)
        match = self._current_side() == observed_side

        warn_match = None if (match) else observed_side
        warn_novel = None if (novel) else observed_side

        if (not self._auto):
             return self._build_recommendation(warn_match, warn_novel)
        
        stable = self.is_stable(colors)
        if (not stable):
            return self._build_recommendation(None, None)
        
        return (status.ACTION_NONE, status.WARN_NONE) if (novel and match) else self._build_recommendation(warn_match, warn_novel)
    
    def get_index(self):
        return self._index
    
    def get_colors(self):
        colors = []
        for color in scan_guide.ORDER:
            colors.append(self._state[color][4] + (255,) if (color in self._state) else (0, 0, 0, 0))
        return colors


#------------------------------------------------------------------------------
# Solve Guide (L1)
#------------------------------------------------------------------------------
# Assumptions:
# correct orientation
# 1 move - 1 assess
# algorithm is not empty

class solve_guide_l1:
    _step2action = {
        'U'   : { '' : status.ACTION_TURN_MU, '\'' : status.ACTION_TURN_PU, },
        'R'   : { '' : status.ACTION_TURN_MR, '\'' : status.ACTION_TURN_PR, },
        'F'   : { '' : status.ACTION_TURN_MF, '\'' : status.ACTION_TURN_PF, },
        'D'   : { '' : status.ACTION_TURN_MD, '\'' : status.ACTION_TURN_PD, },
        'L'   : { '' : status.ACTION_TURN_ML, '\'' : status.ACTION_TURN_PL, },
        'B'   : { '' : status.ACTION_TURN_MB, '\'' : status.ACTION_TURN_PB, },
    }

    _preferred_route = {
        'white'  : status.ACTION_MOVE_MX,
        'red'    : status.ACTION_MOVE_MY,
        'green'  : status.ACTION_MOVE_MY,
        'yellow' : status.ACTION_MOVE_PX,
        'orange' : status.ACTION_MOVE_MY,
        'blue'   : status.ACTION_MOVE_MY,
    }

    def __init__(self, state, algorithm):
        self._cube = cube_simulator(state)
        self._sim_cube = cube_simulator(state)
        self._algorithm = cube_simulator.atomize(algorithm)
        self._sim_index = 0
        self._step = self._algorithm[self._sim_index]
        self._sim_cube.evaluate(self._step) 

    def next(self):
        if (self._sim_index >= (len(self._algorithm) - 1)):
            return False
        self._cube.evaluate(self._step)
        self._sim_index += 1
        self._step = self._algorithm[self._sim_index]
        self._sim_cube.evaluate(self._step)
        return True

    def previous(self):
        if (self._sim_index <= 0):
            return False
        self._sim_cube.evaluate(cube_simulator.invert_step(self._step))
        self._sim_index -= 1
        self._step = self._algorithm[self._sim_index]
        self._cube.evaluate(cube_simulator.invert_step(self._step))
        return True
    
    def assess(self, colors):
        color = colors[4]
        s = colors == self._cube.get_side(color)
        t = colors == self._sim_cube.get_side(color)
        if (s and (not t)):
            return solve_guide_l1._step2action[cube_simulator.absolute_to_relative(cube_simulator.color_to_notation(color), self._step[0])][self._step[1:]]
        if ((not s) and t):
            return status.ACTION_NONE
        if (s and t):
            return solve_guide_l1._preferred_route[color]
        if ((not s) and (not t)):
            return status.ERROR_LOST_STATE

    def get_sim_index(self):
        return self._sim_index

    def get_algorithm(self):
        return list(self._algorithm)
    
    def get_cube(self):
        return self._cube.get_state()
    
    def get_sim_cube(self):
        return self._sim_cube.get_state()
    
    def get_step(self):
        return self._step


#------------------------------------------------------------------------------
# Solve Guide (L2)
#------------------------------------------------------------------------------
# Assumptions:
# 1 move - 1 assess
# algorithm is not empty

class solve_guide_l2(solve_guide_l1):
    _rotate_reference = [status.ACTION_MOVE_PZ, status.ACTION_MOVE_MZ, status.ACTION_MOVE_MZ, status.ACTION_INVALID]

    _tour = {
        'white'  : status.ACTION_MOVE_MY,
        'red'    : status.ACTION_MOVE_MX,
        'green'  : status.ACTION_MOVE_MY,
        'yellow' : status.ACTION_MOVE_MX,
        'orange' : status.ACTION_MOVE_MY,
        'blue'   : status.ACTION_MOVE_MX,
    }

    def assess(self, colors):
        color = colors[4]
        candidates, ambiguous = self._cube.get_orientation_candidates(color)
        sim_candidates = self._sim_cube.get_orientation_candidates(color)[0]
        action = super().assess(colors)
        if (not status.is_error(action)):
            for i in range(0, 4):
                if (sim_candidates[3] == candidates[i]):
                    return solve_guide_l1._preferred_route[color]
            return status.to_recommendation(action, status._warn_top_color[color] if (ambiguous) else status.WARN_NONE)        
        matches = [i for i in range(0, 4) if colors == candidates[i]]
        target = self._cube
        if (len(matches) == 0):
            matches = [i for i in range(0, 4) if colors == sim_candidates[i]]
            target = self._sim_cube
            if (len(matches) == 0):
                return status.ERROR_INCONSISTENT_STATE
        if (len(matches) == 1):
            return solve_guide_l2._rotate_reference[matches[0]]
        for side in palette.COLORS:
            if (side != color):
                if (not target.get_orientation_candidates(side)[1]):
                    return status._action_ask_color[side]
        return status.to_recommendation(status.ACTION_WAIT, status._warn_top_color[color])


#------------------------------------------------------------------------------
# Solve Guide
#------------------------------------------------------------------------------

class solve_guide(solve_guide_l2):
    def assess(self, colors):
        recommendation = super().assess(colors)
        if (status.is_error(recommendation)):
            recommendation = status.ACTION_ASK_RESCAN
        return status.get_action(recommendation), status.get_warn(recommendation)


#------------------------------------------------------------------------------
# Pulse
#------------------------------------------------------------------------------

class filter:
    def __init__(self, hold):
        self._count = 0
        self._hold = hold

    def assess(self, action):
        if (action == status.ACTION_ASK_RESCAN):
            if (self._count >= self._hold):
                return status.ACTION_ASK_RESCAN
            self._count += 1
            return status.ACTION_WAIT
        self._count = 0
        return action
    
    def get_count(self):
        return self._count
    
